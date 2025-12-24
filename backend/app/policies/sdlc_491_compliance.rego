# =========================================================================
# SDLC 4.9.1 Compliance Policies - OPA Rego Rules
# SDLC Orchestrator - Stage 03 (BUILD)
#
# Version: 1.0.0
# Date: December 2, 2025
# Status: ACTIVE - Sprint 21 Day 1 (Compliance Scanner)
# Authority: Backend Lead + CTO Approved
# Foundation: Sprint 21 Plan, SDLC 4.9.1 Framework
#
# Purpose:
# - Define SDLC 4.9.1 compliance rules in Rego
# - Validate gate sequences and evidence requirements
# - Enforce documentation standards
# - Detect policy violations
#
# Usage:
#   OPA evaluates these rules via REST API:
#   POST /v1/data/sdlc/compliance/sdlc_491
#   {"input": {"project": {...}, "gates": [...]}}
#
# Zero Mock Policy: Production-ready Rego rules
# =========================================================================

package sdlc.compliance.sdlc_491

import future.keywords.in
import future.keywords.if
import future.keywords.contains

# ============================================================================
# Default Values
# ============================================================================

default allowed := false
default compliance_score := 0

# ============================================================================
# Helper Functions
# ============================================================================

# Get gate by code
gate_by_code(code) := gate if {
    some gate in input.gates
    gate.gate_code == code
}

# Check if gate is approved
gate_approved(code) if {
    gate := gate_by_code(code)
    gate.status == "approved"
}

# Check if gate exists
gate_exists(code) if {
    some gate in input.gates
    gate.gate_code == code
}

# Count approved gates
approved_gates_count := count([g |
    some g in input.gates
    g.status == "approved"
])

# Count total gates
total_gates_count := count(input.gates)

# ============================================================================
# Stage Sequence Rules
# ============================================================================

# G0.1 must be approved before G0.2
violation contains msg if {
    gate_approved("G0.2")
    not gate_approved("G0.1")
    msg := "Gate G0.2 (Solution Diversity) approved before G0.1 (Problem Definition) - Stage sequence violated"
}

# G0.2 must be approved before G1
violation contains msg if {
    gate_approved("G1")
    not gate_approved("G0.2")
    msg := "Gate G1 (Market Validation) approved before G0.2 (Solution Diversity) - Stage sequence violated"
}

# G1 must be approved before G2
violation contains msg if {
    gate_approved("G2")
    not gate_approved("G1")
    msg := "Gate G2 (Design Ready) approved before G1 (Market Validation) - Stage sequence violated"
}

# G2 must be approved before G3
violation contains msg if {
    gate_approved("G3")
    not gate_approved("G2")
    msg := "Gate G3 (Ship Ready) approved before G2 (Design Ready) - Stage sequence violated"
}

# G3 must be approved before G4
violation contains msg if {
    gate_approved("G4")
    not gate_approved("G3")
    msg := "Gate G4 (Launch Ready) approved before G3 (Ship Ready) - Stage sequence violated"
}

# G4 must be approved before G5
violation contains msg if {
    gate_approved("G5")
    not gate_approved("G4")
    msg := "Gate G5 (Scale Ready) approved before G4 (Launch Ready) - Stage sequence violated"
}

# ============================================================================
# Documentation Structure Rules
# ============================================================================

# Check for WHY stage gates
violation contains msg if {
    total_gates_count > 0
    not any_why_stage
    msg := "Project has gates but no WHY stage (G0.x) gates defined - Missing foundational stage"
}

any_why_stage if {
    some gate in input.gates
    gate.stage == "WHY"
}

# Check for WHAT stage gates when BUILD stage exists
violation contains msg if {
    any_build_stage
    not any_what_stage
    msg := "Project has BUILD stage gates but no WHAT stage gates - Requirements not documented"
}

any_what_stage if {
    some gate in input.gates
    gate.stage == "WHAT"
}

any_build_stage if {
    some gate in input.gates
    gate.stage == "BUILD"
}

# Check for HOW stage gates when BUILD stage exists
violation contains msg if {
    any_build_stage
    not any_how_stage
    msg := "Project has BUILD stage gates but no HOW stage gates - Architecture not documented"
}

any_how_stage if {
    some gate in input.gates
    gate.stage == "HOW"
}

# ============================================================================
# Evidence Requirements
# ============================================================================

# Minimum evidence for G0.1 (Problem Definition)
violation contains msg if {
    gate := gate_by_code("G0.1")
    gate.status == "pending_approval"
    gate.evidence_count < 1
    msg := sprintf("Gate G0.1 has insufficient evidence (%d/1) - Problem statement required", [gate.evidence_count])
}

# Minimum evidence for G1 (Market Validation)
violation contains msg if {
    gate := gate_by_code("G1")
    gate.status == "pending_approval"
    gate.evidence_count < 3
    msg := sprintf("Gate G1 has insufficient evidence (%d/3) - Market research, user interviews required", [gate.evidence_count])
}

# Minimum evidence for G2 (Design Ready)
violation contains msg if {
    gate := gate_by_code("G2")
    gate.status == "pending_approval"
    gate.evidence_count < 5
    msg := sprintf("Gate G2 has insufficient evidence (%d/5) - Architecture docs, ADRs required", [gate.evidence_count])
}

# Minimum evidence for G3 (Ship Ready)
violation contains msg if {
    gate := gate_by_code("G3")
    gate.status == "pending_approval"
    gate.evidence_count < 10
    msg := sprintf("Gate G3 has insufficient evidence (%d/10) - Code, tests, security scan required", [gate.evidence_count])
}

# ============================================================================
# Project Status Rules
# ============================================================================

# Inactive project with pending gates
warning contains msg if {
    input.project.is_active == false
    some gate in input.gates
    gate.status == "pending_approval"
    msg := "Inactive project has pending gates - Consider archiving or reactivating"
}

# Project with no gates after creation
warning contains msg if {
    total_gates_count == 0
    msg := "Project has no gates defined - Create at least G0.1 to start SDLC process"
}

# ============================================================================
# Gate Approval Rules
# ============================================================================

# Gates stuck in pending for too long (>30 days)
warning contains msg if {
    some gate in input.gates
    gate.status == "pending_approval"
    gate.days_pending > 30
    msg := sprintf("Gate %s has been pending for %d days - Consider reviewing or escalating", [gate.gate_code, gate.days_pending])
}

# Too many rejected gates
violation contains msg if {
    rejected_count := count([g | some g in input.gates; g.status == "rejected"])
    rejected_count > 3
    msg := sprintf("Project has %d rejected gates - Review project health and blockers", [rejected_count])
}

# ============================================================================
# Compliance Score Calculation
# ============================================================================

# Base score
base_score := 100

# Deductions per violation severity
critical_deduction := count([v | some v in violation; contains(v, "Stage sequence violated")]) * 25
high_deduction := count([v | some v in violation; contains(v, "insufficient evidence")]) * 15
medium_deduction := count([v | some v in violation; not contains(v, "Stage sequence"); not contains(v, "insufficient")]) * 10
warning_deduction := count(warning) * 2

# Final compliance score
compliance_score := max([0, base_score - critical_deduction - high_deduction - medium_deduction - warning_deduction])

# ============================================================================
# Final Decision
# ============================================================================

# Project is allowed (compliant) if no critical violations
allowed if {
    count([v | some v in violation; contains(v, "Stage sequence violated")]) == 0
    count([v | some v in violation; contains(v, "insufficient evidence")]) == 0
}

# ============================================================================
# Output
# ============================================================================

# Full evaluation result
result := {
    "allowed": allowed,
    "compliance_score": compliance_score,
    "violations": violation,
    "warnings": warning,
    "gates_approved": approved_gates_count,
    "gates_total": total_gates_count,
}
