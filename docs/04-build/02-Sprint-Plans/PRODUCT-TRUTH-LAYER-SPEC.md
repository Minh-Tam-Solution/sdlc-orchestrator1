# Product Truth Layer Specification

**Purpose**: Establish telemetry foundation to measure real product usage  
**Priority**: P0 - Sprint 147  
**Owner**: Backend Lead + Data Engineer  
**Goal**: Replace "82-85% realization" narrative with measured metrics

---

## 🎯 Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│  PRODUCT TRUTH LAYER                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PURPOSE: Answer "Is the product actually being used?"                 │
│                                                                         │
│  Without telemetry:                                                    │
│  • "82-85% framework realization" = narrative, not fact                │
│  • Feature prioritization = guesswork                                  │
│  • Churn reasons = unknown                                             │
│                                                                         │
│  With telemetry:                                                       │
│  • Activation rate = 64% (measured)                                    │
│  • Time-to-first-evidence = 12.5 min (p50)                            │
│  • Feature usage = ranked by actual data                               │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Core Event Taxonomy

### Tier 1: Activation Events (Sprint 147 - MUST HAVE)

```yaml
# 10 Core Events for Activation Funnel

1. user_signed_up:
   description: User completes registration
   properties:
     user_id: string
     signup_method: enum[email, github_oauth, google_oauth]
     referral_source: string (optional)
     timestamp: datetime
   trigger: POST /auth/register success

2. project_created:
   description: User creates first/new project
   properties:
     project_id: string
     user_id: string
     tier: enum[LITE, STANDARD, PROFESSIONAL, ENTERPRISE]
     template_used: string (optional)
     timestamp: datetime
   trigger: POST /projects success

3. project_connected_github:
   description: Project linked to GitHub repository
   properties:
     project_id: string
     user_id: string
     github_repo: string
     timestamp: datetime
   trigger: POST /projects/{id}/github/connect success

4. first_validation_run:
   description: First validation per project
   properties:
     project_id: string
     user_id: string
     validation_type: enum[folder, spec, compliance]
     result: enum[pass, fail]
     errors_count: integer
     timestamp: datetime
   trigger: First POST /validate/* per project

5. first_evidence_uploaded:
   description: First evidence file uploaded
   properties:
     project_id: string
     user_id: string
     evidence_type: string
     file_size_bytes: integer
     timestamp: datetime
   trigger: First POST /evidence per project

6. first_gate_passed:
   description: First gate approval
   properties:
     project_id: string
     user_id: string
     gate_id: string (e.g., G0.1, G1, G2)
     attempt_count: integer
     timestamp: datetime
   trigger: First gate approval per project

7. invite_sent:
   description: Team invitation sent
   properties:
     project_id: string
     inviter_id: string
     invitee_email: string
     role: string
     timestamp: datetime
   trigger: POST /projects/{id}/invitations success

8. invite_accepted:
   description: Team invitation accepted
   properties:
     project_id: string
     user_id: string
     inviter_id: string
     timestamp: datetime
   trigger: POST /invitations/{id}/accept success

9. policy_violation_blocked:
   description: OPA blocked an action
   properties:
     project_id: string
     user_id: string
     policy_id: string
     gate_id: string
     violation_type: string
     timestamp: datetime
   trigger: OPA evaluation returns deny

10. ai_council_used:
    description: AI features accessed
    properties:
      project_id: string
      user_id: string
      query_type: enum[chat, recommendation, decomposition]
      response_time_ms: integer
      timestamp: datetime
    trigger: POST /ai/council/* success
```

### Tier 2: Engagement Events (Sprint 148)

```yaml
# 10 Additional Events for Retention Analysis

11. daily_active_user:
    description: Computed from any authenticated API call
    properties:
      user_id: string
      date: date
      session_count: integer
      api_calls: integer

12. gate_approval_requested:
    description: User requests gate approval
    trigger: POST /gates/{id}/request-approval

13. evidence_viewed:
    description: Evidence file viewed
    trigger: GET /evidence/{id}

14. dashboard_page_viewed:
    description: Frontend page navigation
    properties:
      page: string
      session_id: string
    trigger: Frontend page load

15. cli_command_executed:
    description: CLI tool usage
    properties:
      command: string
      args: object
      exit_code: integer
    trigger: CLI command completion

16. extension_command_executed:
    description: VSCode extension usage
    properties:
      command: string
      context: object
    trigger: VSCode command execution

17. spec_validated:
    description: Spec validation run
    trigger: POST /specs/validate

18. report_generated:
    description: Report exported
    trigger: GET /reports/*

19. policy_pack_applied:
    description: Policy pack added to project
    trigger: POST /projects/{id}/policy-packs

20. vibecoding_score_changed:
    description: Vibecoding index recalculated
    trigger: Vibecoding recalculation
```

---

## 📈 Three Core Funnels

### Funnel 1: Time-to-First-Project

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FUNNEL: TIME-TO-FIRST-PROJECT                                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Step 1: user_signed_up                                                │
│     ↓                                                                   │
│  Step 2: project_created                                               │
│     ↓                                                                   │
│  Step 3: project_connected_github (optional)                           │
│                                                                         │
│  METRICS:                                                              │
│  ┌─────────────────────┬─────────┬─────────────────────────────────┐   │
│  │ Metric              │ Target  │ Measurement                     │   │
│  ├─────────────────────┼─────────┼─────────────────────────────────┤   │
│  │ Signup → Project    │ <5 min  │ p50, p90, p95                   │   │
│  │ Conversion Rate     │ >70%    │ % who create project in 24h    │   │
│  │ GitHub Connection   │ >50%    │ % who connect repo in 7 days   │   │
│  └─────────────────────┴─────────┴─────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Funnel 2: Time-to-First-Evidence

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FUNNEL: TIME-TO-FIRST-EVIDENCE                                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Step 1: project_created                                               │
│     ↓                                                                   │
│  Step 2: first_validation_run                                          │
│     ↓                                                                   │
│  Step 3: first_evidence_uploaded                                       │
│                                                                         │
│  METRICS:                                                              │
│  ┌─────────────────────┬─────────┬─────────────────────────────────┐   │
│  │ Metric              │ Target  │ Measurement                     │   │
│  ├─────────────────────┼─────────┼─────────────────────────────────┤   │
│  │ Project → Evidence  │ <15 min │ p50, p90, p95                   │   │
│  │ Validation Pass %   │ >60%    │ First-run pass rate             │   │
│  │ Evidence Upload %   │ >40%    │ % who upload in 7 days          │   │
│  └─────────────────────┴─────────┴─────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Funnel 3: Time-to-First-Gate-Pass (NORTH STAR)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  FUNNEL: TIME-TO-FIRST-GATE-PASS                                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Step 1: first_evidence_uploaded                                       │
│     ↓                                                                   │
│  Step 2: gate_approval_requested                                       │
│     ↓                                                                   │
│  Step 3: first_gate_passed                                             │
│                                                                         │
│  METRICS:                                                              │
│  ┌─────────────────────┬─────────┬─────────────────────────────────┐   │
│  │ Metric              │ Target  │ Measurement                     │   │
│  ├─────────────────────┼─────────┼─────────────────────────────────┤   │
│  │ Evidence → Gate     │ <60 min │ p50, p90, p95                   │   │
│  │ First Attempt Pass  │ >30%    │ % who pass on first try         │   │
│  │ Gate Completion     │ >25%    │ % who pass any gate in 30 days  │   │
│  └─────────────────────┴─────────┴─────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Implementation Spec

### Database Schema

```sql
-- New table: product_events
CREATE TABLE product_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    event_name VARCHAR(100) NOT NULL,
    user_id UUID REFERENCES users(id),
    project_id UUID REFERENCES projects(id),
    properties JSONB NOT NULL DEFAULT '{}',
    timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    session_id VARCHAR(100),
    interface VARCHAR(20) CHECK (interface IN ('web', 'cli', 'extension', 'api')),
    
    -- Partitioning hint
    created_date DATE GENERATED ALWAYS AS (DATE(timestamp)) STORED
);

-- Indexes for funnel queries
CREATE INDEX idx_events_user_time ON product_events (user_id, timestamp);
CREATE INDEX idx_events_project_time ON product_events (project_id, timestamp);
CREATE INDEX idx_events_name_time ON product_events (event_name, timestamp);
CREATE INDEX idx_events_funnel ON product_events (user_id, event_name, timestamp);

-- Materialized view for daily metrics (refresh every hour)
CREATE MATERIALIZED VIEW daily_activation_metrics AS
SELECT
    DATE(timestamp) as date,
    COUNT(DISTINCT CASE WHEN event_name = 'user_signed_up' THEN user_id END) as signups,
    COUNT(DISTINCT CASE WHEN event_name = 'project_created' THEN user_id END) as projects_created,
    COUNT(DISTINCT CASE WHEN event_name = 'first_evidence_uploaded' THEN user_id END) as first_evidence,
    COUNT(DISTINCT CASE WHEN event_name = 'first_gate_passed' THEN user_id END) as first_gate_pass
FROM product_events
WHERE timestamp > NOW() - INTERVAL '90 days'
GROUP BY DATE(timestamp);

-- Refresh function (called by Celery)
CREATE OR REPLACE FUNCTION refresh_activation_metrics()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY daily_activation_metrics;
END;
$$ LANGUAGE plpgsql;
```

### API Endpoints

```yaml
# Telemetry API

POST /api/v1/telemetry/events:
  description: Track single product event
  auth: required
  body:
    event_name: string (required, max 100 chars)
    properties: object (optional, max 10KB)
  response:
    status: 201 Created
    body: { event_id: uuid }
  rate_limit: 100/min per user

POST /api/v1/telemetry/events/batch:
  description: Track multiple events
  auth: required
  body:
    events: array (max 100 events)
  response:
    status: 201 Created
    body: { tracked: number, failed: number }
  rate_limit: 10/min per user

GET /api/v1/telemetry/funnels/{funnel_name}:
  description: Get funnel metrics
  auth: required (admin)
  params:
    funnel_name: enum[time_to_project, time_to_evidence, time_to_gate]
    start_date: date (default: 30 days ago)
    end_date: date (default: today)
    cohort_by: enum[day, week, month] (default: week)
  response:
    steps: [
      { name: "user_signed_up", count: 1234, conversion: 100% },
      { name: "project_created", count: 987, conversion: 80% },
      { name: "first_gate_passed", count: 321, conversion: 26% }
    ]
    median_times: { step1_to_step2: 180, step2_to_step3: 720 } # seconds

GET /api/v1/telemetry/dashboard:
  description: Get activation dashboard data
  auth: required (admin)
  response:
    signups_7d: integer
    activation_rate: float (0-1)
    time_to_first_project_p50: integer (seconds)
    time_to_first_evidence_p50: integer (seconds)
    time_to_first_gate_p50: integer (seconds)
    weekly_trend: [{ week: "2026-W05", signups: 45, activated: 29 }]
```

### File Structure

```
backend/
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── telemetry.py              # 3 endpoints (~200 LOC)
│   ├── services/
│   │   └── telemetry_service.py          # Event tracking logic (~250 LOC)
│   ├── models/
│   │   └── product_event.py              # SQLAlchemy model (~50 LOC)
│   └── schemas/
│       └── telemetry.py                  # Pydantic schemas (~100 LOC)
├── alembic/
│   └── versions/
│       └── s147_001_product_events.py    # Migration (~80 LOC)
└── tests/
    └── unit/
        └── services/
            └── test_telemetry_service.py # Tests (~150 LOC)

frontend/
├── src/
│   ├── hooks/
│   │   └── useTelemetry.ts              # React hook (~50 LOC)
│   └── lib/
│       └── telemetry.ts                 # Event tracking util (~100 LOC)
```

### Service Implementation

```python
# backend/app/services/telemetry_service.py

from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.product_event import ProductEvent

class TelemetryService:
    """Product telemetry service for event tracking and funnel analysis."""
    
    VALID_EVENTS = {
        'user_signed_up', 'project_created', 'project_connected_github',
        'first_validation_run', 'first_evidence_uploaded', 'first_gate_passed',
        'invite_sent', 'invite_accepted', 'policy_violation_blocked', 'ai_council_used'
    }
    
    async def track_event(
        self,
        db: AsyncSession,
        event_name: str,
        user_id: Optional[str] = None,
        project_id: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        interface: str = 'api'
    ) -> ProductEvent:
        """Track a single product event."""
        if event_name not in self.VALID_EVENTS:
            raise ValueError(f"Invalid event: {event_name}")
        
        event = ProductEvent(
            event_name=event_name,
            user_id=user_id,
            project_id=project_id,
            properties=properties or {},
            timestamp=datetime.now(timezone.utc),
            interface=interface
        )
        
        db.add(event)
        await db.commit()
        await db.refresh(event)
        
        return event
    
    async def get_funnel_metrics(
        self,
        db: AsyncSession,
        funnel_name: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Calculate funnel conversion metrics."""
        
        funnel_steps = {
            'time_to_project': ['user_signed_up', 'project_created'],
            'time_to_evidence': ['project_created', 'first_validation_run', 'first_evidence_uploaded'],
            'time_to_gate': ['first_evidence_uploaded', 'first_gate_passed']
        }
        
        steps = funnel_steps.get(funnel_name, [])
        results = []
        
        for i, step in enumerate(steps):
            count = await self._count_users_at_step(db, step, start_date, end_date)
            conversion = 100.0 if i == 0 else (count / results[0]['count'] * 100 if results[0]['count'] > 0 else 0)
            results.append({
                'name': step,
                'count': count,
                'conversion': round(conversion, 1)
            })
        
        return {
            'funnel_name': funnel_name,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'steps': results
        }

telemetry_service = TelemetryService()
```

---

## 📊 Dashboard MVP (Sprint 147)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ACTIVATION DASHBOARD                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │  Signups    │  │ Activation  │  │ TTP (p50)   │  │ TTE (p50)   │    │
│  │  Last 7d    │  │    Rate     │  │             │  │             │    │
│  │             │  │             │  │             │  │             │    │
│  │    127      │  │    64%      │  │   3.2 min   │  │  12.5 min   │    │
│  │   ▲ +12%    │  │   ▲ +5%     │  │   ▼ -18%    │  │   ▼ -8%     │    │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  ACTIVATION FUNNEL (Last 30 days)                                 │ │
│  │                                                                   │ │
│  │  Signup ████████████████████████████████████████████████ 100%    │ │
│  │         ↓ 82%                                                    │ │
│  │  Project ██████████████████████████████████████         82%     │ │
│  │         ↓ 64%                                                    │ │
│  │  Evidence ████████████████████████████                  52%      │ │
│  │         ↓ 48%                                                    │ │
│  │  Gate Pass █████████████████████                        25%      │ │
│  │                                                                   │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  ┌───────────────────────────────────────────────────────────────────┐ │
│  │  WEEKLY COHORT RETENTION                                          │ │
│  │                                                                   │ │
│  │  Cohort   W1    W2    W3    W4    W5    W6    W7    W8            │ │
│  │  Jan 6   100%   72%   58%   45%   42%   40%   38%   36%           │ │
│  │  Jan 13  100%   68%   52%   41%   38%   35%   -     -             │ │
│  │  Jan 20  100%   65%   48%   -     -     -     -     -             │ │
│  │  Jan 27  100%   61%   -     -     -     -     -     -             │ │
│  │                                                                   │ │
│  └───────────────────────────────────────────────────────────────────┘ │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## ✅ Implementation Checklist

### Sprint 147 Deliverables

- [ ] Database migration: `product_events` table
- [ ] Model: `ProductEvent` SQLAlchemy model
- [ ] Service: `TelemetryService` with track + funnel methods
- [ ] API: 3 endpoints (track, batch, funnels)
- [ ] Frontend: `useTelemetry` hook
- [ ] Instrumentation: 10 core events in web app
- [ ] Dashboard: Basic activation metrics page
- [ ] Tests: >80% coverage on new code

### Success Metrics

| Metric | Target | Verification |
|--------|--------|--------------|
| Events tracked | 10 types | Code review |
| API latency | <50ms | Load test |
| Dashboard loads | <2s | Browser timing |
| Test coverage | >80% | pytest-cov |
| Data retention | 90 days | DB policy |

---

_Specification Version: 1.0_  
_Created: February 3, 2026_  
_Owner: Backend Lead + Data Engineer_
