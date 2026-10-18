from __future__ import annotations

import os
import json
from fastapi import FastAPI, Request, HTTPException

import stripe

from server.license_manager import generate_license
from server.emailer import send_license_email

app = FastAPI(title="ntumba IA - Stripe webhook")

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")


@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature", "")

    if not WEBHOOK_SECRET:
        raise HTTPException(status_code=500, detail="STRIPE_WEBHOOK_SECRET is not configured")

    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=sig_header, secret=WEBHOOK_SECRET)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook signature verification failed: {e}")

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        customer_email = None
        if session.get("customer_details"):
            customer_email = session["customer_details"].get("email")
        if not customer_email:
            customer_email = session.get("customer_email")

        metadata = session.get("metadata") or {}
        plan = metadata.get("plan", "pro")
        try:
            days = int(metadata.get("days", 365))
        except Exception:
            days = 365

        key = generate_license(customer_email or "unknown", plan=plan, days=days)

        try:
            if customer_email:
                send_license_email(customer_email, key, plan=plan)
        except Exception:
            pass

    return {"status": "ok"}
