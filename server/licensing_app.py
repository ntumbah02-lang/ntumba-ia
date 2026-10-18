from __future__ import annotations

import os
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from server.license_manager import validate_license

app = FastAPI(title="ntumba IA licensing API")

# Serve static landing page
landing_path = Path(__file__).resolve().parent.parent / "web"
landing_path.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(landing_path)), name="static")


@app.get("/api/validate-license")
async def validate_license_endpoint(license_key: str = Query(..., alias="key")):
    data = validate_license(license_key)
    if data is None:
        raise HTTPException(status_code=404, detail="License invalid or expired")
    return {
        "valid": True,
        "license": data,
    }


@app.get("/api/license-status")
async def license_status_endpoint(license_key: str = Query(..., alias="key")):
    data = validate_license(license_key)
    return {
        "valid": bool(data),
        "plan": data.get("plan") if data else None,
        "expires_at": data.get("expires_at") if data else None,
    }


@app.get("/", response_class=HTMLResponse)
async def landing_page():
    return """<!doctype html>
<html lang='fr'>
<head>
  <meta charset='utf-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>ntumba IA Pro</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 0; background: #0b1020; color: #ecf3ff; }
    .wrap { max-width: 1100px; margin: 0 auto; padding: 72px 24px; }
    .hero { display: grid; grid-template-columns: 1.3fr 0.7fr; gap: 28px; align-items: center; }
    .card { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 28px; }
    h1 { font-size: clamp(2.2rem, 5vw, 4rem); margin: 0 0 16px; }
    p { line-height: 1.7; color: #cfe0ff; }
    .btn { display: inline-block; padding: 14px 22px; border-radius: 12px; text-decoration: none; font-weight: 700; }
    .primary { background: linear-gradient(135deg, #3b82f6, #8b5cf6); color: white; }
    .secondary { border: 1px solid rgba(255,255,255,0.15); color: white; }
    .price { font-size: 2.5rem; font-weight: 800; }
    ul { padding-left: 18px; }
    .grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; margin-top: 32px; }
    @media (max-width: 780px) { .hero, .grid { grid-template-columns: 1fr; } }
  </style>
</head>
<body>
  <div class='wrap'>
    <div class='hero'>
      <div>
        <p style='letter-spacing: 0.12em; color:#7dd3fc; text-transform: uppercase; font-weight: 700;'>ntumba IA Pro</p>
        <h1>Votre assistant IA pour accélérer votre business.</h1>
        <p>Des réponses plus rapides, plus fiables, plus utiles pour votre travail, votre équipe et vos clients.</p>
        <div style='display:flex; gap:12px; flex-wrap: wrap; margin-top: 24px;'>
          <a class='btn primary' href='#pricing'>Acheter la licence</a>
          <a class='btn secondary' href='/api/validate-license?key=demo'>Tester la clé</a>
        </div>
      </div>
      <div class='card'>
        <div style='font-size: 0.9rem; color: #9cc2ff; margin-bottom: 10px;'>Pro</div>
        <div class='price'>49€<span style='font-size: 1rem; color:#9cc2ff;'>/mois</span></div>
        <ul>
          <li>Accès premium</li>
          <li>Modèles plus puissants</li>
          <li>Support prioritaire</li>
          <li>Usage commercial</li>
        </ul>
      </div>
    </div>

    <div class='grid' id='pricing'>
      <div class='card'>
        <h3>Starter</h3>
        <div class='price' style='font-size: 1.8rem;'>19€<span style='font-size: 0.9rem;'>/mois</span></div>
        <p>Pour utiliser l’outil personnellement.</p>
      </div>
      <div class='card'>
        <h3>Pro</h3>
        <div class='price' style='font-size: 1.8rem;'>49€<span style='font-size: 0.9rem;'>/mois</span></div>
        <p>Pour les professionnels et les équipes.</p>
      </div>
      <div class='card'>
        <h3>Enterprise</h3>
        <div class='price' style='font-size: 1.8rem;'>Sur devis</div>
        <p>Pour les projets, intégrations et support avancé.</p>
      </div>
    </div>
  </div>
</body>
</html>"""
