# =========================================================================
# NIST AI RMF - MANAGE-3.1: Third-Party AI System Monitoring
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MANAGE
# Control: MANAGE-3.1
# Severity: High
#
# Rule: All third-party AI systems must have at least one incident
# record within the last 90 days, demonstrating active monitoring.
# If no third-party systems exist, the policy passes (not applicable).
#
# Input:
#   - third_party_systems: [{id, name}]
#   - incidents: [{ai_system_id, occurred_at}]
#   - cutoff_date: "2026-01-21T00:00:00Z" (90 days ago, pre-computed)
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "high"
#   - details: {total_third_party, monitored, unmonitored_systems}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.manage.third_party_monitoring

import future.keywords.if
import future.keywords.in

# Default result when no third-party systems exist (pass - not applicable)
default result := {
    "allowed": true,
    "reason": "No third-party AI systems declared. Policy not applicable.",
    "severity": "high",
    "details": {
        "total_third_party": 0,
        "monitored": 0,
        "unmonitored_systems": []
    }
}

# Count total third-party systems
total_third_party := count(input.third_party_systems)

# Helper: check if a third-party system has recent monitoring
_has_recent_monitoring(system_id) if {
    incident := input.incidents[_]
    incident.ai_system_id == system_id
    incident.occurred_at >= input.cutoff_date
}

# Collect monitored third-party systems
monitored_systems := [s |
    s := input.third_party_systems[_]
    _has_recent_monitoring(s.id)
]

# Collect unmonitored third-party systems
unmonitored_systems := [s.name |
    s := input.third_party_systems[_]
    not _has_recent_monitoring(s.id)
]

# Pass: all third-party systems have recent monitoring
result := {
    "allowed": true,
    "reason": "All third-party AI systems have incident records within the last 90 days",
    "severity": "high",
    "details": {
        "total_third_party": total_third_party,
        "monitored": count(monitored_systems),
        "unmonitored_systems": []
    }
} if {
    total_third_party > 0
    count(unmonitored_systems) == 0
}

# Fail: some third-party systems lack recent monitoring
result := {
    "allowed": false,
    "reason": sprintf("Third-party AI systems without recent monitoring: %v", [concat(", ", unmonitored_systems)]),
    "severity": "high",
    "details": {
        "total_third_party": total_third_party,
        "monitored": count(monitored_systems),
        "unmonitored_systems": unmonitored_systems
    }
} if {
    total_third_party > 0
    count(unmonitored_systems) > 0
}
