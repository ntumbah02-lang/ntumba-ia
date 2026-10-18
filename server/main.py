from __future__ import annotations

import os
import uuid
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import openai

from server.license_manager import validate_license

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gpt-3.5-turbo")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

app = FastAPI(title="ntumba IA - Chat MVP")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/", StaticFiles(directory="web", html=True), name="web")

DB_PATH = "chat.db"

SYSTEM_PROMPT = (
    "Vous êtes ntumba IA, un assistant utile, poli et concis. Répondez en français par défaut."
)


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    license_key: Optional[str] = None


def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save_message(session_id: str, role: str, content: str) -> None:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO messages (session_id, role, content, created_at) VALUES (?, ?, ?, ?)",
        (session_id, role, content, datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def load_history(session_id: str, limit: int = 10) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT role, content, created_at FROM messages WHERE session_id = ? ORDER BY id DESC LIMIT ?",
        (session_id, limit),
    )
    rows = cur.fetchall()
    conn.close()
    rows.reverse()
    return [{"role": r[0], "content": r[1], "created_at": r[2]} for r in rows]


async def call_openai_chat(messages: List[Dict], model_name: str = DEFAULT_MODEL) -> str:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY n'est pas défini. Ajoutez-le dans .env.")

    def _call():
        resp = openai.ChatCompletion.create(
            model=model_name,
            messages=messages,
            temperature=0.7,
            max_tokens=512,
        )
        choices = resp.get("choices", [])
        if not choices:
            return ""
        return choices[0].get("message", {}).get("content", "")

    reply = await asyncio.to_thread(_call)
    return reply


@app.on_event("startup")
async def startup_event():
    init_db()


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        session_id = req.session_id or str(uuid.uuid4())
        user_message = req.message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="Le message est vide.")

        # Validation Pro
        is_pro = False
        plan = "basic"
        if req.license_key:
            license = validate_license(req.license_key)
            is_pro = bool(license)
            if license:
                plan = license.get("plan", "pro")

        save_message(session_id, "user", user_message)

        history = load_history(session_id, limit=12)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        for m in history:
            messages.append({"role": m["role"], "content": m["content"]})
        messages.append({"role": "user", "content": user_message})

        model_name = DEFAULT_MODEL
        reply = await call_openai_chat(messages, model_name=model_name)

        save_message(session_id, "assistant", reply)

        return JSONResponse({
            "reply": reply,
            "session_id": session_id,
            "plan": plan,
            "is_pro": is_pro,
        })

    except RuntimeError as re:
        raise HTTPException(status_code=500, detail=str(re))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
