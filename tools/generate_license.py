#!/usr/bin/env python3
"""Generate a license key for ntumba IA.

Usage:
  python tools/generate_license.py user@example.com pro 365
"""
from __future__ import annotations

import sys

from server.license_manager import generate_license


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/generate_license.py <customer_email> [plan] [days]")
        sys.exit(1)

    email = sys.argv[1]
    plan = sys.argv[2] if len(sys.argv) > 2 else "pro"
    days = int(sys.argv[3]) if len(sys.argv) > 3 else 365

    key = generate_license(email, plan=plan, days=days)
    print(f"Generated license key for {email}:")
    print(key)
