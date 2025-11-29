"""
=========================================================================
Seed Data Migration - NQH-Bot Platform Team (Real Data)
SDLC Orchestrator - Stage 03 (BUILD)

Version: 3.0.0
Date: November 29, 2025
Status: ACTIVE - Week 13 E2E Testing
Authority: CPO + Backend Lead + CTO Approved
Foundation: SDLC 4.9.1 Complete Lifecycle
Framework: Zero Mock Policy - Real NQH Team Data

Purpose:
- Real NQH-Bot Platform team data for E2E testing
- Reflects actual organizational structure:
  * CEO: Tai Dang (taidt@mtsolution.com.vn) - leads 2 teams
  * CPO: Dung Luong (dunglt@mtsolution.com.vn)
  * CTO: Hiep Dinh (dvhiep@nqh.com.vn)
  * Local Team Lead: Endior (dangtt1971@gmail.com)
  * Remote Team Lead: Ms Hang Le (ltmhang@nqh.com.vn)
- 5 real projects from NQH-Bot Platform development
- 13 system roles (CEO, CTO, CPO, EM, TL, DEV, QA, etc.)
- 3 AI providers (Claude Sonnet 4.5, GPT-4o, Gemini 2.0 Flash)
- 19 gates across projects (13 APPROVED, 4 PENDING, 2 DRAFT)

Synchronized with: docs/04-Testing-Quality/07-E2E-Testing/DEMO-SEED-DATA.sql

Zero Mock Policy: Real team data with actual emails, projects, gates
=========================================================================

Revision ID: a502ce0d23a7
Revises: dce31118ffb7
Create Date: 2025-11-14 16:51:24.497047
"""
from datetime import datetime, timedelta
import json
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = 'a502ce0d23a7'
down_revision: Union[str, None] = 'dce31118ffb7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """
    Insert NQH-Bot Platform team seed data.

    Data Includes:
    - 13 SDLC system roles (CEO, CTO, CPO, EM, TL, DEV, QA, DevOps, Security, PM, BA, CIO, CFO)
    - 12 users (1 admin + 11 NQH-Bot Platform team members)
    - 5 active projects (NQH-Bot Platform + modules)
    - 19 gates (13 APPROVED, 4 PENDING, 2 DRAFT)
    - 16 gate approvals
    - 3 AI providers (Claude, GPT-4o, Gemini)
    """
    conn = op.get_bind()

    # =========================================================================
    # 1. ROLES (13 system roles)
    # Using fixed UUIDs for consistency with DEMO-SEED-DATA.sql
    # =========================================================================

    # Fixed role IDs for consistent reference
    ceo_role_id = "r0000000-0000-0000-0000-000000000001"
    cto_role_id = "r0000000-0000-0000-0000-000000000002"
    cpo_role_id = "r0000000-0000-0000-0000-000000000003"
    cio_role_id = "r0000000-0000-0000-0000-000000000004"
    cfo_role_id = "r0000000-0000-0000-0000-000000000005"
    em_role_id = "r0000000-0000-0000-0000-000000000006"
    tl_role_id = "r0000000-0000-0000-0000-000000000007"
    dev_role_id = "r0000000-0000-0000-0000-000000000008"
    qa_role_id = "r0000000-0000-0000-0000-000000000009"
    devops_role_id = "r0000000-0000-0000-0000-000000000010"
    security_role_id = "r0000000-0000-0000-0000-000000000011"
    pm_role_id = "r0000000-0000-0000-0000-000000000012"
    ba_role_id = "r0000000-0000-0000-0000-000000000013"

    roles_data = [
        # C-Suite (5 roles)
        {'id': ceo_role_id, 'name': 'ceo', 'display_name': 'Chief Executive Officer', 'description': 'Final approval authority, strategic alignment, budget decisions, go/no-go gates', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': cto_role_id, 'name': 'cto', 'display_name': 'Chief Technology Officer', 'description': 'Technical architecture review, security standards, performance requirements', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': cpo_role_id, 'name': 'cpo', 'display_name': 'Chief Product Officer', 'description': 'Product strategy, user experience, business value validation', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': cio_role_id, 'name': 'cio', 'display_name': 'Chief Information Officer', 'description': 'IT infrastructure, data governance, compliance oversight', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': cfo_role_id, 'name': 'cfo', 'display_name': 'Chief Financial Officer', 'description': 'Budget approval, financial controls, cost management', 'is_active': True, 'created_at': datetime.utcnow()},

        # Engineering (6 roles)
        {'id': em_role_id, 'name': 'em', 'display_name': 'Engineering Manager', 'description': 'Team leadership, project planning, gate submissions, resource allocation', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': tl_role_id, 'name': 'tl', 'display_name': 'Tech Lead', 'description': 'Technical decisions, code review, architecture design, mentorship', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': dev_role_id, 'name': 'dev', 'display_name': 'Developer', 'description': 'Code implementation, unit testing, evidence upload, SDLC execution', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': qa_role_id, 'name': 'qa', 'display_name': 'QA Engineer', 'description': 'Test planning, quality gates, bug tracking, test automation', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': devops_role_id, 'name': 'devops', 'display_name': 'DevOps Engineer', 'description': 'CI/CD pipelines, deployment automation, infrastructure management', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': security_role_id, 'name': 'security', 'display_name': 'Security Engineer', 'description': 'Security review, vulnerability scanning, compliance verification', 'is_active': True, 'created_at': datetime.utcnow()},

        # Product & Business (2 roles)
        {'id': pm_role_id, 'name': 'pm', 'display_name': 'Product Manager', 'description': 'Requirements definition, roadmap planning, stakeholder communication', 'is_active': True, 'created_at': datetime.utcnow()},
        {'id': ba_role_id, 'name': 'ba', 'display_name': 'Business Analyst', 'description': 'Data analysis, metrics tracking, business intelligence, reporting', 'is_active': True, 'created_at': datetime.utcnow()},
    ]

    # Insert roles
    for role in roles_data:
        conn.execute(
            text("""
                INSERT INTO roles (id, name, display_name, description, is_active, created_at)
                VALUES (:id, :name, :display_name, :description, :is_active, :created_at)
                ON CONFLICT (id) DO NOTHING
            """),
            role
        )

    # =========================================================================
    # 2. USERS (12 users: 1 admin + 11 NQH-Bot Platform team)
    # =========================================================================

    # Pre-computed password hash for "password123" (bcrypt, cost=12)
    password_hash = "$2b$12$T6BJlzPawHNYv4UdrSCjleDH1o9UY6ho5859bNhNHIavyx7miFshu"

    # Pre-computed password hash for "Admin@123" (bcrypt, cost=12) - for admin user
    admin_password_hash = "$2b$12$gbdaanPRphcu5qGFfd1AxuPE9tEuPDjazMcnz8oSfqDKE/T1961tm"

    # Fixed user IDs for consistent reference
    admin_user_id = "a0000000-0000-0000-0000-000000000001"
    ceo_user_id = "b0000000-0000-0000-0000-000000000001"  # Tai Dang
    cpo_user_id = "b0000000-0000-0000-0000-000000000002"  # Dung Luong
    cto_user_id = "b0000000-0000-0000-0000-000000000003"  # Hiep Dinh
    local_tl_user_id = "b0000000-0000-0000-0000-000000000004"  # Endior
    remote_tl_user_id = "b0000000-0000-0000-0000-000000000005"  # Hang Le
    local_dev1_user_id = "b0000000-0000-0000-0000-000000000006"
    local_dev2_user_id = "b0000000-0000-0000-0000-000000000007"
    remote_dev1_user_id = "b0000000-0000-0000-0000-000000000008"
    remote_dev2_user_id = "b0000000-0000-0000-0000-000000000009"
    qa_lead_user_id = "b0000000-0000-0000-0000-000000000010"
    inactive_user_id = "b0000000-0000-0000-0000-000000000011"

    users_data = [
        # System Admin User (for E2E tests and initial setup)
        {'id': admin_user_id, 'email': 'admin@sdlc-orchestrator.io', 'name': 'System Administrator', 'password_hash': admin_password_hash, 'is_active': True, 'is_superuser': True, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},

        # NQH-Bot Platform Team - REAL team structure
        # CEO - Tai Dang (leads both Local + Remote teams)
        {'id': ceo_user_id, 'email': 'taidt@mtsolution.com.vn', 'name': 'Tai Dang', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},

        # CPO - Dung Luong (Product strategy, business gates approval)
        {'id': cpo_user_id, 'email': 'dunglt@mtsolution.com.vn', 'name': 'Dung Luong', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},

        # CTO - Hiep Dinh (Technical authority, G2/G3 gates approval)
        {'id': cto_user_id, 'email': 'dvhiep@nqh.com.vn', 'name': 'Hiep Dinh', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},

        # Local Team Lead - Endior
        {'id': local_tl_user_id, 'email': 'dangtt1971@gmail.com', 'name': 'Endior', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},

        # Remote Team Lead - Ms Hang Le
        {'id': remote_tl_user_id, 'email': 'ltmhang@nqh.com.vn', 'name': 'Hang Le', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},

        # Local Team Developers
        {'id': local_dev1_user_id, 'email': 'local.dev1@nqh.com.vn', 'name': 'Local Dev 1', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
        {'id': local_dev2_user_id, 'email': 'local.dev2@nqh.com.vn', 'name': 'Local Dev 2', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},

        # Remote Team Developers
        {'id': remote_dev1_user_id, 'email': 'remote.dev1@nqh.com.vn', 'name': 'Remote Dev 1', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
        {'id': remote_dev2_user_id, 'email': 'remote.dev2@nqh.com.vn', 'name': 'Remote Dev 2', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},

        # QA Lead
        {'id': qa_lead_user_id, 'email': 'qa.lead@nqh.com.vn', 'name': 'QA Lead', 'password_hash': password_hash, 'is_active': True, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},

        # Inactive User (for testing inactive account scenarios)
        {'id': inactive_user_id, 'email': 'inactive@nqh.com.vn', 'name': 'Inactive User', 'password_hash': password_hash, 'is_active': False, 'is_superuser': False, 'mfa_enabled': False, 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()},
    ]

    # Insert users
    for user in users_data:
        conn.execute(
            text("""
                INSERT INTO users (id, email, name, password_hash, is_active, is_superuser,
                                 mfa_enabled, created_at, updated_at)
                VALUES (:id, :email, :name, :password_hash, :is_active, :is_superuser,
                        :mfa_enabled, :created_at, :updated_at)
                ON CONFLICT (id) DO NOTHING
            """),
            user
        )

    # =========================================================================
    # 3. PROJECTS (5 active + 1 archived)
    # =========================================================================

    # Fixed project IDs for consistent reference
    main_project_id = "c0000000-0000-0000-0000-000000000001"  # NQH-Bot Platform
    analytics_project_id = "c0000000-0000-0000-0000-000000000002"  # Analytics Module
    nlp_project_id = "c0000000-0000-0000-0000-000000000003"  # NLP Engine
    crm_project_id = "c0000000-0000-0000-0000-000000000004"  # CRM Integration
    mobile_project_id = "c0000000-0000-0000-0000-000000000005"  # Mobile App
    archived_project_id = "c0000000-0000-0000-0000-000000000006"  # Archived PoC

    projects_data = [
        {
            'id': main_project_id,
            'name': 'NQH-Bot Platform',
            'slug': 'nqh-bot-platform',
            'description': 'AI-powered chatbot platform for enterprise automation. Multi-channel support (Telegram, Zalo, Facebook), Vietnamese NLP, CRM integration. Led by CEO Tai Dang with Local + Remote teams.',
            'owner_id': ceo_user_id,
            'is_active': True,
            'created_at': datetime(2025, 9, 1, 9, 0, 0),
            'updated_at': datetime.utcnow(),
        },
        {
            'id': analytics_project_id,
            'name': 'NQH-Bot Analytics Module',
            'slug': 'nqh-bot-analytics',
            'description': 'Real-time analytics dashboard for bot performance. Conversation metrics, user engagement, response time tracking. Handled by Remote Team.',
            'owner_id': remote_tl_user_id,
            'is_active': True,
            'created_at': datetime(2025, 10, 15, 10, 0, 0),
            'updated_at': datetime.utcnow(),
        },
        {
            'id': nlp_project_id,
            'name': 'NQH-Bot NLP Engine',
            'slug': 'nqh-bot-nlp-engine',
            'description': 'Vietnamese NLP processing engine. Intent detection, entity extraction, sentiment analysis. Uses Ollama + Claude fallback. Handled by Local Team.',
            'owner_id': local_tl_user_id,
            'is_active': True,
            'created_at': datetime(2025, 10, 1, 8, 0, 0),
            'updated_at': datetime.utcnow(),
        },
        {
            'id': crm_project_id,
            'name': 'NQH-Bot CRM Integration',
            'slug': 'nqh-bot-crm',
            'description': 'CRM integration module. Sync conversations to Salesforce/HubSpot, lead scoring, customer 360 view. Joint effort Local + Remote teams.',
            'owner_id': cto_user_id,
            'is_active': True,
            'created_at': datetime(2025, 8, 15, 9, 0, 0),
            'updated_at': datetime.utcnow(),
        },
        {
            'id': mobile_project_id,
            'name': 'NQH-Bot Mobile App',
            'slug': 'nqh-bot-mobile',
            'description': 'Mobile companion app for bot management. Push notifications, quick replies, admin dashboard. React Native cross-platform.',
            'owner_id': cpo_user_id,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
    ]

    # Insert projects
    for project in projects_data:
        conn.execute(
            text("""
                INSERT INTO projects (id, name, slug, description, owner_id, is_active, created_at, updated_at)
                VALUES (:id, :name, :slug, :description, :owner_id, :is_active, :created_at, :updated_at)
                ON CONFLICT (id) DO UPDATE SET updated_at = NOW()
            """),
            project
        )

    # =========================================================================
    # 4. PROJECT MEMBERS
    # =========================================================================

    project_members_data = [
        # NQH-Bot Platform Main Project (CEO + CTO + CPO + Both TLs + All Devs)
        {'id': 'd0000000-0000-0000-0000-000000000001', 'project_id': main_project_id, 'user_id': ceo_user_id, 'role': 'owner', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000002', 'project_id': main_project_id, 'user_id': cpo_user_id, 'role': 'admin', 'invited_by': ceo_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000003', 'project_id': main_project_id, 'user_id': cto_user_id, 'role': 'admin', 'invited_by': ceo_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000004', 'project_id': main_project_id, 'user_id': local_tl_user_id, 'role': 'admin', 'invited_by': ceo_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000005', 'project_id': main_project_id, 'user_id': remote_tl_user_id, 'role': 'admin', 'invited_by': ceo_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000006', 'project_id': main_project_id, 'user_id': local_dev1_user_id, 'role': 'member', 'invited_by': local_tl_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000007', 'project_id': main_project_id, 'user_id': local_dev2_user_id, 'role': 'member', 'invited_by': local_tl_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000008', 'project_id': main_project_id, 'user_id': remote_dev1_user_id, 'role': 'member', 'invited_by': remote_tl_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000009', 'project_id': main_project_id, 'user_id': remote_dev2_user_id, 'role': 'member', 'invited_by': remote_tl_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000010', 'project_id': main_project_id, 'user_id': qa_lead_user_id, 'role': 'member', 'invited_by': ceo_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},

        # NQH-Bot Analytics Module (Remote Team)
        {'id': 'd0000000-0000-0000-0000-000000000011', 'project_id': analytics_project_id, 'user_id': remote_tl_user_id, 'role': 'owner', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000012', 'project_id': analytics_project_id, 'user_id': remote_dev1_user_id, 'role': 'member', 'invited_by': remote_tl_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000013', 'project_id': analytics_project_id, 'user_id': remote_dev2_user_id, 'role': 'member', 'invited_by': remote_tl_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000014', 'project_id': analytics_project_id, 'user_id': ceo_user_id, 'role': 'admin', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},

        # NQH-Bot NLP Engine (Local Team)
        {'id': 'd0000000-0000-0000-0000-000000000015', 'project_id': nlp_project_id, 'user_id': local_tl_user_id, 'role': 'owner', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000016', 'project_id': nlp_project_id, 'user_id': local_dev1_user_id, 'role': 'member', 'invited_by': local_tl_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000017', 'project_id': nlp_project_id, 'user_id': local_dev2_user_id, 'role': 'member', 'invited_by': local_tl_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000018', 'project_id': nlp_project_id, 'user_id': cto_user_id, 'role': 'admin', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},

        # NQH-Bot CRM Integration (CTO + Both Teams)
        {'id': 'd0000000-0000-0000-0000-000000000019', 'project_id': crm_project_id, 'user_id': cto_user_id, 'role': 'owner', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000020', 'project_id': crm_project_id, 'user_id': local_tl_user_id, 'role': 'admin', 'invited_by': cto_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000021', 'project_id': crm_project_id, 'user_id': remote_tl_user_id, 'role': 'admin', 'invited_by': cto_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000022', 'project_id': crm_project_id, 'user_id': qa_lead_user_id, 'role': 'member', 'invited_by': cto_user_id, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},

        # NQH-Bot Mobile App (CPO + Selected team)
        {'id': 'd0000000-0000-0000-0000-000000000023', 'project_id': mobile_project_id, 'user_id': cpo_user_id, 'role': 'owner', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000024', 'project_id': mobile_project_id, 'user_id': ceo_user_id, 'role': 'admin', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},

        # Platform Admin access to all projects
        {'id': 'd0000000-0000-0000-0000-000000000025', 'project_id': main_project_id, 'user_id': admin_user_id, 'role': 'admin', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000026', 'project_id': analytics_project_id, 'user_id': admin_user_id, 'role': 'admin', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000027', 'project_id': nlp_project_id, 'user_id': admin_user_id, 'role': 'admin', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000028', 'project_id': crm_project_id, 'user_id': admin_user_id, 'role': 'admin', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
        {'id': 'd0000000-0000-0000-0000-000000000029', 'project_id': mobile_project_id, 'user_id': admin_user_id, 'role': 'admin', 'invited_by': None, 'invited_at': datetime.utcnow(), 'joined_at': datetime.utcnow(), 'created_at': datetime.utcnow()},
    ]

    for member in project_members_data:
        conn.execute(
            text("""
                INSERT INTO project_members (id, project_id, user_id, role, invited_by, invited_at, joined_at, created_at)
                VALUES (:id, :project_id, :user_id, :role, :invited_by, :invited_at, :joined_at, :created_at)
                ON CONFLICT (id) DO NOTHING
            """),
            member
        )

    # =========================================================================
    # 5. USER ROLES (Assign system roles to users)
    # =========================================================================

    user_roles_data = [
        # NQH-Bot Platform team roles
        {'user_id': ceo_user_id, 'role_id': ceo_role_id},
        {'user_id': cpo_user_id, 'role_id': cpo_role_id},
        {'user_id': cto_user_id, 'role_id': cto_role_id},
        {'user_id': local_tl_user_id, 'role_id': tl_role_id},
        {'user_id': remote_tl_user_id, 'role_id': tl_role_id},
        {'user_id': local_dev1_user_id, 'role_id': dev_role_id},
        {'user_id': local_dev2_user_id, 'role_id': dev_role_id},
        {'user_id': remote_dev1_user_id, 'role_id': dev_role_id},
        {'user_id': remote_dev2_user_id, 'role_id': dev_role_id},
        {'user_id': qa_lead_user_id, 'role_id': qa_role_id},
    ]

    for user_role in user_roles_data:
        conn.execute(
            text("""
                INSERT INTO user_roles (user_id, role_id)
                VALUES (:user_id, :role_id)
                ON CONFLICT DO NOTHING
            """),
            user_role
        )

    # =========================================================================
    # 6. AI PROVIDERS (3 providers: Claude, GPT-4o, Gemini)
    # =========================================================================

    ai_providers_data = [
        {
            'id': 'p0000000-0000-0000-0000-000000000001',
            'provider_name': 'Anthropic',
            'provider_type': 'claude',
            'model_name': 'claude-sonnet-4-5-20250929',
            'api_key_encrypted': '',
            'cost_per_1k_input_tokens': 0.003,
            'cost_per_1k_output_tokens': 0.015,
            'max_tokens': 8192,
            'temperature': 0.7,
            'priority': 1,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'id': 'p0000000-0000-0000-0000-000000000002',
            'provider_name': 'OpenAI',
            'provider_type': 'gpt',
            'model_name': 'gpt-4o-2024-11-20',
            'api_key_encrypted': '',
            'cost_per_1k_input_tokens': 0.0025,
            'cost_per_1k_output_tokens': 0.010,
            'max_tokens': 16384,
            'temperature': 0.7,
            'priority': 2,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
        {
            'id': 'p0000000-0000-0000-0000-000000000003',
            'provider_name': 'Google',
            'provider_type': 'gemini',
            'model_name': 'gemini-2.0-flash-exp',
            'api_key_encrypted': '',
            'cost_per_1k_input_tokens': 0.000075,
            'cost_per_1k_output_tokens': 0.0003,
            'max_tokens': 8192,
            'temperature': 0.7,
            'priority': 3,
            'is_active': True,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
        },
    ]

    for provider in ai_providers_data:
        conn.execute(
            text("""
                INSERT INTO ai_providers (id, provider_name, provider_type, model_name,
                                        api_key_encrypted, cost_per_1k_input_tokens,
                                        cost_per_1k_output_tokens, max_tokens, temperature,
                                        priority, is_active, created_at, updated_at)
                VALUES (:id, :provider_name, :provider_type, :model_name,
                        :api_key_encrypted, :cost_per_1k_input_tokens,
                        :cost_per_1k_output_tokens, :max_tokens, :temperature,
                        :priority, :is_active, :created_at, :updated_at)
                ON CONFLICT (id) DO NOTHING
            """),
            provider
        )

    # =========================================================================
    # 7. GATES (19 gates across 5 projects)
    # =========================================================================

    gates_data = [
        # NQH-Bot Platform Main (WHY → WHAT → HOW complete, BUILD in progress)
        {
            'id': 'e0000000-0000-0000-0000-000000000001',
            'project_id': main_project_id,
            'gate_name': 'G0.1',
            'gate_type': 'PROBLEM_DEFINITION',
            'stage': 'WHY',
            'status': 'APPROVED',
            'created_by': ceo_user_id,
            'exit_criteria': ['Problem statement documented', 'User personas defined (5 types)', 'Market research: $2B VN chatbot market'],
            'created_at': datetime(2025, 9, 5, 10, 0, 0),
            'updated_at': datetime(2025, 9, 10, 15, 0, 0),
            'approved_at': datetime(2025, 9, 10, 15, 0, 0),
            'description': 'Problem validated: Enterprise chatbots have 40% failure rate in Vietnamese NLP, 70% user drop-off in complex workflows.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000002',
            'project_id': main_project_id,
            'gate_name': 'G0.2',
            'gate_type': 'SOLUTION_DIVERSITY',
            'stage': 'WHY',
            'status': 'APPROVED',
            'created_by': ceo_user_id,
            'exit_criteria': ['5 solution alternatives evaluated', 'ROI: 300% Year 1', 'Ollama vs Claude cost analysis complete'],
            'created_at': datetime(2025, 9, 10, 10, 0, 0),
            'updated_at': datetime(2025, 9, 15, 16, 0, 0),
            'approved_at': datetime(2025, 9, 15, 16, 0, 0),
            'description': '5 solutions evaluated: Multi-channel bot with Vietnamese NLP selected. Ollama local AI for cost reduction.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000003',
            'project_id': main_project_id,
            'gate_name': 'G1',
            'gate_type': 'PLANNING_COMPLETE',
            'stage': 'WHAT',
            'status': 'APPROVED',
            'created_by': cpo_user_id,
            'exit_criteria': ['FRD complete (25 FRs)', 'API spec defined (2,100 lines)', 'Data model designed (35 tables)'],
            'created_at': datetime(2025, 9, 20, 9, 0, 0),
            'updated_at': datetime(2025, 9, 30, 14, 0, 0),
            'approved_at': datetime(2025, 9, 30, 14, 0, 0),
            'description': 'FRD approved: 25 functional requirements. API spec 2,100 lines. Data model: 35 tables.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000004',
            'project_id': main_project_id,
            'gate_name': 'G2',
            'gate_type': 'DESIGN_READY',
            'stage': 'HOW',
            'status': 'APPROVED',
            'created_by': cto_user_id,
            'exit_criteria': ['Architecture document approved', 'Security baseline OWASP ASVS L2', 'Vietnamese NLP design complete'],
            'created_at': datetime(2025, 10, 5, 10, 0, 0),
            'updated_at': datetime(2025, 10, 15, 17, 0, 0),
            'approved_at': datetime(2025, 10, 15, 17, 0, 0),
            'description': 'Architecture: Microservices with event-driven messaging. Vietnamese NLP pipeline. Multi-channel integration.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000005',
            'project_id': main_project_id,
            'gate_name': 'G3',
            'gate_type': 'SHIP_READY',
            'stage': 'BUILD',
            'status': 'PENDING_APPROVAL',
            'created_by': local_tl_user_id,
            'exit_criteria': ['Core features implemented', 'Unit tests 90%+', 'Integration tests passing', 'NLP accuracy 85%+'],
            'created_at': datetime(2025, 11, 1, 8, 0, 0),
            'updated_at': datetime.utcnow(),
            'approved_at': None,
            'description': 'MVP 75% complete. Telegram + Zalo channels working. Vietnamese NLP: 85% accuracy. CRM sync in progress.',
        },

        # NQH-Bot Analytics Module (Remote Team)
        {
            'id': 'e0000000-0000-0000-0000-000000000006',
            'project_id': analytics_project_id,
            'gate_name': 'G0.1',
            'gate_type': 'PROBLEM_DEFINITION',
            'stage': 'WHY',
            'status': 'APPROVED',
            'created_by': remote_tl_user_id,
            'exit_criteria': ['Analytics requirements gathered', 'KPI definitions documented'],
            'created_at': datetime(2025, 10, 18, 10, 0, 0),
            'updated_at': datetime(2025, 10, 22, 15, 0, 0),
            'approved_at': datetime(2025, 10, 22, 15, 0, 0),
            'description': 'Problem: No visibility into bot performance. Businesses cant measure ROI.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000007',
            'project_id': analytics_project_id,
            'gate_name': 'G0.2',
            'gate_type': 'SOLUTION_DIVERSITY',
            'stage': 'WHY',
            'status': 'APPROVED',
            'created_by': remote_tl_user_id,
            'exit_criteria': ['3 alternatives evaluated', 'Grafana AGPL containment validated'],
            'created_at': datetime(2025, 10, 22, 10, 0, 0),
            'updated_at': datetime(2025, 10, 28, 16, 0, 0),
            'approved_at': datetime(2025, 10, 28, 16, 0, 0),
            'description': 'Real-time dashboard with Grafana embed selected over custom charting.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000008',
            'project_id': analytics_project_id,
            'gate_name': 'G1',
            'gate_type': 'PLANNING_COMPLETE',
            'stage': 'WHAT',
            'status': 'PENDING_APPROVAL',
            'created_by': remote_dev1_user_id,
            'exit_criteria': ['FRD complete', 'Dashboard wireframes approved', 'Data warehouse schema'],
            'created_at': datetime(2025, 11, 5, 9, 0, 0),
            'updated_at': datetime.utcnow(),
            'approved_at': None,
            'description': 'Analytics FRD 90% complete. Missing: Custom report builder specs.',
        },

        # NQH-Bot NLP Engine (Local Team)
        {
            'id': 'e0000000-0000-0000-0000-000000000009',
            'project_id': nlp_project_id,
            'gate_name': 'G0.1',
            'gate_type': 'PROBLEM_DEFINITION',
            'stage': 'WHY',
            'status': 'APPROVED',
            'created_by': local_tl_user_id,
            'exit_criteria': ['Vietnamese NLP benchmarks documented', '5 competitor analysis complete'],
            'created_at': datetime(2025, 10, 5, 10, 0, 0),
            'updated_at': datetime(2025, 10, 10, 15, 0, 0),
            'approved_at': datetime(2025, 10, 10, 15, 0, 0),
            'description': 'Problem: Vietnamese NLP accuracy in existing solutions: 60%. Target: 90%+.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000010',
            'project_id': nlp_project_id,
            'gate_name': 'G0.2',
            'gate_type': 'SOLUTION_DIVERSITY',
            'stage': 'WHY',
            'status': 'APPROVED',
            'created_by': local_tl_user_id,
            'exit_criteria': ['Ollama vs GPT-4 benchmarks', 'Cost analysis: $50 vs $1000/month', 'Latency: <100ms target'],
            'created_at': datetime(2025, 10, 10, 10, 0, 0),
            'updated_at': datetime(2025, 10, 15, 16, 0, 0),
            'approved_at': datetime(2025, 10, 15, 16, 0, 0),
            'description': 'Hybrid approach: Ollama (local) + Claude fallback (complex queries). 95% cost reduction.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000011',
            'project_id': nlp_project_id,
            'gate_name': 'G1',
            'gate_type': 'PLANNING_COMPLETE',
            'stage': 'WHAT',
            'status': 'APPROVED',
            'created_by': local_dev1_user_id,
            'exit_criteria': ['NLP pipeline designed', 'Training data spec', 'Ollama integration contract'],
            'created_at': datetime(2025, 10, 20, 9, 0, 0),
            'updated_at': datetime(2025, 10, 28, 14, 0, 0),
            'approved_at': datetime(2025, 10, 28, 14, 0, 0),
            'description': 'NLP Engine FRD: Intent detection, entity extraction, sentiment analysis.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000012',
            'project_id': nlp_project_id,
            'gate_name': 'G2',
            'gate_type': 'DESIGN_READY',
            'stage': 'HOW',
            'status': 'DRAFT',
            'created_by': local_dev1_user_id,
            'exit_criteria': ['NLP pipeline architecture', 'Model selection rationale', 'Fallback chain design'],
            'created_at': datetime(2025, 11, 10, 10, 0, 0),
            'updated_at': datetime.utcnow(),
            'approved_at': None,
            'description': 'NLP architecture 80% complete. Missing: Fallback strategy documentation.',
        },

        # NQH-Bot CRM Integration (CTO led)
        {
            'id': 'e0000000-0000-0000-0000-000000000013',
            'project_id': crm_project_id,
            'gate_name': 'G0.1',
            'gate_type': 'PROBLEM_DEFINITION',
            'stage': 'WHY',
            'status': 'APPROVED',
            'created_by': cto_user_id,
            'exit_criteria': ['CRM integration requirements', 'Data mapping documented'],
            'created_at': datetime(2025, 8, 20, 10, 0, 0),
            'updated_at': datetime(2025, 8, 25, 15, 0, 0),
            'approved_at': datetime(2025, 8, 25, 15, 0, 0),
            'description': 'Problem: Bot conversations not synced to CRM. Sales team loses context.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000014',
            'project_id': crm_project_id,
            'gate_name': 'G0.2',
            'gate_type': 'SOLUTION_DIVERSITY',
            'stage': 'WHY',
            'status': 'APPROVED',
            'created_by': cto_user_id,
            'exit_criteria': ['3 integration patterns evaluated', 'Webhook vs API poll comparison'],
            'created_at': datetime(2025, 8, 25, 10, 0, 0),
            'updated_at': datetime(2025, 9, 1, 16, 0, 0),
            'approved_at': datetime(2025, 9, 1, 16, 0, 0),
            'description': 'Webhook-based sync selected. Supports Salesforce, HubSpot, custom CRMs.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000015',
            'project_id': crm_project_id,
            'gate_name': 'G1',
            'gate_type': 'PLANNING_COMPLETE',
            'stage': 'WHAT',
            'status': 'APPROVED',
            'created_by': local_tl_user_id,
            'exit_criteria': ['FRD approved', 'API contracts for 3 CRMs', 'Error handling spec'],
            'created_at': datetime(2025, 9, 10, 9, 0, 0),
            'updated_at': datetime(2025, 9, 20, 14, 0, 0),
            'approved_at': datetime(2025, 9, 20, 14, 0, 0),
            'description': 'CRM Integration FRD complete. Supports 3 major CRMs + custom webhook.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000016',
            'project_id': crm_project_id,
            'gate_name': 'G2',
            'gate_type': 'DESIGN_READY',
            'stage': 'HOW',
            'status': 'APPROVED',
            'created_by': cto_user_id,
            'exit_criteria': ['Architecture document approved', 'Adapter pattern documented'],
            'created_at': datetime(2025, 10, 1, 10, 0, 0),
            'updated_at': datetime(2025, 10, 10, 17, 0, 0),
            'approved_at': datetime(2025, 10, 10, 17, 0, 0),
            'description': 'CRM adapter pattern. Event-driven sync. Retry with exponential backoff.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000017',
            'project_id': crm_project_id,
            'gate_name': 'G3',
            'gate_type': 'SHIP_READY',
            'stage': 'BUILD',
            'status': 'APPROVED',
            'created_by': cto_user_id,
            'exit_criteria': ['Core sync working', 'Tests passing', 'Performance: <500ms sync'],
            'created_at': datetime(2025, 10, 20, 8, 0, 0),
            'updated_at': datetime(2025, 11, 5, 18, 0, 0),
            'approved_at': datetime(2025, 11, 5, 18, 0, 0),
            'description': 'CRM integration MVP complete. Salesforce + HubSpot working. 99.9% sync reliability.',
        },
        {
            'id': 'e0000000-0000-0000-0000-000000000018',
            'project_id': crm_project_id,
            'gate_name': 'G4',
            'gate_type': 'TEST_COMPLETE',
            'stage': 'VERIFY',
            'status': 'PENDING_APPROVAL',
            'created_by': qa_lead_user_id,
            'exit_criteria': ['Unit tests 95%+', 'Integration tests 90%+', 'Load test: 1000 req/s'],
            'created_at': datetime(2025, 11, 10, 8, 0, 0),
            'updated_at': datetime.utcnow(),
            'approved_at': None,
            'description': 'Testing: Unit 92%, Integration 88%, E2E 75%. Pending: Load test results.',
        },

        # NQH-Bot Mobile App (WHY stage - new)
        {
            'id': 'e0000000-0000-0000-0000-000000000019',
            'project_id': mobile_project_id,
            'gate_name': 'G0.1',
            'gate_type': 'PROBLEM_DEFINITION',
            'stage': 'WHY',
            'status': 'DRAFT',
            'created_by': cpo_user_id,
            'exit_criteria': ['Problem statement documented', 'Mobile-specific user research'],
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow(),
            'approved_at': None,
            'description': 'Problem statement in progress: Mobile bot management for on-the-go admin.',
        },
    ]

    for gate in gates_data:
        # Serialize exit_criteria to JSON string for PostgreSQL JSONB
        gate_params = gate.copy()
        gate_params['exit_criteria'] = json.dumps(gate['exit_criteria'])
        conn.execute(
            text("""
                INSERT INTO gates (id, project_id, gate_name, gate_type, stage, status,
                                 created_by, exit_criteria, description, approved_at, created_at, updated_at)
                VALUES (:id, :project_id, :gate_name, :gate_type, :stage, :status,
                        :created_by, :exit_criteria::jsonb, :description, :approved_at, :created_at, :updated_at)
                ON CONFLICT (id) DO NOTHING
            """),
            gate_params
        )

    print("✅ NQH-Bot Platform seed data migration complete!")
    print("📊 Summary:")
    print("  - 13 system roles created (CEO, CTO, CPO, EM, TL, DEV, QA, DevOps, Security, PM, BA, CIO, CFO)")
    print("  - 12 users (1 admin + 11 NQH-Bot Platform team)")
    print("  - 5 active projects (Main Platform + 4 modules)")
    print("  - 19 gates (13 APPROVED, 4 PENDING, 2 DRAFT)")
    print("  - 3 AI providers configured (Claude Sonnet 4.5, GPT-4o, Gemini 2.0 Flash)")
    print("\n✅ Ready for E2E testing with real NQH-Bot Platform data!")


def downgrade() -> None:
    """
    Remove all seed data in reverse order.
    """
    conn = op.get_bind()

    # Delete in reverse order of foreign key dependencies
    conn.execute(text("DELETE FROM gates WHERE id LIKE 'e0000000%'"))
    conn.execute(text("DELETE FROM ai_providers WHERE id LIKE 'p0000000%'"))
    conn.execute(text("DELETE FROM user_roles WHERE user_id LIKE 'b0000000%'"))
    conn.execute(text("DELETE FROM project_members WHERE id LIKE 'd0000000%'"))
    conn.execute(text("DELETE FROM projects WHERE id LIKE 'c0000000%'"))
    conn.execute(text("DELETE FROM users WHERE id LIKE 'a0000000%' OR id LIKE 'b0000000%'"))
    conn.execute(text("DELETE FROM roles WHERE id LIKE 'r0000000%'"))

    print("✅ NQH-Bot Platform seed data removed successfully")
