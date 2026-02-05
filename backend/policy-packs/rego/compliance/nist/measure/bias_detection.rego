# =========================================================================
# NIST AI RMF - MEASURE-2.1: Bias Detection
# SDLC Orchestrator - Sprint 157 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MEASURE
# Control: MEASURE-2.1
# Severity: Critical
#
# Rule: Bias metrics (metric_type="bias_score") must exist for at least
#       2 demographic groups per AI system, and all must be within threshold.
#
# Input:
#   - metrics: [{ai_system_id, metric_type, metric_value, threshold_max, demographic_group}]
#   - ai_systems: [{id, name}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "critical"
#   - details: {systems_checked, systems_with_coverage, systems_lacking_coverage, threshold_violations}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.measure.bias_detection

import future.keywords.if
import future.keywords.in

# Default result when no bias metrics exist
default result := {
    "allowed": false,
    "reason": "No bias metrics recorded. Bias detection requires metrics for at least 2 demographic groups per AI system.",
    "severity": "critical",
    "details": {
        "systems_checked": 0,
        "systems_with_coverage": 0,
        "systems_lacking_coverage": [],
        "threshold_violations": []
    }
}

# Filter to only bias_score metrics
bias_metrics := [m |
    m := input.metrics[_]
    m.metric_type == "bias_score"
]

# Total AI systems to check
total_systems := count(input.ai_systems)

# Get unique demographic groups per system
_system_groups(system_id) := groups if {
    groups := {m.demographic_group |
        m := bias_metrics[_]
        m.ai_system_id == system_id
        m.demographic_group != null
        m.demographic_group != ""
    }
}

# Systems with adequate coverage (>=2 groups)
systems_with_coverage := [s.name |
    s := input.ai_systems[_]
    count(_system_groups(s.id)) >= 2
]

# Systems lacking coverage (<2 groups)
systems_lacking_coverage := [s.name |
    s := input.ai_systems[_]
    count(_system_groups(s.id)) < 2
]

# Bias metrics that exceed threshold
threshold_violations := [m.metric_name |
    m := bias_metrics[_]
    m.threshold_max != null
    m.metric_value > m.threshold_max
]

# Pass: all systems have >=2 groups and all bias scores within threshold
result := {
    "allowed": true,
    "reason": "All AI systems have bias metrics for adequate demographic groups and all scores are within thresholds",
    "severity": "critical",
    "details": {
        "systems_checked": total_systems,
        "systems_with_coverage": count(systems_with_coverage),
        "systems_lacking_coverage": [],
        "threshold_violations": []
    }
} if {
    count(bias_metrics) > 0
    total_systems > 0
    count(systems_lacking_coverage) == 0
    count(threshold_violations) == 0
}

# Fail: coverage gaps or threshold violations
result := {
    "allowed": false,
    "reason": sprintf("Systems lacking bias coverage: %v. Threshold violations: %v", [
        concat(", ", systems_lacking_coverage),
        concat(", ", threshold_violations)
    ]),
    "severity": "critical",
    "details": {
        "systems_checked": total_systems,
        "systems_with_coverage": count(systems_with_coverage),
        "systems_lacking_coverage": systems_lacking_coverage,
        "threshold_violations": threshold_violations
    }
} if {
    count(bias_metrics) > 0
    total_systems > 0
    has_issues
}

has_issues if {
    count(systems_lacking_coverage) > 0
}

has_issues if {
    count(threshold_violations) > 0
}
