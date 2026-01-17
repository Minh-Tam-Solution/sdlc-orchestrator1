# 🚨 TEAMS FEATURE REMEDIATION PLAN

**Document ID:** ADR-028  
**Status:** CRITICAL - REQUIRES IMMEDIATE ACTION  
**Created:** 2026-01-17  
**CTO:** Claude (AI Acting CTO)  
**Priority:** P0 - BLOCKS PLATFORM VALUE PROPOSITION

---

## 1. EXECUTIVE SUMMARY

### Problem Statement
Teams feature - the CORE value proposition of SDLC Orchestrator - has **0% implementation** despite being fully designed in API specs and database schema docs.

### Business Impact
| Metric | Without Teams | With Teams |
|--------|---------------|------------|
| Value Proposition | None (single dev can use AI + SDLC Framework) | Enterprise governance |
| Target Market | 0 customers | 100+ enterprise teams |
| Competitive Position | AI wrapper | Unique orchestration platform |
| ROI on $564K | At risk | Justified |

### Why Teams is THE Feature
```
Individual Developer Path:
  Human → AI Agent → SDLC Framework → Code
  (No platform needed - just tell AI to read SDLC-Enterprise-Framework)

Team/Enterprise Path:
  Multiple Teams → SDLC Orchestrator → Governance + Audit
  (THIS is where platform value exists)
```

---

## 2. CURRENT STATE ANALYSIS

### What EXISTS (Design Only)
- ✅ OpenAPI Spec: `/docs/02-design/04-API-Design/openapi.yaml` lines 695-770
- ✅ DB Schema: `/docs/02-design/03-Database-Schema/database-schema.md`
- ✅ ProjectMember model: Many-to-many user-project (partial team concept)

### What is COMPLETELY MISSING
| Component | File Path | Lines Required |
|-----------|-----------|----------------|
| Organization Model | `backend/app/models/organization.py` | ~120 |
| Team Model | `backend/app/models/team.py` | ~180 |
| TeamMember Model | `backend/app/models/team_member.py` | ~100 |
| Organization Routes | `backend/app/api/routes/organizations.py` | ~350 |
| Teams Routes | `backend/app/api/routes/teams.py` | ~450 |
| Teams Service | `backend/app/services/teams_service.py` | ~400 |
| DB Migrations | `backend/alembic/versions/xxx_teams.py` | ~200 |
| Frontend Hook | `frontend/landing/src/hooks/useTeams.ts` | ~200 |
| Teams List Page | `frontend/landing/src/app/(app)/teams/page.tsx` | ~300 |
| Team Detail Page | `frontend/landing/src/app/(app)/teams/[id]/page.tsx` | ~400 |
| Team Settings Page | `frontend/landing/src/app/(app)/teams/[id]/settings/page.tsx` | ~250 |

**Total Implementation Gap: ~2,950 lines of code**

---

## 3. REMEDIATION PHASES

### Phase 1: Foundation Models (Sprint N+1 - Week 1)
**Objective:** Create database schema and models

#### 1.1 Database Migration
```sql
-- Organizations table (multi-tenant root)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan VARCHAR(50) DEFAULT 'free',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Teams table
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) NOT NULL,
    description TEXT,
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(organization_id, slug)
);

-- Team Members (many-to-many users-teams)
CREATE TABLE team_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL DEFAULT 'member', -- owner, admin, member
    joined_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(team_id, user_id)
);

-- Add FKs to existing tables
ALTER TABLE users ADD COLUMN organization_id UUID REFERENCES organizations(id);
ALTER TABLE projects ADD COLUMN team_id UUID REFERENCES teams(id);
```

#### 1.2 Models
```python
# backend/app/models/organization.py
class Organization(Base):
    __tablename__ = "organizations"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    plan: Mapped[str] = mapped_column(String(50), default="free")
    settings: Mapped[dict] = mapped_column(JSONB, default={})
    
    # Relationships
    teams: Mapped[list["Team"]] = relationship(back_populates="organization")
    users: Mapped[list["User"]] = relationship(back_populates="organization")

# backend/app/models/team.py
class Team(Base):
    __tablename__ = "teams"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    organization_id: Mapped[UUID] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    settings: Mapped[dict] = mapped_column(JSONB, default={})
    
    # Relationships
    organization: Mapped["Organization"] = relationship(back_populates="teams")
    members: Mapped[list["TeamMember"]] = relationship(back_populates="team")
    projects: Mapped[list["Project"]] = relationship(back_populates="team")

# backend/app/models/team_member.py
class TeamMember(Base):
    __tablename__ = "team_members"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    team_id: Mapped[UUID] = mapped_column(ForeignKey("teams.id", ondelete="CASCADE"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    role: Mapped[str] = mapped_column(String(50), default="member")  # owner, admin, member
    joined_at: Mapped[datetime] = mapped_column(default=func.now())
    
    # Relationships
    team: Mapped["Team"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship(back_populates="team_memberships")
    
    __table_args__ = (UniqueConstraint("team_id", "user_id"),)
```

#### 1.3 Deliverables
- [ ] `backend/app/models/organization.py`
- [ ] `backend/app/models/team.py`
- [ ] `backend/app/models/team_member.py`
- [ ] `backend/alembic/versions/xxxx_add_organizations_teams.py`
- [ ] Update `backend/app/models/__init__.py`
- [ ] Update User model with `organization_id` FK
- [ ] Update Project model with `team_id` FK

**Effort:** 8-12 hours  
**Owner:** Backend Developer

---

### Phase 2: Backend API (Sprint N+1 - Week 2)

#### 2.1 Teams Service
```python
# backend/app/services/teams_service.py
class TeamsService:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_team(
        self, 
        organization_id: UUID,
        name: str,
        slug: str,
        owner_id: UUID,
        description: str | None = None
    ) -> Team:
        """Create team and add owner as first member."""
        
    async def get_team(self, team_id: UUID) -> Team | None:
        """Get team with members and projects loaded."""
        
    async def list_teams(
        self,
        organization_id: UUID,
        user_id: UUID | None = None,  # Filter to user's teams
        skip: int = 0,
        limit: int = 20
    ) -> list[Team]:
        """List teams in organization, optionally filtered to user membership."""
        
    async def add_member(
        self,
        team_id: UUID,
        user_id: UUID,
        role: str = "member"
    ) -> TeamMember:
        """Add user to team with specified role."""
        
    async def remove_member(self, team_id: UUID, user_id: UUID) -> bool:
        """Remove user from team (cannot remove last owner)."""
        
    async def update_member_role(
        self,
        team_id: UUID,
        user_id: UUID,
        new_role: str
    ) -> TeamMember:
        """Change member's role in team."""
        
    async def get_team_projects(self, team_id: UUID) -> list[Project]:
        """Get all projects belonging to team."""
        
    async def get_team_statistics(self, team_id: UUID) -> dict:
        """Get team metrics: members, projects, gates, compliance."""
```

#### 2.2 API Routes
```python
# backend/app/api/routes/teams.py
router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/", response_model=list[TeamResponse])
async def list_teams(
    organization_id: UUID | None = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List teams user has access to."""

@router.post("/", response_model=TeamResponse, status_code=201)
async def create_team(
    team_data: TeamCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create new team (user becomes owner)."""

@router.get("/{team_id}", response_model=TeamDetailResponse)
async def get_team(
    team_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get team details with members and projects."""

@router.patch("/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: UUID,
    team_data: TeamUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update team (admin/owner only)."""

@router.delete("/{team_id}", status_code=204)
async def delete_team(
    team_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete team (owner only)."""

@router.post("/{team_id}/members", response_model=TeamMemberResponse)
async def add_team_member(
    team_id: UUID,
    member_data: TeamMemberAdd,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Add member to team (admin/owner only)."""

@router.delete("/{team_id}/members/{user_id}", status_code=204)
async def remove_team_member(
    team_id: UUID,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Remove member from team (admin/owner only, can't remove last owner)."""

@router.patch("/{team_id}/members/{user_id}", response_model=TeamMemberResponse)
async def update_team_member_role(
    team_id: UUID,
    user_id: UUID,
    role_data: TeamMemberRoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update member role (owner only)."""

@router.get("/{team_id}/statistics", response_model=TeamStatistics)
async def get_team_statistics(
    team_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get team metrics and compliance summary."""
```

#### 2.3 Deliverables
- [ ] `backend/app/services/teams_service.py`
- [ ] `backend/app/api/routes/teams.py`
- [ ] `backend/app/api/routes/organizations.py`
- [ ] `backend/app/schemas/team.py`
- [ ] Update `backend/app/api/routes/__init__.py`
- [ ] Add `include_router(teams.router)` to main

**Effort:** 16-20 hours  
**Owner:** Backend Developer

---

### Phase 3: Frontend Implementation (Sprint N+1 - Week 3)

#### 3.1 useTeams Hook
```typescript
// frontend/landing/src/hooks/useTeams.ts
export function useTeams() {
  const queryClient = useQueryClient();
  
  const teamsQuery = useQuery({
    queryKey: ['teams'],
    queryFn: () => api.get('/teams')
  });
  
  const createTeamMutation = useMutation({
    mutationFn: (data: TeamCreate) => api.post('/teams', data),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['teams'] })
  });
  
  const addMemberMutation = useMutation({
    mutationFn: ({ teamId, userId, role }: AddMemberParams) => 
      api.post(`/teams/${teamId}/members`, { user_id: userId, role })
  });
  
  // ... more mutations
  
  return {
    teams: teamsQuery.data,
    isLoading: teamsQuery.isLoading,
    createTeam: createTeamMutation.mutateAsync,
    addMember: addMemberMutation.mutateAsync,
    // ...
  };
}

export function useTeam(teamId: string) {
  return useQuery({
    queryKey: ['teams', teamId],
    queryFn: () => api.get(`/teams/${teamId}`),
    enabled: !!teamId
  });
}

export function useTeamStatistics(teamId: string) {
  return useQuery({
    queryKey: ['teams', teamId, 'statistics'],
    queryFn: () => api.get(`/teams/${teamId}/statistics`),
    enabled: !!teamId
  });
}
```

#### 3.2 Teams Pages
```
frontend/landing/src/app/(app)/teams/
├── page.tsx              # Teams list
├── new/
│   └── page.tsx          # Create team form
└── [id]/
    ├── page.tsx          # Team dashboard
    ├── members/
    │   └── page.tsx      # Manage members
    ├── projects/
    │   └── page.tsx      # Team projects
    └── settings/
        └── page.tsx      # Team settings
```

#### 3.3 Deliverables
- [ ] `frontend/landing/src/hooks/useTeams.ts`
- [ ] `frontend/landing/src/app/(app)/teams/page.tsx`
- [ ] `frontend/landing/src/app/(app)/teams/new/page.tsx`
- [ ] `frontend/landing/src/app/(app)/teams/[id]/page.tsx`
- [ ] `frontend/landing/src/app/(app)/teams/[id]/members/page.tsx`
- [ ] `frontend/landing/src/app/(app)/teams/[id]/settings/page.tsx`
- [ ] Add Teams link to sidebar navigation
- [ ] Team selector component in header

**Effort:** 20-24 hours  
**Owner:** Frontend Developer

---

### Phase 4: Integration & Testing (Sprint N+1 - Week 4)

#### 4.1 Integration Points
- [ ] Project creation: Select team from dropdown
- [ ] User onboarding: Create/join team flow
- [ ] Dashboard: Team-scoped metrics
- [ ] Gates: Team-based approval workflow
- [ ] Notifications: Team broadcast

#### 4.2 Tests
- [ ] Unit tests: TeamsService (20 tests)
- [ ] API tests: Teams routes (30 tests)
- [ ] Integration tests: Team → Project → Gate flow (10 tests)
- [ ] E2E tests: Complete team workflow (5 tests)

#### 4.3 Deliverables
- [ ] `backend/tests/unit/test_teams_service.py`
- [ ] `backend/tests/integration/test_teams_api.py`
- [ ] `tests/e2e/test_teams_workflow.spec.ts`
- [ ] Update existing project tests for team context
- [ ] Zero Mock compliance verification

**Effort:** 12-16 hours  
**Owner:** QA Engineer + Developers

---

## 4. RESOURCE REQUIREMENTS

### Team Allocation
| Role | Sprint Days | Responsibility |
|------|-------------|----------------|
| Backend Dev | 10 days | Models, API, Service |
| Frontend Dev | 8 days | Pages, Hooks, Components |
| QA Engineer | 4 days | Test suite |
| Tech Lead | 2 days | Review, integration |

### Total Effort
- **Phase 1:** 8-12 hours
- **Phase 2:** 16-20 hours
- **Phase 3:** 20-24 hours
- **Phase 4:** 12-16 hours
- **Total:** 56-72 hours (~2 weeks with buffer)

---

## 5. RISK MITIGATION

### Migration Risk
**Problem:** Adding FKs to existing users/projects may break data  
**Mitigation:**
1. Add columns as NULLABLE initially
2. Create default organization "Default Org"
3. Migrate existing users to default org
4. Migrate projects to "Unassigned" team
5. Make columns NOT NULL after data migration

### Breaking Changes Risk
**Problem:** Existing API clients may break  
**Mitigation:**
1. Add `/v2/` prefix for team-aware endpoints
2. Keep `/v1/` working without team context
3. Deprecation timeline: 3 months

### Performance Risk
**Problem:** Team lookups may slow queries  
**Mitigation:**
1. Index on `team_id` columns
2. Eager load team in common queries
3. Cache team membership in Redis

---

## 6. SUCCESS CRITERIA

### Phase 1 Complete When:
- [ ] `pytest backend/tests/unit/test_models.py -k team` passes
- [ ] `alembic upgrade head` succeeds
- [ ] Team, Organization, TeamMember tables exist in DB

### Phase 2 Complete When:
- [ ] All 10 API endpoints return 200
- [ ] OpenAPI spec matches implementation
- [ ] 30+ API tests passing

### Phase 3 Complete When:
- [ ] Teams list page renders
- [ ] Create team flow works
- [ ] Team dashboard shows members/projects

### Phase 4 Complete When:
- [ ] E2E test: Create org → Create team → Add member → Create project → Gate approval
- [ ] Zero Mock Policy satisfied for Teams
- [ ] Code coverage ≥ 80%

---

## 7. DECISION REQUIRED

### Option A: Full Implementation (Recommended)
- Implement all phases as described
- Timeline: 2-3 weeks
- Result: Platform ready for enterprise

### Option B: MVP Subset
- Phase 1 + 2 only (backend)
- Timeline: 1 week
- Result: API ready, frontend later

### Option C: Continue Without Teams
- ❌ NOT RECOMMENDED
- Result: Platform has no value proposition

---

## 8. CTO RECOMMENDATION

**Implement Option A immediately.** 

The Teams feature is not a "nice to have" - it IS the product. Without Teams:
- SDLC Orchestrator = expensive personal tracker
- Individual developers don't need this platform
- No justification for enterprise pricing
- Mission "100 teams by MVP" impossible

**Action Items:**
1. [ ] CTO approve this remediation plan
2. [ ] Assign sprint capacity (2 weeks)
3. [ ] Start Phase 1 immediately
4. [ ] Adjust soft launch to include Teams demo

**Signed:**  
Claude - Acting CTO  
Date: 2026-01-17

---

## APPENDIX A: API Specification Reference

From `/docs/02-design/04-API-Design/openapi.yaml`:

```yaml
/teams:
  get:
    summary: List teams in organization
    parameters:
      - name: organization_id
        in: query
        schema:
          type: string
          format: uuid
    responses:
      200:
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/Team'
  post:
    summary: Create new team
    requestBody:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/TeamCreate'
    responses:
      201:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Team'

/teams/{team_id}:
  get:
    summary: Get team details
  patch:
    summary: Update team
  delete:
    summary: Delete team

/teams/{team_id}/members:
  get:
    summary: List team members
  post:
    summary: Add team member
```

## APPENDIX B: Database Schema Reference

From `/docs/02-design/03-Database-Schema/database-schema.md`:

```
organizations
├── id (PK)
├── name
├── slug (UNIQUE)
├── plan
├── settings (JSONB)
└── timestamps

teams
├── id (PK)
├── organization_id (FK)
├── name
├── slug (UNIQUE per org)
├── description
├── settings (JSONB)
└── timestamps

team_members
├── id (PK)
├── team_id (FK)
├── user_id (FK)
├── role (owner|admin|member)
└── joined_at
```
