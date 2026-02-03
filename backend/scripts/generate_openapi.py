#!/usr/bin/env python3
"""
Generate OpenAPI specification from FastAPI app.

Purpose: Extract openapi.json for Stage 03 SSOT compliance
Usage: python3 scripts/generate_openapi.py > ../docs/03-integrate/02-API-Specifications/openapi.json
"""

import json
import sys

# Add backend to path
sys.path.insert(0, '/home/nqh/shared/SDLC-Orchestrator/backend')

from app.main import app

if __name__ == "__main__":
    openapi_schema = app.openapi()
    print(json.dumps(openapi_schema, indent=2))
