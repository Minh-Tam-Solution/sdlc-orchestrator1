# V1→V2 API Consolidation Migration Plan

**Purpose**: Merge duplicate API versions to reduce maintenance burden  
**Priority**: P0 - Sprint 147  
**Owner**: Backend Lead + API Team  
**Goal**: -18 endpoints (Context Authority) + -13 endpoints (Analytics)

---

## 🎯 Executive Summary

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CONSOLIDATION TARGETS                                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CONTEXT AUTHORITY:                                                    │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Before: V1 (528 LOC, 7 endpoints) + V2 (783 LOC, 11 endpoints)  │   │
│  │ After:  Single V2 (600 LOC, 9 endpoints)                        │   │
│  │ Savings: -711 LOC, -9 endpoints                                 │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  ANALYTICS:                                                            │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │ Before: V1 (684 LOC, 15 endpoints) + V2 (282 LOC, 4 endpoints)  │   │
│  │ After:  Single V2 (350 LOC, 6 endpoints)                        │   │
│  │ Savings: -616 LOC, -13 endpoints                                │   │
│  └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│  TOTAL SAVINGS: ~1,327 LOC, -22 endpoints                              │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Context Authority Consolidation

### Current State Analysis

**V1 Endpoints** (`context_authority.py` - 528 LOC):
| Endpoint | Method | Usage | Action |
|----------|--------|-------|--------|
| `/context-authority/{id}` | GET | Low | Redirect to V2 |
| `/context-authority` | POST | Medium | Redirect to V2 |
| `/context-authority/{id}` | PUT | Low | Transform to PATCH |
| `/context-authority/{id}` | DELETE | Low | Redirect to V2 |
| `/context-authority/{id}/history` | GET | Very Low | Transform to /versions |
| `/context-authority/sync` | POST | Medium | Transform to /refresh |
| `/context-authority/search` | GET | Low | Transform to query params |

**V2 Endpoints** (`context_authority_v2.py` - 783 LOC):
| Endpoint | Method | Usage | Action |
|----------|--------|-------|--------|
| `/context-authority/v2/validate` | POST | High | Keep (primary) |
| `/context-authority/v2/overlay` | POST | High | Keep (primary) |
| `/context-authority/v2/templates` | GET | Medium | Keep |
| `/context-authority/v2/templates` | POST | Medium | Keep |
| `/context-authority/v2/templates/{id}` | GET | Low | Keep |
| `/context-authority/v2/templates/{id}` | PUT | Low | Keep |
| `/context-authority/v2/templates/{id}` | DELETE | Low | Keep |
| `/context-authority/v2/templates/{id}/usage` | GET | Low | Keep |
| `/context-authority/v2/snapshots/{id}` | GET | Medium | Keep |
| `/context-authority/v2/{id}` | GET | Medium | Keep |
| `/context-authority/v2/{id}/versions` | GET | Low | Keep |

### Target State

**Merged Endpoints** (9 total):
```
POST   /api/v1/context-authority/validate        # Full validation
POST   /api/v1/context-authority/overlay         # Generate overlay
GET    /api/v1/context-authority/templates       # List templates
POST   /api/v1/context-authority/templates       # Create template
GET    /api/v1/context-authority/templates/{id}  # Get template
PATCH  /api/v1/context-authority/templates/{id}  # Update template
DELETE /api/v1/context-authority/templates/{id}  # Delete template
GET    /api/v1/context-authority/{id}            # Get context
GET    /api/v1/context-authority/{id}/versions   # Get versions
```

### Migration Steps

#### Day 1 Morning: Add Deprecation Layer

```python
# backend/app/api/routes/context_authority.py

from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Request, Response
from app.core.deprecation import deprecated_endpoint

router = APIRouter(prefix="/context-authority", tags=["Context Authority (DEPRECATED)"])

SUNSET_DATE = datetime(2026, 8, 3, tzinfo=timezone.utc)  # 180 days from Feb 3

def add_deprecation_headers(response: Response, successor_path: str):
    """Add RFC 8594 deprecation headers."""
    response.headers["Deprecation"] = "true"
    response.headers["Sunset"] = SUNSET_DATE.strftime("%a, %d %b %Y %H:%M:%S GMT")
    response.headers["Link"] = f'<{successor_path}>; rel="successor-version"'
    return response

@router.get("/{context_id}")
@deprecated_endpoint(
    successor="/api/v1/context-authority/v2/{context_id}",
    sunset_date=SUNSET_DATE
)
async def get_context_v1(context_id: str, response: Response):
    """DEPRECATED: Use V2 endpoint instead."""
    add_deprecation_headers(response, f"/api/v1/context-authority/v2/{context_id}")
    
    # Forward to V2 implementation
    from app.api.routes.context_authority_v2 import get_context_v2
    return await get_context_v2(context_id)
```

#### Day 1 Afternoon: Create Compatibility Layer

```python
# backend/app/api/routes/context_authority.py (continued)

@router.put("/{context_id}")
@deprecated_endpoint(successor="/api/v1/context-authority/v2/{context_id}")
async def update_context_v1(context_id: str, body: dict, response: Response):
    """DEPRECATED: Use PATCH on V2 endpoint."""
    add_deprecation_headers(response, f"/api/v1/context-authority/v2/{context_id}")
    
    # Transform V1 PUT body to V2 PATCH format
    v2_body = transform_v1_to_v2_update(body)
    
    from app.api.routes.context_authority_v2 import patch_context_v2
    return await patch_context_v2(context_id, v2_body)

@router.get("/{context_id}/history")
@deprecated_endpoint(successor="/api/v1/context-authority/v2/{context_id}/versions")
async def get_history_v1(context_id: str, response: Response):
    """DEPRECATED: Use /versions on V2 endpoint."""
    add_deprecation_headers(response, f"/api/v1/context-authority/v2/{context_id}/versions")
    
    from app.api.routes.context_authority_v2 import get_versions_v2
    v2_response = await get_versions_v2(context_id)
    
    # Transform V2 response to V1 format
    return transform_v2_to_v1_history(v2_response)
```

#### Day 2: Frontend Migration

```typescript
// frontend/src/hooks/useContextAuthority.ts

// BEFORE (V1 + V2 mixed)
const useContextAuthority = () => {
  const getContext = async (id: string) => {
    return api.get(`/context-authority/${id}`);  // V1
  };
  
  const validateContext = async (data: any) => {
    return api.post(`/context-authority/v2/validate`, data);  // V2
  };
};

// AFTER (V2 only)
const useContextAuthority = () => {
  const getContext = async (id: string) => {
    return api.get(`/context-authority/v2/${id}`);  // V2
  };
  
  const validateContext = async (data: any) => {
    return api.post(`/context-authority/v2/validate`, data);  // V2
  };
  
  const getVersions = async (id: string) => {
    return api.get(`/context-authority/v2/${id}/versions`);  // V2
  };
};
```

---

## 📋 Analytics Consolidation

### Current State Analysis

**V1 Endpoints** (`analytics.py` - 684 LOC):
| Endpoint | Method | Usage | Action |
|----------|--------|-------|--------|
| `/analytics/overview` | GET | Medium | Keep (merge to V2) |
| `/analytics/projects` | GET | Low | Redirect to V2 |
| `/analytics/gates` | GET | Low | Redirect to V2 |
| `/analytics/users` | GET | Very Low | **REMOVE** |
| `/analytics/export` | GET | Very Low | **REMOVE** |
| `/analytics/track` | POST | Low | **REMOVE** (use telemetry) |
| `/analytics/events` | GET | Low | **REMOVE** |
| `/analytics/events/{id}` | GET | Very Low | **REMOVE** |
| `/analytics/reports/daily` | GET | Low | **REMOVE** |
| `/analytics/reports/weekly` | GET | Low | **REMOVE** |
| `/analytics/reports/monthly` | GET | Low | **REMOVE** |
| `/analytics/custom` | POST | Very Low | **REMOVE** |
| `/analytics/dashboard` | GET | Medium | Redirect to V2 |
| `/analytics/trends` | GET | Low | **REMOVE** |
| `/analytics/compare` | GET | Very Low | **REMOVE** |

**V2 Endpoints** (`analytics_v2.py` - 282 LOC):
| Endpoint | Method | Usage | Action |
|----------|--------|-------|--------|
| `/analytics/v2/events` | POST | High | Keep |
| `/analytics/v2/events/batch` | POST | Medium | Keep |
| `/analytics/v2/metrics/dau` | GET | Medium | Keep |
| `/analytics/v2/metrics/ai-safety` | GET | Low | Keep |

### Target State

**Merged Endpoints** (6 total):
```
POST /api/v1/analytics/events          # Track single event (from V2)
POST /api/v1/analytics/events/batch    # Track batch events (from V2)
GET  /api/v1/analytics/metrics/dau     # Daily active users (from V2)
GET  /api/v1/analytics/metrics/safety  # AI safety metrics (from V2)
GET  /api/v1/analytics/overview        # Overview dashboard (from V1, enhanced)
GET  /api/v1/analytics/dashboard       # Main dashboard (redirect to overview)
```

### Migration Steps

#### Day 2 Morning: Audit Usage

```sql
-- Run this query to identify V1 usage patterns
SELECT 
    path,
    method,
    COUNT(*) as call_count,
    COUNT(DISTINCT user_id) as unique_users,
    MAX(created_at) as last_used
FROM api_logs
WHERE path LIKE '/api/v1/analytics%'
    AND created_at > NOW() - INTERVAL '30 days'
GROUP BY path, method
ORDER BY call_count DESC;
```

#### Day 2 Afternoon: Remove Low-Usage Endpoints

```python
# backend/app/api/routes/analytics.py

# REMOVED endpoints (mark as deprecated, return 410 Gone)
REMOVED_ENDPOINTS = [
    '/analytics/users',
    '/analytics/export', 
    '/analytics/track',
    '/analytics/events',
    '/analytics/reports/daily',
    '/analytics/reports/weekly',
    '/analytics/reports/monthly',
    '/analytics/custom',
    '/analytics/trends',
    '/analytics/compare'
]

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def deprecated_endpoint(path: str, request: Request):
    """Handle removed endpoints with helpful error."""
    if f"/analytics/{path}" in REMOVED_ENDPOINTS:
        return JSONResponse(
            status_code=410,  # Gone
            content={
                "error": "Endpoint removed",
                "message": f"The /analytics/{path} endpoint has been removed.",
                "migration_guide": "/docs/migration/analytics-v2.md",
                "alternatives": {
                    "event_tracking": "POST /api/v1/analytics/v2/events",
                    "metrics": "GET /api/v1/analytics/v2/metrics/dau"
                }
            }
        )
    raise HTTPException(status_code=404, detail="Not found")
```

---

## 📊 Deprecation Monitoring

### Metrics Dashboard

```yaml
# Grafana dashboard: API Deprecation Tracking

panels:
  - title: "V1 API Calls (Should Decrease)"
    query: |
      sum(rate(http_requests_total{
        path=~"/api/v1/context-authority/[^v].*|/api/v1/analytics/[^v].*"
      }[5m])) by (path)
    
  - title: "V2 API Calls (Should Increase)"
    query: |
      sum(rate(http_requests_total{
        path=~"/api/v1/context-authority/v2.*|/api/v1/analytics/v2.*"
      }[5m])) by (path)
    
  - title: "Unique Clients on V1"
    query: |
      count(count by (client_id) (
        http_requests_total{path=~"/api/v1/(context-authority|analytics)/[^v].*"}
      ))

alerts:
  - name: "V1 Still in Use After 30 Days"
    condition: sum(rate(http_requests_total{deprecated="true"}[1d])) > 100
    severity: warning
    
  - name: "V1 Still in Use After 90 Days"
    condition: sum(rate(http_requests_total{deprecated="true"}[1d])) > 0
    severity: critical
```

### Migration Tracking

```python
# backend/app/middleware/deprecation_logger.py

import logging
from datetime import datetime
from fastapi import Request

logger = logging.getLogger("deprecation")

async def log_deprecated_call(request: Request):
    """Log deprecated API usage for migration tracking."""
    
    deprecated_patterns = [
        r"/api/v1/context-authority/(?!v2)",
        r"/api/v1/analytics/(?!v2)"
    ]
    
    for pattern in deprecated_patterns:
        if re.match(pattern, request.url.path):
            logger.warning(
                "Deprecated API call",
                extra={
                    "path": request.url.path,
                    "method": request.method,
                    "client_ip": request.client.host,
                    "user_agent": request.headers.get("user-agent"),
                    "user_id": getattr(request.state, "user_id", None),
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
            break
```

---

## 🔐 Deprecation Policy

```
┌─────────────────────────────────────────────────────────────────────────┐
│  API DEPRECATION POLICY                                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PUBLIC API (External clients):                                        │
│  ───────────────────────────────────────────────────────────────────── │
│  • Notice period: ≥180 days before removal                             │
│  • Migration guide: Required                                           │
│  • Sunset header: Required (RFC 8594)                                  │
│  • Backward compatibility: Required during deprecation                 │
│                                                                         │
│  INTERNAL API (Our frontends only):                                    │
│  ───────────────────────────────────────────────────────────────────── │
│  • Notice period: ≥30 days before removal                              │
│  • Migration guide: Recommended                                        │
│  • Sunset header: Required                                             │
│  • Backward compatibility: Best effort                                 │
│                                                                         │
│  CLASSIFICATION:                                                       │
│  • Context Authority V1: INTERNAL → 30-day deprecation                 │
│  • Analytics V1: INTERNAL → 30-day deprecation                         │
│                                                                         │
│  TIMELINE:                                                             │
│  • Feb 3, 2026: Deprecation headers added                              │
│  • Feb 10, 2026: Frontend migrated (V1 calls = 0)                      │
│  • Mar 5, 2026: V1 endpoints return 410 Gone                           │
│  • Apr 3, 2026: V1 code removed from codebase                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ✅ Exit Criteria

| Metric | Before | Target | Verification |
|--------|--------|--------|--------------|
| Context Authority endpoints | 18 | 9 | `grep -c "@router" context_authority*.py` |
| Analytics endpoints | 19 | 6 | `grep -c "@router" analytics*.py` |
| Total LOC | 2,277 | <1,500 | `wc -l` |
| V1 API calls/day | X | 0 | Deprecation logs |
| Frontend V1 imports | Y | 0 | Code search |
| Test coverage | Z% | >80% | pytest-cov |

---

## 📅 Timeline Summary

| Date | Milestone | Owner |
|------|-----------|-------|
| **Feb 4** | Deprecation headers added | Backend |
| **Feb 5** | Compatibility layer complete | Backend |
| **Feb 6** | Frontend migration complete | Frontend |
| **Feb 7** | CLI/Extension updated | CLI Team |
| **Feb 8** | Verification + documentation | Tech Lead |
| **Mar 5** | V1 returns 410 Gone | Backend |
| **Apr 3** | V1 code removed | Backend |

---

_Migration Plan Version: 1.0_  
_Created: February 3, 2026_  
_Owner: Backend Lead + API Team_
