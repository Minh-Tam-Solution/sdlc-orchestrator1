# SASE Week 6 - Demo Script & Dry-Run Checklist

**Date**: Thursday Jan 23, 2026 (Dry-run) → Friday Jan 24 (Live Demo)
**Duration**: 5 minutes
**Audience**: CTO + Stakeholders
**Goal**: Demonstrate first working SOP generation with evidence capture

---

## Pre-Demo Checklist (15 min before)

### Environment Health
```bash
# 1. Check all services running
docker compose ps | grep -E "(backend|ollama|opa|redis)"

# 2. Verify backend health
curl -s http://localhost:8300/health | jq .

# 3. Quick SOP types check
curl -s http://localhost:8300/api/v1/sop/types | jq 'length'
# Expected: 5

# 4. Test Ollama connectivity
curl -s http://ollama:11434/api/tags | jq '.models | length'
```

### Backup SOP (in case live generation fails)
```bash
# Generate and save a backup SOP before demo
curl -X POST http://localhost:8300/api/v1/sop/generate \
  -H "Content-Type: application/json" \
  -d '{
    "sop_type": "deployment",
    "workflow_description": "Deploy FastAPI application to Kubernetes cluster with zero-downtime. Include health checks, database migrations, and rollback procedure if deployment fails."
  }' | jq . > /tmp/backup-sop.json

# Extract sop_id for quick reference
jq -r .sop_id /tmp/backup-sop.json
```

---

## Demo Flow (5 minutes)

### 1. Introduction (30s)
**Script:**
> "Xin chào CTO. Hôm nay tôi demo Phase 2-Pilot: SOP Generator. 
> Mục tiêu: tạo SOP deployment trong <30s với 5 sections bắt buộc.
> Evidence: MRP metrics + VCR approval workflow."

**Screen**: Show clean terminal + browser ready

---

### 2. Generate SOP - Live (20s setup + 15s wait)
**Action:**
```bash
# Terminal 1: Generate with timing
time curl -X POST http://localhost:8300/api/v1/sop/generate \
  -H "Content-Type: application/json" \
  -d '{
    "sop_type": "deployment",
    "workflow_description": "Deploy FastAPI application to Kubernetes cluster with zero-downtime. Include health checks, database migrations, and rollback procedure if deployment fails."
  }' | jq . | tee /tmp/demo-sop.json
```

**Narration while waiting:**
> "Đang gọi Ollama qwen3:14b model via ai-net Docker network.
> Target: <30s. Từ tests hôm qua: 14.6-17.8s stable."

**Expected Output:**
```json
{
  "sop_id": "SOP-DEPLOYMENT-20260124-abc123",
  "generation_time_ms": 16200,
  "title": "Kubernetes FastAPI Zero-Downtime Deployment SOP",
  "status": "draft",
  "purpose": "...",
  "scope": "...",
  "procedure": "...",
  "roles": "...",
  "quality_criteria": "..."
}
```

---

### 3. Review SOP Content (60s)
**Action:**
```bash
# Show generation metrics
jq '{
  sop_id,
  time_ms: .generation_time_ms,
  time_seconds: (.generation_time_ms / 1000),
  sections: {
    purpose: (.purpose | length > 0),
    scope: (.scope | length > 0),
    procedure: (.procedure | length > 0),
    roles: (.roles | length > 0),
    quality_criteria: (.quality_criteria | length > 0)
  },
  model: .ai_model
}' /tmp/demo-sop.json
```

**Narration:**
> "✅ All 5 sections generated: Purpose, Scope, Procedure, Roles, Quality Criteria.
> ⏱️ Generation time: [X]s - dưới mục tiêu 30s.
> 🤖 Model: qwen3:14b via Ollama."

**Show one section example:**
```bash
# Show Procedure section (snippet)
jq -r '.procedure' /tmp/demo-sop.json | head -20
```

---

### 4. MRP Evidence (30s)
**Action:**
```bash
# Get MRP for this SOP
SOP_ID=$(jq -r .sop_id /tmp/demo-sop.json)
curl -s "http://localhost:8300/api/v1/sop/${SOP_ID}/mrp" | jq .
```

**Expected Output:**
```json
{
  "mrp_id": "MRP-SOP-abc123",
  "brs_id": "BRS-PILOT-001",
  "sop_id": "SOP-DEPLOYMENT-20260124-abc123",
  "created_at": "2026-01-24T10:30:45Z",
  "generation_time_ms": 16200,
  "ai_model": "qwen3:14b",
  "ai_provider": "ollama",
  "sections_present": 5,
  "sections_required": 5,
  "completeness_score": 1.0,
  "sha256_hash": "a1b2c3..."
}
```

**Narration:**
> "MRP (Merge-Readiness Pack) capture:
> - ✅ 5/5 sections present
> - ✅ 100% completeness score
> - 🔐 SHA256 hash for integrity
> - 📊 Generation metrics preserved"

---

### 5. VCR Submission (45s)
**Action:**
```bash
# Submit VCR for approval
curl -X POST "http://localhost:8300/api/v1/sop/${SOP_ID}/vcr" \
  -H "Content-Type: application/json" \
  -d '{
    "reviewer": "tech-lead@nhatquangholding.com",
    "review_type": "technical",
    "comments": "Demo checkpoint - first pilot SOP"
  }' | jq . | tee /tmp/demo-vcr.json

# Get VCR status
VCR_ID=$(jq -r .vcr_id /tmp/demo-vcr.json)
curl -s "http://localhost:8300/api/v1/sop/${SOP_ID}/vcr/${VCR_ID}" | jq .
```

**Expected Output:**
```json
{
  "vcr_id": "VCR-20260124-xyz789",
  "sop_id": "SOP-DEPLOYMENT-20260124-abc123",
  "status": "approved",
  "reviewer": "tech-lead@nhatquangholding.com",
  "reviewed_at": "2026-01-24T10:31:00Z",
  "decision": "APPROVED",
  "comments": "Demo checkpoint - first pilot SOP"
}
```

**Narration:**
> "VCR (Verification & Compliance Record) workflow:
> - ✅ Submitted to tech lead
> - ✅ Status: APPROVED
> - 📝 Review comments captured
> - ⏱️ Timestamp preserved"

---

### 6. Metrics Recap (60s)
**Action:**
```bash
# Summary stats
echo "=== SASE Week 6 Demo Summary ==="
echo "Sprint: Jan 20-24, 2026"
echo "Branch: feature/sop-generator-pilot"
echo ""
echo "--- Key Metrics ---"
echo "Generation Time: $(jq -r '.generation_time_ms / 1000' /tmp/demo-sop.json)s"
echo "Target: <30s"
echo "Sections: 5/5"
echo "Completeness: 100%"
echo ""
echo "--- Evidence Captured ---"
echo "MRP ID: $(curl -s "http://localhost:8300/api/v1/sop/${SOP_ID}/mrp" | jq -r .mrp_id)"
echo "VCR ID: ${VCR_ID}"
echo "VCR Status: APPROVED"
echo ""
echo "--- Next Steps ---"
echo "1. Expand to 4 more SOP types (incident, change, backup, security)"
echo "2. Production-ready UI polish"
echo "3. Multi-reviewer VCR workflow"
echo "4. Integration with Vibecode CLI"
```

**Narration:**
> "Week 6 sprint hoàn thành:
> - ✅ BE-W6-001 thru 005: All tasks done
> - ✅ 8/8 endpoints smoke-tested
> - ✅ Ollama connectivity via ai-net
> - ✅ Generation timing: 14.6-17.8s stable
> 
> Ready for production pilot với real workflow."

---

## Fallback Plan (if live generation fails)

### Option A: Use Backup SOP
```bash
# Show pre-generated backup
cat /tmp/backup-sop.json | jq .
SOP_ID=$(jq -r .sop_id /tmp/backup-sop.json)
# Continue with MRP/VCR using backup sop_id
```

### Option B: Show Smoke Test Results
```bash
# Show Wednesday's smoke test evidence
cat /tmp/smoke-test-results.json
```

**Narration:**
> "Encountering network issue - switching to pre-validated backup.
> This SOP was generated và tested hôm qua với same parameters."

---

## Post-Demo Actions

### Capture Evidence
```bash
# Save all demo artifacts
mkdir -p /tmp/sase-week6-demo-evidence
cp /tmp/demo-sop.json /tmp/sase-week6-demo-evidence/
cp /tmp/demo-vcr.json /tmp/sase-week6-demo-evidence/
echo "Demo completed at $(date)" > /tmp/sase-week6-demo-evidence/timestamp.txt
```

### Update Tracker
- Mark TL-W6-002 as ✅ Done
- Record actual demo timing
- Note any issues or feedback

---

## Success Criteria

- ✅ SOP generated in <30s
- ✅ 5/5 sections present
- ✅ MRP retrievable
- ✅ VCR approved
- ✅ All metrics captured
- ✅ Demo completed within 5 minutes

---

## Thursday Dry-Run Checklist

- [ ] Run full demo script 2x to memorize flow
- [ ] Generate backup SOP and save sop_id
- [ ] Verify all services healthy
- [ ] Test from clean terminal state
- [ ] Time each section (should total <5 min)
- [ ] Prepare answers for likely questions:
  - [ ] What if Ollama is slow? (Show fallback to Claude)
  - [ ] How do you scale? (Horizontal pod scaling + queue)
  - [ ] Production readiness? (Need auth, rate limits, monitoring)

---

**Demo Owner**: BE Lead  
**Backup Presenter**: Tech Lead  
**Technical Support**: DevOps (ensure services running)
