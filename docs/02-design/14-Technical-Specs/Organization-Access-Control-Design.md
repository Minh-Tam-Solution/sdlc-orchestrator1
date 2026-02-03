# Organization Access Control System - Technical Design Document

**Document**: Organization Access Control System
**Version**: 1.0
**Status**: APPROVED
**Date**: February 3, 2026
**Sprint**: 146
**Related ADR**: ADR-047

---

## Executive Summary

This document describes the technical design for the Organization Access Control System, enabling:
- Organization-level invitations (users join orgs without teams)
- Direct member addition (bypass invitation for enterprise)
- Tier-based permissions (effective tier = highest across all orgs)

**Scope**: 1,350 LOC | **Duration**: 5 days | **Risk**: LOW

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │ Org Settings     │  │ Team Settings    │  │ User Profile  │ │
│  │ - Invite Members │  │ - Invite Members │  │ - Show Orgs   │ │
│  │ - Direct Add     │  │ - (Sprint 128)   │  │ - Tier Badge  │ │
│  │ - List Pending   │  └──────────────────┘  └───────────────┘ │
│  └──────────────────┘                                           │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTPS
┌────────────────────────────┴────────────────────────────────────┐
│                        BACKEND API                               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Organization Invitations Routes (7 endpoints)            │   │
│  │ POST   /organizations/{id}/invitations                   │   │
│  │ POST   /org-invitations/{id}/resend                      │   │
│  │ GET    /org-invitations/{token} (PUBLIC)                 │   │
│  │ POST   /org-invitations/{token}/accept (AUTH)            │   │
│  │ POST   /org-invitations/{token}/decline (PUBLIC)         │   │
│  │ GET    /organizations/{id}/invitations                   │   │
│  │ DELETE /org-invitations/{id}                             │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Direct Member Add Route (1 endpoint)                     │   │
│  │ POST   /organizations/{id}/members                       │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ Service Layer                                            │   │
│  │ - organization_invitation_service.py (token gen, email)  │   │
│  │ - email_service.py (SendGrid integration)                │   │
│  │ - cleanup_invitations.py (Celery task)                   │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │ SQL
┌────────────────────────────┴────────────────────────────────────┐
│                        DATABASE (PostgreSQL)                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ organization_invitations (NEW)                           │   │
│  │ - id (PK), organization_id (FK), invited_email           │   │
│  │ - invitation_token_hash (SHA256, UNIQUE)                 │   │
│  │ - role (admin/member), status (pending/accepted/...)     │   │
│  │ - expires_at, resend_count, ip_address, user_agent       │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ user_organizations (EXISTS)                              │   │
│  │ - user_id (PK), organization_id (PK), role, joined_at    │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ organizations (EXISTS)                                   │   │
│  │ - id (PK), name, slug, plan (free/pro/enterprise)        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Model

### New Table: organization_invitations

```sql
CREATE TABLE organization_invitations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    invited_email VARCHAR(255) NOT NULL,
    invitation_token_hash VARCHAR(64) NOT NULL UNIQUE,  -- SHA256
    role VARCHAR(20) NOT NULL DEFAULT 'member',
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    invited_by UUID NOT NULL REFERENCES users(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL,
    accepted_at TIMESTAMPTZ,
    declined_at TIMESTAMPTZ,
    resend_count INTEGER NOT NULL DEFAULT 0,
    last_resent_at TIMESTAMPTZ,
    ip_address INET,
    user_agent TEXT,

    -- Constraints
    CONSTRAINT valid_expiry CHECK (expires_at > created_at),
    CONSTRAINT valid_invitation_role CHECK (role IN ('admin', 'member'))
);

-- Indexes
CREATE INDEX idx_org_invitations_org_id ON organization_invitations(organization_id);
CREATE INDEX idx_org_invitations_email ON organization_invitations(invited_email);
CREATE UNIQUE INDEX idx_org_invitations_token ON organization_invitations(invitation_token_hash);
CREATE INDEX idx_org_invitations_status ON organization_invitations(status);

-- Cleanup index (partial)
CREATE INDEX idx_org_invitations_cleanup ON organization_invitations(created_at)
    WHERE status IN ('accepted', 'declined', 'expired', 'cancelled');
```

### Status Values

| Status | Description | Transitions |
|--------|-------------|-------------|
| `pending` | Awaiting user action | → accepted, declined, expired, cancelled |
| `accepted` | User joined org | Terminal |
| `declined` | User rejected | Terminal |
| `expired` | 7 days elapsed | Terminal |
| `cancelled` | Admin cancelled | Terminal |

---

## Data Flow Diagrams

### Flow 1: Organization Invitation (Admin → User)

```
┌─────────┐                    ┌─────────┐                    ┌──────────┐
│ Admin   │                    │ Backend │                    │ Database │
└────┬────┘                    └────┬────┘                    └────┬─────┘
     │                              │                              │
     │ POST /orgs/{id}/invitations  │                              │
     │─────────────────────────────>│                              │
     │                              │ 1. Check RBAC (owner/admin)  │
     │                              │─────────────────────────────>│
     │                              │<─────────────────────────────│
     │                              │ 2. Check rate limit (50/hr)  │
     │                              │─────────────────────────────>│
     │                              │<─────────────────────────────│
     │                              │ 3. Generate token (32 bytes) │
     │                              │ 4. Hash token (SHA256)       │
     │                              │ 5. Create invitation record  │
     │                              │─────────────────────────────>│
     │                              │<─────────────────────────────│
     │<─────────────────────────────│ 6. Return invitation_id      │
     │                              │                              │
     │                              │ 7. Send email (async)        │
     │                              │─────────────────────────────>│
     │                              │    SendGrid API              │

┌────────┐                    ┌─────────┐                    ┌──────────┐
│ User   │                    │ Backend │                    │ Database │
└───┬────┘                    └────┬────┘                    └────┬─────┘
    │                              │                              │
    │ Click email link             │                              │
    │ GET /org-invitations/{token} │                              │
    │─────────────────────────────>│                              │
    │                              │ 1. Hash token                │
    │                              │ 2. Lookup by hash            │
    │                              │─────────────────────────────>│
    │                              │<─────────────────────────────│
    │                              │ 3. Check expiry, status      │
    │<─────────────────────────────│ 4. Return org details        │
    │                              │                              │
    │ POST /org-invitations/{token}/accept (AUTH)                 │
    │─────────────────────────────>│                              │
    │                              │ 1. Verify email matches      │
    │                              │ 2. Check user not member     │
    │                              │─────────────────────────────>│
    │                              │<─────────────────────────────│
    │                              │ 3. Create UserOrganization   │
    │                              │─────────────────────────────>│
    │                              │ 4. Update invitation.status  │
    │                              │─────────────────────────────>│
    │<─────────────────────────────│ 5. Return org_id, redirect   │
```

### Flow 2: Direct Member Addition

```
┌─────────┐                    ┌─────────┐                    ┌──────────┐
│ Admin   │                    │ Backend │                    │ Database │
└────┬────┘                    └────┬────┘                    └────┬─────┘
     │                              │                              │
     │ POST /orgs/{id}/members      │                              │
     │ {user_email, role}           │                              │
     │─────────────────────────────>│                              │
     │                              │ 1. Check RBAC (owner/admin)  │
     │                              │─────────────────────────────>│
     │                              │<─────────────────────────────│
     │                              │ 2. Verify user exists        │
     │                              │─────────────────────────────>│
     │                              │<─────────────────────────────│
     │                              │ 3. Check not already member  │
     │                              │─────────────────────────────>│
     │                              │<─────────────────────────────│
     │                              │ 4. Create UserOrganization   │
     │                              │─────────────────────────────>│
     │                              │<─────────────────────────────│
     │<─────────────────────────────│ 5. Return membership         │
     │                              │ 6. Send notification (async) │
     │                              │    "You've been added to..." │
```

### Flow 3: Tier Calculation

```
┌────────┐                    ┌─────────┐                    ┌──────────┐
│ User   │                    │ Backend │                    │ Database │
└───┬────┘                    └────┬────┘                    └────┬─────┘
    │                              │                              │
    │ GET /premium-feature (AUTH)  │                              │
    │─────────────────────────────>│                              │
    │                              │ 1. Get current_user          │
    │                              │ 2. Call user.effective_tier  │
    │                              │    (cached_property)         │
    │                              │                              │
    │                              │ 3. Load user.organizations   │
    │                              │    (selectin - single query) │
    │                              │─────────────────────────────>│
    │                              │<─────────────────────────────│
    │                              │ 4. Find max tier (with early │
    │                              │    exit if enterprise found) │
    │                              │ 5. Check if tier allowed     │
    │                              │    (pro, enterprise)         │
    │<─────────────────────────────│ 6. Return feature data       │
    │           OR                 │           OR                 │
    │<─────────────────────────────│ 403 "Requires Pro tier"      │
```

---

## Security Model

### Token Generation & Hashing

```python
import secrets
import hashlib

# 1. Generate secure random token (32 bytes = 256 bits)
raw_token = secrets.token_urlsafe(32)  # "XyZ9-AbC3..."

# 2. Hash for storage (SHA256)
token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

# 3. Store hash in database (NEVER store raw token)
invitation.invitation_token_hash = token_hash

# 4. Send raw token in email
email_link = f"{FRONTEND_URL}/invitations/{raw_token}"

# 5. On acceptance, hash provided token and lookup
provided_hash = hashlib.sha256(provided_token.encode()).hexdigest()
invitation = db.query(OrganizationInvitation).filter(
    OrganizationInvitation.invitation_token_hash == provided_hash
).first()
```

### Rate Limiting (Redis-based)

```python
# Per-organization limit: 50 invitations/hour
key = f"org_invitations:{organization_id}:{hour}"
current_count = redis.incr(key)
redis.expire(key, 3600)  # 1 hour TTL

if current_count > 50:
    raise HTTPException(429, "Rate limit exceeded (50/hour)")
```

### RBAC Permission Matrix

| Action | Owner | Admin | Member |
|--------|-------|-------|--------|
| Send invitation (admin role) | ✅ | ❌ | ❌ |
| Send invitation (member role) | ✅ | ✅ | ❌ |
| Resend invitation | ✅ | ✅ | ❌ |
| Cancel invitation | ✅ | ✅ | ❌ |
| Direct add (admin role) | ✅ | ❌ | ❌ |
| Direct add (member role) | ✅ | ✅ | ❌ |
| Accept invitation | ✅ | ✅ | ✅ |
| Decline invitation | ✅ | ✅ | ✅ |

---

## API Specification

### Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/organizations/{id}/invitations` | Required | Send invitation |
| POST | `/org-invitations/{id}/resend` | Required | Resend invitation |
| GET | `/org-invitations/{token}` | Public | Get invitation details |
| POST | `/org-invitations/{token}/accept` | Required | Accept invitation |
| POST | `/org-invitations/{token}/decline` | Public | Decline invitation |
| GET | `/organizations/{id}/invitations` | Required | List invitations |
| DELETE | `/org-invitations/{id}` | Required | Cancel invitation |
| POST | `/organizations/{id}/members` | Required | Direct add member |

### Request/Response Examples

#### Send Invitation
```http
POST /api/v1/organizations/123/invitations
Authorization: Bearer <token>
Content-Type: application/json

{
  "invited_email": "user@example.com",
  "role": "member",
  "message": "Join our team!"
}
```

**Response 201**:
```json
{
  "invitation_id": "abc-123",
  "email": "user@example.com",
  "role": "member",
  "status": "pending",
  "expires_at": "2026-02-10T00:00:00Z"
}
```

#### Accept Invitation
```http
POST /api/v1/org-invitations/{token}/accept
Authorization: Bearer <token>
```

**Response 200**:
```json
{
  "organization_id": "org-123",
  "role": "member",
  "redirect_url": "/org/acme-corp/dashboard"
}
```

---

## Performance Optimization

### Database Indexes

```sql
-- Primary lookup: by token hash (unique)
CREATE UNIQUE INDEX idx_org_invitations_token
ON organization_invitations(invitation_token_hash);

-- Filter by status (pending invitations list)
CREATE INDEX idx_org_invitations_status
ON organization_invitations(status);

-- Cleanup job (partial index for efficiency)
CREATE INDEX idx_org_invitations_cleanup
ON organization_invitations(created_at)
WHERE status IN ('accepted', 'declined', 'expired', 'cancelled');

-- Organization's invitations (filter by org)
CREATE INDEX idx_org_invitations_org_id
ON organization_invitations(organization_id);
```

### Query Optimization

```python
# Efficient tier calculation (selectin prevents N+1)
class User(Base):
    organizations = relationship(
        secondary="user_organizations",
        lazy="selectin"  # Single query for all orgs
    )

# Early exit optimization
for org in self.organizations:
    rank = TIER_RANK.get(org.plan, 1)
    if rank > max_rank:
        max_rank = rank
        max_tier = org.plan
        if max_rank == 4:  # Enterprise found, stop
            break
```

---

## Error Handling

### HTTP Status Codes

| Code | Scenario | Example |
|------|----------|---------|
| 201 | Invitation created | `{"invitation_id": "...", "expires_at": "..."}` |
| 200 | Invitation accepted | `{"organization_id": "...", "role": "member"}` |
| 400 | Invalid input | `{"error": "invalid_role", "message": "Role must be admin or member"}` |
| 403 | Insufficient permissions | `{"error": "not_authorized", "message": "Only owners can invite admins"}` |
| 404 | Invitation not found | `{"error": "invitation_not_found"}` |
| 409 | User already member | `{"error": "already_member", "message": "User is already a member"}` |
| 410 | Invitation already used | `{"error": "invitation_used", "message": "Invitation already accepted"}` |
| 429 | Rate limit exceeded | `{"error": "rate_limit", "message": "50 invitations/hour limit"}` |

---

## Cleanup Job

```python
# backend/app/tasks/cleanup_invitations.py
from datetime import datetime, timedelta
from celery import Celery
from app.models.organization_invitation import OrganizationInvitation
from app.db.session import SessionLocal

celery = Celery('tasks')

@celery.task
def cleanup_old_invitations():
    """
    Delete non-pending invitations older than 90 days.

    Purpose: Prevent database bloat from historical invitations.
    Runs: Daily at 2:00 AM UTC (Celery Beat schedule)
    Retention: 90 days for audit compliance
    """
    db = SessionLocal()
    try:
        cutoff = datetime.utcnow() - timedelta(days=90)
        deleted_count = db.query(OrganizationInvitation).filter(
            OrganizationInvitation.status.in_(['accepted', 'declined', 'expired', 'cancelled']),
            OrganizationInvitation.created_at < cutoff
        ).delete(synchronize_session=False)

        db.commit()
        return {"deleted_count": deleted_count, "cutoff_date": cutoff.isoformat()}
    finally:
        db.close()
```

---

## Testing Strategy

### Test Categories

| Category | Count | Coverage |
|----------|-------|----------|
| Unit tests (service layer) | 30 | Token generation, rate limiting, validation |
| Integration tests (API) | 15 | Full flows, RBAC, error cases |
| E2E tests (Playwright) | 5 | User journey (invite → accept) |
| **Total** | **50** | **95%+** |

### Critical Test Cases

1. Token security (SHA256 hashing, no collisions)
2. Rate limiting (50/hour enforcement)
3. RBAC (owner vs admin permissions)
4. Email verification (invited email must match)
5. One-time use (status prevents replay)
6. Tier calculation (multi-org, early exit)

---

## Files to Create/Modify

### New Files (7)
| File | LOC | Purpose |
|------|-----|---------|
| `backend/app/models/organization_invitation.py` | 180 | Model |
| `backend/app/api/routes/organization_invitations.py` | 320 | API routes |
| `backend/app/services/organization_invitation_service.py` | 200 | Business logic |
| `backend/app/tasks/cleanup_invitations.py` | 50 | Celery task |
| `backend/alembic/versions/XXX_create_org_invitations.py` | 80 | Migration |
| `frontend/src/components/org/OrgInviteModal.tsx` | 80 | UI component |
| `frontend/tests/e2e/org-invitations.spec.ts` | 100 | E2E tests |

### Modified Files (4)
| File | LOC | Purpose |
|------|-----|---------|
| `backend/app/models/user.py` | +20 | effective_tier property |
| `backend/app/api/routes/organizations.py` | +50 | Direct add endpoint |
| `frontend/src/components/user/UserProfile.tsx` | +50 | Show orgs + tier |
| `backend/app/core/celery_config.py` | +10 | Cleanup schedule |

---

## Authorization

**CTO Signature**: `Ed25519:CTO:Sprint146:DESIGN:APPROVED`
**Approval Code**: `SPEC-ORG-ACCESS-v1.0-APPROVED`
**Date**: February 3, 2026

---

*SDLC Orchestrator - Organization Access Control Technical Design*
*Sprint 146 | 1,350 LOC | 5 days | Risk: LOW*
