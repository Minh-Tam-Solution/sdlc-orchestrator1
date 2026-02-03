# IT Admin Request: SDLC Nginx Route Update

**Request ID**: SDLC-NGINX-2025-12-28
**Priority**: High
**Requested By**: Development Team
**Date**: December 28, 2025

---

## Summary

Update nginx config for `sdlc.nhatquangholding.com` to route `/docs/*` to frontend landing page instead of backend FastAPI docs.

## Current Problem

- URL `https://sdlc.nhatquangholding.com/docs/getting-started` returns `{"detail":"Not Found"}`
- Current config routes `/docs` to backend (port 8300) for FastAPI Swagger UI
- Frontend landing page has documentation pages at `/docs/*` but they are not accessible

## Required Change

**File**: `/etc/nginx/sites-enabled/nhatquangholding-services`

### Current Config (Lines ~32-36):
```nginx
# OpenAPI docs
location /docs {
    proxy_pass http://127.0.0.1:8300;
    include /etc/nginx/snippets/proxy-params.conf;
}
```

### New Config (Replace above with):
```nginx
# OpenAPI Swagger UI - Backend (moved to /openapi-docs)
location /openapi-docs {
    proxy_pass http://127.0.0.1:8300/docs;
    include /etc/nginx/snippets/proxy-params.conf;
}

# Documentation pages - Frontend Landing
location /docs {
    proxy_pass http://127.0.0.1:8310;
    include /etc/nginx/snippets/proxy-params.conf;
}
```

## Commands to Execute

```bash
# 1. Edit nginx config
sudo nano /etc/nginx/sites-enabled/nhatquangholding-services

# 2. Test config
sudo nginx -t

# 3. Reload nginx
sudo systemctl reload nginx
```

## Verification

After update, test these URLs:

| URL | Expected Result |
|-----|-----------------|
| `https://sdlc.nhatquangholding.com/docs` | Frontend docs index page |
| `https://sdlc.nhatquangholding.com/docs/getting-started` | Getting Started guide |
| `https://sdlc.nhatquangholding.com/docs/api-reference` | API Reference page |
| `https://sdlc.nhatquangholding.com/docs/cli-guide` | CLI Guide page |
| `https://sdlc.nhatquangholding.com/docs/vscode-extension` | VS Code Extension page |
| `https://sdlc.nhatquangholding.com/openapi-docs` | FastAPI Swagger UI |
| `https://sdlc.nhatquangholding.com/redoc` | FastAPI ReDoc (unchanged) |

## Impact

- **No downtime required** - nginx reload is graceful
- **Breaking change**: `/docs` now serves frontend instead of Swagger UI
- **New endpoint**: `/openapi-docs` for Swagger UI access

## Rollback

If issues occur, revert to original config:
```nginx
location /docs {
    proxy_pass http://127.0.0.1:8300;
    include /etc/nginx/snippets/proxy-params.conf;
}
```

---

## Execution Summary

**Executed By**: CTO via AI Dev Partner  
**Completed**: December 28, 2025 18:11 UTC+7  
**Duration**: ~3 minutes (graceful reload, zero downdowntime)

### Changes Applied

Backend paths corrected: Swagger/ReDoc at `/api/docs` and `/api/redoc` (not `/docs`).

**Final Routes:**
- `/docs` → Frontend landing (port 8310) ✅
- `/openapi-docs` → Backend `/api/docs` (port 8300) ✅  
- `/redoc` → Backend `/api/redoc` (port 8300) ✅

### Verification Results

| URL | Status | Server |
|-----|--------|--------|
| `https://sdlc.nhatquangholding.com/docs` | ✅ 200 | Next.js |
| `https://sdlc.nhatquangholding.com/docs/getting-started` | ✅ 200 | Next.js |
| `https://sdlc.nhatquangholding.com/openapi-docs` | ✅ 200 | FastAPI |
| `https://sdlc.nhatquangholding.com/redoc` | ✅ 200 | FastAPI |

**Backup**: `/etc/nginx/sites-enabled/nhatquangholding-services.backup-20251228-180826`

---

**Status**: ✅ COMPLETED

---

## Additional Update: VS Code Marketplace Link

**Date**: December 28, 2025 (same day)

**Change**: Updated VS Code Marketplace installation link in documentation:
- **Old URL**: `https://marketplace.visualstudio.com/items?itemName=sdlc-orchestrator`
- **New URL**: `https://marketplace.visualstudio.com/items?itemName=mtsolution.sdlc-orchestrator`

**File Updated**: `frontend/landing/src/app/docs/vscode-extension/page.tsx`

**Deployed**: ✅ Frontend rebuilt and redeployed
