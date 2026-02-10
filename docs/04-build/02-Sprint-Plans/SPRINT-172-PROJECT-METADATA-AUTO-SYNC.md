# Sprint 172: Project Metadata Auto-Sync

**Sprint Duration**: Feb 10-14, 2026 (5 days)
**Status**: 🔄 IN PROGRESS
**Phase**: Phase 6 - Market Expansion + Infrastructure
**Framework**: SDLC 6.0.3 (7-Pillar + Section 7 Quality Assurance)
**CTO Approval**: ✅ APPROVED (Feb 10, 2026)

---

## 🎯 **Sprint Goal**

Implement **Project Metadata Auto-Sync** to eliminate manual database updates by parsing canonical repository files (`.sdlc-config.json`, `AGENTS.md`, `CLAUDE.md`, `README.md`) on project access.

**Success Criteria**:
- ✅ POST `/projects/{id}/sync` endpoint working
- ✅ Auto-sync on project page load
- ✅ 95%+ test coverage
- ✅ <200ms p95 latency
- ✅ SDLC-Orchestrator metadata always accurate

---

## 📋 **Sprint Backlog**

### **Day 1: Backend Implementation** (2 hours)

#### Task 1.1: ProjectSyncService Core (1 hour)
**Owner**: Backend Team
**Priority**: P0

**Deliverables**:
```python
# backend/app/services/project_sync_service.py

class ProjectSyncService:
    - async def sync_project_metadata()
    - async def _parse_sdlc_config()
    - async def _parse_agents_md()
    - async def _parse_claude_md()
    - async def _parse_readme()
    - async def _get_git_metadata()
```

**Acceptance Criteria**:
- [ ] All 6 methods implemented with real file parsing (no mocks)
- [ ] Handles missing files gracefully (returns empty dict)
- [ ] Parses AGENTS.md lines 20-30 for sprint info
- [ ] Parses CLAUDE.md lines 1-10 for framework version
- [ ] README.md first paragraph extraction (<200 chars)

**Test Coverage**: 95%+

#### Task 1.2: API Endpoint (1 hour)
**Owner**: Backend Team
**Priority**: P0

**Deliverables**:
```python
# backend/app/api/routes/projects.py

@router.post("/{project_id}/sync")
async def sync_project_metadata():
    # 1. Check permissions (project member only)
    # 2. Check 5-min cache (Redis)
    # 3. Call ProjectSyncService
    # 4. Update database
    # 5. Set cache
    # 6. Return updated project
```

**Acceptance Criteria**:
- [ ] POST `/api/v1/projects/{id}/sync` endpoint created
- [ ] Auth middleware (requires project membership)
- [ ] 5-min cache with Redis
- [ ] Updates `projects` table with synced metadata
- [ ] Returns `ProjectResponse` schema
- [ ] Error handling (404, 403, 500)

**Test Coverage**: 90%+

---

### **Day 2: Frontend Integration** (1 hour)

#### Task 2.1: useProjectSync Hook (30 min)
**Owner**: Frontend Team
**Priority**: P0

**Deliverables**:
```typescript
// frontend/src/hooks/useProjectSync.ts

export function useProjectSync(projectId: string) {
  return useMutation({
    mutationFn: () => syncProjectMetadata(projectId),
    onSuccess: (updatedProject) => {
      // Update cache
      // Invalidate queries
    }
  });
}
```

**Acceptance Criteria**:
- [ ] Hook created with TanStack Query mutation
- [ ] Calls `POST /projects/{id}/sync` API
- [ ] Updates project cache on success
- [ ] Invalidates project list queries
- [ ] Error handling with console.error

**Test Coverage**: 80%+

#### Task 2.2: Auto-Sync on Page Load (30 min)
**Owner**: Frontend Team
**Priority**: P0

**Deliverables**:
```typescript
// frontend/src/app/app/projects/[id]/page.tsx

export default function ProjectDetailPage({ params }) {
  const syncMutation = useProjectSync(params.id);

  // Auto-sync on mount
  useEffect(() => {
    syncMutation.mutate();
  }, [params.id]);

  return <ProjectDetails />;
}
```

**Acceptance Criteria**:
- [ ] Project detail page calls `syncMutation.mutate()` on mount
- [ ] Non-blocking (page loads with cached data)
- [ ] UI updates when sync completes
- [ ] Optional: Loading indicator during sync

**Test Coverage**: E2E test

---

### **Day 3: Testing & QA** (1 hour)

#### Task 3.1: Unit Tests (30 min)
**Owner**: Backend Team
**Priority**: P0

**Files**:
```bash
backend/tests/unit/services/test_project_sync_service.py
  - test_parse_sdlc_config_valid()
  - test_parse_sdlc_config_missing()
  - test_parse_agents_md_sprint_171()
  - test_parse_agents_md_no_sprint()
  - test_parse_claude_md_framework_version()
  - test_parse_readme_first_paragraph()
  - test_get_git_metadata()
```

**Acceptance Criteria**:
- [ ] 95%+ coverage for ProjectSyncService
- [ ] All edge cases tested (missing files, invalid JSON, empty content)
- [ ] Fast (<1s total test time)

#### Task 3.2: Integration Tests (30 min)
**Owner**: Backend + Frontend Team
**Priority**: P0

**Files**:
```bash
backend/tests/integration/test_project_sync_api.py
  - test_sync_project_metadata_success()
  - test_sync_project_metadata_cache()
  - test_sync_project_metadata_not_member()
  - test_sync_project_metadata_repo_not_found()

frontend/e2e/project-metadata-sync.spec.ts
  - test('auto-syncs on page load')
  - test('displays synced metadata')
```

**Acceptance Criteria**:
- [ ] 90%+ coverage for API endpoint
- [ ] E2E test passes (Playwright)
- [ ] Performance verified (<200ms p95)

---

### **Day 4: Deployment & Verification** (30 min)

#### Task 4.1: Deploy to Staging (15 min)
**Owner**: DevOps Team
**Priority**: P0

**Steps**:
1. Rebuild backend Docker image
2. Deploy to staging environment
3. Restart backend service
4. Verify health checks pass

**Acceptance Criteria**:
- [ ] Backend deployed to staging
- [ ] POST `/projects/{id}/sync` endpoint accessible
- [ ] Logs show no errors

#### Task 4.2: Smoke Testing (15 min)
**Owner**: QA Team
**Priority**: P0

**Test Cases**:
1. Visit https://sdlc.nhatquangholding.com/app/projects/c0000000-0000-0000-0000-000000000003
2. Check Network tab: POST `/projects/{id}/sync` called
3. Verify metadata updated (SDLC 6.0.3, Sprint 171, G3 Ship Ready)
4. Refresh page: metadata still accurate (cached)
5. Wait 6 minutes: metadata re-synced (cache expired)

**Acceptance Criteria**:
- [ ] All smoke tests pass
- [ ] No 500 errors in logs
- [ ] Performance <200ms (Chrome DevTools)

---

### **Day 5: Documentation & Sprint Close** (1 hour)

#### Task 5.1: Update Documentation (30 min)
**Owner**: Tech Lead
**Priority**: P1

**Files to Update**:
```bash
docs/02-design/14-Technical-Specs/Project-Metadata-Auto-Sync-Design.md ✅
docs/04-build/02-Sprint-Plans/SPRINT-172-PROJECT-METADATA-AUTO-SYNC.md ✅
docs/01-planning/05-API-Design/API-Specification.md (add /sync endpoint)
AGENTS.md (update with Sprint 172 completion)
```

**Acceptance Criteria**:
- [ ] Technical spec complete
- [ ] Sprint plan updated
- [ ] API docs include `/sync` endpoint
- [ ] AGENTS.md reflects Sprint 172 status

#### Task 5.2: Sprint Completion Report (30 min)
**Owner**: Scrum Master
**Priority**: P1

**Deliverable**: `SPRINT-172-COMPLETION-REPORT.md`

**Sections**:
- Sprint goal achievement (100%)
- Velocity (LOC added, tests written)
- Performance metrics (latency, test coverage)
- Known issues / technical debt
- Next sprint preview (Phase 3 features)

**Acceptance Criteria**:
- [ ] Report published to docs/04-build/02-Sprint-Plans/
- [ ] CTO review scheduled
- [ ] Stakeholders notified

---

## 📊 **Sprint Metrics**

### Estimated Effort

```yaml
Total Effort: 3-4 hours
  Day 1 (Backend): 2 hours
  Day 2 (Frontend): 1 hour
  Day 3 (Testing): 1 hour
  Day 4 (Deploy): 0.5 hour
  Day 5 (Docs): 1 hour

Team Allocation:
  - Backend Lead: 2.5 hours
  - Frontend Lead: 1 hour
  - QA Engineer: 1 hour
  - DevOps: 0.5 hour
  - Tech Lead: 1 hour (docs)
```

### Code Metrics (Estimated)

```yaml
New Code:
  Backend:
    - project_sync_service.py: ~200 LOC
    - projects.py (endpoint): ~50 LOC
  Frontend:
    - useProjectSync.ts: ~30 LOC
    - page.tsx (integration): ~10 LOC

  Total: ~290 LOC (production code)

Tests:
  - Unit tests: ~150 LOC
  - Integration tests: ~100 LOC
  - E2E tests: ~50 LOC

  Total: ~300 LOC (test code)

Test Coverage: 95%+ (unit + integration)
```

### Performance Targets

```yaml
API Latency (p95):
  - Cache hit: <50ms
  - Cache miss: <200ms

File Parsing Time:
  - .sdlc-config.json: <10ms
  - AGENTS.md: <20ms
  - CLAUDE.md: <20ms
  - README.md: <30ms

Total Pipeline: <130ms (under 200ms target)
```

---

## 🔗 **Related Documents**

### Design Documents (Stage 02)
- ✅ [Technical Specification](../../../02-design/14-Technical-Specs/Project-Metadata-Auto-Sync-Design.md)
- ✅ [ADR-029: AGENTS.md Integration Strategy](../../../02-design/01-ADRs/ADR-029-AGENTS-MD-Integration-Strategy.md)

### Migration (Stage 04)
- ✅ [s172_001_sync_sdlc_orchestrator_metadata.py](../../../backend/alembic/versions/s172_001_sync_sdlc_orchestrator_metadata.py)

### Testing (Stage 05)
- [ ] Unit tests: `backend/tests/unit/services/test_project_sync_service.py`
- [ ] Integration tests: `backend/tests/integration/test_project_sync_api.py`
- [ ] E2E tests: `frontend/e2e/project-metadata-sync.spec.ts`

---

## ⚠️ **Risks & Mitigation**

### Risk 1: Repository Path Not Accessible

**Impact**: HIGH (sync fails for all projects)
**Probability**: MEDIUM

**Mitigation**:
- Validate `repo_path` exists before parsing
- Fallback to default path: `/home/nqh/shared/{project.name}`
- Error handling returns 404 with clear message
- Admin dashboard to configure repo paths

### Risk 2: File Parsing Errors

**Impact**: MEDIUM (partial sync, missing data)
**Probability**: LOW

**Mitigation**:
- Graceful degradation (missing file → empty dict)
- JSON schema validation for .sdlc-config.json
- Regex patterns tested with edge cases
- Logging for debugging (which file/line failed)

### Risk 3: Performance Degradation

**Impact**: MEDIUM (slow page loads)
**Probability**: LOW

**Mitigation**:
- 5-min cache (avoid excessive file I/O)
- Background mutation (non-blocking UI)
- Performance profiling (Chrome DevTools)
- Monitoring alerts (p95 latency >200ms)

---

## ✅ **Definition of Done**

Sprint 172 is **DONE** when:

- [x] **Phase 1** (Quick Fix): SDLC-Orchestrator metadata updated via migration ✅
- [ ] **Phase 2** (Auto-Sync):
  - [ ] POST `/projects/{id}/sync` endpoint live in staging
  - [ ] Auto-sync on project page load (frontend integration)
  - [ ] 95%+ test coverage (unit + integration + E2E)
  - [ ] <200ms p95 latency (measured, not estimated)
  - [ ] All smoke tests pass
  - [ ] Documentation complete (tech spec + sprint plan + API docs)
  - [ ] CTO approval for production deployment

**Sign-off Required**:
- CTO (Technical approval)
- QA Lead (Test verification)
- DevOps (Deployment confirmation)

---

## 📅 **Next Sprint Preview: Sprint 173**

### Phase 3: Production Enhancements

**Features** (Future):
- GitHub API integration (remote repos)
- Webhook triggers (push → auto-sync)
- Background job queue (non-blocking)
- Admin dashboard (sync status monitoring)
- Batch sync for all projects (CLI command)

**Estimated Effort**: 5-7 hours (Sprint 173-174)

---

## 📝 **Sprint Retrospective** (Post-Sprint)

### What Went Well
- Phase 1 completed in 30 min (SQL migration)
- Clear technical spec before implementation
- ADR-029 compliance ensured vendor neutrality

### What Could Be Improved
- TBD (post-sprint)

### Action Items
- TBD (post-sprint)

---

**Sprint Status**: 🔄 IN PROGRESS (Day 1)
**Next Update**: Daily standup (Feb 11, 2026)
**CTO Review**: Sprint close (Feb 14, 2026)
