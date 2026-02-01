# Changelog

All notable changes to sdlcctl will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
