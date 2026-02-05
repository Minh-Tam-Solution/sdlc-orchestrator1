# =========================================================================
# NIST AI RMF - MAP-2.1: AI System Categorization
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MAP
# Control: MAP-2.1
# Severity: Critical
#
# Rule: All AI systems must have valid categorization with risk_tier
# in [minimal, limited, high, unacceptable]. Each system must be
# classified according to its risk profile including data sensitivity,
# autonomy level, and reversibility characteristics.
#
# Input:
#   - ai_systems: [{name, categorization: {risk_tier, data_sensitivity, autonomy_level, reversibility}}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "critical"
#   - details: {total_systems, categorized_systems, uncategorized_systems}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.map.system_categorization

import future.keywords.if
import future.keywords.in

# Valid risk tiers per NIST AI RMF categorization
valid_risk_tiers := {"minimal", "limited", "high", "unacceptable"}

# Default result when no AI systems are declared
default result := {
    "allowed": false,
    "reason": "No AI systems declared. At least one AI system must be categorized.",
    "severity": "critical",
    "details": {
        "total_systems": 0,
        "categorized_systems": 0,
        "uncategorized_systems": []
    }
}

# Count total AI systems
total_systems := count(input.ai_systems)

# Collect systems that have valid categorization
categorized_systems := [s |
    s := input.ai_systems[_]
    _has_valid_categorization(s)
]

# Collect systems without valid categorization
uncategorized_systems := [s.name |
    s := input.ai_systems[_]
    not _has_valid_categorization(s)
]

# Helper: check if system has valid categorization with recognized risk tier
_has_valid_categorization(system) if {
    system.categorization != null
    system.categorization.risk_tier in valid_risk_tiers
}

# Pass: all AI systems have valid categorization
result := {
    "allowed": true,
    "reason": "All AI systems have valid risk categorization",
    "severity": "critical",
    "details": {
        "total_systems": total_systems,
        "categorized_systems": count(categorized_systems),
        "uncategorized_systems": []
    }
} if {
    total_systems > 0
    count(uncategorized_systems) == 0
}

# Fail: some AI systems lack valid categorization
result := {
    "allowed": false,
    "reason": sprintf("AI systems without valid categorization: %v", [concat(", ", uncategorized_systems)]),
    "severity": "critical",
    "details": {
        "total_systems": total_systems,
        "categorized_systems": count(categorized_systems),
        "uncategorized_systems": uncategorized_systems
    }
} if {
    total_systems > 0
    count(uncategorized_systems) > 0
}
