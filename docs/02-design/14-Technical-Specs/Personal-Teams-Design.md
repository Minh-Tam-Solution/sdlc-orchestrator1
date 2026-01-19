# Personal Teams Feature Design

**Version**: 1.0.0
**Status**: DRAFT - Pending CTO Approval
**Date**: January 19, 2026
**Author**: AI Assistant (Claude)
**Sprint**: Sprint 79 Enhancement
**Reference**: GitHub Organization Model

---

## 1. Overview

### 1.1 Problem Statement

Current implementation requires `organization_id` when creating a Team, but:
- Frontend has no UI to create Organization
- Mock `organization_id` causes foreign key constraint errors
- Solo developers cannot create teams without first creating an organization

### 1.2 Proposed Solution

Implement **Personal Teams** feature similar to GitHub's model:
- Users can create **Personal Teams** without an organization
- Users can optionally create **Organizations** and add Teams to them
- Organizations have subscription tiers (free/starter/pro/enterprise) - all organizations are equal, just different features based on plan

### 1.3 Comparison with GitHub

| Feature | GitHub | SDLC Orchestrator |
|---------|--------|-------------------|
| Personal Repos/Teams | Yes | Yes (proposed) |
| Organization Repos/Teams | Yes | Yes (existing) |
| Enterprise as separate tier | Yes (paid to create) | **No** |
| Enterprise as subscription | N/A | Yes (plan = "enterprise") |
| Free tier | Yes | Yes |
| Pro/Paid tiers | Yes | Yes (starter, pro, enterprise) |

**Key Difference**: GitHub requires payment to create an "Enterprise" organization. SDLC Orchestrator uses subscription tiers (free/starter/pro/enterprise) for ALL organizations equally - no separate Enterprise creation process.

---

## 2. Architecture

### 2.1 Team Ownership Model

```
┌─────────────────────────────────────────────────────────────────┐
│                    Team Ownership Model                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Personal Team:                                                 │
│  ┌──────────────┐     ┌──────────────┐                        │
│  │    User      │────▶│    Team      │                        │
│  │  (owner_id)  │     │ org_id=NULL  │                        │
│  └──────────────┘     └──────────────┘                        │
│                                                                 │
│  Organization Team:                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐   │
│  │    User      │────▶│ Organization │────▶│    Team      │   │
│  │  (member)    │     │              │     │ org_id=UUID  │   │
│  └──────────────┘     └──────────────┘     └──────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 Team Types

| Type | organization_id | owner_id | Description |
|------|-----------------|----------|-------------|
| Personal Team | NULL | User UUID | Belongs to user directly |
| Organization Team | Org UUID | NULL | Belongs to organization |

### 2.3 Slug Uniqueness Rules

- **Personal Team**: Slug unique globally (no org scope)
- **Organization Team**: Slug unique within organization

---

## 3. Database Changes

### 3.1 Team Model Updates

```python
# backend/app/models/team.py

class Team(Base):
    __tablename__ = "teams"

    # Existing fields...

    # Modified: organization_id is now optional
    organization_id: Mapped[Optional[uuid4]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,  # Changed from False
        index=True,
        doc="Parent organization (null for personal teams)"
    )

    # New: owner_id for personal teams
    owner_id: Mapped[Optional[uuid4]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        doc="Owner user ID (for personal teams)"
    )
```

### 3.2 Migration Script

```sql
-- Migration: Add owner_id column to teams table

-- Add owner_id column
ALTER TABLE teams
ADD COLUMN owner_id UUID REFERENCES users(id) ON DELETE CASCADE;

-- Make organization_id nullable
ALTER TABLE teams
ALTER COLUMN organization_id DROP NOT NULL;

-- Add index for owner_id
CREATE INDEX idx_teams_owner_id ON teams(owner_id);

-- Constraint: Either organization_id OR owner_id must be set (not both, not neither)
ALTER TABLE teams
ADD CONSTRAINT teams_ownership_check
CHECK (
    (organization_id IS NOT NULL AND owner_id IS NULL) OR
    (organization_id IS NULL AND owner_id IS NOT NULL)
);

-- Update unique constraint for slug
-- Personal teams: slug unique globally where organization_id IS NULL
-- Org teams: slug unique per organization
DROP CONSTRAINT IF EXISTS teams_org_slug_unique;

-- For organization teams: unique per org
CREATE UNIQUE INDEX teams_org_slug_unique
ON teams(organization_id, slug)
WHERE organization_id IS NOT NULL;

-- For personal teams: unique per owner
CREATE UNIQUE INDEX teams_personal_slug_unique
ON teams(owner_id, slug)
WHERE owner_id IS NOT NULL;
```

---

## 4. API Changes

### 4.1 Schema Updates

```python
# backend/app/schemas/team.py

class TeamCreate(BaseModel):
    """Schema for creating a new team.

    For Personal Teams: omit organization_id
    For Organization Teams: provide organization_id
    """
    organization_id: Optional[UUID] = Field(
        None,
        description="Parent organization UUID (omit for personal team)"
    )
    name: str = Field(...)
    slug: str = Field(...)
    description: Optional[str] = Field(None)
    settings: Optional[TeamSettings] = Field(default_factory=TeamSettings)


class TeamResponse(BaseModel):
    """Schema for team response."""
    id: UUID
    organization_id: Optional[UUID] = Field(
        None,
        description="Parent organization UUID (null for personal teams)"
    )
    owner_id: Optional[UUID] = Field(
        None,
        description="Owner user ID (null for organization teams)"
    )
    is_personal: bool = Field(
        ...,
        description="True if personal team, false if organization team"
    )
    # ... other fields
```

### 4.2 API Behavior Changes

| Endpoint | Current | Proposed |
|----------|---------|----------|
| POST /teams | Requires organization_id | organization_id optional |
| GET /teams | Filter by org membership | Include personal teams + org teams |
| DELETE /teams | Requires org owner role | Personal team: user must be owner |

### 4.3 Create Team Logic

```python
async def create_team(data: TeamCreate, user_id: UUID) -> Team:
    if data.organization_id:
        # Organization team - existing logic
        # Verify user is member of organization
        # Slug unique within organization
        team = Team(
            organization_id=data.organization_id,
            owner_id=None,
            ...
        )
    else:
        # Personal team - new logic
        # Slug unique per user's personal teams
        team = Team(
            organization_id=None,
            owner_id=user_id,
            ...
        )

    # Add creator as owner member
    member = TeamMember(
        team_id=team.id,
        user_id=user_id,
        role="owner"
    )

    return team
```

---

## 5. Frontend Changes

### 5.1 CreateTeamDialog Updates

```typescript
// frontend/web/src/components/teams/CreateTeamDialog.tsx

interface CreateTeamData {
  name: string;
  slug: string;
  description?: string;
  organization_id?: string;  // Optional now
}

export default function CreateTeamDialog({ ... }) {
  // Form state
  const [teamType, setTeamType] = useState<'personal' | 'organization'>('personal');
  const [selectedOrg, setSelectedOrg] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const data: CreateTeamData = {
      name,
      slug,
      description: description || undefined,
    };

    // Only include organization_id if creating org team
    if (teamType === 'organization' && selectedOrg) {
      data.organization_id = selectedOrg;
    }

    await createTeam.mutateAsync(data);
    onOpenChange(false);
  };

  return (
    <Dialog>
      {/* Team Type Selection */}
      <RadioGroup value={teamType} onValueChange={setTeamType}>
        <RadioGroupItem value="personal" label="Personal Team" />
        <RadioGroupItem value="organization" label="Organization Team" />
      </RadioGroup>

      {/* Organization Selector (only for org teams) */}
      {teamType === 'organization' && (
        <OrganizationSelector
          value={selectedOrg}
          onChange={setSelectedOrg}
        />
      )}

      {/* Name, Slug, Description fields */}
      ...
    </Dialog>
  );
}
```

### 5.2 Slug Validation

```typescript
// Add client-side validation for slug
const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

const validateSlug = (value: string): string | null => {
  if (!value) return "Slug is required";
  if (value.length < 2) return "Slug must be at least 2 characters";
  if (value.length > 100) return "Slug must be at most 100 characters";
  if (!slugPattern.test(value)) {
    return "Slug can only contain lowercase letters, numbers, and hyphens";
  }
  return null;
};
```

---

## 6. Business Rules

### 6.1 Ownership Rules

| Action | Personal Team | Organization Team |
|--------|---------------|-------------------|
| Create | Any authenticated user | Organization members |
| View | Team members | Team members |
| Update | Team owner/admin | Team owner/admin |
| Delete | Team owner | Team owner |
| Add members | Team owner/admin | Team owner/admin |

### 6.2 Permission Matrix

```yaml
Personal Team Permissions:
  owner: Full access (CRUD + members)
  admin: Update team + manage members
  member: Read access + project work

Organization Team Permissions:
  org_admin: Can create/delete teams in org
  team_owner: Full access to team
  team_admin: Update team + manage members
  team_member: Read access + project work
```

---

## 7. Migration Strategy

### 7.1 Phase 1: Schema Updates (Sprint 79)
1. Add `owner_id` column to teams table
2. Make `organization_id` nullable
3. Add constraints and indexes
4. Update Pydantic schemas

### 7.2 Phase 2: Service Updates (Sprint 79)
1. Update TeamsService to handle both team types
2. Update permission checks
3. Update slug uniqueness validation

### 7.3 Phase 3: Frontend Updates (Sprint 79)
1. Update CreateTeamDialog
2. Add team type selection
3. Update Teams list to show personal vs org teams
4. Add slug validation with proper error messages

### 7.4 Data Migration
- Existing teams: Keep as organization teams (no change needed)
- No backward compatibility issues

---

## 8. Testing Strategy

### 8.1 Unit Tests

```python
# Tests for personal teams
def test_create_personal_team():
    """User can create team without organization."""

def test_personal_team_slug_unique_per_user():
    """Slug unique among user's personal teams."""

def test_personal_team_owner_permissions():
    """Only owner can delete personal team."""
```

### 8.2 Integration Tests

```python
def test_create_personal_team_api():
    """POST /teams without organization_id creates personal team."""

def test_list_teams_includes_personal():
    """GET /teams returns user's personal teams."""
```

### 8.3 E2E Tests

```typescript
test('User can create personal team', async () => {
  // Open create team dialog
  // Select "Personal Team"
  // Fill name and slug
  // Submit
  // Verify team created
});
```

---

## 9. Success Criteria

| Metric | Target |
|--------|--------|
| Personal team creation | Works without organization |
| Slug validation | Shows clear error for invalid input |
| Error handling | Toast shows API errors |
| No regressions | Existing org teams still work |

---

## 10. Approval

- [ ] **CTO Approval**: Design review and approval
- [ ] **Backend Lead**: Schema and API changes
- [ ] **Frontend Lead**: UI/UX changes

---

## Appendix A: Error Messages

```yaml
Validation Errors:
  INVALID_SLUG: "Slug can only contain lowercase letters, numbers, and hyphens"
  SLUG_TOO_SHORT: "Slug must be at least 2 characters"
  SLUG_TOO_LONG: "Slug must be at most 100 characters"
  SLUG_EXISTS_PERSONAL: "You already have a team with this slug"
  SLUG_EXISTS_ORG: "A team with this slug already exists in the organization"

Permission Errors:
  NOT_TEAM_MEMBER: "You are not a member of this team"
  NOT_TEAM_OWNER: "Only team owner can perform this action"
  NOT_ORG_MEMBER: "You are not a member of this organization"
```

---

**Document Status**: DRAFT
**Next Step**: CTO Review
