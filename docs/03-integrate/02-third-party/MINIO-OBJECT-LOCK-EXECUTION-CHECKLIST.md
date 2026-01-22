# MinIO Object Lock Execution Checklist

**Priority:** P1 - SCALE BLOCKER
**Deadline:** January 25, 2026 (3 days remaining)
**Status:** ✅ READY FOR EXECUTION
**Owner:** DevOps Lead

---

## Prerequisites (Before Execution)

| Item | Status | Command to Verify |
|------|--------|-------------------|
| Docker Compose running | ⏳ | `docker-compose ps` |
| MinIO container up | ⏳ | `docker ps \| grep minio` |
| mc client available | ⏳ | `docker-compose exec minio mc --version` |
| Backup existing data | ⏳ | Manual backup recommended |

---

## Execution Steps

### Step 1: Pre-Execution Review (10 minutes)

- [ ] Review [minio-object-lock-guide.md](minio-object-lock-guide.md)
- [ ] Understand GOVERNANCE vs COMPLIANCE modes
- [ ] Confirm 7-year retention requirement (2555 days)
- [ ] Backup existing evidence data (if any)

**Decision Point:**
- If `sdlc-evidence` bucket exists → Choose Option 2 (create new bucket `sdlc-evidence-v2`)
- If bucket doesn't exist → Proceed with `sdlc-evidence`

---

### Step 2: Execute Configuration Script (15 minutes)

```bash
# Navigate to project root
cd /home/nqh/shared/SDLC-Orchestrator

# Make script executable
chmod +x scripts/setup-minio-object-lock.sh

# Execute script
./scripts/setup-minio-object-lock.sh

# Expected output:
# - ✅ Bucket created with Object Lock
# - ✅ Default retention policy configured (GOVERNANCE, 7 years)
# - ✅ Test file uploaded and WORM protection verified
```

**Script Features:**
- ✅ Interactive prompts for existing bucket handling
- ✅ Automatic prerequisite checks
- ✅ Retention policy configuration
- ✅ WORM protection testing
- ✅ Configuration summary output

---

### Step 3: Backend Integration (30 minutes)

#### 3.1 Update Configuration

Edit `backend/app/core/config.py`:

```python
# MinIO Configuration
MINIO_BUCKET_NAME: str = "sdlc-evidence"  # Or "sdlc-evidence-v2" if new bucket
MINIO_OBJECT_LOCK_ENABLED: bool = True  # NEW
MINIO_RETENTION_DAYS: int = 2555  # 7 years (NEW)
MINIO_RETENTION_MODE: str = "GOVERNANCE"  # NEW
```

#### 3.2 Update MinIO Service

`backend/app/services/minio_service.py` already supports Object Lock (Sprint 82 implementation). Verify:

```python
# Check for these methods (should already exist from Sprint 82):
- upload_evidence_with_retention()
- set_legal_hold()
- verify_object_lock()
```

**Action:** Run grep to confirm:
```bash
grep -n "upload_evidence_with_retention\|set_legal_hold\|verify_object_lock" backend/app/services/minio_service.py
```

**If missing:** Implement methods per [minio-object-lock-guide.md](minio-object-lock-guide.md) Part 3.

---

### Step 4: Verification (20 minutes)

#### 4.1 Bucket Verification

```bash
# Check Object Lock status
docker-compose exec minio mc stat myminio/sdlc-evidence

# Expected output:
# Object Lock: ENABLED

# Check default retention
docker-compose exec minio mc retention info --default myminio/sdlc-evidence

# Expected output:
# Governance mode, 2555 days
```

#### 4.2 Upload Test

```bash
# Upload test evidence via backend API
curl -X POST http://localhost:8000/api/v1/evidence \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test-evidence.pdf" \
  -F "project_id=<project-uuid>"

# Verify retention metadata
docker-compose exec minio mc stat myminio/sdlc-evidence/project-xxx/evidence-xxx.pdf

# Expected: Retention mode GOVERNANCE, Retain until 2033-01-22
```

#### 4.3 WORM Protection Test

```bash
# Try to delete (should fail)
docker-compose exec minio mc rm myminio/sdlc-evidence/project-xxx/evidence-xxx.pdf

# Expected error: "Object is WORM protected and cannot be overwritten"
```

---

### Step 5: Documentation Update (15 minutes)

- [ ] Update [minio-object-lock-guide.md](minio-object-lock-guide.md) with execution results
- [ ] Add configuration date and bucket name used
- [ ] Document any issues encountered
- [ ] Update [CURRENT-SPRINT.md](../../04-build/02-Sprint-Plans/CURRENT-SPRINT.md) with completion status

---

## Success Criteria

| Criterion | Verification | Status |
|-----------|--------------|--------|
| **Object Lock Enabled** | `mc stat` shows "Object Lock: ENABLED" | ⏳ |
| **Default Retention Set** | `mc retention info` shows "GOVERNANCE, 2555 days" | ⏳ |
| **WORM Protection Works** | Delete attempt fails with protection error | ⏳ |
| **Backend Integration** | Evidence upload includes retention metadata | ⏳ |
| **Configuration Saved** | `/tmp/minio-object-lock-config.txt` exists | ⏳ |

---

## Rollback Plan (If Needed)

If configuration fails or causes issues:

```bash
# Option 1: Delete new bucket
docker-compose exec minio mc rb --force myminio/sdlc-evidence-v2

# Option 2: Recreate bucket without Object Lock
docker-compose exec minio mc rb --force myminio/sdlc-evidence
docker-compose exec minio mc mb myminio/sdlc-evidence  # Without --with-lock

# Option 3: Restore from backup
# (Manual restore of evidence data from backup location)
```

---

## Timeline

| Phase | Duration | Owner |
|-------|----------|-------|
| **Pre-Execution Review** | 10 min | DevOps Lead |
| **Script Execution** | 15 min | DevOps Lead |
| **Backend Integration** | 30 min | Backend Lead |
| **Verification** | 20 min | QA + DevOps |
| **Documentation** | 15 min | PM |
| **Total** | **90 minutes** | Team |

**Recommended Execution Time:** Business hours (9am-5pm) with CTO available for approval.

---

## Post-Execution

### Immediate (Same Day)
1. ✅ Verify all success criteria met
2. ✅ Update CURRENT-SPRINT.md with completion
3. ✅ Commit configuration changes to git
4. ✅ Notify team in Slack #sdlc-orchestrator channel

### Short-term (Within 7 Days)
1. Monitor Evidence Vault uploads (check retention metadata)
2. Run full integration test suite
3. Verify no regressions in evidence upload/download
4. Update Pre-Launch Status Report

### Long-term (Before Launch)
1. Document legal compliance (SEC 17a-4, FINRA 4511)
2. Test evidence retrieval after 1 month
3. Prepare customer-facing documentation

---

## Reference Documents

- [minio-object-lock-guide.md](minio-object-lock-guide.md) - Full technical guide
- [Sprint 82 Plan](../../04-build/02-Sprint-Plans/SPRINT-82-HARDENING-EVIDENCE.md) - Original requirements
- [Expert Feedback Plan](../../09-govern/04-Strategic-Updates/) - P1 priority justification

---

## Approvals

- [ ] **DevOps Lead:** Ready to execute script
- [ ] **Backend Lead:** Backend integration plan reviewed
- [ ] **CTO:** Final approval for production execution

---

**Status:** ✅ READY FOR EXECUTION
**Next Action:** Execute script when Docker Compose is running
**Deadline:** January 25, 2026 (3 days remaining)

---

**Created:** January 22, 2026
**Owner:** DevOps Lead + Backend Lead
**Reviewer:** CTO
