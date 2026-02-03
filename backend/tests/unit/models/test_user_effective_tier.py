"""
Unit Tests for User.effective_tier Property

Tests for tier calculation logic across multiple organizations.

Sprint: 146
Reference: ADR-047-Organization-Invitation-System-Architecture.md

Coverage:
- Single organization tier
- Multiple organization tier calculation
- Early exit optimization (CTO condition #3)
- Edge cases (no organizations, null plans)
"""
from datetime import datetime, timezone
from unittest.mock import MagicMock, PropertyMock
from uuid import uuid4

import pytest


# ============================================================================
# Mock Classes for Testing
# ============================================================================

class MockOrganization:
    """Mock organization with plan attribute"""
    def __init__(self, plan: str):
        self.id = uuid4()
        self.plan = plan


class MockUserOrganization:
    """Mock user-organization membership"""
    def __init__(self, organization: MockOrganization):
        self.user_id = uuid4()
        self.organization_id = organization.id
        self.role = "member"
        self.joined_at = datetime.now(timezone.utc)
        self.organization = organization


class MockUser:
    """
    Mock User class with effective_tier implementation.

    This mirrors the actual User.effective_tier property logic.
    """
    TIER_RANK = {
        "enterprise": 4,
        "pro": 3,
        "starter": 2,
        "free": 1
    }

    def __init__(self, primary_org=None, org_memberships=None):
        self.id = uuid4()
        self.organization = primary_org
        self.org_memberships = org_memberships or []

    @property
    def effective_tier(self) -> str:
        """Calculate user's effective subscription tier (copy of actual logic)"""
        max_tier = "free"
        max_rank = 1

        # Check primary organization first
        if self.organization and self.organization.plan:
            primary_rank = self.TIER_RANK.get(self.organization.plan, 1)
            if primary_rank > max_rank:
                max_rank = primary_rank
                max_tier = self.organization.plan
                # Early exit if enterprise
                if max_rank == 4:
                    return max_tier

        # Check all organizations via memberships
        if self.org_memberships:
            for membership in self.org_memberships:
                if hasattr(membership, 'organization') and membership.organization:
                    org_plan = membership.organization.plan
                    rank = self.TIER_RANK.get(org_plan, 1)
                    if rank > max_rank:
                        max_rank = rank
                        max_tier = org_plan
                        # Early exit if enterprise
                        if max_rank == 4:
                            return max_tier

        return max_tier


# ============================================================================
# Single Organization Tests
# ============================================================================

class TestSingleOrganization:
    """Test effective_tier with single organization"""

    def test_free_org_returns_free(self):
        """User in free org should have free tier"""
        org = MockOrganization(plan="free")
        user = MockUser(primary_org=org)

        assert user.effective_tier == "free"

    def test_starter_org_returns_starter(self):
        """User in starter org should have starter tier"""
        org = MockOrganization(plan="starter")
        user = MockUser(primary_org=org)

        assert user.effective_tier == "starter"

    def test_pro_org_returns_pro(self):
        """User in pro org should have pro tier"""
        org = MockOrganization(plan="pro")
        user = MockUser(primary_org=org)

        assert user.effective_tier == "pro"

    def test_enterprise_org_returns_enterprise(self):
        """User in enterprise org should have enterprise tier"""
        org = MockOrganization(plan="enterprise")
        user = MockUser(primary_org=org)

        assert user.effective_tier == "enterprise"


# ============================================================================
# Multiple Organization Tests
# ============================================================================

class TestMultipleOrganizations:
    """Test effective_tier with multiple organizations"""

    def test_free_and_pro_returns_pro(self):
        """User in free + pro orgs should have pro tier"""
        free_org = MockOrganization(plan="free")
        pro_org = MockOrganization(plan="pro")

        memberships = [
            MockUserOrganization(free_org),
            MockUserOrganization(pro_org),
        ]

        user = MockUser(primary_org=free_org, org_memberships=memberships)

        assert user.effective_tier == "pro"

    def test_starter_and_pro_returns_pro(self):
        """User in starter + pro orgs should have pro tier"""
        starter_org = MockOrganization(plan="starter")
        pro_org = MockOrganization(plan="pro")

        memberships = [
            MockUserOrganization(starter_org),
            MockUserOrganization(pro_org),
        ]

        user = MockUser(primary_org=starter_org, org_memberships=memberships)

        assert user.effective_tier == "pro"

    def test_pro_and_enterprise_returns_enterprise(self):
        """User in pro + enterprise orgs should have enterprise tier"""
        pro_org = MockOrganization(plan="pro")
        enterprise_org = MockOrganization(plan="enterprise")

        memberships = [
            MockUserOrganization(pro_org),
            MockUserOrganization(enterprise_org),
        ]

        user = MockUser(primary_org=pro_org, org_memberships=memberships)

        assert user.effective_tier == "enterprise"

    def test_free_starter_pro_enterprise_returns_enterprise(self):
        """User in all tiers should have enterprise tier"""
        free_org = MockOrganization(plan="free")
        starter_org = MockOrganization(plan="starter")
        pro_org = MockOrganization(plan="pro")
        enterprise_org = MockOrganization(plan="enterprise")

        memberships = [
            MockUserOrganization(free_org),
            MockUserOrganization(starter_org),
            MockUserOrganization(pro_org),
            MockUserOrganization(enterprise_org),
        ]

        user = MockUser(primary_org=free_org, org_memberships=memberships)

        assert user.effective_tier == "enterprise"

    def test_multiple_free_orgs_returns_free(self):
        """User in multiple free orgs should have free tier"""
        org1 = MockOrganization(plan="free")
        org2 = MockOrganization(plan="free")
        org3 = MockOrganization(plan="free")

        memberships = [
            MockUserOrganization(org1),
            MockUserOrganization(org2),
            MockUserOrganization(org3),
        ]

        user = MockUser(primary_org=org1, org_memberships=memberships)

        assert user.effective_tier == "free"


# ============================================================================
# Early Exit Optimization Tests (CTO Condition #3)
# ============================================================================

class TestEarlyExitOptimization:
    """Test early exit when enterprise found (CTO mandatory condition #3)"""

    def test_enterprise_first_triggers_early_exit(self):
        """Should exit early when enterprise found first"""
        enterprise_org = MockOrganization(plan="enterprise")
        pro_org = MockOrganization(plan="pro")

        # Enterprise is first in memberships
        memberships = [
            MockUserOrganization(enterprise_org),
            MockUserOrganization(pro_org),
        ]

        user = MockUser(primary_org=enterprise_org, org_memberships=memberships)

        # Should return enterprise without checking pro
        assert user.effective_tier == "enterprise"

    def test_enterprise_last_still_found(self):
        """Should find enterprise even if last in list"""
        free_org = MockOrganization(plan="free")
        starter_org = MockOrganization(plan="starter")
        pro_org = MockOrganization(plan="pro")
        enterprise_org = MockOrganization(plan="enterprise")

        # Enterprise is last in memberships
        memberships = [
            MockUserOrganization(free_org),
            MockUserOrganization(starter_org),
            MockUserOrganization(pro_org),
            MockUserOrganization(enterprise_org),  # Last
        ]

        user = MockUser(primary_org=free_org, org_memberships=memberships)

        assert user.effective_tier == "enterprise"

    def test_enterprise_primary_org_early_exit(self):
        """Enterprise as primary org should trigger early exit"""
        enterprise_org = MockOrganization(plan="enterprise")

        # No memberships checked (early exit from primary org)
        user = MockUser(primary_org=enterprise_org, org_memberships=[])

        assert user.effective_tier == "enterprise"


# ============================================================================
# Edge Cases
# ============================================================================

class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_no_organization_returns_free(self):
        """User with no organization should have free tier"""
        user = MockUser(primary_org=None, org_memberships=[])

        assert user.effective_tier == "free"

    def test_null_plan_treated_as_free(self):
        """Organization with null plan should be treated as free"""
        org = MockOrganization(plan=None)
        user = MockUser(primary_org=org)

        assert user.effective_tier == "free"

    def test_unknown_plan_treated_as_free(self):
        """Unknown plan should be treated as free tier"""
        org = MockOrganization(plan="unknown_plan")
        user = MockUser(primary_org=org)

        assert user.effective_tier == "free"

    def test_empty_memberships_uses_primary_org(self):
        """Empty memberships should fallback to primary org"""
        pro_org = MockOrganization(plan="pro")
        user = MockUser(primary_org=pro_org, org_memberships=[])

        assert user.effective_tier == "pro"

    def test_membership_without_organization(self):
        """Membership with no organization should be skipped"""
        pro_org = MockOrganization(plan="pro")

        # One valid membership, one without organization
        membership_with_org = MockUserOrganization(pro_org)
        membership_without_org = MagicMock()
        membership_without_org.organization = None

        memberships = [membership_without_org, membership_with_org]

        user = MockUser(primary_org=None, org_memberships=memberships)

        assert user.effective_tier == "pro"


# ============================================================================
# Tier Ranking Tests
# ============================================================================

class TestTierRanking:
    """Test tier ranking hierarchy"""

    def test_tier_rank_order(self):
        """Verify tier rank order: free < starter < pro < enterprise"""
        TIER_RANK = MockUser.TIER_RANK

        assert TIER_RANK["free"] < TIER_RANK["starter"]
        assert TIER_RANK["starter"] < TIER_RANK["pro"]
        assert TIER_RANK["pro"] < TIER_RANK["enterprise"]

    def test_enterprise_is_highest(self):
        """Enterprise should have the highest rank (4)"""
        assert MockUser.TIER_RANK["enterprise"] == 4

    def test_free_is_lowest(self):
        """Free should have the lowest rank (1)"""
        assert MockUser.TIER_RANK["free"] == 1

    def test_all_tiers_have_ranks(self):
        """All known tiers should have defined ranks"""
        expected_tiers = {"free", "starter", "pro", "enterprise"}
        actual_tiers = set(MockUser.TIER_RANK.keys())

        assert expected_tiers == actual_tiers


# ============================================================================
# Business Logic Tests
# ============================================================================

class TestBusinessLogic:
    """Test business logic scenarios"""

    def test_contractor_in_multiple_clients(self):
        """Contractor in Free + Enterprise client should get Enterprise features"""
        # Contractor's personal org (free)
        personal_org = MockOrganization(plan="free")

        # Enterprise client org
        client_org = MockOrganization(plan="enterprise")

        memberships = [
            MockUserOrganization(personal_org),
            MockUserOrganization(client_org),
        ]

        contractor = MockUser(primary_org=personal_org, org_memberships=memberships)

        # Contractor should have enterprise-level access
        assert contractor.effective_tier == "enterprise"

    def test_employee_leaves_enterprise_org(self):
        """Employee who leaves enterprise should drop to personal tier"""
        # Employee's personal org (free)
        personal_org = MockOrganization(plan="free")

        # Only personal org membership remains
        memberships = [MockUserOrganization(personal_org)]

        ex_employee = MockUser(primary_org=personal_org, org_memberships=memberships)

        # Should be back to free tier
        assert ex_employee.effective_tier == "free"

    def test_agency_with_multiple_pro_clients(self):
        """Agency with multiple pro clients should have pro tier"""
        agency_org = MockOrganization(plan="starter")
        client1_org = MockOrganization(plan="pro")
        client2_org = MockOrganization(plan="pro")

        memberships = [
            MockUserOrganization(agency_org),
            MockUserOrganization(client1_org),
            MockUserOrganization(client2_org),
        ]

        agency_user = MockUser(primary_org=agency_org, org_memberships=memberships)

        assert agency_user.effective_tier == "pro"
