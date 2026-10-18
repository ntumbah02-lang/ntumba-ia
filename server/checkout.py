from __future__ import annotations

import os
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import stripe

from server.license_manager import generate_license

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

app = FastAPI(title="ntumba IA - Checkout")


class CheckoutRequest(BaseModel):
    plan: str = "pro"
    email: Optional[str] = None
    days: int = 365


@app.post("/api/create-checkout-session")
async def create_checkout_session(req: CheckoutRequest):
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="STRIPE_SECRET_KEY is not configured")

    plan = req.plan.lower()
    if plan not in {"starter", "pro", "enterprise"}:
        raise HTTPException(status_code=400, detail="Unsupported plan")

    price_map = {
        "starter": 1900,
        "pro": 4900,
        "enterprise": 9900,
    }

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{
            "price_data": {
                "currency": "eur",
                "product_data": {
                    "name": f"ntumba IA {plan.title()}",
                    "description": f"Licence {plan.title()} pour ntumba IA",
                },
                "unit_amount": price_map[plan],
                "recurring": {
                    "interval": "month",
                },
            },
            "quantity": 1,
        }],
        customer_email=req.email,
        metadata={
            "plan": plan,
            "days": str(req.days),
        },
        success_url="https://example.com/success?session_id={CHECKOUT_SESSION_ID}",
        cancel_url="https://example.com/cancel",
    )

    return JSONResponse({"url": session.url})


@app.post("/api/dev-create-license")
async def dev_create_license(req: CheckoutRequest):
    key = generate_license(req.email or "demo@example.com", plan=req.plan, days=req.days)
    return JSONResponse({
        "license_key": key,
        "plan": req.plan,
        "expires_at": "generated in dev mode",
    })
