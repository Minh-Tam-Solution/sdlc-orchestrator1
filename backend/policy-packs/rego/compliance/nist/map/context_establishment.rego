# =========================================================================
# NIST AI RMF - MAP-1.1 / MAP-1.2: AI System Context Establishment
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MAP
# Control: MAP-1.1, MAP-1.2
# Severity: High
#
# Rule: All AI systems must have non-empty purpose, non-empty scope,
# non-null owner, and non-empty stakeholders array.
# Each system must clearly establish its operational context including
# intended purpose, scope of deployment, responsible owner, and
# identified stakeholders with their roles and impact types.
#
# Input:
#   - ai_systems: [{name, purpose, scope, owner, stakeholders: [{role, name, impact_type}]}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "high"
#   - details: {total_systems, systems_with_context, incomplete_systems}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.map.context_establishment

import future.keywords.if
import future.keywords.in

# Default result when no AI systems are declared
default result := {
    "allowed": false,
    "reason": "No AI systems declared. At least one AI system must be documented with context.",
    "severity": "high",
    "details": {
        "total_systems": 0,
        "systems_with_context": 0,
        "incomplete_systems": []
    }
}

# Count total AI systems
total_systems := count(input.ai_systems)

# Collect systems that have complete context
systems_with_context := [s |
    s := input.ai_systems[_]
    _has_complete_context(s)
]

# Collect systems with incomplete context
incomplete_systems := [s.name |
    s := input.ai_systems[_]
    not _has_complete_context(s)
]

# Helper: check if system has a non-empty string field
_non_empty_string(val) if {
    val != null
    val != ""
}

# Helper: check if system has complete context
_has_complete_context(system) if {
    _non_empty_string(system.purpose)
    _non_empty_string(system.scope)
    system.owner != null
    system.owner != ""
    count(system.stakeholders) > 0
}

# Pass: all AI systems have complete context
result := {
    "allowed": true,
    "reason": "All AI systems have established context with purpose, scope, owner, and stakeholders",
    "severity": "high",
    "details": {
        "total_systems": total_systems,
        "systems_with_context": count(systems_with_context),
        "incomplete_systems": []
    }
} if {
    total_systems > 0
    count(incomplete_systems) == 0
}

# Fail: some AI systems lack complete context
result := {
    "allowed": false,
    "reason": sprintf("AI systems with incomplete context: %v", [concat(", ", incomplete_systems)]),
    "severity": "high",
    "details": {
        "total_systems": total_systems,
        "systems_with_context": count(systems_with_context),
        "incomplete_systems": incomplete_systems
    }
} if {
    total_systems > 0
    count(incomplete_systems) > 0
}
