# SDLC Orchestrator VS Code Extension

**Version**: 1.7.1
**Status**: GA (General Availability)
**Framework**: SDLC 6.0.6 (7-Pillar + AI Governance Principles)
**Sprint**: 174 - Anthropic Best Practices Integration
**Last Updated**: February 16, 2026

Gate status monitoring, AI-powered code generation, and compliance assistance directly in VS Code. Part of the SDLC Orchestrator governance platform - the **Operating System for Software 3.0**.

## What's New in 1.7.0 (Sprint 174)

### Anthropic Best Practices Integration
- **SDLC 6.0.6 Framework**: Full alignment with 7-Pillar Architecture + AI Governance Principles
- **Context Cache Awareness**: Extension recognizes new `sdlcctl cache` commands (stats, clear, warm)
- **MCP Client Integration**: Backend MCP service support (AsyncExitStack + SSE transport)
- **Version Sync**: Synchronized with `sdlcctl` CLI v1.8.0

### Framework-First Compliance
- All framework references updated from 6.0.5 to 6.0.6
- Spec validation aligned with Section 8 Specification Standard
- CLAUDE.md PRO tier awareness for project onboarding

## What's New in 1.6.x (Sprints 147-173)

### v1.6.3 (Sprint 172)
- **Gate Status Fix**: Resolved cold-start hydration issues
- **Project Auto-Detection**: Improved workspace detection reliability
- **Ownership Transfer**: Design support for project ownership changes

### v1.6.2 (Sprint 172)
- **Project Init Fix**: Existing project initialization now correctly registers with backend
- **Marketplace Release**: Published to VS Code Marketplace

### v1.6.1 (Sprint 147)
- **Gate URL Fix**: Fixed 404 error by adding `/app` prefix to gate URLs
- **Codebase Cleanup**: Sprint 147 Spring Cleaning alignment

## What's New in 1.5.0 (Sprint 139)

### E2E Testing Commands (RFC-SDLC-602)
- **E2E Validate** (`Cmd+Shift+E`): Validate E2E testing compliance with CLI integration
- **E2E Cross-Reference**: Validate Stage 03 ↔ Stage 05 bidirectional links
- **E2E Initialize**: Create E2E testing folder structure in Stage 05
- **E2E Validate with Options**: Advanced validation with custom pass rate threshold
- **Show E2E Results**: View detailed validation results in tree view

### New Backend API Endpoints
- `POST /api/v1/cross-reference/validate`: Full cross-reference validation
- `GET /api/v1/cross-reference/coverage/{id}`: Quick coverage check
- `GET /api/v1/cross-reference/missing-tests/{id}`: Get missing test endpoints
- `GET /api/v1/cross-reference/ssot-check/{id}`: SSOT compliance check

### SSOT Enforcement
- Validates `openapi.json` exists only in Stage 03
- Detects duplicate OpenAPI files in Stage 05 or other folders
- Reports violations with actionable fix suggestions

### CLI Integration (Zero Mock Policy)
- Real `sdlcctl e2e validate` execution via Extension
- Falls back to local validation when CLI unavailable
- JSON output parsing for structured results

## Previous Releases

<details>
<summary>1.4.0 (Sprint 138) - E2E API Testing</summary>

- **Framework 6.0.6**: RFC-SDLC-602 E2E API Testing Enhancement
- **E2E API Testing Workflow**: 6-phase standardized testing process awareness
- **Stage Cross-Reference**: Stage 03 ↔ Stage 05 bidirectional traceability
- **OWASP API Top 10**: Security checklist integration ready
- **Version Sync**: Synchronized with `sdlcctl` CLI v1.4.0
- **4 New Evidence Types**: e2e_test_report, security_test_report, api_coverage_report, cross_reference_validation
</details>

<details>
<summary>1.3.0 (Sprint 136) - Stage Consistency</summary>

- **SPEC-0021**: Stage Consistency Validation support
- Extension recognizes `sdlcctl validate-consistency` command
- Cross-stage consistency: Stage 01 ↔ 02, Stage 02 ↔ 03, Stage 03 ↔ 04, Stage 01 ↔ 04
</details>

<details>
<summary>1.2.0 (Sprint 127) - Multi-Frontend Alignment</summary>

- **Specification Validation**: YAML frontmatter validation (SPEC-0002 compliant)
- **BDD Requirements**: GIVEN-WHEN-THEN validation support
- **Tier-Specific Sections**: LITE/STANDARD/PROFESSIONAL/ENTERPRISE validation
- **Extension Parity**: 67% → 89% feature parity (+22 points)
</details>

## Key Features

### App Builder
- **Blueprint Editor**: Visual tree view for building AppBlueprint specifications
- **Module Management**: Add/remove modules with entity definitions
- **Domain Templates**: Pre-built templates for Vietnamese SME (Restaurant, Hotel, Retail, HRM, CRM)
- **Real-time Validation**: Immediate feedback on blueprint structure

### Code Generation
- **IR-Based Generation**: Deterministic output via Intermediate Representation
- **Multi-Provider**: Ollama (primary) -> Claude (fallback) -> Rule-based
- **4-Gate Quality Pipeline**: Syntax -> Security -> Context -> Tests
- **SSE Streaming**: Real-time progress with file-by-file updates
- **Resume Capability**: Checkpoint-based recovery for failed generations

### Contract Lock
- **Specification Immutability**: Lock blueprints before code generation
- **SHA256 Hash Verification**: Cryptographic integrity checking
- **Audit Trail**: Full history of lock/unlock operations
- **Auto-Expiry**: Orphaned locks expire after 1 hour

### Gate Status Sidebar
- View G0-G5 gate progress in real-time
- See evidence count and approval status
- Auto-refresh every 30 seconds
- Click to open gates in browser
- Progress percentage visualization
- Gate approval/rejection actions directly from sidebar

### Context Overlay Panel
- Dynamic context based on current gate status
- Copy context as PR comment
- Stage-aware guidance for AI assistants

### Inline AI Chat (@gate)
Use Copilot-style commands in VS Code Chat:

```
@gate /status      - Show current gate status (G0-G5)
@gate /evaluate    - Run compliance evaluation, show violations
@gate /fix <id>    - Get AI recommendation for a violation
@gate /council <id> - Use AI Council 3-stage deliberation
```

### Specification Validation (SDLC 6.0.6)
- **YAML Frontmatter**: Validate spec metadata (tier, status, version)
- **BDD Requirements**: GIVEN-WHEN-THEN format checking
- **Tier Validation**: LITE/STANDARD/PROFESSIONAL/ENTERPRISE compliance
- **Auto-validate on Save**: Optional setting for continuous validation

### Violations Panel
- View compliance violations grouped by severity (Critical, High, Medium, Low)
- Quick actions to get AI recommendations
- Navigate to file locations
- Filter by status (open, resolved)

### Projects Panel
- List all projects you have access to
- Quick project selection
- View compliance scores
- See current gate status
- Auto-detection from workspace

### Evidence Submission
- Submit evidence directly from VS Code
- Attach files to quality gates
- Track evidence lifecycle

### GitHub Integration
- Connect/disconnect GitHub repositories
- Sync repository metadata
- Scan repositories for compliance

### Offline Mode Support
- Automatic cache fallback when network unavailable
- Stale-while-revalidate pattern for smooth UX
- Visual indicator when using cached data
- Graceful degradation with user-friendly messages

## Installation

### From VS Code Marketplace
1. Open VS Code Extensions (Ctrl+Shift+X)
2. Search for "SDLC Orchestrator"
3. Click Install

### From CLI
```bash
code --install-extension mtsolution.sdlc-orchestrator
```

### From VSIX (Development)
1. Download the latest `.vsix` file from releases
2. In VS Code, open Command Palette (Cmd+Shift+P / Ctrl+Shift+P)
3. Run "Extensions: Install from VSIX..."
4. Select the downloaded file

## Quick Start

1. **Install** the extension
2. **Create API Key** (Recommended):
   - Go to SDLC Orchestrator Dashboard → Settings → API Keys
   - Click "Create New API Key"
   - Copy the key (starts with `sdlc_live_`)
3. **Login** using Command Palette > "SDLC: Login"
   - Select "API Token" (Recommended - Never expires)
   - Paste your API key
4. **Select Project** using Command Palette > "SDLC: Select Project"
5. **View Gates** in the SDLC sidebar

**Why API Key?** Unlike email/password (JWT expires after 8 hours), API keys never expire until you revoke them - perfect for development tools!

6. **Generate Code**:
   - Open App Builder: "SDLC: Open App Builder"
   - Create a blueprint with modules and entities
   - Lock the specification: "SDLC: Lock Contract Spec"
   - Generate code: "SDLC: Generate from Blueprint"

## Commands

| Command | Keybinding | Description |
|---------|------------|-------------|
| SDLC: Refresh Gate Status | Cmd+Shift+R | Refresh all views |
| SDLC: Select Project | - | Choose project to monitor |
| SDLC: Login | - | Login to SDLC Orchestrator |
| SDLC: Logout | - | Logout and clear tokens |
| SDLC: Initialize SDLC Project | Cmd+Shift+I | Initialize project structure |
| SDLC: Open App Builder | Cmd+Shift+B | Open blueprint editor |
| SDLC: Generate from Blueprint | Cmd+Shift+G | Start code generation |
| SDLC: Magic Mode | Cmd+Shift+M | Natural language to code |
| SDLC: Lock Contract Spec | Cmd+Shift+L | Lock blueprint for generation |
| SDLC: Unlock Contract Spec | - | Unlock blueprint for editing |
| SDLC: Preview Generated Code | Cmd+Alt+P | Preview with QR code |
| SDLC: Resume Failed Generation | - | Resume from checkpoint |
| SDLC: Validate Specification | Cmd+Shift+V | Validate spec (SDLC 6.0.6) |
| SDLC: Approve Gate | - | Approve a quality gate |
| SDLC: Reject Gate | - | Reject a quality gate |
| SDLC: Submit Evidence | - | Submit evidence to gate |
| SDLC: Connect GitHub | - | Connect GitHub repository |
| SDLC: Check SSOT Compliance | - | Check Single Source of Truth |
| E2E: Validate Testing Compliance | Cmd+Shift+E | Validate E2E testing with CLI |
| E2E: Validate Cross-References | - | Validate Stage 03 ↔ 05 links |
| E2E: Initialize Testing Structure | - | Create E2E folder structure |
| E2E: Validate with Options | - | Advanced validation with options |
| E2E: Show Validation Results | - | View detailed E2E results |

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `sdlc.apiUrl` | `https://sdlc.nhatquangholding.com` | Backend API URL |
| `sdlc.autoRefreshInterval` | `30` | Auto-refresh interval (seconds) |
| `sdlc.defaultProjectId` | `` | (Optional) Manual project UUID - auto-detected from workspace if not set |
| `sdlc.enableNotifications` | `true` | Show gate status notifications |
| `sdlc.aiCouncilEnabled` | `true` | Enable AI Council for critical violations |
| `sdlc.showViolationBadge` | `true` | Show violation count in activity bar |
| `sdlc.validateSpecOnSave` | `false` | Auto-validate spec files on save (SDLC 6.0.6) |
| `sdlc.defaultSpecTier` | `PROFESSIONAL` | Default tier for spec validation (LITE/STANDARD/PROFESSIONAL/ENTERPRISE) |
| `sdlc.showProjectsPanel` | `false` | Always show Projects panel (auto-hidden when project detected) |

## Requirements

- VS Code 1.80.0 or higher
- SDLC Orchestrator backend running (v1.7.0+)
- Valid API token or GitHub OAuth

## Architecture

```
src/
├── extension.ts                # Main entry point, activation (32KB)
├── commands/
│   ├── appBuilderCommand.ts    # Blueprint editor commands
│   ├── connectGithubCommand.ts # GitHub integration
│   ├── e2eCrossRefCommand.ts   # Cross-reference validation (Sprint 139)
│   ├── e2eValidateCommand.ts   # E2E validation with CLI (Sprint 139)
│   ├── evidenceSubmissionCommand.ts # Evidence upload
│   ├── gateApprovalCommand.ts  # Gate approve/reject
│   ├── generateCommand.ts      # Code generation commands
│   ├── initCommand.ts          # SDLC project initialization
│   ├── lockCommand.ts          # Contract lock/unlock
│   ├── magicCommand.ts         # Natural language mode
│   ├── previewCommand.ts       # Code preview with QR
│   ├── resumeCommand.ts        # Resume failed generation
│   └── specValidationCommand.ts # Spec validation (SDLC 6.0.6)
├── services/
│   ├── apiClient.ts            # Backend API client (axios-based)
│   ├── authService.ts          # JWT token management, OAuth flow
│   ├── cacheService.ts         # Offline cache with TTL
│   ├── codegenApi.ts           # Code generation API client
│   ├── fileService.ts          # File system operations
│   ├── projectDetector.ts      # Workspace project auto-detection
│   ├── sdlcStructureService.ts # SDLC folder structure service
│   ├── sseClient.ts            # Server-Sent Events client
│   └── telemetryService.ts     # Usage telemetry
├── panels/
│   ├── appBuilderPanel.ts      # Blueprint editor webview
│   └── generationPanel.ts      # Real-time generation view
├── providers/
│   └── blueprintProvider.ts    # Blueprint tree data provider
├── views/
│   ├── complianceChat.ts       # Chat participant (@gate)
│   ├── contextPanel.ts         # Context Overlay panel
│   ├── gateStatusView.ts       # Gate sidebar TreeDataProvider
│   ├── projectsView.ts         # Projects TreeDataProvider
│   ├── streamingStatusBar.ts   # SSE streaming status bar
│   └── violationsView.ts       # Violations TreeDataProvider
├── validation/
│   └── ssotValidator.ts        # SSOT compliance validator
├── types/
│   ├── codegen.ts              # Type definitions for codegen
│   └── evidence.ts             # E2E evidence types (RFC-SDLC-602)
├── utils/
│   ├── config.ts               # Configuration manager
│   ├── errors.ts               # Error classification & handling
│   └── logger.ts               # Structured logging
└── test/
    └── suite/
        ├── apiClient.test.ts
        ├── authService.test.ts
        ├── cacheService.test.ts
        ├── codegenApi.test.ts
        ├── complianceChat.test.ts
        ├── contextPanel.test.ts
        ├── e2eValidation.test.ts
        ├── errorHandling.test.ts
        ├── errors.test.ts
        ├── gateStatusView.test.ts
        ├── github.test.ts
        ├── offlineMode.test.ts
        ├── projectsView.test.ts
        ├── specValidation.test.ts
        ├── streaming.test.ts
        └── violationsView.test.ts
```

## Development

### Prerequisites
- Node.js 18+
- npm 9+
- VS Code 1.80+

### Setup
```bash
cd vscode-extension
npm install
npm run compile
```

### Watch Mode
```bash
npm run watch
```

### Package Extension
```bash
npm run package
# Creates sdlc-orchestrator-1.7.1.vsix
```

### Run Tests
```bash
npm run test
```

### Debug in VS Code
1. Open `vscode-extension` folder in VS Code
2. Press F5 to launch Extension Development Host
3. The extension will be loaded in a new VS Code window

## Cache Strategy

| Data Type | TTL | Description |
|-----------|-----|-------------|
| Projects | 10 min | List of all projects |
| Gates | 2 min | Gate status (frequently updated) |
| Violations | 2 min | Compliance violations |
| Sessions | 5 min | Onboarding sessions |
| Blueprints | 10 min | App blueprints |

## Troubleshooting

### Connection Refused
- Ensure SDLC Orchestrator backend is running
- Check `sdlc.apiUrl` configuration
- Verify firewall/proxy settings

### Token Expired
- Run "SDLC: Logout" then "SDLC: Login"
- Check token expiration in dashboard
- Use API Token instead of email/password for long-lived sessions

### Generation Failed
- Check if blueprint is locked: "SDLC: Lock Contract Spec"
- Verify backend AI providers are available
- Try "SDLC: Resume Failed Generation" if checkpoint exists

### Lock Expired
- Locks auto-expire after 1 hour of inactivity
- Re-lock the specification before generation

### Gate URL 404 Error
- Ensure backend v1.6.1+ is running (gate URL prefix fix)
- Check `sdlc.apiUrl` points to correct backend

## License

Apache-2.0

## Support

- GitHub Issues: https://github.com/Minh-Tam-Solution/SDLC-Orchestrator/issues
- Documentation: https://docs.sdlc-orchestrator.dev
- VS Code Marketplace: https://marketplace.visualstudio.com/items?itemName=mtsolution.sdlc-orchestrator
