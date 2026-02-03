# Changelog

All notable changes to the SDLC Orchestrator VS Code Extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.5.0] - 2026-02-02

### Added

**Sprint 139: E2E Commands Implementation (RFC-SDLC-602)**

#### E2E Testing Commands (5 New Commands)
- **E2E: Validate Testing Compliance** (`Cmd+Shift+E`): Validate E2E testing with real CLI integration
  - Calls `sdlcctl e2e validate --format json` under the hood
  - Falls back to local validation when CLI unavailable
  - Shows pass rate, coverage, and compliance checklist
- **E2E: Validate Cross-References**: Validate Stage 03 ↔ Stage 05 bidirectional links
  - Parses OpenAPI from Stage 03, matches to test files in Stage 05
  - Calculates endpoint coverage percentage
  - Identifies missing tests with priority (critical > important > normal)
- **E2E: Initialize Testing Structure**: Create E2E testing folder structure in Stage 05
  - Creates `docs/05-deploy/03-E2E-Testing/` directory
  - Generates template test script and README
- **E2E: Validate with Options**: Advanced validation with customizable settings
  - Configurable minimum pass rate threshold
  - Strict mode option (fail if coverage < 80%)
  - Init mode for first-time setup
- **E2E: Show Validation Results**: View detailed validation results in tree view
  - Displays errors, warnings, and checklist items
  - Shows endpoint coverage breakdown

#### New Evidence Types (RFC-SDLC-602)
- `E2E_TESTING_REPORT`: E2E test execution results
- `API_DOCUMENTATION_REFERENCE`: OpenAPI spec metadata
- `SECURITY_TESTING_RESULTS`: OWASP security scan results
- `STAGE_CROSS_REFERENCE`: Bidirectional stage links

#### Backend Cross-Reference API (4 Endpoints)
- `POST /api/v1/cross-reference/validate`: Full cross-reference validation
- `GET /api/v1/cross-reference/coverage/{id}`: Quick coverage metrics
- `GET /api/v1/cross-reference/missing-tests/{id}`: Get uncovered endpoints
- `GET /api/v1/cross-reference/ssot-check/{id}`: SSOT compliance check

#### SSOT Enforcement
- Validates `openapi.json` exists only in Stage 03 (Single Source of Truth)
- Detects duplicate OpenAPI files in Stage 05 or other folders
- Reports SSOT-001 violations with actionable fix suggestions

#### Zero Mock Policy Compliance
- Real CLI integration via `child_process.exec`
- Graceful fallback to local validation when CLI unavailable
- JSON output parsing for structured results
- Error handling with retry recommendations

### Changed
- Package version bumped from 1.4.0 to 1.5.0
- Description updated to include E2E testing capabilities
- README updated with E2E commands section

### Technical Details
- **New Files Created**:
  - `src/commands/e2eValidateCommand.ts` (~500 LOC)
  - `src/commands/e2eCrossRefCommand.ts` (~450 LOC)
  - `src/types/evidence.ts` (~350 LOC)
  - `src/test/suite/e2eValidation.test.ts` (~500 LOC)
  - `backend/app/api/v1/endpoints/cross_reference.py` (~560 LOC)
- **Files Modified**:
  - `src/extension.ts` - Command registration
  - `package.json` - 5 new commands, 1 keybinding
  - `backend/app/main.py` - Router registration
- **Total LOC Added**: ~2,360

---

## [1.3.0] - 2026-02-01

### Added

**Sprint 136: SDLC Framework 6.0.1 + Stage Consistency Validation**

#### Framework 6.0.1 Support
- Updated framework version from 6.0.0 to **6.0.1**
- Added support for SPEC-0021 Stage Consistency Validation
- Synchronized version with `sdlcctl` CLI v1.3.0

#### New CLI Command: `validate-consistency`
- Extension now recognizes the new `sdlcctl validate-consistency` command
- Validates cross-stage consistency between:
  - Stage 01 (Planning) ↔ Stage 02 (Design)
  - Stage 02 (Design) ↔ Stage 03 (Integrate)
  - Stage 03 (Integrate) ↔ Stage 04 (Build)
  - Stage 01 (Planning) ↔ Stage 04 (Build)

#### Related Documents
- [SPEC-0021: Stage Consistency Validation](../SDLC-Enterprise-Framework/05-Templates-Tools/01-Specification-Standard/SPEC-0021-Stage-Consistency-Validation.md)
- [FR-036: Validate Consistency Command](../docs/01-planning/03-Functional-Requirements/FR-036-Validate-Consistency-Command.md)
- [ADR-046: Validate Consistency Command Architecture](../docs/02-design/01-ADRs/ADR-046-Validate-Consistency-Command.md)

### Changed
- Description updated to reference SDLC 6.0.1
- Version synchronized with sdlcctl CLI (1.3.0)

---

## [1.2.3] - 2026-01-30

### Added

**Sprint 127: Auto-Detect Project**

#### Auto-Detect Project from Workspace
- **Automatic Project Detection**: Extension now automatically detects project from workspace
  - 4-level priority detection: `.sdlc/config.yaml` → `package.json` → `.git/config` → folder name
  - Resolves project name to UUID via backend API automatically
  - 5-minute cache with automatic invalidation on workspace changes
  - Monorepo support: Multiple `.sdlc/config.yaml` files detected
  - Eliminates need for manual project UUID configuration in settings

#### Projects Panel Auto-Hide
- **Smart Panel Visibility**: PROJECTS panel now hidden by default when project is auto-detected
  - Panel shown only for monorepos (multiple `.sdlc/config.yaml` files) or when user enables `sdlc.showProjectsPanel`
  - Reduces UI clutter when working in single-project workspace
  - New setting: `sdlc.showProjectsPanel` to always show panel (opt-in)

#### Technical Details
- Added `ProjectDetector` service (`vscode-extension/src/services/projectDetector.ts`)
- Added `js-yaml` dependency for parsing `.sdlc/config.yaml`
- Updated `ContextPanelProvider` to use auto-detected project
- Updated `ProjectsProvider` with smart visibility logic
- Specification: [SPEC-0015](../docs/02-design/14-Technical-Specs/SPEC-0015-Extension-Auto-Detect-Project.md)

### Changed
- Context Overlay now uses auto-detected project instead of requiring manual `sdlc.defaultProjectId` configuration
- Error messages updated to guide users when project detection fails
- Improved project detection logging for debugging

## [1.2.2] - 2026-01-30

### Fixed

**Sprint 127: GitHub OAuth Device Flow Backend Support**

#### GitHub Login Issue Resolved
- **Backend Device Flow Endpoints Added**: Fixed 404 error when attempting GitHub OAuth login
  - Backend now provides `POST /api/v1/auth/github/device` (initiate flow)
  - Backend now provides `POST /api/v1/auth/github/token` (poll for completion)
  - Extension's Device Flow implementation was already correct ✅

#### How GitHub Login Works Now
1. Extension → "SDLC: Login" → "GitHub OAuth"
2. Shows notification with user code (e.g., `WDJB-MJHT`)
3. Click "Open Browser" → Opens https://github.com/login/device
4. Enter user code → Authorize app
5. Extension auto-logs in (polls every 5 seconds)

#### Backend Requirements
- **Minimum Backend Version**: v1.2.0 (January 30, 2026)
- Includes OAuth Device Flow endpoints for CLI/Desktop apps
- See: [Backend CHANGELOG](../../backend/CHANGELOG.md)

#### Technical Details
- Device Flow is the industry-standard OAuth pattern for CLI/Desktop apps
- No localhost callback needed (unlike web OAuth)
- User-friendly 8-character code (XXXX-XXXX format)
- Secure: No client secret in Extension code
- See: [GitHub OAuth Device Flow Docs](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps#device-flow)

## [1.2.0] - 2026-01-30

### Added - Sprint 127: Multi-Frontend Alignment

#### SDLC 6.0.0 Framework Support
- **Specification Validation**: YAML frontmatter validation (SPEC-0002 compliant)
- **BDD Requirements**: GIVEN-WHEN-THEN format validation
- **Tier-Specific Sections**: Support for LITE/STANDARD/PROFESSIONAL/ENTERPRISE sections
- **Framework Alignment**: Full compatibility with SDLC 6.0.0 methodology

### Changed

#### Stage Folder Naming Convention
- Updated to SDLC 6.0.0 lowercase naming format:
  - `00-Project-Foundation` → `00-foundation`
  - `01-Planning-Analysis` → `01-planning`
  - `02-Design-Architecture` → `02-design`
  - `03-Development-Implementation` → `03-integrate`
  - All 11 stages (00-10) updated throughout codebase

#### Parity Improvements
- **Extension Parity**: Increased from 67% → 89% (+22 points)
- **Feature Alignment**: Synchronized with Web Dashboard and CLI
- **Validation Rules**: Consistent error codes across all surfaces

### Fixed

- **Compilation**: Zero TypeScript errors, production-ready build
- **Lint Warnings**: 34 pre-existing warnings documented (not Sprint 127 scope)
- **Documentation**: Updated README and CHANGELOG for SDLC 6.0.0

### Technical Details

- **Package Version**: 1.2.0
- **Framework**: SDLC 6.0.0
- **Build Size**: 1.3MB (VSIX)
- **Status**: Production-ready, published to VS Code Marketplace

## [1.0.0] - 2025-12-26

### Added - Sprint 53: VS Code Extension + Contract Lock

#### Day 1: Extension Foundation (~4,500 lines)
- **Types**: Complete TypeScript type definitions for codegen API
  - `AppBlueprint`, `BlueprintModule`, `BlueprintMetadata`
  - `GeneratedFile`, `QualityGateResult`, `CodegenSession`
  - `ContractLockStatus`, `ContractLockResponse`, `UnlockReason`
  - SSE event types: `SSEStartedEvent`, `SSEFileGeneratedEvent`, etc.
- **Services**: CodegenApiService for backend communication
  - Session management (create, get, update, list)
  - Code generation (start, stream, resume, cancel)
  - Contract lock (lock, unlock, status, verify-hash)
  - Blueprint validation and domain templates
- **Commands**: Lock/unlock command registration
  - `sdlc.lock` - Lock contract specification
  - `sdlc.unlock` - Unlock contract specification
  - `sdlc.lockStatus` - View lock status
  - `sdlc.verifyHash` - Verify specification hash

#### Day 2: App Builder Panel (~2,600 lines)
- **Blueprint Editor**: Visual webview panel for building specifications
  - Tree view with modules and entities
  - Add/remove module with entity definitions
  - Edit blueprint metadata (name, version, description)
  - Domain selection (restaurant, hotel, retail, hrm, crm)
- **Blueprint Tree View**: Sidebar tree data provider
  - Hierarchical view of blueprint structure
  - Context menu actions for modules and entities
  - Real-time updates on blueprint changes
- **Panel Integration**: Webview lifecycle management
  - State persistence across panel close/reopen
  - Message passing between extension and webview
  - Error handling with user-friendly messages

#### Day 3: Streaming Integration (~2,200 lines)
- **Generation Panel**: Real-time code generation view
  - SSE event stream parsing and display
  - File-by-file generation progress
  - Quality gate status visualization
  - Error display with recovery options
- **SSE Client**: Server-Sent Events handling
  - Reconnection with exponential backoff
  - Event type discrimination
  - Checkpoint tracking for resume
- **Resume Capability**: Checkpoint-based recovery
  - Session resume banner
  - Last checkpoint display
  - One-click resume action

#### Day 4: Contract Lock Backend (~1,800 lines)
- **Schemas**: Pydantic models for Contract Lock API
  - `SpecLockRequest`, `SpecUnlockRequest`, `HashVerifyRequest`
  - `SpecLockResponse`, `SpecUnlockResponse`, `HashVerifyResponse`
  - `LockAuditLogEntry`, `LockAuditLogResponse`
  - `UnlockReason` enum (modification_needed, generation_failed, admin_override, session_expired)
- **Service**: ContractLockService with business logic
  - Lock with SHA256 hash calculation
  - Unlock with permission validation (owner or admin)
  - Hash verification for integrity checking
  - Audit log for compliance
  - Auto-unlock for expired locks (1 hour timeout)
- **API Routes**: FastAPI endpoints
  - `POST /api/v1/onboarding/{session_id}/lock`
  - `POST /api/v1/onboarding/{session_id}/unlock`
  - `GET /api/v1/onboarding/{session_id}/lock-status`
  - `POST /api/v1/onboarding/{session_id}/verify-hash`
  - `GET /api/v1/onboarding/{session_id}/lock-audit`
  - `POST /api/v1/onboarding/{session_id}/force-unlock` (admin)
- **Migration**: Database schema changes
  - Added columns to `onboarding_sessions`: locked, spec_hash, locked_at, locked_by, lock_expires_at, lock_version
  - Created `lock_audit_log` table with indexes

#### Day 5: Testing + Publish (~500 lines)
- **Unit Tests**: Type and API tests
  - `codegenApi.test.ts` - Blueprint and lock type tests
  - `streaming.test.ts` - SSE event parsing tests
- **README**: Updated for v1.0.0 with new features
- **CHANGELOG**: Complete Sprint 53 documentation

### Changed
- Updated `package.json` version to 1.0.0
- Updated README with new commands and features
- Enhanced error handling with UnlockReason enum

### Technical Details
- Total lines added: ~11,600
- TypeScript compilation: Clean (0 errors)
- Test coverage: ~200 test cases
- API endpoints: 6 new Contract Lock routes
- Database tables: 1 new table, 6 new columns

---

## [0.2.0] - 2025-12-20

### Added - Sprint 51B: QR Preview
- QR code generation for mobile preview
- Preview modal with copy/share functionality

---

## [0.1.0] - 2025-12-04

### Added

#### Core Services
- **AuthService**: JWT token management with secure storage
- **ApiClient**: Axios-based HTTP client with authentication
- **CacheService**: Stale-while-revalidate caching with offline support
- **ConfigManager**: Centralized settings management
- **Logger**: Debug logging with configurable levels

#### Tree View Providers
- **Gate Status View**: Real-time gate status (G0-G5) with status icons
- **Violations View**: Grouped violations by severity with quick actions
- **Projects View**: Project list with quick switching

#### Chat Participant (@gate)
- `/status` command: Show current gate status
- `/evaluate` command: Run compliance evaluation
- `/fix <id>` command: Get AI fix recommendation
- `/council <id>` command: AI Council decision

#### Error Handling
- Comprehensive error classification (network, auth, API, client)
- User-friendly error messages with suggested actions
- Retry logic with exponential backoff

#### Offline Mode
- Cache-first data fetching strategy
- Graceful degradation when backend unavailable
- Visual indicators for cached data

### Technical Details
- TypeScript strict mode enabled
- ESLint with @typescript-eslint rules
- Mocha test framework with TDD UI
- VS Code 1.80.0+ compatibility
