# CLAUDE.md - AI Assistant Guidelines for SDLC 5.0.0

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

The **SDLC-Enterprise-Framework** is a universal, battle-tested AI+Human development framework (**v5.0.0**) with complete 10-Stage lifecycle (WHY → GOVERN), Governance & Compliance standards, and 4-Tier Classification system. Built through 6 months of real platform development (June-December 2025) across BFlow, NQH-Bot, and MTEP platforms, this framework achieves **14,822% ROI** through proven patterns, crisis response protocols, and implementation profiles that deliver 10x-50x productivity gains.

**What's New in 5.0.0 (December 5, 2025)**:
- ✅ **Contract-First Stage Restructuring** - INTEGRATE moved from Stage 07 → Stage 03 (API Design BEFORE coding)
- ✅ **ISO/IEC 12207:2017 Alignment** - Integration in Technical processes (pre-operation)
- ✅ **Simplified Stage Naming** - Lowercase, hyphenated stage names (foundation, planning, design, etc.)
- ✅ **Governance & Compliance Standards** - Quality Gates, Security Gates, Observability, Change Management
- ✅ **4-Tier Classification** - LITE (1-2), STANDARD (3-10), PROFESSIONAL (10-50), ENTERPRISE (50+)
- ✅ **Industry Best Practices** - CMMI v3.0, SAFe 6.0, DORA Metrics, OWASP ASVS, NIST SSDF
- ✅ **Folder Restructure** - Documentation-Standards & Governance-Compliance moved to 02-Core-Methodology

**What's in SDLC 4.9.1 (November 29, 2025)**:
- ✅ **Code File Naming Standards** - Python: snake_case, TypeScript: camelCase, React: PascalCase

**What's in SDLC 4.9 (November 13, 2025)** *(Stage order updated in 5.0.0)*:
- ✅ **Complete 10-Stage Lifecycle** - WHY → WHAT → HOW → INTEGRATE → BUILD → TEST → DEPLOY → OPERATE → COLLABORATE → GOVERN
- ✅ **Perfect /docs Alignment** - 10 SDLC stages → 10 /docs folders (00-09)
- ✅ **14,822% ROI** - 2x improvement over SDLC 4.8's 7,322%
- ✅ **BFlow 52-Day Journey** - Flagship validation, 827:1 ROI

## Key Framework Concepts

### The Complete 10-Stage Lifecycle (SDLC 5.0.0 - Contract-First Order)

```yaml
# LINEAR STAGES (Sequential per release):
Stage 00 - foundation:   WHY - Problem Definition          → 00-foundation/
Stage 01 - planning:     WHAT - Requirements Analysis      → 01-planning/
Stage 02 - design:       HOW - Architecture Design         → 02-design/
Stage 03 - integration:  API Design & System Integration   → 03-integration/     ← Contract-First (BEFORE BUILD)
Stage 04 - build:        Development & Implementation      → 04-build/
Stage 05 - test:         Quality Assurance                 → 05-test/
Stage 06 - deploy:       Release & Deployment              → 06-deploy/
Stage 07 - operate:      Production & Operations           → 07-operate/

# CONTINUOUS STAGES (Ongoing throughout project):
Stage 08 - collaborate:  Team Coordination & Communication → 08-collaborate/
Stage 09 - govern:       Governance & Compliance           → 09-govern/
```

**Why Contract-First (Stage 03 before Stage 04)?**
- OpenAPI specs must exist BEFORE coding begins
- ISO/IEC 12207:2017 Alignment: Integration in Technical processes (pre-operation)
- Prevents: "It worked in dev" syndrome when API contracts change
- DevOps CI: Continuous Integration occurs during Build, not post-production

### Code File Naming Standards (NEW in 4.9.1)

```yaml
Python Files:
  Format: snake_case
  Max Length: 50 characters
  Examples: user_service.py, invoice_repository.py

TypeScript Files:
  Format: camelCase
  Max Length: 50 characters
  Examples: arService.ts, paymentSlice.ts

React Components:
  Format: PascalCase
  Max Length: 50 characters
  Examples: ARDashboard.tsx, InvoiceList.tsx

Documentation Files:
  Format: kebab-case
  No version in filename
  Examples: SDLC-Core-Methodology.md
```

### The Six Universal Pillars (Complete Architecture)

**Pillar 0: Design Thinking Foundation**
- Stanford d.school 5-phase methodology (Empathize, Define, Ideate, Prototype, Test)
- System Thinking integration (4-layer Iceberg Model)
- 96% time savings proven (NQH-Bot: 4 weeks vs 6 months)

**Pillar 1: AI-Native Excellence Standards**
- Zero Mock Policy (679 mocks → 0 in 48 hours)
- Works with ANY AI (Claude Code, Cursor, Copilot, CodeRabbit)
- 90%+ test coverage with real services

**Pillar 2: AI+Human Orchestration Model**
- NQH-Bot: 5 specialized AI agents
- BFlow: 20x productivity with 4-6 developers
- Universal role interchangeability

**Pillar 3: Quality Governance System**
- System Thinking (4-layer Iceberg Model)
- Universal Code Review (3 tiers)
- Crisis response <48 hours proven

**Pillar 4: Documentation Permanence**
- 919 files standardized (NQH-Bot)
- Document naming standards (no sprint references)
- Archive management (99-Legacy)

**Pillar 5: Continuous Compliance Platform**
- 24-48 hour emergency response capability
- Mock Detection Agent V3.0
- Vietnamese Cultural Intelligence (96.4% accuracy)

## Repository Structure

### Core Documentation Structure (SDLC 5.0.0)
```
SDLC-Orchestrator/SDLC-Enterprise-Framework/
├── README.md                      # Main framework documentation (5.0.0)
├── CHANGELOG.md                   # Complete version history
├── CLAUDE.md                      # This file - AI assistant guidelines
│
├── 01-Overview/                   # Strategic overview
│   └── SDLC-Executive-Summary.md  # Complete 10-stage overview
│
├── 02-Core-Methodology/           # Core principles
│   ├── SDLC-Core-Methodology.md   # Complete 10-stage framework
│   ├── SDLC-Design-Thinking-Principles.md
│   ├── Documentation-Standards/   # ⭐ MOVED HERE
│   │   ├── SDLC-Document-Naming-Standards.md
│   │   ├── SDLC-Code-File-Naming-Standards.md
│   │   └── Team-Collaboration/
│   └── Governance-Compliance/     # ⭐ NEW IN 5.0
│       ├── SDLC-Quality-Gates.md
│       ├── SDLC-Security-Gates.md
│       ├── SDLC-Observability-Checklist.md
│       └── SDLC-Change-Management-Standard.md
│
├── 03-Templates-Tools/            # ⭐ REORGANIZED
│   ├── 1-AI-Tools/                # PRIMARY: 96% time savings
│   ├── 2-Agent-Templates/         # 17 AI agents configured
│   ├── 3-Manual-Templates/        # Backup templates
│   └── 4-Scripts/                 # Validators + automation
│
├── 04-Case-Studies/               # Case studies
│   ├── BFlow-52-Day-Journey-Case-Study.md  # 827:1 ROI
│   └── SDLC-Design-Thinking-Case-Study-NQH-Bot.md
│
├── 05-Implementation-Guides/      # Practical guides
│   ├── SDLC-Implementation-Guide.md
│   ├── SDLC-Universal-Code-Review-Framework.md
│   └── SDLC-Platform-Patterns.md
│
├── 06-Training-Materials/         # Training resources
├── 07-Deployment-Toolkit/         # Deployment tools
├── 08-Continuous-Improvement/     # Improvement processes
├── 09-Version-History/            # Version history
│
└── 99-Legacy/                     # Historical archive
    └── SDLC-4.9-Upgrade-Archive/  # 4.9 upgrade documents
```

## Development Workflow

### When Working with Framework Documentation
1. **Check current version**: Framework is at **SDLC 5.0.0** (December 5, 2025)
2. **Apply 10-stage lifecycle**: Contract-First order (INTEGRATE at Stage 03, before BUILD)
3. **Use English only**: All technical content must be in English
4. **Follow code file naming**: Python snake_case, TypeScript camelCase, React PascalCase
5. **Maintain version consistency**: Update to 5.0.0 across related documents

### When Updating Framework Content
1. **Review CHANGELOG.md**: Check version history
2. **Check 02-Core-Methodology/**: Core principles and 10-stage framework (Contract-First)
3. **Update consistently**: Version 5.0.0, dates December 5, 2025
4. **Preserve legacy**: Use 99-Legacy/ for superseded content
5. **Apply code file naming**: All new files must follow naming standards

### When Creating New Content
1. **Start with Design Thinking**: Apply 5-phase methodology before coding
2. **Choose Code Review tier**: Manual (Tier 1), AI-powered (Tier 2), or CodeRabbit (Tier 3)
3. **Follow 10-stage lifecycle**: Map content to appropriate stage
4. **Apply code file naming**: snake_case/camelCase/PascalCase as appropriate
5. **Measure success**: Track ROI, productivity, and quality metrics

## Framework Compliance Standards

### Required Compliance Metrics (SDLC 5.0.0)
- **Contract-First Development**: API Design (Stage 03) BEFORE coding (Stage 04)
- **10-Stage Lifecycle Applied**: All 10 stages in Contract-First order considered
- **Code File Naming**: Python snake_case, TypeScript camelCase, React PascalCase
- **Design Thinking Applied**: 5-phase methodology for all new features
- **Code Review Active**: At least Tier 1 (manual) for all code changes
- **Productivity Gains**: 10x minimum, 50x achievable
- **Mock Instance Detection**: 0 instances (absolute Zero Mock Policy)
- **Test Coverage**: >90% with real services only
- **Performance**: <50ms response time target

### Quality Gates (SDLC 5.0.0)
- **Pre-Design Thinking**: User validation before coding starts
- **Contract-First Validation**: OpenAPI spec must exist before implementation
- **Pre-commit hooks**: Block commits with mock instances
- **Code file naming validation**: Enforce naming standards
- **Code Review enforcement**: At least Tier 1 for all changes
- **CI pipeline gates**: Enforce Zero Mock and performance standards

## Framework Evolution Context

```
SDLC 1.0 (June 2025)
  ↓ CEO + Claude Code collaboration begins
SDLC 3.x (July 2025)
  ↓ BFlow Platform teaches System Thinking
SDLC 4.6 (September 24, 2025)
  ↓ 679 mock crisis → Zero Mock Policy born
SDLC 4.7 (September 27, 2025)
  ↓ Battle-tested 5 pillars (HOW to build with excellence)
SDLC 4.8 (November 7, 2025)
  ↓ Design Thinking enhancement (WHAT to build that matters)
SDLC 4.9 (November 13, 2025)
  ↓ 10-Stage Complete Lifecycle (WHY → GOVERN full journey)
SDLC 4.9.1 (November 29, 2025)
  ↓ Code File Naming Standards Restored
SDLC 5.0.0 (December 5, 2025)
  ↓ Contract-First Stage Restructuring (INTEGRATE moved 07→03)
  ↓ ISO/IEC 12207:2017 Alignment + 4-Tier Classification
  ↓ Governance & Compliance + Industry Best Practices
```

## Proven ROI (SDLC 5.0.0)
- **14,822% combined ROI** (2x improvement over 4.8)
- **827:1 ROI** - BFlow 52-day journey
- **96% time savings** with Design Thinking
- **10x-50x productivity gains** across 3 platforms
- **<2 minute code review** with CodeRabbit (Tier 3)
- **24-48 hour crisis resolution** proven multiple times
- **99.9%+ uptime** - BFlow production excellence

## Quick Reference Links

**Essential Documentation**:
- Main README: [README.md](README.md)
- Core Methodology: [02-Core-Methodology/SDLC-Core-Methodology.md](02-Core-Methodology/SDLC-Core-Methodology.md)
- Implementation Guide: [05-Implementation-Guides/SDLC-Implementation-Guide.md](05-Implementation-Guides/SDLC-Implementation-Guide.md)
- Code File Naming: [02-Core-Methodology/Documentation-Standards/SDLC-Code-File-Naming-Standards.md](02-Core-Methodology/Documentation-Standards/SDLC-Code-File-Naming-Standards.md)

**NEW in 5.0**:
- Quality Gates: [02-Core-Methodology/Governance-Compliance/SDLC-Quality-Gates.md](02-Core-Methodology/Governance-Compliance/SDLC-Quality-Gates.md)
- Security Gates: [02-Core-Methodology/Governance-Compliance/SDLC-Security-Gates.md](02-Core-Methodology/Governance-Compliance/SDLC-Security-Gates.md)
- Observability Checklist: [02-Core-Methodology/Governance-Compliance/SDLC-Observability-Checklist.md](02-Core-Methodology/Governance-Compliance/SDLC-Observability-Checklist.md)

**NEW in 4.9.1**:
- Code File Naming Standards: [02-Core-Methodology/Documentation-Standards/SDLC-Code-File-Naming-Standards.md](02-Core-Methodology/Documentation-Standards/SDLC-Code-File-Naming-Standards.md)

**NEW in 4.9**:
- BFlow 52-Day Journey: [04-Case-Studies/BFlow-52-Day-Journey-Case-Study.md](04-Case-Studies/BFlow-52-Day-Journey-Case-Study.md)

---

The framework represents not theory but battle-tested patterns from 6 months of real platform development. With SDLC 5.0.0, we achieve excellence faster: **Contract-First 10-stage lifecycle, ISO/IEC 12207 alignment, 4-tier classification, 14,822% ROI, production-ready in 1-2 weeks.**

**Migration from 4.9.x**: Use `sdlcctl migrate --from 4.9.1 --to 5.0.0 --path /path/to/project` for automated migration.

**Last Updated**: December 5, 2025
**Framework Version**: SDLC 5.0.0 (Contract-First Stage Restructuring)
**Status**: PRODUCTION READY - Contract-First 10-Stage Lifecycle + ISO/IEC 12207 Alignment + 4-Tier Classification
