# =========================================================================
# NIST AI RMF - GOVERN-1.1: AI System Accountability Structure
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: GOVERN
# Control: GOVERN-1.1
# Severity: Critical
#
# Rule: All AI systems must have designated owners.
# Each AI system must be assigned to a specific team member responsible
# for governance, monitoring, and risk management.
#
# Input:
#   - ai_systems: [{name, owner, type}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "critical"
#   - details: {total_systems, systems_with_owner, unowned_systems}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.govern.accountability

import future.keywords.if
import future.keywords.in

# Default result when no AI systems are declared
default result := {
    "allowed": false,
    "reason": "No AI systems declared. At least one AI system must be documented.",
    "severity": "critical",
    "details": {
        "total_systems": 0,
        "systems_with_owner": 0,
        "unowned_systems": []
    }
}

# Count total AI systems
total_systems := count(input.ai_systems)

# Collect systems that have an owner
systems_with_owner := [s |
    s := input.ai_systems[_]
    s.owner != null
    s.owner != ""
]

# Collect systems without an owner
unowned_systems := [s.name |
    s := input.ai_systems[_]
    not _has_owner(s)
]

# Helper: check if system has a valid owner
_has_owner(system) if {
    system.owner != null
    system.owner != ""
}

# Pass: all AI systems have designated owners
result := {
    "allowed": true,
    "reason": "All AI systems have designated owners",
    "severity": "critical",
    "details": {
        "total_systems": total_systems,
        "systems_with_owner": count(systems_with_owner),
        "unowned_systems": []
    }
} if {
    total_systems > 0
    count(unowned_systems) == 0
}

# Fail: some AI systems lack owners
result := {
    "allowed": false,
    "reason": sprintf("AI systems without owners: %v", [concat(", ", unowned_systems)]),
    "severity": "critical",
    "details": {
        "total_systems": total_systems,
        "systems_with_owner": count(systems_with_owner),
        "unowned_systems": unowned_systems
    }
} if {
    total_systems > 0
    count(unowned_systems) > 0
}
