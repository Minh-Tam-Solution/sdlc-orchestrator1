# =========================================================================
# NIST AI RMF - MANAGE-2.1: Resource Allocation for Risk Responses
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MANAGE
# Control: MANAGE-2.1
# Severity: High
#
# Rule: At least 50% of actionable risk responses (excluding "accept"
# response type) must have resource allocation with budget > 0.
# Accepted risks are excluded because they require no active spending.
#
# Input:
#   - risk_responses: [{id, response_type, resources_allocated: [{type, description, budget}]}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "high"
#   - details: {total_actionable, with_budget, percentage}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.manage.resource_allocation

import future.keywords.if
import future.keywords.in

# Default result when no actionable responses exist
default result := {
    "allowed": false,
    "reason": "No actionable risk responses found. At least one non-accept response must exist.",
    "severity": "high",
    "details": {
        "total_actionable": 0,
        "with_budget": 0,
        "percentage": 0
    }
}

# Collect actionable responses (exclude "accept" response type per CTO condition)
actionable_responses := [r |
    r := input.risk_responses[_]
    r.response_type != "accept"
]

total_actionable := count(actionable_responses)

# Helper: check if a response has at least one resource with budget > 0
_has_budget(response) if {
    res := response.resources_allocated[_]
    res.budget > 0
}

# Collect actionable responses with budget allocation
with_budget := [r |
    r := actionable_responses[_]
    _has_budget(r)
]

# Collect actionable responses without budget allocation
under_resourced := [r.id |
    r := actionable_responses[_]
    not _has_budget(r)
]

# Calculate percentage of responses with budget
_percentage := round((count(with_budget) / total_actionable) * 100) if {
    total_actionable > 0
}

# Pass: >= 50% of actionable responses have budget allocation
result := {
    "allowed": true,
    "reason": sprintf("%v%% of actionable risk responses have budget allocation (threshold: 50%%)", [_percentage]),
    "severity": "high",
    "details": {
        "total_actionable": total_actionable,
        "with_budget": count(with_budget),
        "percentage": _percentage
    }
} if {
    total_actionable > 0
    _percentage >= 50
}

# Fail: < 50% of actionable responses have budget allocation
result := {
    "allowed": false,
    "reason": sprintf("Only %v%% of actionable risk responses have budget allocation (threshold: 50%%). Under-resourced: %v", [_percentage, concat(", ", under_resourced)]),
    "severity": "high",
    "details": {
        "total_actionable": total_actionable,
        "with_budget": count(with_budget),
        "percentage": _percentage
    }
} if {
    total_actionable > 0
    _percentage < 50
}
