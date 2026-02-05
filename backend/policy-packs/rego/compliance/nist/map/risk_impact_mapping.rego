# =========================================================================
# NIST AI RMF - MAP-3.1/3.2: Risk & Impact Mapping + Dependencies
# SDLC Orchestrator - Sprint 157 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MAP
# Controls: MAP-3.1, MAP-3.2
# Severity: High
#
# Rule: All risks must have >=1 impact_areas and >=1 affected_stakeholders.
#       All AI systems must have >=1 dependency documented.
#
# Input:
#   - risks: [{title, impact_areas: [...], affected_stakeholders: [...]}]
#   - ai_systems: [{name, dependencies: [...]}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "high"
#   - details: {total_risks, mapped_risks, unmapped_risks, systems_without_deps}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.map.risk_impact_mapping

import future.keywords.if
import future.keywords.in

# Default result when no risks are declared
default result := {
    "allowed": false,
    "reason": "No risks declared. At least one risk must be documented for MAP-3.1.",
    "severity": "high",
    "details": {
        "total_risks": 0,
        "mapped_risks": 0,
        "unmapped_risks": [],
        "systems_without_deps": []
    }
}

# Count total risks
total_risks := count(input.risks)

# Collect risks that have both impact_areas and affected_stakeholders
mapped_risks := [r |
    r := input.risks[_]
    count(r.impact_areas) > 0
    count(r.affected_stakeholders) > 0
]

# Collect risks missing impact_areas or affected_stakeholders
unmapped_risks := [r.title |
    r := input.risks[_]
    not _is_fully_mapped(r)
]

# Helper: check if risk has complete mappings
_is_fully_mapped(risk) if {
    count(risk.impact_areas) > 0
    count(risk.affected_stakeholders) > 0
}

# Collect AI systems without dependencies
systems_without_deps := [s.name |
    s := input.ai_systems[_]
    not _has_deps(s)
]

# Helper: check if system has dependencies
_has_deps(system) if {
    count(system.dependencies) > 0
}

# Pass: all risks mapped AND all systems have dependencies
result := {
    "allowed": true,
    "reason": "All risks have impact mappings and all systems have documented dependencies",
    "severity": "high",
    "details": {
        "total_risks": total_risks,
        "mapped_risks": count(mapped_risks),
        "unmapped_risks": [],
        "systems_without_deps": []
    }
} if {
    total_risks > 0
    count(unmapped_risks) == 0
    count(systems_without_deps) == 0
}

# Fail: some risks unmapped or systems lack dependencies
result := {
    "allowed": false,
    "reason": sprintf("Unmapped risks: %v. Systems without dependencies: %v", [
        concat(", ", unmapped_risks),
        concat(", ", systems_without_deps)
    ]),
    "severity": "high",
    "details": {
        "total_risks": total_risks,
        "mapped_risks": count(mapped_risks),
        "unmapped_risks": unmapped_risks,
        "systems_without_deps": systems_without_deps
    }
} if {
    total_risks > 0
    unmapped_or_missing
}

# Combined check: either unmapped risks OR missing deps
unmapped_or_missing if {
    count(unmapped_risks) > 0
}

unmapped_or_missing if {
    count(systems_without_deps) > 0
}
