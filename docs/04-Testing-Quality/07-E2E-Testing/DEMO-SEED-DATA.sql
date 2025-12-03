-- =========================================================================
-- DEMO SEED DATA - SDLC Orchestrator
-- Version: 1.0.0
-- Date: November 27, 2025
-- Status: ACTIVE - STAGE 03 (BUILD)
-- Authority: QA Lead + Backend Lead Approved
-- Framework: SDLC 4.9 Complete Lifecycle
--
-- Purpose:
-- Comprehensive seed data for E2E testing and demo scenarios.
-- Covers all 5 Functional Requirements (FR1-FR5).
--
-- Usage:
-- psql -h localhost -U sdlc_user -d sdlc_orchestrator -f DEMO-SEED-DATA.sql
-- =========================================================================

-- =========================================================================
-- SECTION 1: CLEANUP (Optional - uncomment to reset)
-- =========================================================================
-- WARNING: This will delete ALL existing data!
-- DELETE FROM gate_evidence;
-- DELETE FROM gate_approvals;
-- DELETE FROM policy_evaluations;
-- DELETE FROM gates;
-- DELETE FROM project_members;
-- DELETE FROM projects;
-- DELETE FROM refresh_tokens;
-- DELETE FROM users WHERE email NOT IN ('admin@sdlc-orchestrator.io');

-- =========================================================================
-- SECTION 2: USERS & ROLES
-- Password for all users: password123 (bcrypt hashed)
-- Admin password: Admin@123
-- =========================================================================

-- Insert demo users (skip if exists)
-- NOTE: Column is "name" not "full_name" per actual schema
-- Password hash generated with: python3 -c "import bcrypt; print(bcrypt.hashpw('password123'.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8'))"
INSERT INTO users (id, email, name, password_hash, is_active, is_superuser, mfa_enabled, created_at, updated_at)
VALUES
  -- CTO - Can approve G2, G3 gates
  ('b0000000-0000-0000-0000-000000000001', 'cto@bflow.vn', 'Nguyen Van CTO',
   '$2b$12$T6BJlzPawHNYv4UdrSCjleDH1o9UY6ho5859bNhNHIavyx7miFshu', -- password123
   true, false, false, NOW(), NOW()),

  -- CPO - Can approve business gates
  ('b0000000-0000-0000-0000-000000000002', 'cpo@bflow.vn', 'Tran Thi CPO',
   '$2b$12$T6BJlzPawHNYv4UdrSCjleDH1o9UY6ho5859bNhNHIavyx7miFshu', -- password123
   true, false, false, NOW(), NOW()),

  -- PM - Project Manager
  ('b0000000-0000-0000-0000-000000000003', 'pm@bflow.vn', 'Le Van PM',
   '$2b$12$T6BJlzPawHNYv4UdrSCjleDH1o9UY6ho5859bNhNHIavyx7miFshu', -- password123
   true, false, false, NOW(), NOW()),

  -- Developer
  ('b0000000-0000-0000-0000-000000000004', 'dev@bflow.vn', 'Pham Van Dev',
   '$2b$12$T6BJlzPawHNYv4UdrSCjleDH1o9UY6ho5859bNhNHIavyx7miFshu', -- password123
   true, false, false, NOW(), NOW()),

  -- QA Lead
  ('b0000000-0000-0000-0000-000000000005', 'qa@bflow.vn', 'Hoang Thi QA',
   '$2b$12$T6BJlzPawHNYv4UdrSCjleDH1o9UY6ho5859bNhNHIavyx7miFshu', -- password123
   true, false, false, NOW(), NOW()),

  -- External Stakeholder (NQH)
  ('b0000000-0000-0000-0000-000000000006', 'ceo@nqh.vn', 'Nguyen Quoc Hung',
   '$2b$12$T6BJlzPawHNYv4UdrSCjleDH1o9UY6ho5859bNhNHIavyx7miFshu', -- password123
   true, false, false, NOW(), NOW()),

  -- External Developer (NQH)
  ('b0000000-0000-0000-0000-000000000007', 'dev@nqh.vn', 'Tran Dev NQH',
   '$2b$12$T6BJlzPawHNYv4UdrSCjleDH1o9UY6ho5859bNhNHIavyx7miFshu', -- password123
   true, false, false, NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- =========================================================================
-- SECTION 3: PROJECTS
-- 5 projects covering different stages and scenarios
-- =========================================================================

-- Project 1: BFlow v3.0 - In HOW stage (most advanced)
INSERT INTO projects (id, name, slug, description, owner_id, is_active, created_at, updated_at)
VALUES (
  'c0000000-0000-0000-0000-000000000001',
  'BFlow Workflow Automation - v3.0',
  'bflow-workflow-v3',
  'Workflow automation platform for BFlow. Visual workflow designer with 50+ pre-built templates, Zapier-style integrations. Target: 10K workflows/month, <5 min learning curve.',
  'b0000000-0000-0000-0000-000000000003', -- PM owns
  true,
  '2025-10-01 10:00:00',
  NOW()
) ON CONFLICT (id) DO UPDATE SET updated_at = NOW();

-- Project 2: NQH E-commerce - In WHAT stage
INSERT INTO projects (id, name, slug, description, owner_id, is_active, created_at, updated_at)
VALUES (
  'c0000000-0000-0000-0000-000000000002',
  'NQH E-commerce Platform - Phase 2',
  'nqh-ecommerce-phase2',
  'E-commerce platform upgrade with AI product recommendations, VNPay/Momo integration, real-time inventory sync. Target: 4.5% conversion rate, <200ms API response.',
  'b0000000-0000-0000-0000-000000000006', -- NQH CEO owns
  true,
  '2025-09-15 09:00:00',
  NOW()
) ON CONFLICT (id) DO UPDATE SET updated_at = NOW();

-- Project 3: MTS SDLC Tool - In BUILD stage
INSERT INTO projects (id, name, slug, description, owner_id, is_active, created_at, updated_at)
VALUES (
  'c0000000-0000-0000-0000-000000000003',
  'MTS Internal Tool - SDLC Automation',
  'mtc-sdlc-automation',
  'Internal developer productivity tool. Automates SDLC workflows, reduces gate approvals from 3 days to 2 hours. Target: 95% test coverage, zero deployment failures.',
  'b0000000-0000-0000-0000-000000000001', -- CTO owns
  true,
  '2025-08-01 08:00:00',
  NOW()
) ON CONFLICT (id) DO UPDATE SET updated_at = NOW();

-- Project 4: Demo Project - Fresh (no gates)
INSERT INTO projects (id, name, slug, description, owner_id, is_active, created_at, updated_at)
VALUES (
  'c0000000-0000-0000-0000-000000000004',
  'Demo Project - Getting Started',
  'demo-getting-started',
  'Sample project for onboarding new users. Shows how to create gates, upload evidence, and pass quality checks.',
  'a0000000-0000-0000-0000-000000000001', -- Admin owns
  true,
  NOW(),
  NOW()
) ON CONFLICT (id) DO UPDATE SET updated_at = NOW();

-- Project 5: Archived Project (inactive)
INSERT INTO projects (id, name, slug, description, owner_id, is_active, created_at, updated_at, deleted_at)
VALUES (
  'c0000000-0000-0000-0000-000000000005',
  'Legacy CRM Migration (Archived)',
  'legacy-crm-migration',
  'Completed migration of legacy CRM system. Archived after successful deployment.',
  'b0000000-0000-0000-0000-000000000003',
  false,
  '2025-01-01 10:00:00',
  '2025-06-30 17:00:00',
  '2025-07-01 09:00:00'
) ON CONFLICT (id) DO UPDATE SET updated_at = NOW();

-- =========================================================================
-- SECTION 4: PROJECT MEMBERS
-- Team assignments for each project
-- =========================================================================

-- BFlow v3.0 Team
INSERT INTO project_members (id, project_id, user_id, role, invited_by, invited_at, joined_at, created_at)
VALUES
  ('d0000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001',
   'b0000000-0000-0000-0000-000000000003', 'owner', NULL, NOW(), NOW(), NOW()),
  ('d0000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000001',
   'b0000000-0000-0000-0000-000000000001', 'admin', 'b0000000-0000-0000-0000-000000000003', NOW(), NOW(), NOW()),
  ('d0000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000001',
   'b0000000-0000-0000-0000-000000000004', 'member', 'b0000000-0000-0000-0000-000000000003', NOW(), NOW(), NOW()),
  ('d0000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000001',
   'b0000000-0000-0000-0000-000000000005', 'member', 'b0000000-0000-0000-0000-000000000003', NOW(), NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- NQH E-commerce Team
INSERT INTO project_members (id, project_id, user_id, role, invited_by, invited_at, joined_at, created_at)
VALUES
  ('d0000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000002',
   'b0000000-0000-0000-0000-000000000006', 'owner', NULL, NOW(), NOW(), NOW()),
  ('d0000000-0000-0000-0000-000000000006', 'c0000000-0000-0000-0000-000000000002',
   'b0000000-0000-0000-0000-000000000007', 'member', 'b0000000-0000-0000-0000-000000000006', NOW(), NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- MTS SDLC Tool Team (all internal)
INSERT INTO project_members (id, project_id, user_id, role, invited_by, invited_at, joined_at, created_at)
VALUES
  ('d0000000-0000-0000-0000-000000000007', 'c0000000-0000-0000-0000-000000000003',
   'b0000000-0000-0000-0000-000000000001', 'owner', NULL, NOW(), NOW(), NOW()),
  ('d0000000-0000-0000-0000-000000000008', 'c0000000-0000-0000-0000-000000000003',
   'b0000000-0000-0000-0000-000000000002', 'admin', 'b0000000-0000-0000-0000-000000000001', NOW(), NOW(), NOW()),
  ('d0000000-0000-0000-0000-000000000009', 'c0000000-0000-0000-0000-000000000003',
   'b0000000-0000-0000-0000-000000000003', 'admin', 'b0000000-0000-0000-0000-000000000001', NOW(), NOW(), NOW()),
  ('d0000000-0000-0000-0000-000000000010', 'c0000000-0000-0000-0000-000000000003',
   'b0000000-0000-0000-0000-000000000004', 'member', 'b0000000-0000-0000-0000-000000000001', NOW(), NOW(), NOW()),
  ('d0000000-0000-0000-0000-000000000011', 'c0000000-0000-0000-0000-000000000003',
   'b0000000-0000-0000-0000-000000000005', 'member', 'b0000000-0000-0000-0000-000000000001', NOW(), NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- =========================================================================
-- SECTION 5: GATES
-- Gates for each project at different stages
-- =========================================================================

-- BFlow v3.0 Gates (WHY → WHAT → HOW complete, BUILD in progress)
INSERT INTO gates (id, project_id, gate_name, gate_type, stage, status, description, created_by, created_at, updated_at)
VALUES
  -- Stage 00: WHY
  ('e0000000-0000-0000-0000-000000000001', 'c0000000-0000-0000-0000-000000000001',
   'G0.1', 'PROBLEM_DEFINITION', 'WHY', 'APPROVED',
   'Problem statement validated: Current workflow tools require 2+ hours to learn, 60% feature waste.',
   'b0000000-0000-0000-0000-000000000003', '2025-10-05 10:00:00', '2025-10-10 15:00:00'),

  ('e0000000-0000-0000-0000-000000000002', 'c0000000-0000-0000-0000-000000000001',
   'G0.2', 'SOLUTION_DIVERSITY', 'WHY', 'APPROVED',
   '5 solutions evaluated: Visual designer + templates approach selected (highest ROI).',
   'b0000000-0000-0000-0000-000000000003', '2025-10-10 10:00:00', '2025-10-15 16:00:00'),

  -- Stage 01: WHAT
  ('e0000000-0000-0000-0000-000000000003', 'c0000000-0000-0000-0000-000000000001',
   'G1', 'PLANNING_COMPLETE', 'WHAT', 'APPROVED',
   'FRD approved: 20 functional requirements, API spec (1,629 lines), data model designed.',
   'b0000000-0000-0000-0000-000000000003', '2025-10-20 09:00:00', '2025-10-30 14:00:00'),

  -- Stage 02: HOW
  ('e0000000-0000-0000-0000-000000000004', 'c0000000-0000-0000-0000-000000000001',
   'G2', 'DESIGN_READY', 'HOW', 'APPROVED',
   'Architecture design complete: 4-layer architecture, AGPL containment validated, security baseline.',
   'b0000000-0000-0000-0000-000000000001', '2025-11-01 10:00:00', '2025-11-10 17:00:00'),

  -- Stage 03: BUILD (in progress)
  ('e0000000-0000-0000-0000-000000000005', 'c0000000-0000-0000-0000-000000000001',
   'G3', 'SHIP_READY', 'BUILD', 'PENDING_APPROVAL',
   'MVP development: 60% complete. Authentication, Dashboard, Projects pages done.',
   'b0000000-0000-0000-0000-000000000004', '2025-11-15 08:00:00', NOW())
ON CONFLICT (id) DO NOTHING;

-- NQH E-commerce Gates (WHY complete, WHAT in progress)
INSERT INTO gates (id, project_id, gate_name, gate_type, stage, status, description, created_by, created_at, updated_at)
VALUES
  -- Stage 00: WHY
  ('e0000000-0000-0000-0000-000000000006', 'c0000000-0000-0000-0000-000000000002',
   'G0.1', 'PROBLEM_DEFINITION', 'WHY', 'APPROVED',
   'Problem: Current platform has 2.3% conversion, 68% cart abandonment. Target: 4.5% and 45%.',
   'b0000000-0000-0000-0000-000000000006', '2025-09-20 10:00:00', '2025-09-25 15:00:00'),

  ('e0000000-0000-0000-0000-000000000007', 'c0000000-0000-0000-0000-000000000002',
   'G0.2', 'SOLUTION_DIVERSITY', 'WHY', 'APPROVED',
   'AI recommendations + payment integration selected over full rebuild.',
   'b0000000-0000-0000-0000-000000000006', '2025-09-25 10:00:00', '2025-10-01 16:00:00'),

  -- Stage 01: WHAT (in progress)
  ('e0000000-0000-0000-0000-000000000008', 'c0000000-0000-0000-0000-000000000002',
   'G1', 'PLANNING_COMPLETE', 'WHAT', 'PENDING_APPROVAL',
   'FRD 80% complete. Missing: AI recommendation specs, payment gateway integration details.',
   'b0000000-0000-0000-0000-000000000007', '2025-10-10 09:00:00', NOW())
ON CONFLICT (id) DO NOTHING;

-- MTS SDLC Tool Gates (Complete through BUILD, VERIFY in progress)
INSERT INTO gates (id, project_id, gate_name, gate_type, stage, status, description, created_by, created_at, updated_at)
VALUES
  -- All WHY, WHAT, HOW, BUILD approved
  ('e0000000-0000-0000-0000-000000000009', 'c0000000-0000-0000-0000-000000000003',
   'G0.1', 'PROBLEM_DEFINITION', 'WHY', 'APPROVED',
   'Problem: Manual gate approvals take 3 days, 65% feature waste.',
   'b0000000-0000-0000-0000-000000000001', '2025-08-05 10:00:00', '2025-08-10 15:00:00'),

  ('e0000000-0000-0000-0000-000000000010', 'c0000000-0000-0000-0000-000000000003',
   'G0.2', 'SOLUTION_DIVERSITY', 'WHY', 'APPROVED',
   'Bridge-first approach: Integrate with existing tools, not replace.',
   'b0000000-0000-0000-0000-000000000001', '2025-08-10 10:00:00', '2025-08-15 16:00:00'),

  ('e0000000-0000-0000-0000-000000000011', 'c0000000-0000-0000-0000-000000000003',
   'G1', 'PLANNING_COMPLETE', 'WHAT', 'APPROVED',
   'Full FRD with 20 functional requirements, OpenAPI 3.0 spec.',
   'b0000000-0000-0000-0000-000000000002', '2025-08-25 09:00:00', '2025-09-05 14:00:00'),

  ('e0000000-0000-0000-0000-000000000012', 'c0000000-0000-0000-0000-000000000003',
   'G2', 'DESIGN_READY', 'HOW', 'APPROVED',
   '4-layer architecture, AGPL containment, security baseline OWASP ASVS L2.',
   'b0000000-0000-0000-0000-000000000001', '2025-09-15 10:00:00', '2025-09-25 17:00:00'),

  ('e0000000-0000-0000-0000-000000000013', 'c0000000-0000-0000-0000-000000000003',
   'G3', 'SHIP_READY', 'BUILD', 'APPROVED',
   'MVP complete: Auth, Dashboard, Projects, Gates, Evidence Vault.',
   'b0000000-0000-0000-0000-000000000001', '2025-10-15 08:00:00', '2025-11-01 18:00:00'),

  -- Stage 04: VERIFY (in progress)
  ('e0000000-0000-0000-0000-000000000014', 'c0000000-0000-0000-0000-000000000003',
   'G4', 'TEST_COMPLETE', 'VERIFY', 'PENDING',
   'Testing phase: Unit tests 85%, integration tests 70%, E2E tests 50%.',
   'b0000000-0000-0000-0000-000000000005', '2025-11-05 08:00:00', NOW())
ON CONFLICT (id) DO NOTHING;

-- =========================================================================
-- SECTION 6: GATE APPROVALS
-- Approval history for approved gates
-- =========================================================================

INSERT INTO gate_approvals (id, gate_id, approver_id, status, comment, approved_at, created_at)
VALUES
  -- BFlow G0.1 approval
  ('f0000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000001',
   'b0000000-0000-0000-0000-000000000002', 'APPROVED',
   'Problem statement is clear and measurable. Approved to proceed.',
   '2025-10-10 15:00:00', '2025-10-10 15:00:00'),

  -- BFlow G0.2 approval
  ('f0000000-0000-0000-0000-000000000002', 'e0000000-0000-0000-0000-000000000002',
   'b0000000-0000-0000-0000-000000000002', 'APPROVED',
   'Solution diversity well explored. Visual designer approach has best ROI.',
   '2025-10-15 16:00:00', '2025-10-15 16:00:00'),

  -- BFlow G1 approval (dual approval: CTO + CPO)
  ('f0000000-0000-0000-0000-000000000003', 'e0000000-0000-0000-0000-000000000003',
   'b0000000-0000-0000-0000-000000000001', 'APPROVED',
   'Technical requirements are sound. API spec comprehensive.',
   '2025-10-29 14:00:00', '2025-10-29 14:00:00'),
  ('f0000000-0000-0000-0000-000000000004', 'e0000000-0000-0000-0000-000000000003',
   'b0000000-0000-0000-0000-000000000002', 'APPROVED',
   'Business requirements align with market needs.',
   '2025-10-30 14:00:00', '2025-10-30 14:00:00'),

  -- BFlow G2 approval
  ('f0000000-0000-0000-0000-000000000005', 'e0000000-0000-0000-0000-000000000004',
   'b0000000-0000-0000-0000-000000000001', 'APPROVED',
   'Architecture is solid. AGPL containment validated. Security baseline met.',
   '2025-11-10 17:00:00', '2025-11-10 17:00:00'),

  -- MTS G3 approval
  ('f0000000-0000-0000-0000-000000000006', 'e0000000-0000-0000-0000-000000000013',
   'b0000000-0000-0000-0000-000000000001', 'APPROVED',
   'MVP fully functional. Ready for testing phase.',
   '2025-11-01 18:00:00', '2025-11-01 18:00:00')
ON CONFLICT (id) DO NOTHING;

-- =========================================================================
-- SECTION 7: GATE EVIDENCE
-- Sample evidence documents for gates
-- =========================================================================

INSERT INTO gate_evidence (id, gate_id, evidence_type, title, description, file_path, file_name, file_size, mime_type, sha256_hash, uploaded_by, created_at, updated_at)
VALUES
  -- BFlow G0.1 evidence
  ('g0000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000001',
   'DOCUMENT', 'Problem Statement Document', 'Detailed analysis of workflow tool pain points and market research',
   's3://evidence-vault/bflow-v3/g01/problem-statement.pdf', 'problem-statement.pdf',
   2048576, 'application/pdf', 'a1b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef12345678',
   'b0000000-0000-0000-0000-000000000003', '2025-10-05 11:00:00', '2025-10-05 11:00:00'),

  ('g0000000-0000-0000-0000-000000000002', 'e0000000-0000-0000-0000-000000000001',
   'DATA', 'User Survey Results', 'Survey of 100 potential users about workflow tool frustrations',
   's3://evidence-vault/bflow-v3/g01/user-survey.xlsx', 'user-survey.xlsx',
   524288, 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
   'b2c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456789a',
   'b0000000-0000-0000-0000-000000000003', '2025-10-06 14:00:00', '2025-10-06 14:00:00'),

  -- BFlow G0.2 evidence
  ('g0000000-0000-0000-0000-000000000003', 'e0000000-0000-0000-0000-000000000002',
   'DOCUMENT', 'Solution Alternatives Analysis', 'Comparison of 5 potential approaches with ROI calculations',
   's3://evidence-vault/bflow-v3/g02/solution-alternatives.pdf', 'solution-alternatives.pdf',
   3145728, 'application/pdf', 'c3d4e5f6789012345678901234567890abcdef1234567890abcdef123456789ab1',
   'b0000000-0000-0000-0000-000000000003', '2025-10-11 10:00:00', '2025-10-11 10:00:00'),

  -- BFlow G1 evidence
  ('g0000000-0000-0000-0000-000000000004', 'e0000000-0000-0000-0000-000000000003',
   'DOCUMENT', 'Functional Requirements Document', 'Complete FRD with 20 functional requirements',
   's3://evidence-vault/bflow-v3/g1/frd.pdf', 'functional-requirements.pdf',
   5242880, 'application/pdf', 'd4e5f6789012345678901234567890abcdef1234567890abcdef123456789ab1c2',
   'b0000000-0000-0000-0000-000000000003', '2025-10-22 09:00:00', '2025-10-22 09:00:00'),

  ('g0000000-0000-0000-0000-000000000005', 'e0000000-0000-0000-0000-000000000003',
   'CODE', 'API Specification', 'OpenAPI 3.0 specification (1,629 lines)',
   's3://evidence-vault/bflow-v3/g1/openapi.yaml', 'openapi.yaml',
   102400, 'application/x-yaml', 'e5f6789012345678901234567890abcdef1234567890abcdef123456789ab1c2d3',
   'b0000000-0000-0000-0000-000000000004', '2025-10-25 11:00:00', '2025-10-25 11:00:00'),

  ('g0000000-0000-0000-0000-000000000006', 'e0000000-0000-0000-0000-000000000003',
   'DIAGRAM', 'Data Model ERD', 'Entity-Relationship Diagram for 21 tables',
   's3://evidence-vault/bflow-v3/g1/data-model-erd.png', 'data-model-erd.png',
   1048576, 'image/png', 'f6789012345678901234567890abcdef1234567890abcdef123456789ab1c2d3e4',
   'b0000000-0000-0000-0000-000000000004', '2025-10-26 14:00:00', '2025-10-26 14:00:00'),

  -- BFlow G2 evidence
  ('g0000000-0000-0000-0000-000000000007', 'e0000000-0000-0000-0000-000000000004',
   'DOCUMENT', 'System Architecture Document', '4-layer architecture with bridge-first pattern',
   's3://evidence-vault/bflow-v3/g2/system-architecture.pdf', 'system-architecture.pdf',
   4194304, 'application/pdf', '6789012345678901234567890abcdef1234567890abcdef123456789ab1c2d3e4f5',
   'b0000000-0000-0000-0000-000000000001', '2025-11-02 10:00:00', '2025-11-02 10:00:00'),

  ('g0000000-0000-0000-0000-000000000008', 'e0000000-0000-0000-0000-000000000004',
   'DOCUMENT', 'Security Baseline', 'OWASP ASVS Level 2 compliance checklist (264/264)',
   's3://evidence-vault/bflow-v3/g2/security-baseline.pdf', 'security-baseline.pdf',
   2097152, 'application/pdf', '789012345678901234567890abcdef1234567890abcdef123456789ab1c2d3e4f56',
   'b0000000-0000-0000-0000-000000000001', '2025-11-05 11:00:00', '2025-11-05 11:00:00'),

  ('g0000000-0000-0000-0000-000000000009', 'e0000000-0000-0000-0000-000000000004',
   'DOCUMENT', 'AGPL Containment Brief', 'Legal analysis of OSS component integration',
   's3://evidence-vault/bflow-v3/g2/agpl-containment.pdf', 'agpl-containment.pdf',
   1572864, 'application/pdf', '89012345678901234567890abcdef1234567890abcdef123456789ab1c2d3e4f567',
   'b0000000-0000-0000-0000-000000000001', '2025-11-06 15:00:00', '2025-11-06 15:00:00'),

  -- MTS G4 evidence (testing phase)
  ('g0000000-0000-0000-0000-000000000010', 'e0000000-0000-0000-0000-000000000014',
   'REPORT', 'Test Coverage Report', 'Current test coverage: Unit 85%, Integration 70%, E2E 50%',
   's3://evidence-vault/mtc-sdlc/g4/coverage-report.html', 'coverage-report.html',
   524288, 'text/html', '9012345678901234567890abcdef1234567890abcdef123456789ab1c2d3e4f5678',
   'b0000000-0000-0000-0000-000000000005', '2025-11-20 16:00:00', NOW())
ON CONFLICT (id) DO NOTHING;

-- =========================================================================
-- SECTION 8: POLICIES
-- Policy packs and individual policies
-- =========================================================================

INSERT INTO policies (id, name, description, stage, rego_code, is_active, version, created_by, created_at, updated_at)
VALUES
  -- Stage 00: WHY policies
  ('h0000000-0000-0000-0000-000000000001', 'problem_statement_required',
   'Problem statement document must be uploaded', 'WHY',
   'package sdlc.why.problem

default allow = false

allow {
  count(input.evidence) > 0
  some e in input.evidence
  e.type == "DOCUMENT"
  contains(lower(e.title), "problem")
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW()),

  ('h0000000-0000-0000-0000-000000000002', 'user_research_required',
   'User research or survey data must be provided', 'WHY',
   'package sdlc.why.research

default allow = false

allow {
  count(input.evidence) > 0
  some e in input.evidence
  e.type == "DATA"
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW()),

  ('h0000000-0000-0000-0000-000000000003', 'solution_alternatives_required',
   'At least 3 solution alternatives must be evaluated', 'WHY',
   'package sdlc.why.solutions

default allow = false

allow {
  input.solution_count >= 3
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW()),

  -- Stage 01: WHAT policies
  ('h0000000-0000-0000-0000-000000000004', 'frd_required',
   'Functional Requirements Document must be uploaded', 'WHAT',
   'package sdlc.what.frd

default allow = false

allow {
  some e in input.evidence
  e.type == "DOCUMENT"
  contains(lower(e.title), "functional")
  contains(lower(e.title), "requirement")
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW()),

  ('h0000000-0000-0000-0000-000000000005', 'api_spec_required',
   'API specification (OpenAPI) must be provided for API projects', 'WHAT',
   'package sdlc.what.api

default allow = false

allow {
  some e in input.evidence
  e.type == "CODE"
  endswith(e.file_name, ".yaml")
}

allow {
  some e in input.evidence
  e.type == "CODE"
  endswith(e.file_name, ".json")
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW()),

  ('h0000000-0000-0000-0000-000000000006', 'data_model_required',
   'Data model or ERD must be provided', 'WHAT',
   'package sdlc.what.data

default allow = false

allow {
  some e in input.evidence
  e.type == "DIAGRAM"
  contains(lower(e.title), "data")
}

allow {
  some e in input.evidence
  e.type == "DIAGRAM"
  contains(lower(e.title), "erd")
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW()),

  -- Stage 02: HOW policies
  ('h0000000-0000-0000-0000-000000000007', 'architecture_doc_required',
   'System architecture document must be uploaded', 'HOW',
   'package sdlc.how.architecture

default allow = false

allow {
  some e in input.evidence
  e.type == "DOCUMENT"
  contains(lower(e.title), "architecture")
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW()),

  ('h0000000-0000-0000-0000-000000000008', 'security_baseline_required',
   'Security baseline document must be provided', 'HOW',
   'package sdlc.how.security

default allow = false

allow {
  some e in input.evidence
  e.type == "DOCUMENT"
  contains(lower(e.title), "security")
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW()),

  -- Stage 04: VERIFY policies
  ('h0000000-0000-0000-0000-000000000009', 'test_coverage_threshold',
   'Code coverage must be at least 80%', 'VERIFY',
   'package sdlc.verify.coverage

default allow = false

allow {
  input.coverage >= 80
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW()),

  ('h0000000-0000-0000-0000-000000000010', 'no_critical_bugs',
   'No critical or blocker bugs in bug tracker', 'VERIFY',
   'package sdlc.verify.bugs

default allow = false

allow {
  input.critical_bugs == 0
  input.blocker_bugs == 0
}',
   true, '1.0.0', 'a0000000-0000-0000-0000-000000000001', NOW(), NOW())
ON CONFLICT (id) DO NOTHING;

-- =========================================================================
-- SECTION 9: POLICY EVALUATIONS
-- Sample policy evaluation results
-- =========================================================================

INSERT INTO policy_evaluations (id, gate_id, policy_id, result, details, evaluated_at, created_at)
VALUES
  -- BFlow G0.1 evaluations
  ('i0000000-0000-0000-0000-000000000001', 'e0000000-0000-0000-0000-000000000001',
   'h0000000-0000-0000-0000-000000000001', 'PASS',
   '{"message": "Problem statement document found", "evidence_id": "g0000000-0000-0000-0000-000000000001"}',
   '2025-10-09 14:00:00', '2025-10-09 14:00:00'),

  ('i0000000-0000-0000-0000-000000000002', 'e0000000-0000-0000-0000-000000000001',
   'h0000000-0000-0000-0000-000000000002', 'PASS',
   '{"message": "User research data found", "evidence_id": "g0000000-0000-0000-0000-000000000002"}',
   '2025-10-09 14:00:00', '2025-10-09 14:00:00'),

  -- BFlow G1 evaluations
  ('i0000000-0000-0000-0000-000000000003', 'e0000000-0000-0000-0000-000000000003',
   'h0000000-0000-0000-0000-000000000004', 'PASS',
   '{"message": "FRD document found", "evidence_id": "g0000000-0000-0000-0000-000000000004"}',
   '2025-10-28 10:00:00', '2025-10-28 10:00:00'),

  ('i0000000-0000-0000-0000-000000000004', 'e0000000-0000-0000-0000-000000000003',
   'h0000000-0000-0000-0000-000000000005', 'PASS',
   '{"message": "OpenAPI spec found", "evidence_id": "g0000000-0000-0000-0000-000000000005"}',
   '2025-10-28 10:00:00', '2025-10-28 10:00:00'),

  ('i0000000-0000-0000-0000-000000000005', 'e0000000-0000-0000-0000-000000000003',
   'h0000000-0000-0000-0000-000000000006', 'PASS',
   '{"message": "Data model ERD found", "evidence_id": "g0000000-0000-0000-0000-000000000006"}',
   '2025-10-28 10:00:00', '2025-10-28 10:00:00'),

  -- BFlow G2 evaluations
  ('i0000000-0000-0000-0000-000000000006', 'e0000000-0000-0000-0000-000000000004',
   'h0000000-0000-0000-0000-000000000007', 'PASS',
   '{"message": "Architecture document found", "evidence_id": "g0000000-0000-0000-0000-000000000007"}',
   '2025-11-09 16:00:00', '2025-11-09 16:00:00'),

  ('i0000000-0000-0000-0000-000000000007', 'e0000000-0000-0000-0000-000000000004',
   'h0000000-0000-0000-0000-000000000008', 'PASS',
   '{"message": "Security baseline found", "evidence_id": "g0000000-0000-0000-0000-000000000008"}',
   '2025-11-09 16:00:00', '2025-11-09 16:00:00')
ON CONFLICT (id) DO NOTHING;

-- =========================================================================
-- SECTION 10: AUDIT LOGS
-- Sample audit trail entries
-- =========================================================================

INSERT INTO audit_logs (id, user_id, action, entity_type, entity_id, details, ip_address, user_agent, created_at)
VALUES
  ('j0000000-0000-0000-0000-000000000001', 'b0000000-0000-0000-0000-000000000003',
   'CREATE', 'PROJECT', 'c0000000-0000-0000-0000-000000000001',
   '{"project_name": "BFlow Workflow Automation - v3.0"}',
   '192.168.1.100', 'Mozilla/5.0 Chrome/119.0', '2025-10-01 10:00:00'),

  ('j0000000-0000-0000-0000-000000000002', 'b0000000-0000-0000-0000-000000000003',
   'CREATE', 'GATE', 'e0000000-0000-0000-0000-000000000001',
   '{"gate_name": "G0.1", "stage": "WHY"}',
   '192.168.1.100', 'Mozilla/5.0 Chrome/119.0', '2025-10-05 10:00:00'),

  ('j0000000-0000-0000-0000-000000000003', 'b0000000-0000-0000-0000-000000000003',
   'UPLOAD', 'EVIDENCE', 'g0000000-0000-0000-0000-000000000001',
   '{"file_name": "problem-statement.pdf", "file_size": 2048576}',
   '192.168.1.100', 'Mozilla/5.0 Chrome/119.0', '2025-10-05 11:00:00'),

  ('j0000000-0000-0000-0000-000000000004', 'b0000000-0000-0000-0000-000000000002',
   'APPROVE', 'GATE', 'e0000000-0000-0000-0000-000000000001',
   '{"status": "APPROVED", "comment": "Problem statement is clear and measurable"}',
   '192.168.1.101', 'Mozilla/5.0 Chrome/119.0', '2025-10-10 15:00:00'),

  ('j0000000-0000-0000-0000-000000000005', 'a0000000-0000-0000-0000-000000000001',
   'LOGIN', 'USER', 'a0000000-0000-0000-0000-000000000001',
   '{"method": "email_password"}',
   '192.168.1.1', 'Mozilla/5.0 Chrome/119.0', NOW())
ON CONFLICT (id) DO NOTHING;

-- =========================================================================
-- SECTION 11: VERIFICATION QUERIES
-- Run these queries to verify seed data is loaded correctly
-- =========================================================================

-- Verify users count
SELECT 'Users' as entity, COUNT(*) as count FROM users;

-- Verify projects count
SELECT 'Projects' as entity, COUNT(*) as count FROM projects WHERE deleted_at IS NULL;

-- Verify gates count by status
SELECT status, COUNT(*) as count FROM gates WHERE deleted_at IS NULL GROUP BY status;

-- Verify evidence count
SELECT 'Evidence' as entity, COUNT(*) as count FROM gate_evidence WHERE deleted_at IS NULL;

-- Verify policies count
SELECT 'Policies' as entity, COUNT(*) as count FROM policies WHERE is_active = true;

-- Summary report
SELECT
  (SELECT COUNT(*) FROM users) as total_users,
  (SELECT COUNT(*) FROM projects WHERE deleted_at IS NULL) as total_projects,
  (SELECT COUNT(*) FROM gates WHERE deleted_at IS NULL) as total_gates,
  (SELECT COUNT(*) FROM gate_evidence WHERE deleted_at IS NULL) as total_evidence,
  (SELECT COUNT(*) FROM policies WHERE is_active = true) as total_policies;

-- =========================================================================
-- END OF SEED DATA
-- =========================================================================
