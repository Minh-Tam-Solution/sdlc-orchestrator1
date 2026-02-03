# Analytics V1 to Telemetry API Migration Guide

**Version**: 1.0.0
**Date**: February 4, 2026
**Sprint**: 147 - Spring Cleaning
**Status**: ACTIVE
**Sunset Date**: March 6, 2026

---

## Overview

Analytics V1 API endpoints are deprecated and will be removed on **March 6, 2026**. This guide helps you migrate to the new Telemetry API, which provides:

- **Activation Funnels**: Time-to-First-Project, Time-to-First-Evidence, Time-to-First-Gate
- **Interface Breakdown**: Track usage across web, CLI, extension, API
- **Measured Metrics**: Replace "82-85% realization" narrative with real data
- **Standardized Events**: 10 core events + 10 engagement events

---

## Quick Reference

| V1 Endpoint | Telemetry Endpoint | Notes |
|-------------|-------------------|-------|
| `POST /analytics/sessions/start` | `POST /telemetry/events` | Use `event_name: "session_started"` |
| `POST /analytics/sessions/{id}/end` | `POST /telemetry/events` | Use `event_name: "session_ended"` |
| `GET /analytics/sessions/active` | N/A | Sessions tracked via events |
| `POST /analytics/events` | `POST /telemetry/events` | Direct mapping |
| `POST /analytics/events/page-view` | `POST /telemetry/events` | Use `event_name: "dashboard_page_viewed"` |
| `POST /analytics/events/feature` | `POST /telemetry/events` | Use appropriate event name |
| `GET /analytics/my-activity` | `GET /telemetry/dashboard` | Dashboard has richer data |
| `GET /analytics/engagement` | `GET /telemetry/dashboard` | Included in dashboard |
| `GET /analytics/features` | `GET /telemetry/interfaces` | Interface breakdown |
| `GET /analytics/pilot-metrics` | `GET /telemetry/funnels/{name}` | Use activation funnels |
| `POST /analytics/pilot-metrics/calculate` | N/A | Real-time event tracking |
| `GET /analytics/retention/stats` | `GET /telemetry/health` | Health includes stats |
| `POST /analytics/retention/cleanup` | Admin endpoint | Admin-only access |
| `GET /analytics/circuit-breaker/status` | `GET /telemetry/health` | Health includes status |
| `GET /analytics/summary` | `GET /telemetry/dashboard` | Dashboard endpoint |

---

## Migration Steps

### Step 1: Update Event Tracking Calls

**Before (V1):**
```typescript
const result = await fetch('/api/v1/analytics/events', {
  method: 'POST',
  body: JSON.stringify({
    event_type: 'FEATURE_USE',
    event_name: 'gate_evaluation',
    session_token: sessionToken,
    metadata: { gate_id: 'G2' },
  }),
});
```

**After (Telemetry):**
```typescript
const result = await fetch('/api/v1/telemetry/events', {
  method: 'POST',
  body: JSON.stringify({
    event_name: 'gate_evaluation_completed',  // Use past tense snake_case
    project_id: projectId,  // Associate with project
    properties: { gate_id: 'G2', result: 'pass' },
    interface: 'web',  // Track source interface
  }),
});
```

### Step 2: Update Dashboard Queries

**Before (V1):**
```typescript
// Multiple calls needed
const engagement = await fetch('/api/v1/analytics/engagement');
const pilotMetrics = await fetch('/api/v1/analytics/pilot-metrics?days=7');
const features = await fetch('/api/v1/analytics/features?days=7');
```

**After (Telemetry):**
```typescript
// Single dashboard call
const dashboard = await fetch('/api/v1/telemetry/dashboard');

// Response includes:
// - signups_7d, projects_7d, activation_rate
// - All three funnel summaries
// - Generated timestamp

// For specific funnels:
const funnel = await fetch('/api/v1/telemetry/funnels/time_to_first_project');
```

### Step 3: Update Page View Tracking

**Before (V1):**
```typescript
await fetch('/api/v1/analytics/events/page-view', {
  method: 'POST',
  body: JSON.stringify({
    page_url: '/projects',
    session_token: sessionToken,
    referrer_url: document.referrer,
  }),
});
```

**After (Telemetry):**
```typescript
await fetch('/api/v1/telemetry/events', {
  method: 'POST',
  body: JSON.stringify({
    event_name: 'dashboard_page_viewed',
    properties: {
      page: '/projects',
      referrer: document.referrer,
    },
    interface: 'web',
  }),
});
```

---

## Event Name Mapping

### Core Activation Events (Tier 1)

| Purpose | V1 Event | Telemetry Event |
|---------|----------|-----------------|
| User registered | `user_registered` | `user_signed_up` |
| Project created | `project_created` | `project_created` |
| GitHub connected | `github_connected` | `project_connected_github` |
| First validation | `validation_run` | `first_validation_run` |
| First evidence | `evidence_uploaded` | `first_evidence_uploaded` |
| First gate pass | `gate_passed` | `first_gate_passed` |
| Invite sent | `invite_sent` | `invite_sent` |
| Invite accepted | `invite_accepted` | `invite_accepted` |
| Policy blocked | `policy_violation` | `policy_violation_blocked` |
| AI council used | `ai_chat` | `ai_council_used` |

### Engagement Events (Tier 2)

| Purpose | V1 Event | Telemetry Event |
|---------|----------|-----------------|
| Page viewed | `page_view` | `dashboard_page_viewed` |
| Gate requested | `gate_request` | `gate_approval_requested` |
| Evidence viewed | `evidence_view` | `evidence_viewed` |
| CLI command | `cli_command` | `cli_command_executed` |
| Extension command | `extension_command` | `extension_command_executed` |
| Spec validated | `spec_validate` | `spec_validated` |
| Report generated | `report_generate` | `report_generated` |
| Policy applied | `policy_apply` | `policy_pack_applied` |
| Vibecoding changed | `vibecoding_update` | `vibecoding_score_changed` |

---

## Activation Funnels

### Available Funnels

1. **time_to_first_project**
   - Signup → Project Created → GitHub Connected
   - Target: <5 min, >70% conversion

2. **time_to_first_evidence**
   - Project Created → First Validation → First Evidence
   - Target: <15 min, >40% conversion

3. **time_to_first_gate**
   - First Evidence → Gate Requested → Gate Passed
   - Target: <60 min, >25% conversion

### Funnel API Usage

```typescript
// Get specific funnel metrics
const response = await fetch('/api/v1/telemetry/funnels/time_to_first_project?start_date=2026-01-05&end_date=2026-02-04');

// Response:
{
  "funnel_name": "time_to_first_project",
  "period": { "start": "2026-01-05", "end": "2026-02-04" },
  "steps": [
    { "name": "Signup", "count": 127, "rate": 100.0 },
    { "name": "Project Created", "count": 104, "rate": 81.9 },
    { "name": "GitHub Connected", "count": 52, "rate": 50.0 }
  ],
  "overall_conversion": 81.9,
  "target": { "conversion_rate": 70, "median_time_minutes": 5 }
}
```

---

## Interface Breakdown

Track usage across different interfaces (web, CLI, extension, API).

```typescript
const response = await fetch('/api/v1/telemetry/interfaces?start_date=2026-01-28&end_date=2026-02-04');

// Response:
{
  "period": { "start": "2026-01-28", "end": "2026-02-04" },
  "breakdown": { "web": 1500, "cli": 800, "extension": 600, "api": 200 },
  "total": 3100,
  "percentages": { "web": 48.4, "cli": 25.8, "extension": 19.4, "api": 6.5 }
}
```

---

## Deprecation Headers

All V1 endpoints now return deprecation headers:

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: 2026-03-06
Link: </api/v1/telemetry/events>; rel="successor-version"
X-Deprecation-Reason: Use Telemetry API with standardized event taxonomy
X-Migration-Guide: /docs/migration/analytics-v2.md
```

---

## CLI Migration

**Before (V1 via sdlcctl):**
```bash
# V1 analytics commands (deprecated)
sdlcctl analytics engagement
sdlcctl analytics features
```

**After (Telemetry):**
```bash
# New telemetry commands
sdlcctl telemetry dashboard
sdlcctl telemetry funnel time_to_first_project
sdlcctl telemetry interfaces
```

---

## VS Code Extension Migration

Extension v1.5.0+ automatically uses Telemetry API. Update your extension:

```bash
code --install-extension mtsolution.sdlc-orchestrator@1.5.0
```

---

## FAQ

**Q: What happens after March 6, 2026?**
A: V1 endpoints will return `410 Gone` status. All V1 clients will fail.

**Q: Can I use V1 and Telemetry simultaneously?**
A: Yes, during the deprecation period both work. Migrate gradually.

**Q: Are session tokens still needed?**
A: No. Telemetry API uses session_id (optional) instead of tokens.

**Q: How do I track custom events?**
A: Use the `properties` field for custom event data:
```typescript
{
  "event_name": "custom_action",
  "properties": { "custom_field": "value" }
}
```

**Q: Where are my pilot metrics?**
A: Use activation funnels. They provide richer data than pilot metrics.

---

## Support

- **Questions**: Open issue at https://github.com/Minh-Tam-Solution/SDLC-Orchestrator/issues
- **Slack**: #sdlc-platform-migration
- **Deadline**: March 6, 2026

---

**Document Status**: ACTIVE
**Last Updated**: February 4, 2026
**Author**: Backend Team
