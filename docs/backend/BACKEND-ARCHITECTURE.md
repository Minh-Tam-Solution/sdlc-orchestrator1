# Kiến Trúc Backend & Microservices - SDLC Orchestrator

**Version**: 1.0.0
**Date**: 2026-02-18
**Status**: ACTIVE

## 📊 Tổng Quan

SDLC Orchestrator Backend là một **monolithic FastAPI application** với **microservices architecture pattern** thông qua Docker Compose orchestration.

### Thống Kê

```yaml
Services:         97 service files
API Routes:       77 route files (91 endpoints)
Models:           61 database models (33 tables)
Middleware:       16 middleware components
Architecture:     5-layer Software 3.0
Framework:        FastAPI 0.115.6 + SQLAlchemy 2.0.36
Database:         PostgreSQL 15.5 (33 tables)
Cache:            Redis 7.2
Storage:          MinIO S3-compatible
Policy Engine:    OPA 0.58.0
Monitoring:       Prometheus + Grafana
```

---

## 🏗️ Kiến Trúc 5-Layer

```
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 5: AI CODERS (External - We Orchestrate)                  │
│  • Cursor, Claude Code, Copilot, DeepCode                       │
│  • Governed via API + Quality Gates                             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 4: EP-06 CODEGEN (Innovation - Sprint 45-50)              │
│  • IR Processor Service (Spec → IR)                             │
│  • Multi-Provider Gateway (Ollama → Claude → DeepCode)          │
│  • 4-Gate Quality Pipeline (Syntax → Security → Context → Test) │
│  • Validation Loop Orchestrator (max_retries=3)                 │
│  • Evidence State Machine (8 states)                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 3: BUSINESS LOGIC (Core - Proprietary Apache-2.0)         │
│  • Gate Engine API (OPA Policy-as-Code)                         │
│  • Evidence Vault API (S3 + 8-state lifecycle)                  │
│  • AI Context Engine (Multi-provider AI)                        │
│  • SAST Integration (Semgrep)                                   │
│  • Override Queue (Tiered approval)                             │
│  • Multi-Agent Team Engine (EP-07, Sprint 176-178)              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 2: INTEGRATION (Thin Adapters - Apache-2.0)               │
│  • opa_service.py → OPA REST API                                │
│  • minio_service.py → MinIO S3 API (boto3)                      │
│  • semgrep_service.py → Semgrep CLI                             │
│  • ollama_service.py → Ollama REST API                          │
│  • redis_service.py → Redis Protocol                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 1: INFRASTRUCTURE (OSS Components)                        │
│  • PostgreSQL 15.5 (postgres-central:15432) - 33 tables         │
│  • Redis 7.2 (port 6395) - Caching + sessions                   │
│  • MinIO (ai-platform-minio:9000) - Evidence storage            │
│  • OPA 0.58.0 (port 8185) - Policy evaluation                   │
│  • Prometheus (port 9096) - Metrics collection                  │
│  • Grafana (port 3002) - Dashboards                             │
│  • Alertmanager (port 9095) - Alert routing                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🐳 Microservices Architecture

### Container-Based Microservices (Docker Compose)

#### 1. **sdlc-backend** (Main Application)

```yaml
Service: FastAPI Backend
Container: sdlc-backend
Port: 8300
Image: python:3.11-slim
Dependencies: postgres-central, redis, opa, ai-platform-minio

Responsibilities:
  - RESTful API (91 endpoints)
  - Business logic (97 services)
  - Database ORM (SQLAlchemy)
  - JWT authentication
  - OAuth 2.0 (GitHub, Google)
  - Background jobs (APScheduler)

Tech Stack:
  - FastAPI 0.115.6 (async)
  - SQLAlchemy 2.0.36 (async ORM)
  - Pydantic 2.12.4 (validation)
  - Alembic 1.12.1 (migrations)
  - Uvicorn 0.38.0 (ASGI server)

Health Check:
  curl http://localhost:8300/health
  Expected: {"status": "healthy", "version": "1.2.0"}
```

#### 2. **sdlc-redis** (Cache & Sessions)

```yaml
Service: Redis Cache
Container: sdlc-redis
Port: 6395 (mapped from 6379)
Image: redis:7.2-alpine
Persistence: AOF (Append-Only File)

Responsibilities:
  - Session storage (JWT tokens)
  - Rate limiting counters
  - Cache layer (API responses)
  - Real-time pub/sub (WebSocket notifications)
  - Agent conversation cooldowns (EP-07)

Configuration:
  - Appendonly: yes (durability)
  - Password: REDIS_PASSWORD env var
  - Max memory: Default (no limit)
  - Eviction policy: noeviction

Health Check:
  docker-compose exec redis redis-cli -a PASSWORD ping
  Expected: PONG
```

#### 3. **sdlc-opa** (Policy Engine)

```yaml
Service: Open Policy Agent
Container: sdlc-opa
Port: 8185 (mapped from 8181)
Image: openpolicyagent/opa:0.58.0
Platform: linux/amd64

Responsibilities:
  - Gate evaluation (policy-as-code)
  - Compliance validation
  - Sprint governance policies
  - AI safety policies
  - Access control (RBAC)

Policy Packs:
  - backend/policy-packs/rego/gates/       # Gate policies
  - backend/policy-packs/rego/ai-safety/   # AI safety
  - backend/policy-packs/rego/compliance/  # Compliance
  - backend/policy-packs/rego/sprint/      # Sprint governance

Health Check:
  curl http://localhost:8185/health
  Expected: {}
```

#### 4. **ai-platform-minio** (Object Storage) - EXTERNAL

```yaml
Service: MinIO S3-Compatible Storage
Container: ai-platform-minio
Port: 9020 (S3 API), 9021 (Console)
Image: minio/minio
Network: ai-net (external)

Responsibilities:
  - Evidence vault storage (WORM compliance)
  - Artifact storage (code, documents)
  - Immutable audit trail (Object Lock)
  - Presigned URLs (browser downloads)

Buckets:
  - evidence-vault-v2 (Object Lock enabled, 7-year retention)
  - artifacts
  - documents

Configuration:
  - Object Lock: GOVERNANCE mode
  - Retention: 2555 days (7 years)
  - Versioning: Enabled
  - Encryption: Server-side (SSE-S3)

Health Check:
  curl http://ai-platform-minio:9000/minio/health/live
  Expected: 200 OK
```

#### 5. **sdlc-prometheus** (Metrics Collection)

```yaml
Service: Prometheus
Container: sdlc-prometheus
Port: 9096 (mapped from 9090)
Image: prom/prometheus:v2.48.0

Responsibilities:
  - Metrics collection (backend, OPA, Redis)
  - Time-series database
  - Alert evaluation
  - Service discovery

Scrape Targets:
  - Backend API: http://backend:8300/metrics
  - OPA: http://opa:8181/metrics
  - Redis: http://redis:6379 (via exporter)
  - Prometheus self: http://localhost:9090/metrics

Configuration:
  - Scrape interval: 15s
  - Retention: 15 days
  - Storage: /prometheus (Docker volume)

Health Check:
  curl http://localhost:9096/-/healthy
  Expected: Prometheus is Healthy.
```

#### 6. **sdlc-grafana** (Visualization)

```yaml
Service: Grafana
Container: sdlc-grafana
Port: 3002 (mapped from 3000)
Image: grafana/grafana:10.2.0

Responsibilities:
  - Dashboard visualization
  - Alert management
  - Metrics exploration
  - OnCall integration

Dashboards:
  - API Performance (latency, throughput, errors)
  - DORA Metrics (deployment frequency, MTTR)
  - Business Metrics (gates, evidence, users)
  - Infrastructure Health (CPU, memory, disk)

Credentials:
  - Username: admin (from GRAFANA_ADMIN_USER)
  - Password: admin_changeme (from GRAFANA_ADMIN_PASSWORD)

Health Check:
  curl http://localhost:3002/api/health
  Expected: {"commit":"...", "database":"ok", "version":"10.2.0"}
```

#### 7. **sdlc-alertmanager** (Alert Routing)

```yaml
Service: Alertmanager
Container: sdlc-alertmanager
Port: 9095 (mapped from 9093)
Image: prom/alertmanager:v0.26.0

Responsibilities:
  - Alert deduplication
  - Alert grouping
  - Alert routing (email, Slack, PagerDuty)
  - Silencing rules

Configuration:
  - Routes: infrastructure/monitoring/prometheus/alertmanager.yml
  - Receivers: Email, Webhook
  - Group wait: 10s
  - Repeat interval: 12h

Health Check:
  curl http://localhost:9095/-/healthy
  Expected: 200 OK
```

#### 8. **postgres-central** (Database) - EXTERNAL

```yaml
Service: PostgreSQL Database
Container: postgres-central
Port: 15432 (mapped from 5432)
Image: postgres:15.5
Network: ai-net (external)

Responsibilities:
  - Primary data storage (33 tables)
  - ACID transactions
  - Full-text search (tsvector)
  - JSON storage (JSONB)
  - Vector embeddings (pgvector)

Databases:
  - sdlc_orchestrator (main database)

Configuration:
  - Max connections: 100
  - Shared buffers: 256MB
  - Work mem: 4MB
  - Timezone: UTC

Health Check:
  docker exec -it postgres-central pg_isready -U sdlc_user
  Expected: postgres-central:5432 - accepting connections
```

#### 9. **sdlc-frontend** (Web Application)

```yaml
Service: Next.js Frontend
Container: sdlc-frontend
Port: 8310 (mapped from 3000)
Image: node:20-alpine

Responsibilities:
  - Web UI (React 18 + Next.js 14)
  - API client (TanStack Query)
  - Authentication flow (JWT + OAuth)
  - Real-time updates (WebSocket)

Routes:
  - / (Landing page)
  - /login (Authentication)
  - /app/* (Main application)
  - /admin/* (Admin panel)

Health Check:
  curl http://localhost:8310
  Expected: 200 OK (HTML response)
```

---

## 📁 Backend Cấu Trúc Chi Tiết

### Cấu Trúc Thư Mục

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app entry point
│   │
│   ├── api/                             # API Layer
│   │   ├── routes/                      # 77 route files (91 endpoints)
│   │   │   ├── auth.py                  # Authentication (7 endpoints)
│   │   │   ├── gates.py                 # Gates (12 endpoints)
│   │   │   ├── evidence.py              # Evidence (8 endpoints)
│   │   │   ├── codegen.py               # Code generation (10 endpoints)
│   │   │   ├── agent_team.py            # Multi-Agent (11 endpoints - EP-07)
│   │   │   ├── compliance.py            # Compliance (6 endpoints)
│   │   │   ├── projects.py              # Projects (8 endpoints)
│   │   │   ├── github.py                # GitHub integration (5 endpoints)
│   │   │   ├── planning.py              # Planning hierarchy (12 endpoints)
│   │   │   ├── ceo_dashboard.py         # Executive dashboard (4 endpoints)
│   │   │   └── ... (67 more route files)
│   │   │
│   │   └── v1/endpoints/                # API v1 endpoints
│   │       ├── cross_reference.py       # Cross-reference validation
│   │       └── e2e_testing.py           # E2E test execution
│   │
│   ├── core/                            # Core Layer
│   │   ├── config.py                    # Settings & environment config
│   │   ├── security.py                  # JWT, OAuth, MFA
│   │   ├── dependencies.py              # FastAPI dependencies
│   │   └── exceptions.py                # Custom exceptions
│   │
│   ├── db/                              # Database Layer
│   │   ├── base.py                      # SQLAlchemy base
│   │   ├── session.py                   # Database session
│   │   └── init_db.py                   # Database initialization
│   │
│   ├── models/                          # Data Models (61 files)
│   │   ├── user.py                      # User model
│   │   ├── gate.py                      # Gate model (30 fields)
│   │   ├── gate_evidence.py             # Evidence model
│   │   ├── project.py                   # Project model
│   │   ├── agent_conversations.py       # Multi-Agent conversations (EP-07)
│   │   ├── agent_definitions.py         # Agent definitions (EP-07)
│   │   ├── agent_messages.py            # Agent messages (EP-07)
│   │   └── ... (58 more models)
│   │
│   ├── schemas/                         # Pydantic Schemas (41 files)
│   │   ├── auth.py                      # Auth request/response schemas
│   │   ├── gate.py                      # Gate schemas
│   │   ├── evidence.py                  # Evidence schemas
│   │   ├── agent_team.py                # Multi-Agent schemas (EP-07)
│   │   └── ... (37 more schema files)
│   │
│   ├── services/                        # Business Logic (97 services)
│   │   ├── gate_service.py              # Gate CRUD + lifecycle
│   │   ├── evidence_manifest_service.py # Evidence manifest (36KB)
│   │   ├── opa_service.py               # OPA integration
│   │   ├── minio_service.py             # MinIO S3 API
│   │   ├── ollama_service.py            # Ollama AI integration
│   │   ├── ai_council_service.py        # AI Council deliberation (69KB)
│   │   ├── ai_recommendation_service.py # AI recommendations (37KB)
│   │   ├── semgrep_service.py           # SAST scanning
│   │   ├── github_service.py            # GitHub API integration
│   │   ├── notification_service.py      # Notifications
│   │   ├── agent_team/                  # Multi-Agent Team Engine (EP-07)
│   │   │   ├── agent_registry.py        # Agent CRUD
│   │   │   ├── message_queue.py         # Lane-based queue
│   │   │   ├── mention_parser.py        # @mention routing
│   │   │   ├── conversation_tracker.py  # Parent-child inheritance
│   │   │   ├── agent_invoker.py         # Provider failover
│   │   │   ├── failover_classifier.py   # Error classification
│   │   │   ├── input_sanitizer.py       # 12 injection patterns
│   │   │   ├── shell_guard.py           # Shell command protection
│   │   │   └── tool_context.py          # Tool permissions
│   │   ├── codegen/                     # EP-06 Codegen Engine
│   │   │   ├── codegen_service.py       # Main orchestrator (23KB)
│   │   │   ├── quality_pipeline.py      # 4-Gate pipeline
│   │   │   ├── ollama_provider.py       # Ollama integration
│   │   │   ├── claude_provider.py       # Claude integration
│   │   │   ├── provider_registry.py     # Auto-registration
│   │   │   ├── intent_router.py         # Intent detection
│   │   │   ├── error_classifier.py      # Auto-fix feedback
│   │   │   └── session_manager.py       # Session tracking
│   │   ├── governance/                  # Governance services
│   │   │   ├── gates_engine.py          # Gate evaluation engine
│   │   │   ├── context_authority_v2.py  # Context Authority V2 (61KB)
│   │   │   ├── vibecoding_service.py    # Vibecoding index
│   │   │   └── stage_gating_service.py  # Stage gating
│   │   └── ... (77 more service files)
│   │
│   ├── middleware/                      # Middleware (16 files)
│   │   ├── prometheus_metrics.py        # Metrics collection
│   │   ├── rate_limiter.py              # Rate limiting (Redis)
│   │   ├── security_headers.py          # Security headers
│   │   ├── cache_headers.py             # Cache headers
│   │   ├── request_id.py                # Request ID tracking
│   │   ├── error_handler.py             # Error handling
│   │   └── ... (10 more middleware)
│   │
│   ├── utils/                           # Utilities
│   │   ├── redis.py                     # Redis client
│   │   ├── logger.py                    # Structured logging
│   │   ├── validators.py                # Custom validators
│   │   └── helpers.py                   # Helper functions
│   │
│   ├── jobs/                            # Background Jobs
│   │   ├── compliance_scan.py           # Daily compliance scans
│   │   ├── queue_processor.py           # Queue processing
│   │   └── scheduled_tasks.py           # Scheduled tasks
│   │
│   ├── events/                          # Event Handlers
│   │   ├── websocket.py                 # WebSocket events
│   │   ├── push_notifications.py        # Push notifications
│   │   └── pubsub.py                    # Pub/sub events
│   │
│   └── policies/                        # Policy Definitions
│       ├── gate_policies.py             # Gate policies
│       └── compliance_policies.py       # Compliance policies
│
├── alembic/                             # Database Migrations
│   ├── versions/                        # Migration files
│   └── env.py                           # Alembic config
│
├── tests/                               # Test Suite
│   ├── unit/                            # Unit tests
│   ├── integration/                     # Integration tests
│   ├── e2e/                             # E2E tests
│   └── load/                            # Load tests (Locust)
│
├── policy-packs/                        # Policy Packs
│   ├── rego/                            # OPA Rego policies
│   │   ├── gates/                       # Gate policies
│   │   ├── ai-safety/                   # AI safety
│   │   ├── compliance/                  # Compliance
│   │   └── sprint/                      # Sprint governance
│   └── semgrep/                         # Semgrep SAST rules
│       ├── ai-security.yml              # AI-specific security
│       └── owasp-python.yml             # OWASP Top 10
│
├── scripts/                             # Utility Scripts
│   ├── seed_data.py                     # Database seeding
│   ├── migrate.py                       # Migration helper
│   └── backup.py                        # Database backup
│
├── Dockerfile                           # Production Docker image
├── requirements.txt                     # Python dependencies (398 packages)
├── requirements-docker.txt              # Docker-optimized deps
└── pytest.ini                           # Pytest configuration
```

---

## 🔧 Core Services Chi Tiết

### 1. **Gate Engine Services**

#### gate_service.py
```python
Purpose: Gate lifecycle management
Lines: ~1,500 lines
Key Functions:
  - create_gate(project_id, gate_type, exit_criteria)
  - evaluate_gate(gate_id) → triggers OPA policy check
  - submit_gate(gate_id) → change state to SUBMITTED
  - approve_gate(gate_id, approver_id) → multi-approver workflow
  - reject_gate(gate_id, reason)
  - compute_gate_actions(gate) → available state transitions

State Machine:
  DRAFT → EVALUATED → SUBMITTED → APPROVED/REJECTED → ARCHIVED

Dependencies:
  - opa_service.py (policy evaluation)
  - evidence_manifest_service.py (evidence binding)
  - notification_service.py (alerts)
```

#### gates_engine.py (Governance)
```python
Purpose: OPA-powered gate evaluation with Context Authority V2
Lines: ~2,000 lines
Key Functions:
  - evaluate_gate_policy(gate_id, context)
  - apply_context_authority(requirements, project_profile)
  - compute_compliance_score(gate_id)
  - generate_gate_report(gate_id)

Integration:
  - OPA REST API (policy evaluation)
  - Context Authority V2 (requirement filtering)
  - Evidence Vault (artifact validation)
```

### 2. **Evidence Vault Services**

#### evidence_manifest_service.py (36KB)
```python
Purpose: Immutable evidence storage with SHA256 integrity
Lines: ~1,200 lines
Key Functions:
  - upload_evidence(file, gate_id, type, source)
  - verify_integrity(evidence_id) → recompute SHA256
  - lock_evidence(evidence_id) → prevent modifications
  - generate_manifest(gate_id) → hash chain
  - create_presigned_url(evidence_id, expires=3600)

8-State Lifecycle:
  uploaded → validating → evidence_locked → awaiting_vcr → merged
                ↓              ↓
            retrying → escalated → aborted

Storage:
  - MinIO S3 (via boto3)
  - PostgreSQL (metadata)
  - SHA256 hashing (integrity)
  - WORM compliance (7-year retention)
```

#### minio_service.py
```python
Purpose: MinIO S3 API adapter (AGPL-safe, network-only)
Lines: ~500 lines
Key Functions:
  - upload_file(bucket, object_name, file_data)
  - download_file(bucket, object_name)
  - delete_file(bucket, object_name) → requires GOVERNANCE bypass
  - generate_presigned_url(bucket, object_name, expires)
  - ensure_bucket_exists(bucket)

AGPL Containment:
  ✅ Uses boto3 (Apache 2.0) - NOT minio SDK (AGPL)
  ✅ Network-only access (HTTP/S API calls)
  ✅ No code linking or imports from AGPL libraries
```

### 3. **AI Context Engine Services**

#### ai_council_service.py (69KB - Largest Service)
```python
Purpose: Multi-LLM deliberation for AI recommendations
Lines: ~2,300 lines
Key Functions:
  - deliberate(task, context) → 3-stage council
  - stage_1_queries(task) → collect model outputs
  - stage_2_peer_review(outputs) → cross-review
  - stage_3_synthesis(reviews) → final decision
  - evaluate_quality(decision) → scoring

3-Stage Council:
  STAGE_1_QUERIES → STAGE_2_PEER_REVIEW → STAGE_3_SYNTHESIS

Providers:
  - Ollama (primary, $50/mo)
  - Claude (fallback 1, $1000/mo)
  - GPT-4o (fallback 2)
  - Rule-based (final fallback)
```

#### ollama_service.py
```python
Purpose: Local LLM integration (10-model configuration)
Lines: ~600 lines
Key Functions:
  - generate(model, prompt, max_tokens, temperature)
  - chat(model, messages, stream=False)
  - embeddings(model, text)
  - health_check() → verify Ollama availability

10-Model Configuration (RTX 5090 32GB):
  - qwen3:32b (20GB) - PRIMARY CHAT
  - qwen3-coder:30b (18GB) - PRIMARY CODE (256K context)
  - deepseek-r1:32b (19GB) - DEEP REASONING
  - mistral-small3.2:24b (15GB) - SOP RAG
  - qwen3:14b (9.3GB) - VIETNAMESE FAST
  - qwen3:8b (5.2GB) - FASTEST CHAT
  - bge-m3:latest (1.2GB) - EMBEDDINGS

Cost Savings:
  - Year 1: $11,400 saved (95% reduction vs cloud)
  - Latency: 3x faster (<100ms vs 300ms)
```

#### context_authority_v2.py (61KB - FROZEN Sprint 173)
```python
Purpose: Context-aware requirement classification
Lines: ~2,000 lines
Key Functions:
  - evaluate_requirement_applicability(req, project)
  - classify_tier(req) → MANDATORY/RECOMMENDED/OPTIONAL
  - compute_context_score(project, dimensions)
  - filter_requirements(reqs, context)

5 Context Dimensions:
  1. Scale (team size, users)
  2. Team (experience, roles)
  3. Industry (compliance, regulations)
  4. Risk (data sensitivity, criticality)
  5. Practices (agile, DevOps maturity)

Output:
  - Red (MANDATORY): Must implement
  - Yellow (RECOMMENDED): Should implement
  - Gray (OPTIONAL): Nice to have
```

### 4. **EP-06 Codegen Services** (Sprint 45-50)

#### codegen_service.py (23KB)
```python
Purpose: IR-based code generation orchestrator
Lines: ~900 lines
Key Functions:
  - generate_code(spec, mode, provider_chain)
  - validate_quality(code) → 4-Gate pipeline
  - retry_generation(session_id, feedback)
  - escalate_to_council(session_id)
  - finalize_session(session_id)

Quality Modes:
  - SCAFFOLD: Lenient (G1+G2 mandatory, G3 soft-fail, G4 smoke)
  - PRODUCTION: Strict (all gates mandatory, full test suite)

Validation Loop:
  - max_retries: 3 (configurable)
  - Deterministic feedback to LLM
  - Escalation: auto-fix → council → human → abort
```

#### quality_pipeline.py
```python
Purpose: 4-Gate Quality Pipeline for generated code
Lines: ~700 lines

Gate 1 - Syntax Check (<5s):
  - ast.parse (Python)
  - tsc --noEmit (TypeScript)
  - ruff lint (Python linting)

Gate 2 - Security Scan (<10s):
  - Semgrep SAST (OWASP rules)
  - AI-specific security rules
  - Secret detection

Gate 3 - Context Validation (<10s):
  - Import validation (dependencies exist)
  - File structure check
  - Naming conventions

Gate 4 - Test Execution (<60s):
  - Dockerized pytest
  - Smoke tests (SCAFFOLD mode)
  - Full test suite (PRODUCTION mode)
```

### 5. **Multi-Agent Team Engine Services** (EP-07, Sprint 176-178)

#### agent_team/ (12 service files)

**agent_registry.py**
```python
Purpose: Agent definition CRUD + session scoping
Lines: ~600 lines
Key Functions:
  - create_definition(config) → with snapshot precedence
  - scope_to_session(def_id, session_id) → immutable snapshot
  - update_definition(def_id, updates) → only affects new sessions
  - get_active_definitions() → filter by SDLC role

P0 Modes:
  - queue: Lane-based FIFO (SKIP LOCKED)
  - steer: Human-initiated delegation
  - interrupt: Cancel running agent
```

**message_queue.py**
```python
Purpose: Lane-based concurrency (SKIP LOCKED + Redis notify)
Lines: ~500 lines
Key Functions:
  - enqueue(conversation_id, content, from_agent)
  - dequeue_next(lane) → SKIP LOCKED for concurrency
  - mark_processed(message_id)
  - dead_letter(message_id, reason)
  - notify_queue(lane) → Redis pub/sub

Lane Contract:
  - DB is truth (PostgreSQL SKIP LOCKED)
  - Redis is notify-only (pub/sub)
  - Dead-letter queue for failures
  - Deduplication by correlation_id
```

**failover_classifier.py**
```python
Purpose: 6-reason error classification for provider failover
Lines: ~400 lines

6 Failover Reasons:
  1. auth: Invalid API key, token expired
  2. format: Malformed request/response
  3. rate_limit: Quota exceeded
  4. billing: Insufficient credits
  5. timeout: Request timeout (>30s)
  6. unknown: Other errors

Abort Matrix:
  - auth + billing: ABORT (no fallback can fix)
  - format + timeout: RETRY with different provider
  - rate_limit: Wait + cooldown + retry
```

**input_sanitizer.py**
```python
Purpose: 12 injection patterns for OTT external content
Lines: ~300 lines

12 Injection Patterns:
  1. Command injection (`;`, `&&`, `|`)
  2. Path traversal (`../`, `..\\`)
  3. SQL injection (`'; DROP TABLE`)
  4. XSS (`<script>`, `onerror=`)
  5. LDAP injection (`*`, `(`, `)`)
  6. XML injection (`<!ENTITY`)
  7. YAML injection (Python `!!`)
  8. Template injection (`{{`, `{%`)
  9. Server-side includes (`<!--#exec`)
  10. Header injection (`\r\n`)
  11. JSON injection (unescaped quotes)
  12. Markdown injection (dangerous links)
```

**shell_guard.py**
```python
Purpose: 8 deny regex patterns + path traversal detection
Lines: ~250 lines

8 Deny Patterns:
  1. `rm -rf /` (destructive)
  2. `dd if=/dev/zero` (disk wipe)
  3. `:(){ :|:& };:` (fork bomb)
  4. `curl ... | bash` (remote code exec)
  5. `wget ... && chmod +x` (malware)
  6. `eval` (arbitrary code)
  7. `exec` (command execution)
  8. `sudo` (privilege escalation)

Path Traversal:
  - Block: `../`, `..\\`, `/etc/passwd`, `/root/`
  - Allow: Workspace-restricted paths only
```

---

## 🔌 API Endpoints Summary

### Authentication (7 endpoints)
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
GET    /api/v1/auth/me
POST   /api/v1/auth/github/callback
POST   /api/v1/auth/google/callback
```

### Gates (12 endpoints)
```
GET    /api/v1/gates
POST   /api/v1/gates
GET    /api/v1/gates/{id}
PUT    /api/v1/gates/{id}
DELETE /api/v1/gates/{id}
POST   /api/v1/gates/{id}/evaluate
POST   /api/v1/gates/{id}/submit
POST   /api/v1/gates/{id}/approve
POST   /api/v1/gates/{id}/reject
GET    /api/v1/gates/{id}/policy-result
POST   /api/v1/gates/{id}/override
GET    /api/v1/gates/{id}/evidence
```

### Evidence (8 endpoints)
```
GET    /api/v1/evidence
POST   /api/v1/evidence/upload
GET    /api/v1/evidence/{id}
DELETE /api/v1/evidence/{id}
GET    /api/v1/evidence/{id}/download
GET    /api/v1/evidence/{id}/verify
POST   /api/v1/evidence/{id}/lock
GET    /api/v1/evidence/manifest
```

### Codegen (10 endpoints - EP-06)
```
POST   /api/v1/codegen/generate
GET    /api/v1/codegen/sessions
GET    /api/v1/codegen/sessions/{id}
POST   /api/v1/codegen/sessions/{id}/retry
POST   /api/v1/codegen/sessions/{id}/escalate
GET    /api/v1/codegen/sessions/{id}/quality
GET    /api/v1/codegen/providers
GET    /api/v1/codegen/providers/{id}/stats
POST   /api/v1/codegen/validate
DELETE /api/v1/codegen/sessions/{id}
```

### Multi-Agent Team (11 endpoints - EP-07)
```
POST   /api/v1/agent-team/definitions
GET    /api/v1/agent-team/definitions
GET    /api/v1/agent-team/definitions/{id}
PUT    /api/v1/agent-team/definitions/{id}
DELETE /api/v1/agent-team/definitions/{id}
POST   /api/v1/agent-team/conversations
GET    /api/v1/agent-team/conversations/{id}
POST   /api/v1/agent-team/conversations/{id}/messages
POST   /api/v1/agent-team/conversations/{id}/interrupt
GET    /api/v1/agent-team/messages/{id}
POST   /api/v1/agent-team/messages/{id}/retry
```

### Planning Hierarchy (12 endpoints)
```
GET    /api/v1/planning/roadmaps
POST   /api/v1/planning/roadmaps
GET    /api/v1/planning/roadmaps/{id}
PUT    /api/v1/planning/roadmaps/{id}
DELETE /api/v1/planning/roadmaps/{id}
GET    /api/v1/planning/phases
POST   /api/v1/planning/phases
GET    /api/v1/planning/sprints
POST   /api/v1/planning/sprints
GET    /api/v1/planning/backlog
POST   /api/v1/planning/backlog
POST   /api/v1/planning/sync
```

**Total**: 91 endpoints across 77 route files

---

## 📊 Database Schema (33 Tables)

### Core Tables
```sql
users                    -- User accounts (13 roles)
projects                 -- Projects (team workspace)
gates                    -- Quality gates (30 fields)
gate_evidence            -- Evidence bindings
gate_approvals           -- Multi-approver workflow
policies                 -- OPA policies
policy_packs             -- Policy collections
```

### Multi-Agent Tables (EP-07)
```sql
agent_definitions        -- Agent config (22 columns)
agent_conversations      -- Conversation lifecycle (19 columns)
agent_messages           -- Message queue (22 columns)
```

### Planning Tables
```sql
roadmaps                 -- 12-month vision
phases                   -- 4-8 week themes
sprints                  -- 5-10 day iterations
backlog_items            -- Individual tasks
```

### Evidence Tables
```sql
evidence_manifests       -- Evidence hash chains
evidence_locks           -- Immutability enforcement
evidence_timeline        -- Audit trail
```

### AI Governance Tables
```sql
decomposition_sessions   -- AI task decomposition
decomposed_tasks         -- Generated sub-tasks
requirement_contexts     -- Context profiles
context_overrides        -- Project customizations
```

**Total**: 33 tables (view full schema in Data-Model-ERD.md)

---

## 🎯 Key Patterns & Best Practices

### 1. **Zero Mock Policy**
```python
# ❌ BANNED
def get_user(user_id):
    # TODO: Implement
    return {"id": user_id, "mock": True}

# ✅ REQUIRED
def get_user(user_id: int, db: Session) -> User | None:
    """Get user by ID with real database query."""
    return db.query(User).filter(User.id == user_id).first()
```

### 2. **AGPL Containment**
```python
# ❌ BANNED (AGPL contamination)
from minio import Minio
client = Minio("localhost:9000")

# ✅ REQUIRED (network-only, Apache 2.0)
import boto3
s3_client = boto3.client('s3', endpoint_url='http://minio:9000')
```

### 3. **Async/Await Pattern**
```python
# ✅ All I/O operations use async/await
async def get_gates(db: AsyncSession) -> list[Gate]:
    result = await db.execute(select(Gate))
    return result.scalars().all()
```

### 4. **Type Hints (100% Coverage)**
```python
# ✅ Strict type hints with mypy
def evaluate_gate(
    gate_id: int,
    context: dict[str, Any],
    db: AsyncSession
) -> GateEvaluationResult:
    ...
```

### 5. **Error Handling**
```python
# ✅ Proper exception handling with logging
try:
    result = await opa_service.evaluate_policy(gate_id)
except OPAConnectionError as e:
    logger.error(f"OPA connection failed: {e}")
    raise HTTPException(status_code=503, detail="Policy engine unavailable")
```

---

## 🚀 Deployment Instructions

### Docker Desktop KHÔNG chạy - Hướng Dẫn Khởi Động

```bash
# 1. Mở Docker Desktop application
# macOS: Cmd+Space → "Docker" → Enter
# Hoặc: Applications → Docker.app

# 2. Đợi Docker daemon start (icon trên menu bar)

# 3. Verify Docker đã chạy
docker ps
# Expected: Table với headers (có thể empty)

# 4. Tiếp tục deploy backend
```

### Deployment Steps

```bash
# Bước 1: Kiểm tra Docker daemon
docker ps
# Nếu lỗi: Start Docker Desktop trước

# Bước 2: Kiểm tra environment variables
cat .env | grep -E "DATABASE_URL|SECRET_KEY|REDIS_PASSWORD|MINIO"

# Bước 3: Rebuild backend (NO CACHE)
docker-compose build --no-cache backend

# Bước 4: Start backend
docker-compose up -d backend

# Bước 5: Verify health
sleep 10
curl http://localhost:8300/health
# Expected: {"status":"healthy","version":"1.2.0"}

# Bước 6: Check logs
docker-compose logs -f backend
```

---

**Last Updated**: 2026-02-18
**Status**: ✅ ACTIVE - Gate G3 APPROVED (98.2%)
**Total Services**: 97 service files, 91 API endpoints, 33 database tables
