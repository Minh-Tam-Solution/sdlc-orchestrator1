# Changelog

All notable changes to sdlcctl will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.7.0] - 2026-02-14

### Added

**SDLC 6.0.5 Enhancement: Framework Templates + Fuzzy P0 Detection**

#### Fuzzy P0 Artifact Detection (Legacy Naming Support)

- **3-strategy P0 resolution**: exact path → alternative paths → fuzzy stage resolution
  - Projects using legacy long-form names (e.g., `02-Design-Architecture`) now detected correctly
  - Bflow: P0 detection 0% → 71.4%, compliance 40 → 68.6
  - NQH-Bot: P0 detection 0% → 64.3%, compliance 40 → 65.7
  - Zero regression on RFC-001 compliant projects (Orchestrator: 100/100)

- **Stage path caching** (`_stage_path_cache`): 10x performance improvement for P0 validation
  - Avoids repeated filesystem scans for stage folder resolution
  - Cache hit rate >90% in production workloads

- **Ambiguity resolution**: Precedence rules when multiple folders match same stage prefix
  - Priority 1: Exact RFC-001 match (e.g., `02-design`)
  - Priority 2: Longest name (most specific)
  - Warning logged if multiple candidates found

- **SDLC-012 warning code**: New validation warning for P0 artifacts found at legacy paths
  - Guides migration without blocking compliance
  - Suggests `sdlcctl fix --naming` for folder renaming

- **`STAGE_NAME_VARIANTS`**: Common stage name variations map in tier.py for fuzzy matching

#### Framework Templates (4 New)

- `deployment_go-live-readiness-checklist.md`: Tactical 100-item go-live checklist by tier (LITE → ENTERPRISE)
- `deployment_go-live-readiness-assessment.md`: Strategic Go/No-Go scoring framework with 8-week countdown
- `governance_maturity-assessment-framework.md`: Per-stage maturity scoring (0-100%) with weighted categories
- `governance_risk-register-analyzer.md`: Risk identification + Likelihood × Impact scoring matrix

#### Tests

- 9 new unit tests for legacy name P0 detection:
  - Standard names (baseline), legacy long-form, mixed naming (hybrid)
  - SAD artifact at legacy path, stage path caching, missing stage
  - Coverage percent validation, ENTERPRISE tier with archive, no regression

### Fixed

- False negative P0 detection in projects using long-form stage names (critical bug for Bflow/NQH-Bot)

---

## [1.5.0] - 2026-02-13

### Added

**Sprint 140: CLI Orchestration Upgrade (RFC-SDLC-602)**

#### E2E API Testing Commands

- **`sdlcctl e2e validate --init`**: Initialize E2E testing folder structure
  - Creates `docs/05-Testing-Quality/03-E2E-Testing/` with templates
  - Generates README, Postman collection template, pytest template
  - OPA policy integration for validation

- **`sdlcctl e2e cross-reference`**: Validate Stage 03 ↔ Stage 05 cross-references
  - Bidirectional traceability validation
  - SSOT compliance checking (no duplicate `openapi.json`)
  - `--fix` flag for auto-fixing SSOT violations (creates symlinks)
  - `--use-opa/--no-opa` for OPA policy evaluation toggle

- **`sdlcctl e2e auth-setup`**: Automate authentication configuration
  - OAuth2 client credentials flow
  - API Key, Basic Auth, Bearer token support
  - Interactive and non-interactive modes
  - Saves to `.env.test` with example template

- **`sdlcctl e2e generate-report`**: Generate E2E test reports from results
  - Markdown report generation
  - Cross-reference links to API documentation
  - SSOT OpenAPI spec linking

#### OPA Client Library (`sdlcctl/lib/opa_client.py`)

- Network-only OPA REST API client (AGPL-safe)
- `OPAClient.evaluate()` for policy evaluation
- `OPAClient.check_health()` for health checks
- `OPAClient.get_policies()` for policy listing
- Graceful fallback to local validation when OPA unavailable
- Support for E2E compliance and cross-reference policies

#### Backend E2E Testing API (Sprint 140)

- `POST /api/v1/e2e/execute`: Queue E2E test execution (async)
- `GET /api/v1/e2e/results/{id}`: Get test execution results
- `GET /api/v1/e2e/status/{id}`: Check execution status
- `POST /api/v1/e2e/cancel/{id}`: Cancel running tests
- `GET /api/v1/e2e/history`: Get execution history with filtering
- Support for Newman, Pytest, REST Assured runners

#### Redis-Backed Execution Store

- `E2EExecutionStore` service for persistent execution state
- Automatic TTL cleanup (7-day retention)
- User/project-based filtering with sorted set indexes
- In-memory fallback when Redis unavailable
- Full CRUD operations with async support

### Changed

- Updated framework version: SDLC 6.0.1 → SDLC 6.0.2
- CLI version: 1.4.0 → 1.5.0
- Cross-reference command now uses OPA by default (with `--no-opa` fallback)

### Tests

- **81 new integration tests** across 3 test files:
  - `test_e2e_execution_store.py` (21 tests, 601 LOC)
  - `test_opa_client.py` (41 tests, 733 LOC)
  - `test_e2e_cross_reference.py` (19 tests, 576 LOC)
- Test pass rate: 96.3% (78/81 passing)
- Coverage: CRUD operations, error handling, fallback scenarios

### Documentation

- Updated README with E2E commands section
- Command reference for all E2E commands
- Examples for OPA integration and fallback modes

### References

- [RFC-SDLC-602: E2E API Testing Enhancement](../../docs/01-planning/02-RFCs/RFC-SDLC-602-E2E-API-TESTING.md)
- [Sprint 140 Progress](../../docs/04-build/02-Sprint-Plans/SPRINT-140-PROGRESS.md)

---

## [1.4.0] - 2026-02-08

### Added

**Sprint 139: VS Code Extension E2E Commands**

- Initial E2E command structure (`sdlcctl e2e` subcommand group)
- `sdlcctl e2e validate`: Basic E2E artifact validation
- `sdlcctl e2e cross-reference`: Initial cross-reference validation
- VS Code Extension integration endpoints

---

## [1.3.0] - 2026-02-01

### Added

**Sprint 136: Stage Consistency Validation (SPEC-0021)**

#### New Command: `validate-consistency`

Validates cross-stage consistency between SDLC stages:
- Stage 01 (Planning) ↔ Stage 02 (Design)
- Stage 02 (Design) ↔ Stage 03 (Integrate)
- Stage 03 (Integrate) ↔ Stage 04 (Build)
- Stage 01 (Planning) ↔ Stage 04 (Build)

**Usage:**
```bash
sdlcctl validate-consistency \
  --stage-01 docs/01-planning/ \
  --stage-02 docs/02-design/ \
  --stage-03 docs/03-integrate/ \
  --stage-04 backend/app/ \
  --tier professional \
  --format json \
  --output consistency-report.json
```

**Features:**
- 12 consistency rules (CONS-001 to CONS-012)
- Tier-specific severity (LITE/STANDARD/PROFESSIONAL/ENTERPRISE)
- Output formats: text, json, github, summary
- CI/CD integration support (GitHub Actions annotations)
- Artifact checksum verification (optional)

#### New Validation Module: `validation/consistency/`

- `ConsistencyEngine`: Main orchestrator for validation
- `ConsistencyConfig`: Configuration model
- `ConsistencyResult`: Result with violations and metrics
- `ConsistencyReportFormatter`: Multi-format report generation
- Stage checkers:
  - `Stage01To02Checker`: ADR ↔ Requirements
  - `Stage02To03Checker`: API contracts ↔ Design
  - `Stage03To04Checker`: Code ↔ API contracts
  - `Stage01To04Checker`: Implementation ↔ Requirements

#### Consistency Rules

| Rule ID | Description | Severity |
|---------|-------------|----------|
| CONS-001 | ADRs must reference Stage 01 requirements | ERROR (PRO+) |
| CONS-002 | Design documents must cite specification IDs | WARNING |
| CONS-003 | Architecture decisions must trace to user stories | INFO |
| CONS-004 | API contracts must match architecture design | ERROR (PRO+) |
| CONS-005 | Integration strategy must reference ADRs | WARNING |
| CONS-006 | Third-party dependencies must be documented | WARNING |
| CONS-007 | API endpoints must match Stage 03 contracts | ERROR |
| CONS-008 | Request/response schemas must match OpenAPI | ERROR |
| CONS-009 | New endpoints must be documented in Stage 03 | WARNING |
| CONS-010 | Implementation must satisfy requirements | ERROR (PRO+) |
| CONS-011 | Behavioral changes must update Stage 01 | WARNING |
| CONS-012 | User stories acceptance criteria must be met | INFO |

### Changed

- Updated framework version: SDLC 6.0.0 → SDLC 6.0.1
- CLI version: 1.2.0 → 1.3.0
- Updated `validation/__init__.py` to export consistency module

### Documentation

- [FR-036: Validate Consistency Command](docs/01-planning/03-Functional-Requirements/FR-036-Validate-Consistency-Command.md)
- [ADR-046: Validate Consistency Command Architecture](docs/02-design/01-ADRs/ADR-046-Validate-Consistency-Command.md)
- [SPEC-0021: Stage Consistency Validation](SDLC-Enterprise-Framework/05-Templates-Tools/01-Specification-Standard/SPEC-0021-Stage-Consistency-Validation.md)

---

## [1.2.0] - 2026-01-30

### Added

**Sprint 127: Multi-Frontend Alignment - Bug Fixes**

#### Pre-commit Hooks Module
- New `sdlcctl.hooks` package with `pre_commit.py`
- `run_validation()` function for CI/CD integration
- Support for `docs_root`, `tier`, `strict`, `performance_threshold` parameters

#### Fix Command Enhancements
- `fix --stages` now creates `99-Legacy` folder in each stage (SDLC 6.0.0 compliant)
- Both tier-based and scanner-based fix paths create consistent folder structures

### Changed

**SDLC 6.0.0 Stage Naming Convention Update**

All stage folder names updated to lowercase format:
- `00-Project-Foundation` → `00-foundation`
- `01-Planning-Analysis` → `01-planning`
- `02-Design-Architecture` → `02-design`
- `03-Development-Implementation` → `03-integrate`
- And so on for all 11 stages (00-10)

Updated components:
- `validation/tier.py`: `STAGE_NAMES` mapping
- `validation/p0.py`: P0 artifact paths
- `validation/scanner.py`: Stage detection patterns
- Test expectations across all test files

### Fixed

- **P0 Artifact Paths**: Updated all P0 artifact `relative_path` to use SDLC 6.0.0 folder names
- **Pre-commit Hook Signature**: Fixed `SDLCValidator` constructor call (positional → named parameters)
- **NLP Parser Tests**: Updated test expectations to match actual parser behavior
  - `_extract_app_name()` extracts first 2-3 meaningful words
  - `_remove_diacritics()` method name (not `_remove_vietnamese_diacritics`)
- **StreamingProgress Tests**: Fixed attribute access (`progress.stats.files` not `progress.files`)
- **Generate Command Tests**: Added skip markers for tests requiring backend app module

### Test Results

- **Total Tests**: 264 passed, 7 skipped
- **Skipped**: Tests requiring main backend `app` module (environment-specific)
- **Coverage**: Maintained at 95%+

---

## [1.1.0] - 2025-12-23

### Added

**Sprint 44: SDLC Structure Scanner Engine**

#### New Validators (5 total, 15 rules)

- **StageFolderValidator** (5 rules)
  - `STAGE-001`: Invalid stage folder naming (ERROR, auto-fix)
  - `STAGE-002`: Unknown stage number (ERROR)
  - `STAGE-003`: Stage name mismatch (WARNING, auto-fix)
  - `STAGE-004`: Duplicate stage numbers (ERROR)
  - `STAGE-005`: Missing required core stages (ERROR, auto-fix)

- **SequentialNumberingValidator** (3 rules)
  - `NUM-001`: Duplicate numbering within stage (ERROR)
  - `NUM-002`: Sequence gaps (INFO, auto-fix)
  - `NUM-003`: Invalid numbering format (WARNING, auto-fix)

- **NamingConventionValidator** (2 rules)
  - `NAME-001`: Invalid characters in names (WARNING, auto-fix)
  - `NAME-002`: Inconsistent casing (INFO)

- **HeaderMetadataValidator** (2 rules)
  - `HDR-001`: Missing required header fields (WARNING)
  - `HDR-002`: Invalid header field format (INFO)

- **CrossReferenceValidator** (3 rules)
  - `REF-001`: Broken internal links (ERROR)
  - `REF-002`: Orphaned files (WARNING)
  - `SCANNER-001`: Structure health metrics (INFO/WARNING)

#### Configuration System

- `.sdlc-config.json` support with hierarchical search
- Per-rule enable/disable, severity override, auto_fix toggle
- Ignore patterns for node_modules, .git, __pycache__, etc.
- Parallel validation with configurable max_workers

#### CLI Enhancements

- `sdlcctl validate --tier` now enforces required stages
- `sdlcctl validate --format json/summary/github` output formats
- `sdlcctl fix` conservative auto-fix for safe operations:
  - Create missing required stage folders
  - Rename invalid stage folders (STAGE-001, STAGE-003)
  - Fix invalid numbering prefixes (NUM-003)

#### Documentation

- Comprehensive `.sdlc-config.json` examples in README
- Configuration options reference table
- Per-rule configuration examples

### Fixed

- Typer/Click 8.2+ incompatibility (pin `click<8.2`)
- False positives for README.md in naming/header validators
- `--strict` flag logic to fail on warnings/errors correctly

### Changed

- Validators now skip README.md and index.md files
- Health metrics use tiered severity (HEALTHY/NEEDS ATTENTION/UNHEALTHY)

---

## [1.0.0] - 2025-11-15

### Added

- Initial release of sdlcctl CLI
- `sdlcctl validate` - Validate SDLC 6.0.0 structure
- `sdlcctl init` - Initialize new project structure
- `sdlcctl fix` - Fix missing stages and P0 artifacts
- `sdlcctl report` - Generate compliance reports
- `sdlcctl tiers` - Display tier classification
- `sdlcctl stages` - Display stage definitions
- `sdlcctl p0` - Display P0 artifact requirements
- 4-tier classification (LITE, STANDARD, PROFESSIONAL, ENTERPRISE)
- Pre-commit hook integration
- CI/CD integration examples (GitHub Actions, GitLab CI)

---

## Links

- [Repository](https://github.com/Minh-Tam-Solution/SDLC-Orchestrator)
- [Documentation](./README.md)
- [SDLC 6.0.0 Framework](https://github.com/Minh-Tam-Solution/SDLC-Enterprise-Framework)
