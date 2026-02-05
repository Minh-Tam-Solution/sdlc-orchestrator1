# =========================================================================
# NIST AI RMF - MANAGE-1.1: Risk Response Planning
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MANAGE
# Control: MANAGE-1.1
# Severity: Critical
#
# Rule: Every open risk must have at least one response plan with an
# assigned owner and a due date. Unplanned risks indicate governance
# gaps that could lead to unmitigated AI system failures.
#
# Input:
#   - risks: [{id, title, status}]
#   - risk_responses: [{risk_id, assigned_to, due_date, response_type, status}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "critical"
#   - details: {total_risks, risks_with_response, unresponded_risks}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.manage.risk_response_planning

import future.keywords.if
import future.keywords.in

# Default result when no risks are declared
default result := {
    "allowed": false,
    "reason": "No risks declared. At least one risk must be documented.",
    "severity": "critical",
    "details": {
        "total_risks": 0,
        "risks_with_response": 0,
        "unresponded_risks": []
    }
}

# Count total open risks
open_risks := [r |
    r := input.risks[_]
    r.status == "open"
]

total_risks := count(open_risks)

# Collect risk IDs that have at least one valid response
_risk_has_valid_response(risk_id) if {
    resp := input.risk_responses[_]
    resp.risk_id == risk_id
    resp.assigned_to != null
    resp.assigned_to != ""
    resp.due_date != null
}

# Collect open risks with valid responses
risks_with_response := [r |
    r := open_risks[_]
    _risk_has_valid_response(r.id)
]

# Collect open risks without valid responses
unresponded_risks := [r.title |
    r := open_risks[_]
    not _risk_has_valid_response(r.id)
]

# Pass: all open risks have response plans
result := {
    "allowed": true,
    "reason": "All open risks have response plans with assigned owners and due dates",
    "severity": "critical",
    "details": {
        "total_risks": total_risks,
        "risks_with_response": count(risks_with_response),
        "unresponded_risks": []
    }
} if {
    total_risks > 0
    count(unresponded_risks) == 0
}

# Fail: some open risks lack response plans
result := {
    "allowed": false,
    "reason": sprintf("Open risks without response plans: %v", [concat(", ", unresponded_risks)]),
    "severity": "critical",
    "details": {
        "total_risks": total_risks,
        "risks_with_response": count(risks_with_response),
        "unresponded_risks": unresponded_risks
    }
} if {
    total_risks > 0
    count(unresponded_risks) > 0
}
