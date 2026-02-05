# =========================================================================
# NIST AI RMF - MANAGE-4.1: Post-Deployment AI System Monitoring
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MANAGE
# Control: MANAGE-4.1
# Severity: Critical
#
# Rule: All active AI systems must have:
#   a) At least one metric record within the last 30 days (pre-filtered)
#   b) No unresolved critical incidents
# Systems without recent metrics or with critical incidents indicate
# inadequate post-deployment monitoring practices.
#
# Input:
#   - active_systems: [{id, name}]
#   - recent_metrics: [{ai_system_id}]
#   - critical_incidents: [{ai_system_id, title}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "critical"
#   - details: {total_systems, monitored, unmonitored_systems, systems_with_critical_incidents}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.manage.post_deployment_monitoring

import future.keywords.if
import future.keywords.in

# Default result when no active systems are declared
default result := {
    "allowed": false,
    "reason": "No active AI systems declared. At least one active system must be documented.",
    "severity": "critical",
    "details": {
        "total_systems": 0,
        "monitored": 0,
        "unmonitored_systems": [],
        "systems_with_critical_incidents": []
    }
}

# Count total active systems
total_systems := count(input.active_systems)

# Helper: check if a system has recent metrics
_has_recent_metrics(system_id) if {
    metric := input.recent_metrics[_]
    metric.ai_system_id == system_id
}

# Helper: check if a system has unresolved critical incidents
_has_critical_incident(system_id) if {
    incident := input.critical_incidents[_]
    incident.ai_system_id == system_id
}

# Collect systems with recent metrics
monitored_systems := [s |
    s := input.active_systems[_]
    _has_recent_metrics(s.id)
]

# Collect systems without recent metrics
unmonitored_systems := [s.name |
    s := input.active_systems[_]
    not _has_recent_metrics(s.id)
]

# Collect systems with unresolved critical incidents
systems_with_critical_incidents := [s.name |
    s := input.active_systems[_]
    _has_critical_incident(s.id)
]

# Pass: all systems have recent metrics and no critical incidents
result := {
    "allowed": true,
    "reason": "All active AI systems have recent metrics and no unresolved critical incidents",
    "severity": "critical",
    "details": {
        "total_systems": total_systems,
        "monitored": count(monitored_systems),
        "unmonitored_systems": [],
        "systems_with_critical_incidents": []
    }
} if {
    total_systems > 0
    count(unmonitored_systems) == 0
    count(systems_with_critical_incidents) == 0
}

# Fail: some systems lack metrics or have critical incidents
result := {
    "allowed": false,
    "reason": sprintf("Post-deployment monitoring gaps detected. Unmonitored: %v. Critical incidents: %v", [concat(", ", unmonitored_systems), concat(", ", systems_with_critical_incidents)]),
    "severity": "critical",
    "details": {
        "total_systems": total_systems,
        "monitored": count(monitored_systems),
        "unmonitored_systems": unmonitored_systems,
        "systems_with_critical_incidents": systems_with_critical_incidents
    }
} if {
    total_systems > 0
    _any_monitoring_gap
}

# Helper: determine if any monitoring gap exists
_any_monitoring_gap if {
    count(unmonitored_systems) > 0
}

_any_monitoring_gap if {
    count(systems_with_critical_incidents) > 0
}
