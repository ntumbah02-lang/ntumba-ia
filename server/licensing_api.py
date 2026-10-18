from __future__ import annotations

import os
from typing import Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from server.license_manager import validate_license

app = FastAPI(title="ntumba IA license API")


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
