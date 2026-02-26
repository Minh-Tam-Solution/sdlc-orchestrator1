---
sdlc_version: "6.1.1"
document_type: "Sprint Plan"
status: "IN_PROGRESS"
sprint: "209"
spec_id: "SPRINT-209"
tier: "STANDARD"
stage: "04 - Build"
---

# Sprint 209 — OTT Identity + Team Collaboration

**Sprint Duration**: Feb 26–28, 2026 (3 working days P0+P1, 5 days with P2)
**Sprint Goal**: Enable team collaboration via Telegram group chat with identity-linked permissions — `/link`, `/verify`, `/unlink` commands + identity resolver integration
**Status**: IN PROGRESS
**Priority**: P0 (Identity blocker) + P1 (Security + UX)
**Framework**: SDLC 6.1.1
**Previous Sprint**: [Sprint 208 — Pre-Release Hardening](SPRINT-208-RELEASE-HARDENING.md)
**Sprint Close**: [SPRINT-209-CLOSE.md](SPRINT-209-CLOSE.md) *(to be created at close)*
**Release Target**: v1.2.0 — Team Collaboration via OTT
**ADR**: [ADR-068 — OTT Identity Linking](../../02-design/01-ADRs/ADR-068-OTT-Identity-Linking.md)
**FR**: [FR-050 — OTT Identity Linking](../../01-planning/03-Functional-Requirements/FR-050-OTT-Identity-Linking.md)
**Reviewed By**: Architect (APPROVED w/ revisions) + CTO (APPROVED w/ revisions)

---

## Sprint 209 Goal

Sprint 208 closed the Pre-Release Hardening milestone. Dogfooding on Telegram revealed a **Day 1 blocker**: Telegram sends numeric `sender_id` (e.g., `7023486123`) but all governance commands expect internal User UUID. Without identity resolution, every permission-gated OTT command fails silently.

**P0 Blockers**:
1. No mechanism to link Telegram account → SDLC user (`/link` + `/verify`)
2. `ott_identity_resolver.py` has wrong import path + no DB session passed
3. `OAuthAccount.access_token` is `nullable=False` — OTT linking has no OAuth token → INSERT fails
4. No UniqueConstraint on `(provider, provider_account_id)` — duplicates possible

**P1 Security**:
5. Unlinked users can set workspace and see project names (Track C security fix)
6. No rate limiting on `/link` (spam vector)

**P1 UX**:
7. No `/unlink` command (wrong email recovery)
8. Identity cache TTL too short (5 min → 60 min)

---

## CRITICAL SETUP — BotFather Group Privacy

**MUST complete before group chat testing (Track D)**:
```
BotFather → /setprivacy → @SdlcOrchestratorbot → Disable
```
Without this, bot only sees `/commands` in groups, not free-text messages.

---

## Day Timeline (3 Working Days — P0+P1)

| Day | Time | Block | Track |
|-----|------|-------|-------|
| 1 | 09:00–09:30 | Track A-DB: Alembic migration | `s209_001_oauth_ott_linking.py` |
| 1 | 09:30–10:00 | Track B-1: Fix `ott_identity_resolver.py` | Import path + TTL |
| 1 | 10:00–13:00 | Track A: `ott_link_handler.py` | `/link` + `/verify` + `/unlink` + rate limiting |
| 2 | 09:00–10:30 | Track B-2: Integrate identity resolver | `ai_response_handler.py` modification |
| 2 | 10:30–11:00 | Track C: Deny unlinked workspace access | `workspace_service.py` security fix |
| 2 | 11:00–11:30 | Track A-2: Route `/link`, `/verify`, `/unlink` | `ai_response_handler.py` routing |
| 3 | 09:00–12:00 | Track E: Tests | 13 test cases (E1-E13) |
| 3 | 12:00–12:30 | Regression guard | Full test suite run |
| 3 | 12:30–13:00 | Rebuild staging + E2E verification | Docker rebuild + Telegram testing |

**Total estimated**: ~12 hours coding + 3 hours testing/docs = **3 working days**

---

## Sprint 209 Backlog

### Track A-DB — P0: Alembic Migration (~30 min)

| ID | Item | Est | Status |
|----|------|-----|--------|
| ADB1 | `access_token` column: `nullable=False` → `nullable=True, server_default=''` | 10 min | ⏳ |
| ADB2 | UniqueConstraint on `(provider, provider_account_id)` | 10 min | ⏳ |
| ADB3 | Verify migration runs cleanly on staging DB | 10 min | ⏳ |

**New file**: `backend/alembic/versions/s209_001_oauth_ott_linking.py`

**Why P0**: Without ADB1, `OAuthAccount` INSERT raises `IntegrityError` (access_token NOT NULL). Without ADB2, duplicate `/link` creates multiple rows → `scalar_one_or_none()` raises `MultipleResultsFound`.

**Schema change**:
```python
# ADB1: access_token nullable for OTT linking (no OAuth token)
op.alter_column('oauth_accounts', 'access_token',
    existing_type=sa.String(512),
    nullable=True,
    server_default='')

# ADB2: Prevent duplicate provider+account linking
op.create_unique_constraint(
    'uq_oauth_provider_account',
    'oauth_accounts',
    ['provider', 'provider_account_id'])
```

---

### Track A — P0: OTT Link Handler (~3 hours)

| ID | Item | Est | Status |
|----|------|-----|--------|
| A1 | `/link <email>` — email lookup + 6-digit code + Redis store + email send | 60 min | ⏳ |
| A2 | `/verify <code>` — code validation + oauth_accounts upsert + cache clear | 45 min | ⏳ |
| A3 | `/unlink` — oauth_accounts delete + cache clear | 20 min | ⏳ |
| A4 | Rate limiting — max 5 `/link` per 15 min per sender | 15 min | ⏳ |
| A5 | Route `/link`, `/verify`, `/unlink` in `ai_response_handler.py` | 30 min | ⏳ |

**New file**: `backend/app/services/agent_bridge/ott_link_handler.py` (~180 LOC)

**Key design decisions** (from ADR-068):
- `asyncio.to_thread(send_email, ...)` — email_service is sync (smtplib), must not block event loop
- Import `OAuthAccount` from `app.models.user` — NOT `app.models.oauth_account` (file doesn't exist)
- Redis key: `ott:link_code:{channel}:{sender_id}` — channel-agnostic for future Zalo/Slack
- GETDEL for single-use code consumption (not GET + DELETE)
- `access_token=""` — empty string, not NULL (future-proof for OAuth providers)

**Rate limiting**:
- Redis key: `ott:link_rate:{channel}:{sender_id}` → INCR with 15-min TTL
- Max 5 attempts → "⚠️ Too many link attempts. Try again in 15 minutes."

**Reuses**:
- `email_service.send_email()` from `backend/app/services/email_service.py`
- `OAuthAccount` model from `backend/app/models/user.py:425+`
- `User` model from `backend/app/models/user.py`
- Redis client from `app.utils.redis.get_redis_client()`
- `AsyncSessionLocal` from `app.db.session`

---

### Track B — P0: Identity Resolver Fix + Integration (~2 hours)

| ID | Item | Est | Status |
|----|------|-----|--------|
| B1 | Fix import: `app.models.oauth_account` → `app.models.user` | 5 min | ⏳ |
| B2 | Upgrade cache TTL: 300s (5 min) → 3600s (60 min) | 5 min | ⏳ |
| B3 | Add identity resolution to `ai_response_handler.py` with `AsyncSessionLocal` DB session | 45 min | ⏳ |
| B4 | Pass `effective_user_id` to workspace, governance, and agent team handlers | 30 min | ⏳ |
| B5 | Unlinked user guard — "⚠️ Account not linked" reply for governance commands | 20 min | ⏳ |

**Modified files**:
- `ott_identity_resolver.py` — fix import (B1), upgrade TTL (B2)
- `ai_response_handler.py` — identity resolution block (B3), effective_user_id passthrough (B4), unlinked guard (B5)

**Key change in `ai_response_handler.py`** (after `_extract_chat_context`):
```python
from app.services.agent_bridge.ott_identity_resolver import resolve_ott_user_id
from app.db.session import AsyncSessionLocal

redis = await get_redis_client()
async with AsyncSessionLocal() as db:
    resolved_user_id = await resolve_ott_user_id(channel, sender_id, redis, db=db)
effective_user_id = resolved_user_id or sender_id
```

Then replace `sender_id` with `effective_user_id` in:
- `execute_workspace_command(user_id=effective_user_id)`
- `execute_governance_action(user_id=effective_user_id)`
- `handle_agent_team_request(sender_id=effective_user_id)`

---

### Track C — P0: Deny Unlinked Workspace Access (~30 min)

| ID | Item | Est | Status |
|----|------|-----|--------|
| C1 | `resolve_project_by_name()` — return empty for non-UUID user_id | 15 min | ⏳ |
| C2 | Verify OTT_GATEWAY_USER_ID env var path still works | 15 min | ⏳ |

**Modified file**: `backend/app/services/agent_bridge/workspace_service.py`

**Security fix** (CTO C1 + Architect P1-3): Unlinked users MUST NOT see project names via workspace.

```python
# workspace_service.py line 168-172 — EXISTING CODE already does this correctly:
try:
    UUID(user_id)
except (ValueError, AttributeError):
    return {"exact": None, "matches": []}  # Unlinked → deny access
```

The existing code already returns empty for non-UUID user_id. Track C confirms this behavior is correct and adds a log message for auditability.

---

### Track D — P1: Group Chat Awareness (No code changes)

| ID | Item | Est | Status |
|----|------|-----|--------|
| D1 | BotFather: `/setprivacy` → Disable for @SdlcOrchestratorbot | 2 min | ⏳ |
| D2 | Document Group Privacy setup in sprint plan (this document) | Done | ✅ DONE |

Architecture already supports group chat:
- `chat_id` = group ID (negative number) → shared workspace
- `sender_id` = individual user ID → individual identity resolution
- No code changes needed — BotFather configuration only

---

### Track E — P0: Tests (~3 hours)

| ID | Item | Est | Status |
|----|------|-----|--------|
| E1 | `/link` with valid email → code generated, stored in Redis | 15 min | ⏳ |
| E2 | `/link` with unknown email → error reply | 10 min | ⏳ |
| E3 | `/verify` with correct code → oauth_accounts upserted (access_token="" OK) | 15 min | ⏳ |
| E4 | `/verify` with wrong code → error reply | 10 min | ⏳ |
| E5 | `/verify` with expired code → error reply | 10 min | ⏳ |
| E6 | Double `/verify` → second attempt fails (GETDEL single-use) | 10 min | ⏳ |
| E7 | Identity resolve with oauth_accounts match → returns User UUID | 10 min | ⏳ |
| E8 | Identity resolve with OTT_GATEWAY_USER_ID fallback → returns env UUID | 10 min | ⏳ |
| E9 | Identity resolve with no mapping → returns None | 10 min | ⏳ |
| E10 | Identity resolve with UUID sender_id (web/CLI) → passthrough | 10 min | ⏳ |
| E11 | `/unlink` → oauth_accounts deleted, cache cleared | 10 min | ⏳ |
| E12 | `/link` rate limiting → 6th attempt blocked | 10 min | ⏳ |
| E13 | Group chat: different sender_id → different resolved users | 15 min | ⏳ |

**New files**:
- `backend/tests/unit/test_ott_link_handler.py` (~140 LOC, tests E1-E6 + E11-E12)
- `backend/tests/unit/test_ott_identity_resolver.py` (~80 LOC, tests E7-E10 + E13)

---

### Track F — P2: Admin OTT Link Management (Sprint 210 deferrable)

| ID | Item | Est | Status |
|----|------|-----|--------|
| F1 | `GET /api/v1/admin/ott-links` — list linked accounts | 40 min | ⏳ |
| F2 | `DELETE /api/v1/admin/ott-links/{id}` — admin unlink | 40 min | ⏳ |

**Priority**: P2 — implement if time permits Day 4-5, otherwise Sprint 210.

---

## Definition of Done — Sprint 209

- [ ] Alembic migration `s209_001` — `access_token` nullable + UniqueConstraint
- [ ] `ott_link_handler.py` — `/link`, `/verify`, `/unlink` with rate limiting
- [ ] `ott_identity_resolver.py` — import fix (`app.models.user`) + TTL 60 min
- [ ] `ai_response_handler.py` — identity resolution with `AsyncSessionLocal` + `effective_user_id`
- [ ] `workspace_service.py` — unlinked user deny confirmed + audit log
- [ ] `/link` sends 6-digit code to email via `asyncio.to_thread(send_email)`
- [ ] `/verify` upserts `oauth_accounts` with `access_token=""`
- [ ] `/unlink` deletes oauth_accounts + clears identity cache
- [ ] Rate limiting: max 5 `/link` per 15 min per sender
- [ ] Unlinked users: governance commands reply "⚠️ Account not linked"
- [ ] 13/13 Sprint 209 tests passing (E1-E13)
- [ ] 310+ regression guards passing | 0 regressions
- [ ] CURRENT-SPRINT.md updated to Sprint 209
- [ ] BotFather Group Privacy OFF for @SdlcOrchestratorbot

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Email delivery fails (SMTP/SendGrid) | Medium | High | `EMAIL_SANDBOX_MODE=true` for dev; fallback to manual code display |
| UniqueConstraint migration fails on existing duplicates | Low | High | Pre-check: `SELECT provider, provider_account_id, COUNT(*) ... HAVING COUNT(*) > 1` |
| Redis GETDEL not available (Redis <6.2) | Low | Medium | Fallback to GET + DELETE (non-atomic but acceptable for link codes) |
| Group Privacy setting forgotten | Medium | High | Documented as CRITICAL SETUP in sprint plan + deployment checklist |

---

## Architecture Notes

### Identity Resolution Flow (Post-Sprint 209)
```
Telegram webhook → ott_gateway.py → ai_response_handler.py
                                          │
                                    ┌─────┴─────┐
                                    │ Extract    │
                                    │ sender_id  │
                                    └─────┬─────┘
                                          │
                                    ┌─────┴──────────┐
                                    │ resolve_ott_    │
                                    │ user_id()       │
                                    │ (Redis cache    │
                                    │  → oauth_accts  │
                                    │  → env var      │
                                    │  → None)        │
                                    └─────┬──────────┘
                                          │
                              ┌───────────┴───────────┐
                              │                       │
                        resolved (UUID)          unlinked (None)
                              │                       │
                     governance OK             "⚠️ /link first"
                     workspace OK
```

### Channel-Agnostic Design
All Redis keys use `{channel}:{sender_id}` namespace — adding Zalo (Sprint 210+), Slack (Sprint 212+), or MS Teams (Sprint 215+) requires only:
1. New webhook endpoint + normalizer in `ott_gateway.py`
2. New responder (e.g., `zalo_responder.py`)
3. No changes to identity resolver, workspace service, or governance handler

---

## Key Files Summary

| File | Action | LOC | Track |
|------|--------|-----|-------|
| `alembic/versions/s209_001_oauth_ott_linking.py` | NEW | ~30 | A-DB |
| `agent_bridge/ott_link_handler.py` | NEW | ~180 | A |
| `agent_bridge/ott_identity_resolver.py` | FIX | ~10 | B |
| `agent_bridge/ai_response_handler.py` | MODIFY | ~40 | A+B |
| `agent_bridge/workspace_service.py` | VERIFY | ~5 | C |
| `tests/unit/test_ott_link_handler.py` | NEW | ~140 | E |
| `tests/unit/test_ott_identity_resolver.py` | NEW | ~80 | E |
| **Total (P0+P1)** | | **~485** | |

---

## G-Sprint-Close Gate — Sprint 209

- [ ] All P0 items implemented and tested
- [ ] 13/13 new tests passing
- [ ] 310+ regression guards: 0 regressions
- [ ] Staging rebuild successful
- [ ] E2E Telegram test: `/link` → `/verify` → `/workspace set` → governance command
- [ ] PM verification: code audit CLEAN
- [ ] CTO score: ≥ 9.0/10

---

## Quality Scorecard (CTO Review)

| Dimension | Target | Notes |
|-----------|--------|-------|
| Zero Mock | 10/10 | Real email via to_thread, real DB via AsyncSessionLocal |
| Type Hints | 10/10 | Full typing on all new functions |
| AGPL Compliance | 10/10 | No AGPL imports |
| Error Handling | 9/10 | Graceful degradation on Redis/email failures |
| Security | 10/10 | Rate limiting, single-use codes, deny unlinked access |
| Testing | 10/10 | 13 new tests covering happy + unhappy paths |

---

## CURRENT-SPRINT.md Update

After Sprint 209 close:
```markdown
# Current Sprint: Sprint 209 — OTT Identity + Team Collaboration
Sprint Duration: Feb 26–28, 2026 (3 working days)
Sprint Goal: Enable team collaboration via Telegram with identity-linked permissions
Previous Sprint: Sprint 208 — Pre-Release Hardening
```

---

*Created*: February 26, 2026
*Next Sprint*: Sprint 210 — Zalo OA Notification Channel (tentative)
