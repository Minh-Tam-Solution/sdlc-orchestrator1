# Context Authority V1 to V2 Migration Guide

**Version**: 1.0.0
**Date**: February 4, 2026
**Sprint**: 147 - Spring Cleaning
**Status**: ACTIVE
**Sunset Date**: March 6, 2026

---

## Overview

Context Authority V1 API endpoints are deprecated and will be removed on **March 6, 2026**. This guide helps you migrate to the V2 API, which provides:

- **Gate-aware validation**: Context rules change based on current gate status
- **Dynamic overlays**: AGENTS.md updates automatically based on project state
- **Snapshot history**: Track context changes over time
- **Template system**: Reusable overlay configurations

---

## Quick Reference

| V1 Endpoint | V2 Endpoint | Notes |
|-------------|-------------|-------|
| `POST /context-authority/validate` | `POST /context-authority/v2/validate` | V2 adds gate context |
| `GET /context-authority/adrs` | `GET /context-authority/v2/templates` | Use template system |
| `GET /context-authority/adrs/{id}` | `GET /context-authority/v2/templates/{id}` | Use template system |
| `POST /context-authority/check-adr-linkage` | `POST /context-authority/v2/validate` | Included in validation |
| `POST /context-authority/check-spec` | `POST /context-authority/v2/validate` | Included in validation |
| `GET /context-authority/agents-md` | `POST /context-authority/v2/overlay` | Dynamic generation |
| `GET /context-authority/health` | `GET /context-authority/v2/health` | Same interface |

---

## Migration Steps

### Step 1: Update Imports

**Before (V1):**
```typescript
import { validateContext, listADRs } from '@/api/contextAuthority';
```

**After (V2):**
```typescript
import { validateContextV2, listTemplates } from '@/api/contextAuthorityV2';
```

### Step 2: Update Validation Calls

**Before (V1):**
```typescript
const result = await fetch('/api/context-authority/validate', {
  method: 'POST',
  body: JSON.stringify({
    submission_id: submissionId,
    project_id: projectId,
    changed_files: files,
    affected_modules: modules,
    is_new_feature: true,
  }),
});
```

**After (V2):**
```typescript
const result = await fetch('/api/context-authority/v2/validate', {
  method: 'POST',
  body: JSON.stringify({
    submission_id: submissionId,
    project_id: projectId,
    changed_files: files,
    affected_modules: modules,
    is_new_feature: true,
    // V2 additions:
    gate_id: 'G2',  // Current gate context
    tier: 'PROFESSIONAL',  // Project tier
  }),
});
```

### Step 3: Handle New Response Format

**V1 Response:**
```json
{
  "valid": true,
  "violations_count": 0,
  "warnings_count": 1,
  "violations": [],
  "warnings": [...],
  "adr_count": 15,
  "linked_adrs": ["ADR-001", "ADR-002"],
  "spec_found": true,
  "agents_md_fresh": true,
  "module_consistency": true,
  "validated_at": "2026-02-04T10:00:00Z"
}
```

**V2 Response:**
```json
{
  "valid": true,
  "v1_result": { /* V1 compatible result */ },
  "v2_result": {
    "gate_context": {
      "current_gate": "G2",
      "gate_status": "in_progress",
      "stage": "Build"
    },
    "overlay_applied": true,
    "overlay_template_id": "template-123",
    "dynamic_rules": [
      {
        "rule": "strict_testing",
        "active": true,
        "reason": "G2 gate requires comprehensive tests"
      }
    ],
    "vibecoding_zone": "green"
  },
  "snapshot_id": "snapshot-456",
  "validated_at": "2026-02-04T10:00:00Z"
}
```

### Step 4: Use Dynamic Overlays

**New V2 Feature - Generate Dynamic AGENTS.md:**
```typescript
const overlay = await fetch('/api/context-authority/v2/overlay', {
  method: 'POST',
  body: JSON.stringify({
    project_id: projectId,
    gate_id: 'G2',
    tier: 'PROFESSIONAL',
    template_id: 'template-123',  // Optional
    custom_rules: [
      { name: 'no_console_logs', severity: 'error' }
    ],
  }),
});

// Response includes generated AGENTS.md content
const agentsMdContent = overlay.generated_content;
```

### Step 5: Use Template System

**Replace ADR listing with templates:**
```typescript
// V1: List ADRs
const adrs = await fetch('/api/context-authority/adrs');

// V2: Use templates for reusable configurations
const templates = await fetch('/api/context-authority/v2/templates');

// Get specific template
const template = await fetch('/api/context-authority/v2/templates/template-123');
```

---

## Deprecation Headers

All V1 endpoints now return deprecation headers:

```http
HTTP/1.1 200 OK
Deprecation: true
Sunset: 2026-03-06
Link: </context-authority/v2/validate>; rel="successor-version"
X-Deprecation-Reason: Use V2 for gate-aware context validation
X-Migration-Guide: /docs/migration/context-authority-v2.md
```

### Detecting Deprecated Calls

Monitor your logs for deprecation warnings:
```
DEPRECATED_ENDPOINT_CALLED: /context-authority/validate | removal=2026-03-06 | successor=/context-authority/v2/validate | client=MyApp/1.0
```

---

## CLI Migration

**Before (sdlcctl with V1):**
```bash
sdlcctl context validate --project-id abc-123
```

**After (sdlcctl with V2):**
```bash
sdlcctl context validate --project-id abc-123 --gate G2 --use-v2
```

CLI automatically uses V2 endpoints when `--use-v2` flag is provided.

---

## VS Code Extension Migration

Extension v1.5.0+ automatically uses V2 endpoints. Update your extension:

```bash
code --install-extension mtsolution.sdlc-orchestrator@1.5.0
```

---

## FAQ

**Q: What happens after March 6, 2026?**
A: V1 endpoints will return `410 Gone` status. All V1 clients will fail.

**Q: Can I use V1 and V2 simultaneously?**
A: Yes, during the deprecation period both work. Migrate gradually.

**Q: How do I track migration progress?**
A: Check `/admin/api-deprecation` dashboard for V1 call counts.

**Q: Do I need to update database schemas?**
A: No, V2 uses the same underlying data. Only API contracts change.

---

## Support

- **Questions**: Open issue at https://github.com/Minh-Tam-Solution/SDLC-Orchestrator/issues
- **Slack**: #sdlc-platform-migration
- **Deadline**: March 6, 2026

---

**Document Status**: ACTIVE
**Last Updated**: February 4, 2026
**Author**: Backend Team
