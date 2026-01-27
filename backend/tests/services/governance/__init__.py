"""
=========================================================================
Governance Services Tests Package
SDLC Orchestrator - Sprint 110 (CEO Dashboard & Observability)

Version: 1.1.0
Date: January 27, 2026
Status: ACTIVE - Sprint 110 Day 7
Authority: CTO + Backend Lead Approved
Framework: SDLC 5.3.0 Quality Assurance System

Test Modules:
- test_signals_engine.py: Vibecoding Index Engine tests (5 signals)
- test_stage_gating.py: Stage-Aware PR Gating tests (11 SDLC stages)
- test_context_authority.py: Context Authority V1 tests (4 checks)
- test_kill_switch.py: Kill Switch validation tests (4 trigger criteria)

Kill Switch Trigger Criteria (per MONITORING-PLAN.md):
1. rejection_rate >80%
2. latency_p95 >500ms
3. false_positive_rate >20%
4. developer_complaints >5/day

Zero Mock Policy: Real implementations tested
=========================================================================
"""
