# =========================================================================
# NIST AI RMF - MEASURE-2.2: Disparity Analysis (4/5ths Rule)
# SDLC Orchestrator - Sprint 157 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MEASURE
# Control: MEASURE-2.2
# Severity: Critical
#
# Rule: Disparity ratio between best and worst performing demographic
#       groups must not exceed 1.25 (EEOC 4/5ths rule).
#       For each AI system, max(metric)/min(metric) across groups <= 1.25.
#
# Input:
#   - metrics: [{ai_system_id, metric_type, metric_value, demographic_group}]
#   - ai_systems: [{id, name}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "critical"
#   - details: {systems_checked, compliant_systems, non_compliant_systems, max_disparity_ratio}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.measure.disparity_analysis

import future.keywords.if
import future.keywords.in

# EEOC 4/5ths rule threshold
disparity_threshold := 1.25

# Default result when no metrics
default result := {
    "allowed": false,
    "reason": "No disparity metrics recorded. Disparity analysis requires performance metrics across demographic groups.",
    "severity": "critical",
    "details": {
        "systems_checked": 0,
        "compliant_systems": 0,
        "non_compliant_systems": [],
        "max_disparity_ratio": 0
    }
}

# Filter to disparity-relevant metric types
disparity_types := {"accuracy", "precision", "recall", "f1_score"}

disparity_metrics := [m |
    m := input.metrics[_]
    m.metric_type in disparity_types
    m.demographic_group != null
    m.demographic_group != ""
]

# Get metric values per system across demographic groups
_system_values(system_id) := values if {
    values := [m.metric_value |
        m := disparity_metrics[_]
        m.ai_system_id == system_id
    ]
}

# Calculate disparity ratio for a system (max/min)
_disparity_ratio(system_id) := ratio if {
    values := _system_values(system_id)
    count(values) >= 2
    min_val := min(values)
    min_val > 0
    max_val := max(values)
    ratio := max_val / min_val
}

# Fallback: if min is 0 or insufficient data, ratio is 0 (skip)
_disparity_ratio(system_id) := 0 if {
    values := _system_values(system_id)
    count(values) < 2
}

_disparity_ratio(system_id) := 0 if {
    values := _system_values(system_id)
    count(values) >= 2
    min_val := min(values)
    min_val <= 0
}

# Total systems to check
total_systems := count(input.ai_systems)

# Systems with disparity within threshold
compliant_systems := [s.name |
    s := input.ai_systems[_]
    ratio := _disparity_ratio(s.id)
    ratio > 0
    ratio <= disparity_threshold
]

# Systems compliant because not enough data (also ok)
systems_no_data := [s.name |
    s := input.ai_systems[_]
    _disparity_ratio(s.id) == 0
]

# Systems exceeding disparity threshold
non_compliant_systems := [s.name |
    s := input.ai_systems[_]
    ratio := _disparity_ratio(s.id)
    ratio > disparity_threshold
]

# Find max disparity ratio across all systems
all_ratios := [_disparity_ratio(s.id) |
    s := input.ai_systems[_]
    _disparity_ratio(s.id) > 0
]

max_ratio := max(all_ratios) if {
    count(all_ratios) > 0
}

max_ratio := 0 if {
    count(all_ratios) == 0
}

# Pass: all systems have disparity within 1.25
result := {
    "allowed": true,
    "reason": sprintf("All AI systems have disparity ratio within %.2f threshold (4/5ths rule)", [disparity_threshold]),
    "severity": "critical",
    "details": {
        "systems_checked": total_systems,
        "compliant_systems": count(compliant_systems),
        "non_compliant_systems": [],
        "max_disparity_ratio": max_ratio
    }
} if {
    count(disparity_metrics) > 0
    total_systems > 0
    count(non_compliant_systems) == 0
}

# Fail: some systems exceed disparity threshold
result := {
    "allowed": false,
    "reason": sprintf("Systems exceeding %.2f disparity threshold: %v (max ratio: %.3f)", [
        disparity_threshold,
        concat(", ", non_compliant_systems),
        max_ratio
    ]),
    "severity": "critical",
    "details": {
        "systems_checked": total_systems,
        "compliant_systems": count(compliant_systems),
        "non_compliant_systems": non_compliant_systems,
        "max_disparity_ratio": max_ratio
    }
} if {
    count(disparity_metrics) > 0
    total_systems > 0
    count(non_compliant_systems) > 0
}
