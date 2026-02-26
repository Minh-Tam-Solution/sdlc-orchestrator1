---
sdlc_version: "6.1.1"
document_type: user-story
status: approved
sprint: "209"
spec_id: US-COLLAB-001
tier: PROFESSIONAL
stage: "04-BUILD"
title: Team Collaboration Flow
epic: EP-07-Multi-Agent-Team-Engine
author: PM
last_updated: "2026-02-26"
---

# Team Collaboration Flow — SDLC Orchestrator

> **CEO Directive (Sprint 190)**: Conversation-First — OTT + CLI = PRIMARY (daily work), Web App = ADMIN ONLY (owner/admin).

---

## 1. Organization Structure

```
Organization (Company)
  └── Team (Project Team)
        ├── Owner  (CTO/CEO) — SE4H Coach, full governance authority
        ├── Admin  (PM/Lead) — SE4H Coach, manage members + sprint
        ├── Member (Dev/QA/Architect) — SE4H Member, execute + submit evidence
        └── AI Agent — SE4A Executor, execute ONLY, NO governance approval
```

**SASE Enforcement** (Database Level):

| Role | `member_type` | SASE Role | Governance |
|------|--------------|-----------|------------|
| `owner` | `human` | SE4H Coach | Full authority |
| `admin` | `human` | SE4H Coach | Manage team + sprint |
| `member` | `human` | SE4H Member | Execute + submit evidence |
| `ai_agent` | `ai_agent` | SE4A Executor | Execute only |

```sql
-- PostgreSQL CHECK constraint: AI agents CANNOT be owner/admin
CHECK NOT (member_type = 'ai_agent' AND role IN ('owner', 'admin'))
```

**TeamMember Model** (`backend/app/models/team_member.py`):
- `team_id` (UUID FK) + `user_id` (UUID FK) — `UNIQUE(team_id, user_id)`
- `role`: `owner | admin | member | ai_agent`
- `member_type`: `human | ai_agent`
- Soft delete via `deleted_at` (nullable DateTime)

---

## 2. Four Interfaces — Role Matrix

| Action | Web App (admin-only) | CLI (`sdlcctl`) | Extension (VS Code) | OTT (Telegram/Zalo/Teams/Slack) |
|--------|---------------------|-----------------|---------------------|-------------------------------|
| Create project | Admin form | `sdlcctl create-project` | — | `"create project BFlow"` |
| Invite member | Admin invite UI | `sdlcctl invite` | — | `/invite email@...` |
| Set workspace | — | — | — | `/workspace set BFlow` (group shared) |
| Submit evidence | File upload | `sdlcctl submit-evidence` | `Cmd+Shift+E` | `"submit evidence: tests passed"` |
| View gate status | Dashboard | `sdlcctl gate-status` | Context overlay | `"gate status"` or `/gates` |
| Approve gate | Click approve | — | — | `/approve G2` (Magic Link for G3/G4) |
| Close sprint | — | `sdlcctl close-sprint` | — | `"close sprint"` |
| Export audit | Download button | `sdlcctl export-audit` | — | `"export audit"` |
| AI chat | — | — | — | Free-text (Vietnamese/English) |
| CEO Dashboard | Metrics, charts | — | — | — |

---

## 3. Sprint Lifecycle — Team Collaboration

```
╔══════════════════════════════════════════════════════════════════════╗
║  SPRINT LIFECYCLE — Team of 5 (CTO, PM, 2 Dev, 1 QA)              ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  PHASE 1: Planning (PM lead)                                       ║
║  ┌──────────┐                                                      ║
║  │ Web App  │ PM creates sprint plan, sets exit criteria,          ║
║  │ (admin)  │ assigns gate approvers.                              ║
║  │          │ CTO reviews on CEO Dashboard.                        ║
║  └──────────┘                                                      ║
║       │                                                            ║
║  PHASE 2: Execution (Dev + QA)                                     ║
║  ┌──────────┐  ┌──────────┐  ┌──────────┐                         ║
║  │   CLI    │  │Extension │  │   OTT    │                          ║
║  │ Dev runs │  │ Dev      │  │ Team     │                          ║
║  │ sdlcctl  │  │ submits  │  │ standup  │                          ║
║  │ submit   │  │ evidence │  │ "gate    │                          ║
║  │ evidence │  │Cmd+Shf+E │  │  status" │                          ║
║  └──────────┘  └──────────┘  └──────────┘                          ║
║       │              │              │                               ║
║       └──────────────┴──────────────┘                              ║
║                      ↓                                             ║
║         Evidence Vault (SHA256, source tracking)                   ║
║         submitted_by=<user_uuid>, source=cli|extension|ott         ║
║                      ↓                                             ║
║  PHASE 3: Gate Approval (CTO/PM)                                   ║
║  ┌──────────┐  ┌──────────┐                                        ║
║  │   OTT    │  │ Web App  │                                        ║
║  │PM: close │  │CTO: view │                                        ║
║  │ sprint   │  │dashboard │                                        ║
║  │CTO: gate │  │approve   │                                        ║
║  │ approve  │  │gate      │                                        ║
║  │→ magic   │  │          │                                        ║
║  │  link    │  │          │                                        ║
║  └──────────┘  └──────────┘                                        ║
║                                                                    ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## 4. Gate Approval — Multi-Approver Workflow

The most critical collaboration mechanism in SDLC Orchestrator.

### 4.1 Approval Flow

```
Developer submits evidence (CLI / Extension / OTT)
         ↓
PM submits gate for review
         ↓
   ┌─────────────────────────────────────┐
   │     GateApproval (multi-approver)   │
   │                                     │
   │  Approver 1 (CTO): ✅ APPROVED     │
   │  Approver 2 (CPO): ⏳ PENDING      │ ← ALL must approve
   │  Approver 3 (Lead): ❌ REJECTED    │ ← ANY rejection → REJECTED
   │                                     │
   └─────────────────────────────────────┘
```

### 4.2 Approval by Gate Level

| Gate | Sensitivity | OTT Approval | Web Approval |
|------|-------------|-------------|--------------|
| G1 (Design Ready) | Normal | Direct `/approve G1` | Click approve |
| G2 (Security + Arch) | Normal | Direct `/approve G2` | Click approve |
| G3 (Ship Ready) | **Sensitive** | Magic Link (OOB) | Click approve |
| G4 (Production) | **Sensitive** | Magic Link (OOB) | Click approve |
| G-Sprint | Normal | Direct `/approve` | Click approve |
| G-Sprint-Close | **Sensitive** | Magic Link (OOB) | Click approve |

### 4.3 Magic Link OOB Auth (G3/G4)

For sensitive gates approved via OTT:

```
CTO types: "/approve G3" in Telegram
         ↓
Bot generates Magic Link:
  - HMAC-SHA256 signed
  - 5-minute TTL
  - Single-use (Redis SET NX)
         ↓
Bot sends: "Click to confirm G3 approval: https://sdlc.../magic/abc123"
         ↓
CTO clicks link → Browser opens → Confirms identity → Gate APPROVED
```

**Implementation**: `backend/app/services/agent_team/magic_link_service.py` (ADR-064, FR-047)

### 4.4 Gate State Machine

```
DRAFT ──evaluate──> EVALUATED ──submit──> SUBMITTED ──approve──> APPROVED
                        │                     │
                        │                     └──reject──> REJECTED
                        │
                        └──(24h stale)──> EVALUATED_STALE
                                               │
                                               └──re-evaluate──> EVALUATED

All terminal states ──archive──> ARCHIVED
```

**SSOT**: `compute_gate_actions()` in `gate_service.py` — single source of truth for valid state transitions.

---

## 5. OTT Multi-Channel Architecture

### 5.1 Supported Channels

| Channel | Tier Requirement | Sprint | Status |
|---------|-----------------|--------|--------|
| Telegram | STANDARD+ | Sprint 181 | ✅ COMPLETE |
| Zalo | STANDARD+ (Vietnam pilot) | Sprint 181 | ✅ COMPLETE |
| MS Teams | PROFESSIONAL+ | Sprint 182 | ✅ COMPLETE |
| Slack | PROFESSIONAL+ | Sprint 183 | ✅ COMPLETE |

### 5.2 Protocol Adapter Architecture

All OTT channels normalize to a single canonical message type before processing:

```
Telegram webhook ──→ telegram_normalizer.py ──→ ┐
Zalo webhook     ──→ zalo_normalizer.py     ──→ ├──→ OrchestratorMessage ──→ ai_response_handler
Teams webhook    ──→ teams_normalizer.py    ──→ │
Slack webhook    ──→ slack_normalizer.py    ──→ ┘
```

**OrchestratorMessage** (`protocol_adapter.py`, frozen dataclass):

| Field | Type | Description |
|-------|------|-------------|
| `channel` | `str` | `"telegram"` / `"zalo"` / `"teams"` / `"slack"` |
| `sender_id` | `str` | Channel-specific stable user identifier |
| `content` | `str` | Sanitized text (max 4096 chars, 12 injection patterns filtered) |
| `timestamp` | `datetime` | UTC datetime of message origin |
| `correlation_id` | `str` | Unique trace ID: `"{channel}_{message_id}"` |
| `metadata` | `dict` | Channel-specific extras (chat_id, tenant_id, etc.) |

**Channel Registry Pattern**:
```python
_CHANNEL_REGISTRY: dict[str, NormalizerFn] = {}

def register_normalizer(channel: str, fn: NormalizerFn) -> None:
    _CHANNEL_REGISTRY[channel] = fn
```

Each normalizer self-registers at import time. Public API: `normalize(raw_payload, channel)`.

### 5.3 Per-Channel Message Mapping

**Telegram**:
- `sender_id` ← `message.from.id` (numeric, cast to string)
- `content` ← `message.text`
- `metadata.chat_id` ← `message.chat.id`
- `metadata.chat_type` ← `message.chat.type` (private / group / supergroup)

**Zalo**:
- `sender_id` ← `sender.id`
- `content` ← `message.text`
- Supported event: `user_send_text` only
- Timestamp in milliseconds (divided by 1000)

**MS Teams**:
- `sender_id` ← `from.aadObjectId` (Azure AD object ID, stable)
- `content` ← `activity.text`
- `metadata.tenant_id` ← `channelData.tenant.id`
- Validates `channelId == "msteams"` (PA-35)

**Slack**:
- `sender_id` ← `event.user`
- `content` ← `event.text`
- `metadata.team_id` ← `team_id`
- Handles `url_verification` challenge response
- Supported events: `message`, `app_mention`

### 5.4 Webhook Security Per Channel

| Channel | Verification Method | Replay Protection | Env Vars |
|---------|-------------------|-------------------|----------|
| Telegram | Shared secret token (timing-safe compare) | No | `TELEGRAM_WEBHOOK_SECRET` |
| Zalo | SHA256 (app_id + body + timestamp + secret) | No (acknowledged) | `ZALO_APP_SECRET`, `ZALO_APP_ID` |
| MS Teams | HMAC-SHA256 | Via Bot Framework | — |
| Slack | HMAC-SHA256 (`v0:timestamp:body`) | 300s window | `SLACK_SIGNING_SECRET` |

**Event Deduplication** (all channels, Sprint 189):
- Redis key: `webhook_dedupe:{channel}:{event_id}` — `SET NX EX 3600`
- Prevents duplicate processing on webhook re-delivery

### 5.5 Input Sanitization (ADR-058 Pattern C)

All OTT content passes through 12 injection pattern filters before processing:
- Prompt injection attempts → `[BLOCKED:prompt_injection]`
- Command injection → `[BLOCKED:command_injection]`
- Path traversal → `[BLOCKED:path_traversal]`
- Implementation: `backend/app/services/agent_team/input_sanitizer.py`

---

## 6. OTT Group Chat — Shared Workspace, Individual Permissions

### 6.1 Workspace Concept

```
Telegram Group: "SDLC Team" (5 members, 1 bot)
──────────────────────────────────────────────

chat_id  = group ID → SHARED workspace (same project for all)
sender_id = individual → INDIVIDUAL permissions (different roles)

PM:  /workspace set BFlow     → Sets workspace for ENTIRE group
Dev: "submit evidence: ..."   → Evidence recorded: submitted_by=Dev
QA:  "gate status"            → Read-only OK for all members
CTO: "/approve G-Sprint"      → ✅ Has approver role
Dev: "/approve G-Sprint"      → ❌ Permission denied (needs approver role)
```

### 6.2 Workspace Redis Schema (D-067-02)

```
Key: ott:workspace:{channel}:{chat_id}  →  Redis HASH
TTL: 604,800 seconds (7 days, reset on every command use)
```

| Hash Field | Type | Description |
|-----------|------|-------------|
| `project_id` | UUID string | Bound project |
| `project_name` | string | Display name |
| `tier` | string | `LITE` / `STANDARD` / `PROFESSIONAL` / `ENTERPRISE` |
| `sdlc_stage` | string | Current stage (e.g., `"04-BUILD"`) |
| `set_at` | ISO 8601 | When workspace was set |
| `set_by` | string | `sender_id` of who ran `/workspace set` |

### 6.3 Project Resolution Priority (D-067-04)

For any governance command, project context resolves in this order:

```
1. Explicit project_id in message (e.g., "/gates proj-uuid") → use directly
2. Workspace project_id from Redis HASH → inject automatically
3. OTT_DEFAULT_PROJECT_ID env var → fallback
4. Error: "No project context. Set workspace first: /workspace set <name>"
```

### 6.4 Workspace Commands (D-067-03)

| Command | Action |
|---------|--------|
| `/workspace set <name-or-id>` | Set active project for this chat |
| `/workspace` or `/workspace info` | Show current workspace binding |
| `/workspace list` | List accessible projects (max 10) |
| `/workspace clear` | Clear binding (return to no-workspace) |

### 6.5 Key Separation

```
Redis workspace (ott:workspace:*)     = UX convenience (cache)
PostgreSQL RBAC (team_members, etc.)  = Authorization truth (always verified)
```

Workspace NEVER caches permissions, gate status, or approval history. Every governance action re-verifies against PostgreSQL.

---

## 7. OTT Identity Resolution (Sprint 209)

### 7.1 Problem

OTT channels use channel-specific sender IDs (e.g., Telegram numeric ID), but governance commands require internal User UUIDs for RBAC verification.

### 7.2 Resolution Chain (D-068-01)

```
sender_id arrives from OTT channel
         ↓
1. Is it already a UUID? (web/CLI user) → return as-is
         ↓
2. Redis cache hit? (ott:identity:{channel}:{sender_id}) → return cached
         ↓
3. oauth_accounts lookup: provider='{channel}', provider_account_id='{sender_id}'
   → Found: cache + return user_id
         ↓
4. OTT_GATEWAY_USER_ID env var (self-hosted single operator fallback)
   → Found: cache + return
         ↓
5. None (anonymous) → governance commands blocked, prompt to /link
```

**Implementation**: `backend/app/services/agent_bridge/ott_identity_resolver.py`
- Redis cache TTL: 3600s (60 minutes)
- Cache key: `ott:identity:{channel}:{sender_id}`
- Negative cache: `"__none__"` sentinel value

### 7.3 Account Linking Flow (Sprint 209)

For users who need to link their OTT identity to their SDLC account:

```
User: /link dangtt@gmail.com
  ↓
Bot: "Verification code sent to dangtt@gmail.com. Use /verify <code> within 10 minutes."
  ↓
Email: "Your verification code: 847293"
  ↓
User: /verify 847293
  ↓
Bot: "✅ Linked! Telegram → dangtt@gmail.com (Dev role in SDLC Core)"
  ↓
OAuthAccount row created: provider='telegram', provider_account_id='12345678', user_id=<UUID>
Redis cache invalidated → next command resolves via DB
```

| Command | Action |
|---------|--------|
| `/link <email>` | Initiate linking — sends verification code |
| `/verify <code>` | Complete linking — creates OAuthAccount binding |
| `/unlink` | Remove linking — deletes OAuthAccount row + clears cache |
| `/whoami` | Show current identity binding status |

---

## 8. Evidence Attribution — Who Submitted, From Where?

Every piece of evidence tracks full provenance:

| Field | Description | Example |
|-------|-------------|---------|
| `submitted_by` | User UUID (who submitted) | `a1b2c3d4-...` |
| `source` | Interface used | `cli` / `extension` / `web` / `ott` |
| `sha256_hash` | Integrity verification | `e3b0c44298fc...` |
| `criteria_snapshot_id` | Bound to which gate exit criteria version | `v2` |

**Audit trail example**:
> "Dev Minh submitted test results from VS Code Extension at 14:30, bound to G3 exit criteria v2"

---

## 9. Invitation Flow

```
Admin (Web/OTT) → Invite dangtt@gmail.com to Team "SDLC Core"
  ↓
TeamInvitation created:
  - SHA256 token hash (no plaintext stored)
  - 7-day expiry
  - Rate limit: max 3 resends, 5-min cooldown
  ↓
Email sent → User clicks link → Accept/Decline
  ↓
TeamMember created: role=member, member_type=human
```

---

## 10. AI Agent Collaboration

AI agents participate as team members with `SE4A Executor` role:

```
┌─────────────────────────────────────────┐
│  Agent Team Pipeline (EP-07)            │
│                                         │
│  Initializer → Coder → Reviewer        │
│       │           │          │          │
│       └───── @mention routing ──────┘   │
│                                         │
│  Lane-based queue (SKIP LOCKED)         │
│  Budget circuit breaker                 │
│  Parent-child session inheritance       │
│  6-reason failover classification       │
│  Output credential scrubbing (ADR-058)  │
└─────────────────────────────────────────┘
```

**Key constraints**:
- AI agents **CANNOT** approve gates (human oversight enforced at DB level)
- AI agents **CANNOT** hold owner/admin roles
- All AI output passes through credential scrubbing (6 patterns)
- History auto-compaction at 80% token capacity
- Delegation depth limits prevent infinite agent chains

**OTT Integration**: Users interact with AI agents through natural language in OTT channels. The `ai_response_handler.py` routes free-text to the agent pipeline, with results delivered back via `send_result_message()`.

---

## 11. Summary Table

| Layer | Collaboration Mechanism | Enforced By |
|-------|------------------------|-------------|
| Team membership | Owner / Admin / Member / AI Agent | PostgreSQL + CHECK constraint |
| Gate approval | Multi-approver, all-must-approve | `compute_gate_actions()` SSOT |
| Workspace | Group shared, individual permissions | Redis (UX) + PostgreSQL (auth) |
| Evidence | Multi-source tracking | `submitted_by` + `source` fields |
| Sprint governance | G-Sprint / G-Sprint-Close gates | Human-only approval (SE4H) |
| Sensitive actions | Magic Link OOB auth | HMAC-SHA256, 5-min TTL, single-use |
| Identity | OTT sender_id → User UUID | `ott_identity_resolver.py` + OAuthAccount |
| Channel abstraction | Protocol adapter + normalizers | `OrchestratorMessage` canonical type |
| Input security | 12 injection pattern filters | `input_sanitizer.py` (ADR-058 Pattern C) |
| AI agents | SE4A Executor, no governance authority | DB CHECK constraint + SASE rules |

---

## 12. Key Takeaway

A team of 5 can collaborate entirely through a Telegram group chat for daily work. Only CTO/PM need to open the Web Dashboard for metrics or user administration. The system enforces governance through RBAC at every layer — the chat interface is convenient, but PostgreSQL is always the authorization truth.

```
Daily Work:   OTT (Telegram/Zalo) + CLI = PRIMARY interface
Admin Work:   Web App = owner/admin ONLY
Evidence:     CLI + Extension + OTT → Evidence Vault (SHA256 integrity)
Approval:     OTT (Magic Link for sensitive) + Web App
AI Agents:    Execute only, NEVER approve — human oversight always
```
