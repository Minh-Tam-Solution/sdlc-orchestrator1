# Sprint 149: V2 API Finalization
## Vibecoding + AI Detection Consolidation

**Sprint ID**: S149  
**Phase**: Phase 1 - Consolidation  
**Dates**: February 18-22, 2026 (5 days)  
**Status**: 📋 PLANNED  
**Priority**: P0 - Tech Debt Reduction  
**Budget**: $7,000  
**Team**: 2 FTE (Backend + Frontend)

---

## Executive Summary

**Objective**: Consolidate Vibecoding V1/V2 and AI Detection services, finalize Phase 1 consolidation.

**Success Criteria**:
- [ ] Vibecoding services: 3 files → 1 consolidated service
- [ ] AI Detection services: 4 files → 2 consolidated services
- [ ] Service count: 140 → 130 (-10 services, -7% reduction)
- [ ] MCP Analytics Dashboard MVP live
- [ ] Phase 1 consolidation 90% complete

**Business Impact**:
- **Vibecoding Index**: Unified calculation across all code paths
- **AI Detection**: Consistent detection across Cursor, Claude, Copilot
- **MCP Analytics**: Visibility into MCP usage patterns
- **Phase 1 Progress**: 90% complete (10% ahead of schedule)

---

## Day-by-Day Plan

### Day 1: Vibecoding V1/V2 Audit + Merge Plan

**Objectives**:
- Analyze Vibecoding implementations (V1, V2, Framework 6.0)
- Identify merge strategy
- Create unified Vibecoding service

**Tasks**:

#### Analysis (3 hours)
- [ ] Audit Vibecoding implementations:
  - `vibecoding_service.py` (V1): 485 LOC, 5 signals
  - `vibecoding_v2_service.py` (V2): 623 LOC, 5 signals + MAX CRITICALITY
  - `governance_signals_engine.py` (Framework 6.0): 550 LOC, Vibecoding Index 0-100
- [ ] Identify differences:
  - Signal calculation methods
  - Index calculation (V1: 0-4 scale, V2: 0-100 scale)
  - MAX CRITICALITY override (V2 only)
- [ ] Document breaking changes
- [ ] Create merge plan

#### Merge Plan (3 hours)
- [ ] Decision: Keep V2 as canonical implementation
- [ ] Migrate V1 clients to V2 API
- [ ] Merge Framework 6.0 enhancements into V2
- [ ] Deprecate V1 endpoints (4 endpoints)
- [ ] Create migration guide

#### Implementation Start (2 hours)
- [ ] Create `vibecoding_unified_service.py`
- [ ] Port V2 signal calculations
- [ ] Add MAX CRITICALITY logic
- [ ] Add Framework 6.0 Governance Signals Engine

**Deliverables**:
- `docs/04-build/04-Analysis/vibecoding-consolidation-analysis.md`
- `backend/app/services/vibecoding_unified_service.py` (skeleton, ~200 LOC)
- Migration plan document

**Exit Criteria**:
- [ ] Merge strategy approved by CTO
- [ ] Migration plan documented
- [ ] Unified service skeleton created

### Day 2: Vibecoding V2 Migration + V1 Deprecation

**Objectives**:
- Complete Vibecoding unified service
- Deprecate V1 endpoints
- Migrate all V1 clients to V2

**Tasks**:

#### Service Implementation (4 hours)
- [ ] Complete `vibecoding_unified_service.py`:
  - 5 signal calculations (Architectural Smell, Abstraction Complexity, AI Dependency, Change Surface Area, Drift Velocity)
  - Vibecoding Index calculation (0-100 scale)
  - MAX CRITICALITY override logic
  - Caching layer (Redis)
- [ ] Add telemetry tracking:
  - `vibecoding_index_calculated` event
  - `max_criticality_triggered` event
- [ ] Write 25 unit tests

#### V1 Deprecation (2 hours)
- [ ] Add deprecation headers to 4 V1 endpoints:
  - `POST /api/v1/vibecoding/calculate`
  - `GET /api/v1/vibecoding/index/{pr_id}`
  - `GET /api/v1/vibecoding/signals/{pr_id}`
  - `POST /api/v1/vibecoding/batch`
- [ ] Sunset date: March 22, 2026 (30 days)
- [ ] Create migration guide: `docs/04-build/03-Migration-Guides/vibecoding-v2.md`

#### Client Migration (2 hours)
- [ ] Update 15 internal clients to use V2 API
- [ ] Update frontend components (VibecodeIndexBadge, PRReviewPanel)
- [ ] Update CLI (`sdlcctl vibecode`)
- [ ] Update VS Code Extension

**Deliverables**:
- `backend/app/services/vibecoding_unified_service.py` (complete, ~800 LOC)
- 25 unit tests
- Migration guide
- Deprecated V1 endpoints (4)
- Updated clients (15 files)

**Exit Criteria**:
- [ ] Vibecoding unified service complete
- [ ] All tests passing (25/25)
- [ ] V1 clients migrated to V2

### Day 3: AI Detection Service Consolidation

**Objectives**:
- Consolidate AI Detection services (4 → 2)
- Improve detection accuracy
- Add telemetry

**Tasks**:

#### Audit (2 hours)
- [ ] Analyze AI Detection implementations:
  - `ai_detection_service.py` (pattern-based): 345 LOC
  - `ai_metadata_extractor.py` (metadata-based): 289 LOC
  - `ai_commit_analyzer.py` (commit pattern analysis): 412 LOC
  - `ai_confidence_scorer.py` (ML-based scoring): 378 LOC
- [ ] Identify duplication:
  - Pattern detection (2 implementations)
  - Confidence scoring (overlap between services)
- [ ] Create merge plan

#### Consolidation (4 hours)
- [ ] Merge into 2 services:
  - `ai_detection_service.py` (core detection logic): Pattern + metadata + commit analysis
  - `ai_confidence_scorer.py` (ML scoring): Keep separate for maintainability
- [ ] Unify detection logic:
  - Cursor detection: Check for `cursor-` in commit metadata
  - Copilot detection: Check for `co-authored-by: github-copilot` in commit message
  - Claude Code detection: Check for `claude-code-` in branch name or commit metadata
- [ ] Add telemetry:
  - `ai_code_detected` event (tool, confidence, method)
  - `ai_detection_false_positive` event (for user feedback)

#### Testing (2 hours)
- [ ] Write 20 unit tests
- [ ] Write 5 integration tests (E2E PR detection)
- [ ] Test accuracy against 100 known AI-generated PRs (target: ≥95% accuracy)

**Deliverables**:
- `backend/app/services/ai_detection_service.py` (consolidated, ~900 LOC)
- `backend/app/services/ai_confidence_scorer.py` (ML scoring, ~400 LOC)
- 25 tests
- Accuracy report: ≥95% on test set

**Exit Criteria**:
- [ ] AI Detection consolidated (4 → 2 services)
- [ ] Detection accuracy ≥95%
- [ ] All tests passing (25/25)

### Day 4: MCP Analytics Dashboard MVP

**Objectives**:
- Build MCP Analytics Dashboard UI
- Track MCP usage patterns
- Visualize context provider performance

**Tasks**:

#### Backend (2 hours)
- [ ] Create MCP analytics endpoints:
  - `GET /api/v1/mcp/analytics/usage` - MCP requests over time
  - `GET /api/v1/mcp/analytics/providers` - Context provider usage breakdown
  - `GET /api/v1/mcp/analytics/performance` - Average response time per provider
  - `POST /api/v1/mcp/analytics/export` - Export CSV/JSON
- [ ] Query telemetry data (from Sprint 147 Product Truth Layer)
- [ ] Add caching (Redis, 5-minute TTL)

#### Frontend (4 hours)
- [ ] Create `MCPAnalyticsDashboard.tsx`:
  - MCP request volume chart (daily, weekly, monthly)
  - Context provider usage pie chart (12 providers from Sprint 145)
  - Performance metrics table (avg response time, p95, p99)
  - Top 10 users by MCP usage
- [ ] Create `ContextProviderUsageChart.tsx` component
- [ ] Create `MCPPerformanceTable.tsx` component
- [ ] Add dashboard route: `/admin/mcp-analytics`

#### Testing (2 hours)
- [ ] Write 8 backend tests
- [ ] Write 5 frontend tests
- [ ] E2E test: View dashboard → Export CSV

**Deliverables**:
- 4 new backend endpoints
- `frontend/src/components/admin/MCPAnalyticsDashboard.tsx` (~600 LOC)
- `frontend/src/components/charts/ContextProviderUsageChart.tsx` (~200 LOC)
- `frontend/src/components/tables/MCPPerformanceTable.tsx` (~150 LOC)
- 13 tests

**Exit Criteria**:
- [ ] MCP Analytics Dashboard live
- [ ] All 4 charts/tables functional
- [ ] Dashboard loads in <2s

### Day 5: Phase 1 Verification + Documentation

**Objectives**:
- Verify Phase 1 consolidation complete (90%)
- Final documentation
- Tag release

**Tasks**:

#### Phase 1 Verification (3 hours)
- [ ] Service count verification:
  - Sprint 147 baseline: 164
  - Sprint 148: 140 (-24)
  - Sprint 149: 130 (-10)
  - **Total reduction: -34 services (-21%)**
- [ ] API endpoint verification:
  - Sprint 147: -22 V1 endpoints (Context Authority, Analytics)
  - Sprint 149: -4 V1 endpoints (Vibecoding)
  - **Total reduction: -26 endpoints (-18%)**
- [ ] Telemetry verification:
  - 10 core events instrumented (Sprint 147)
  - 3 funnels operational (Sprint 147)
  - MCP analytics live (Sprint 149)
- [ ] Test coverage: ≥95% maintained

#### Documentation (3 hours)
- [ ] Update `ROADMAP-147-170.md`:
  - Phase 1 progress: 90% → 100% (ahead of schedule)
  - Sprint 150 preview
- [ ] Update `AGENTS.md`:
  - New Vibecoding API
  - AI Detection service changes
  - MCP Analytics dashboard
- [ ] Create Phase 1 completion report:
  - `docs/04-build/05-Phase-Reports/PHASE-1-CONSOLIDATION-COMPLETE.md`
  - Achievements, metrics, lessons learned
- [ ] Update `CHANGELOG.md`

#### Release (2 hours)
- [ ] Code review by CTO
- [ ] Merge to main branch
- [ ] Tag release: `sprint-149-v1.0.0`
- [ ] Tag Phase 1 milestone: `phase-1-consolidation-complete`
- [ ] Deploy to staging
- [ ] Smoke test

**Deliverables**:
- Phase 1 completion report
- Updated roadmap and AGENTS.md
- Git tags: `sprint-149-v1.0.0`, `phase-1-consolidation-complete`
- Staging deployment

**Exit Criteria**:
- [ ] Phase 1 verification complete (90%)
- [ ] All documentation updated
- [ ] Release tagged
- [ ] Ready for Phase 2 kickoff

---

## Key Performance Indicators (KPIs)

| Metric | Baseline (S148) | Target (S149) | Achieved |
|--------|-----------------|---------------|----------|
| **Service Count** | 140 | 130 | ⏳ |
| **Vibecoding Services** | 3 | 1 | ⏳ |
| **AI Detection Services** | 4 | 2 | ⏳ |
| **V1 Endpoints Deprecated** | 22 (S147) | +4 = 26 total | ⏳ |
| **MCP Analytics Dashboard** | No | Yes (MVP) | ⏳ |
| **AI Detection Accuracy** | ~85% | ≥95% | ⏳ |
| **Test Coverage** | 95% | ≥95% | ⏳ |
| **Phase 1 Progress** | 75% | 90% | ⏳ |

**Phase 1 Consolidation Summary**:
- Sprint 147: V1/V2 API merge (-22 endpoints), Telemetry (10 events)
- Sprint 148: Service consolidation (-24 services)
- Sprint 149: Vibecoding/AI Detection merge (-10 services, -4 endpoints)
- **Total**: -34 services (-21%), -26 endpoints (-18%)

---

## Vibecoding V2 Unified Service

### Architecture

```python
class VibecodeUnifiedService:
    """
    Unified Vibecoding service combining V1, V2, and Framework 6.0.
    
    Features:
    - 5 signals (Architectural Smell, Abstraction Complexity, AI Dependency, 
      Change Surface Area, Drift Velocity)
    - Vibecoding Index (0-100 scale)
    - MAX CRITICALITY override
    - Redis caching
    - Telemetry integration
    """
    
    def calculate_index(self, pr: PullRequest) -> VibecodeIndex:
        """
        Calculate Vibecoding Index (0-100) for a PR.
        
        Returns:
        - index: int (0-100)
        - signals: Dict[str, int] (5 signals, each 0-20)
        - max_criticality_triggered: bool
        - recommendation: str (Green/Yellow/Orange/Red)
        """
        pass
```

### Signal Definitions

| Signal | Weight | Calculation | Max Score |
|--------|--------|-------------|-----------|
| **Architectural Smell** | 20% | Cyclomatic complexity, God classes | 20 |
| **Abstraction Complexity** | 20% | Nesting depth, function length | 20 |
| **AI Dependency** | 20% | AI-generated LOC / Total LOC | 20 |
| **Change Surface Area** | 20% | Files changed, LOC changed | 20 |
| **Drift Velocity** | 20% | Days since last ADR, stale AGENTS.md | 20 |

**Vibecoding Index** = Sum of 5 signals (0-100)

**Routing**:
- 0-30: Green (Auto-approve)
- 31-60: Yellow (Fast review)
- 61-80: Orange (Deep review)
- 81-100: Red (CTO/CEO approval)

**MAX CRITICALITY Override**: Any signal >80 → Red, regardless of index

---

## AI Detection Unified Service

### Detection Methods

| Method | Description | Accuracy | Priority |
|--------|-------------|----------|----------|
| **Metadata** | Check commit metadata for AI tool signatures | 98% | P0 |
| **Pattern** | Analyze code patterns (consistent style, generic names) | 85% | P1 |
| **Commit Message** | Check for `co-authored-by: github-copilot` | 95% | P0 |
| **Branch Name** | Check for `cursor-`, `claude-code-`, `copilot-` | 90% | P1 |
| **ML Scoring** | TF-IDF + RandomForest classifier | 92% | P2 |

### Detection Flow

```python
def detect_ai_generated_code(pr: PullRequest) -> AIDetectionResult:
    """
    Detect if PR contains AI-generated code.
    
    Returns:
    - detected: bool
    - tool: str (Cursor/Copilot/Claude/Unknown)
    - confidence: float (0.0-1.0)
    - methods: List[str] (detection methods used)
    """
    
    # 1. Check metadata (fastest, highest accuracy)
    metadata_result = check_metadata(pr)
    if metadata_result.detected:
        return metadata_result
    
    # 2. Check commit message
    commit_result = check_commit_message(pr)
    if commit_result.detected:
        return commit_result
    
    # 3. Check branch name
    branch_result = check_branch_name(pr)
    if branch_result.detected:
        return branch_result
    
    # 4. Pattern analysis (slower)
    pattern_result = analyze_patterns(pr)
    if pattern_result.confidence > 0.8:
        return pattern_result
    
    # 5. ML scoring (slowest, last resort)
    ml_result = ml_score(pr)
    return ml_result
```

**Target Accuracy**: ≥95% on test set of 100 known AI-generated PRs

---

## MCP Analytics Dashboard

### Metrics

| Metric | Description | Visualization |
|--------|-------------|---------------|
| **MCP Request Volume** | Total MCP requests over time | Line chart (daily/weekly/monthly) |
| **Context Provider Usage** | Breakdown by 12 providers | Pie chart |
| **Performance** | Avg response time per provider | Table (sortable) |
| **Top Users** | Users by MCP usage | Bar chart (top 10) |
| **Error Rate** | Failed MCP requests over time | Line chart |

### Context Providers (from Sprint 145)

1. `project_context` - Project metadata
2. `gate_context` - Gate configurations
3. `evidence_context` - Evidence vault files
4. `ai_council_context` - AI Council suggestions
5. `sprint_context` - Sprint data
6. `organization_context` - Organization settings
7. `user_context` - User profile
8. `policy_context` - OPA policies
9. `adr_context` - ADR documents
10. `agents_md_context` - AGENTS.md freshness
11. `telemetry_context` - Product events
12. `vibecode_context` - Vibecoding Index history

---

## Risk Management

| Risk | Impact | Probability | Mitigation | Status |
|------|--------|-------------|------------|--------|
| **Vibecoding migration breaks clients** | High | Medium | Gradual rollout + V1 deprecation period | ⏳ |
| **AI Detection accuracy <95%** | Medium | Medium | Fallback to conservative detection | ⏳ |
| **MCP Analytics slow (>2s load)** | Low | Low | Redis caching + pagination | ⏳ |
| **Phase 1 incomplete** | High | Low | Buffer day in Sprint 150 | ⏳ |

---

## Dependencies

### Upstream (Blockers)
- ✅ Sprint 148 complete (Service consolidation to 140)
- ✅ Sprint 147 telemetry baseline operational

### Downstream (Depends on Sprint 149)
- Sprint 150: Phase 1 verification requires Sprint 149 metrics
- Sprint 151: Phase 2 kickoff requires Phase 1 complete

---

## Success Metrics Summary

### Primary Metrics
- ✅ Service count: 140 → 130 (-7%)
- ✅ Vibecoding unified (3 → 1)
- ✅ AI Detection consolidated (4 → 2)
- ✅ MCP Analytics Dashboard MVP

### Phase 1 Metrics (Sprint 147-149)
- ✅ Service reduction: 164 → 130 (-21%)
- ✅ Endpoint reduction: -26 (-18%)
- ✅ Telemetry: 10 events, 3 funnels
- ✅ Progress: 90% (ahead of schedule)

### Business Metrics
- **Framework Realization**: 82% → 85% (measurable via telemetry)
- **Developer Experience**: Unified APIs reduce confusion
- **Maintainability**: -21% service overhead

---

## Retrospective Template (Post-Sprint)

*To be filled after Sprint 149 completion (Feb 22, 2026)*

### What Went Well
- TBD

### What Could Be Improved
- TBD

### Action Items for Sprint 150
- TBD

---

## References

- [ROADMAP-147-170.md](ROADMAP-147-170.md) - Overall roadmap
- [SPRINT-147-SPRING-CLEANING.md](SPRINT-147-SPRING-CLEANING.md) - Sprint 147 plan
- [SPRINT-148-SERVICE-CONSOLIDATION.md](SPRINT-148-SERVICE-CONSOLIDATION.md) - Sprint 148 plan
- [vibecoding-v2.md](../03-Migration-Guides/vibecoding-v2.md) - Vibecoding migration guide

---

**Sprint Owner**: CTO  
**Created**: February 3, 2026  
**Next Sprint Planning**: February 22, 2026 (Sprint 150)
