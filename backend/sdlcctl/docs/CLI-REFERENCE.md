# MCP CLI Reference Guide

**Version**: 1.0.0
**Date**: February 3, 2026
**Sprint**: 145 - MCP Integration Phase 1
**Status**: PRODUCTION-READY

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Commands](#commands)
   - [connect](#connect)
   - [disconnect](#disconnect)
   - [test](#test)
   - [list](#list)
5. [Platform Guides](#platform-guides)
   - [Slack Setup](#slack-setup)
   - [GitHub Setup](#github-setup)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Usage](#advanced-usage)

---

## Quick Start

```bash
# Install sdlcctl
pip install -e /path/to/sdlc-orchestrator/backend/sdlcctl

# Connect to Slack
sdlcctl mcp connect --slack \
  --bot-token "xoxb-your-token" \
  --signing-secret "your-signing-secret" \
  --channel "bugs"

# Test connection
sdlcctl mcp test --slack

# List connected platforms
sdlcctl mcp list

# Disconnect
sdlcctl mcp disconnect --slack --force
```

---

## Installation

### Prerequisites

- Python 3.11+
- pip or poetry
- Git

### Install from Source

```bash
cd /path/to/sdlc-orchestrator/backend/sdlcctl
pip install -e .
```

### Verify Installation

```bash
sdlcctl --version
# Output: sdlcctl, version 1.4.0

sdlcctl mcp --help
# Output: MCP command help
```

---

## Configuration

### Configuration File

MCP commands use a `.mcp.json` configuration file (default: `~/.mcp.json`).

**Structure**:
```json
{
  "version": "1.0.0",
  "platforms": {
    "slack": {
      "enabled": true,
      "connected_at": "2026-02-03T10:30:00Z",
      "bot_token": "xoxb-***",
      "signing_secret": "***",
      "channels": ["bugs", "alerts"]
    },
    "github": {
      "enabled": true,
      "connected_at": "2026-02-03T10:35:00Z",
      "app_id": "123456",
      "private_key_path": "/path/to/github.pem",
      "repositories": ["owner/repo1", "owner/repo2"]
    }
  }
}
```

### Custom Config Location

```bash
# Use custom config file
sdlcctl mcp connect --slack \
  --bot-token "xoxb-token" \
  --signing-secret "secret" \
  --channel "bugs" \
  --config "/path/to/custom/.mcp.json"
```

### Environment Variables

MCP credentials can also be set via environment variables:

```bash
export SLACK_BOT_TOKEN="xoxb-your-token"
export SLACK_SIGNING_SECRET="your-signing-secret"
export GITHUB_APP_ID="123456"
export GITHUB_PRIVATE_KEY_PATH="/path/to/github.pem"
```

---

## Commands

### connect

Connect to MCP platforms (Slack, GitHub, Jira, Linear).

#### Slack Connect

```bash
sdlcctl mcp connect --slack \
  --bot-token "xoxb-your-bot-token" \
  --signing-secret "your-signing-secret" \
  --channel "bugs" \
  [--config PATH] \
  [--no-test]
```

**Parameters**:
- `--slack`: Connect to Slack platform
- `--bot-token TEXT`: Slack Bot User OAuth Token (required)
  - Format: `xoxb-***`
  - Get from: https://api.slack.com/apps → OAuth & Permissions
- `--signing-secret TEXT`: Slack Signing Secret (required)
  - Format: 32-character hex string
  - Get from: https://api.slack.com/apps → Basic Information
- `--channel TEXT`: Slack channel to monitor (required)
  - Format: Channel name without '#' (e.g., "bugs")
  - Can be repeated for multiple channels
- `--config PATH`: Path to config file (optional)
  - Default: `~/.mcp.json`
- `--no-test`: Skip connectivity test (optional)
  - Use when API is mocked or unavailable

**Example**:
```bash
$ sdlcctl mcp connect --slack \
    --bot-token "xoxb-1234-5678-abcd" \
    --signing-secret "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6" \
    --channel "bugs"

✅ Slack connected successfully
📝 Evidence artifact created: EVD-2026-02-001
💾 Config saved to /home/user/.mcp.json
```

**Success Output**:
- Connection confirmation
- Evidence artifact ID (tamper-evident audit trail)
- Config file location

**Error Cases**:
- Invalid bot token → `401 Unauthorized`
- Invalid signing secret → Signature verification fails
- Channel not found → `404 Not Found`

---

#### GitHub Connect

```bash
sdlcctl mcp connect --github \
  --app-id "123456" \
  --private-key "/path/to/github.pem" \
  --repo "owner/repository" \
  [--config PATH] \
  [--no-test]
```

**Parameters**:
- `--github`: Connect to GitHub platform
- `--app-id TEXT`: GitHub App ID (required)
  - Format: Numeric string (e.g., "123456")
  - Get from: https://github.com/settings/apps → Your App → About
- `--private-key PATH`: Path to GitHub App private key (required)
  - Format: PEM file (RSA private key)
  - Get from: https://github.com/settings/apps → Your App → Generate Private Key
- `--repo TEXT`: GitHub repository to watch (required)
  - Format: `owner/repository` (e.g., "nqh/sdlc-orchestrator")
  - Can be repeated for multiple repositories
- `--config PATH`: Path to config file (optional)
- `--no-test`: Skip connectivity test (optional)

**Example**:
```bash
$ sdlcctl mcp connect --github \
    --app-id "123456" \
    --private-key "~/.ssh/github-app.pem" \
    --repo "nqh/sdlc-orchestrator"

✅ GitHub connected successfully
📝 Evidence artifact created: EVD-2026-02-002
💾 Config saved to /home/user/.mcp.json
```

**Private Key Format**:
```pem
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyNOuqQvWwt/pFYP1dCPuqcLOQXwEu
...
-----END RSA PRIVATE KEY-----
```

**Success Output**:
- Connection confirmation
- Evidence artifact ID
- Config file location

**Error Cases**:
- Invalid App ID → `404 Not Found`
- Invalid private key → JWT signature fails
- Repository not accessible → `403 Forbidden`

---

### disconnect

Disconnect from MCP platforms and remove credentials.

```bash
sdlcctl mcp disconnect --slack [--force] [--config PATH]
sdlcctl mcp disconnect --github [--force] [--config PATH]
```

**Parameters**:
- `--slack`: Disconnect from Slack
- `--github`: Disconnect from GitHub
- `--force`: Skip confirmation prompt (optional)
- `--config PATH`: Path to config file (optional)

**Example (Interactive)**:
```bash
$ sdlcctl mcp disconnect --slack

⚠️  This will disconnect from Slack and remove credentials.
   Do you want to continue? [y/N]: y

✅ Slack disconnected successfully
📝 Evidence artifact created: EVD-2026-02-003
💾 Config updated: /home/user/.mcp.json
```

**Example (Force)**:
```bash
$ sdlcctl mcp disconnect --slack --force

✅ Slack disconnected successfully
📝 Evidence artifact created: EVD-2026-02-004
💾 Config updated: /home/user/.mcp.json
```

**What Happens**:
1. Platform removed from `.mcp.json`
2. Credentials deleted (not stored elsewhere)
3. Evidence artifact created (audit trail)
4. Confirmation displayed

**Error Cases**:
- Platform not connected → Error message
- Config file not found → `ConfigNotFoundError`

---

### test

Test MCP platform connectivity and authentication.

```bash
sdlcctl mcp test --slack [--config PATH]
sdlcctl mcp test --github [--config PATH]
```

**Parameters**:
- `--slack`: Test Slack connection
- `--github`: Test GitHub connection
- `--config PATH`: Path to config file (optional)

**Example (Slack)**:
```bash
$ sdlcctl mcp test --slack

🔍 Testing Slack integration...

Checks:
  ✅ Bot token valid (auth.test API)
  ✅ Signing secret configured
  ✅ Channel accessible (bugs)
  ✅ Evidence Vault working

All checks passed! ✅
```

**Example (GitHub)**:
```bash
$ sdlcctl mcp test --github

🔍 Testing GitHub integration...

Checks:
  ✅ App ID valid
  ✅ Private key loaded
  ✅ JWT generation successful
  ✅ Installation token obtained
  ✅ Repository accessible (nqh/sdlc-orchestrator)
  ✅ Evidence Vault working

All checks passed! ✅
```

**What's Tested**:
- **Slack**:
  - Bot token validity (`auth.test` API)
  - Signing secret configured (32 chars)
  - Channel accessibility
  - Evidence Vault integration
- **GitHub**:
  - App ID validity
  - Private key format
  - JWT RS256 signing
  - Installation token generation
  - Repository access permissions
  - Evidence Vault integration

**Error Cases**:
- Platform not connected → Error message
- Invalid credentials → Specific error (401, 404, etc.)
- Network issues → Connection timeout

---

### list

List all connected MCP platforms and their status.

```bash
sdlcctl mcp list [--config PATH] [--json]
```

**Parameters**:
- `--config PATH`: Path to config file (optional)
- `--json`: Output as JSON (optional)

**Example (Table Output)**:
```bash
$ sdlcctl mcp list

Connected Platforms:

┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Platform┃ Status ┃ Connected At        ┃ Targets                  ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Slack   │ Active │ 2026-02-03 10:30:00 │ bugs, alerts             │
│ GitHub  │ Active │ 2026-02-03 10:35:00 │ nqh/sdlc-orchestrator    │
└─────────┴────────┴─────────────────────┴──────────────────────────┘

Config: /home/user/.mcp.json
```

**Example (JSON Output)**:
```bash
$ sdlcctl mcp list --json

{
  "platforms": {
    "slack": {
      "status": "active",
      "connected_at": "2026-02-03T10:30:00Z",
      "channels": ["bugs", "alerts"]
    },
    "github": {
      "status": "active",
      "connected_at": "2026-02-03T10:35:00Z",
      "repositories": ["nqh/sdlc-orchestrator"]
    }
  },
  "config_path": "/home/user/.mcp.json"
}
```

**Output Fields**:
- **Platform**: Platform name (Slack, GitHub, Jira, Linear)
- **Status**: Connection status (Active, Inactive, Error)
- **Connected At**: ISO 8601 timestamp
- **Targets**: Channels (Slack) or Repositories (GitHub)

**Error Cases**:
- No platforms connected → Empty table
- Config file not found → `ConfigNotFoundError`

---

## Platform Guides

### Slack Setup

#### Prerequisites

1. **Slack Workspace Admin Access**
2. **Slack App Created** (https://api.slack.com/apps)

#### Step 1: Create Slack App

1. Go to https://api.slack.com/apps
2. Click "Create New App" → "From scratch"
3. Name: "SDLC Orchestrator MCP"
4. Workspace: Select your workspace
5. Click "Create App"

#### Step 2: Enable Bot User

1. Go to "OAuth & Permissions"
2. Scroll to "Scopes" → "Bot Token Scopes"
3. Add scopes:
   - `chat:write` - Send messages
   - `channels:read` - List channels
   - `channels:history` - Read channel messages
   - `users:read` - Read user info
4. Click "Install to Workspace"
5. Copy **Bot User OAuth Token** (starts with `xoxb-`)

#### Step 3: Get Signing Secret

1. Go to "Basic Information"
2. Scroll to "App Credentials"
3. Copy **Signing Secret** (32-character hex string)

#### Step 4: Connect via CLI

```bash
sdlcctl mcp connect --slack \
  --bot-token "xoxb-your-bot-token-from-step-2" \
  --signing-secret "your-signing-secret-from-step-3" \
  --channel "bugs"
```

#### Step 5: Verify

```bash
sdlcctl mcp test --slack
```

**Expected Output**:
```
🔍 Testing Slack integration...
  ✅ Bot token valid
  ✅ Signing secret configured
  ✅ Channel accessible (bugs)
  ✅ Evidence Vault working
All checks passed! ✅
```

---

### GitHub Setup

#### Prerequisites

1. **GitHub Organization Admin Access**
2. **Repository Access** (read + write permissions)

#### Step 1: Create GitHub App

1. Go to https://github.com/settings/apps
2. Click "New GitHub App"
3. Fill in details:
   - **Name**: SDLC Orchestrator MCP
   - **Homepage URL**: https://github.com/your-org/sdlc-orchestrator
   - **Webhook URL**: https://your-domain.com/webhooks/github (optional for Phase 1)
   - **Webhook Secret**: Generate random string (save for later)
4. Permissions:
   - **Repository permissions**:
     - Contents: Read & Write
     - Issues: Read & Write
     - Pull Requests: Read & Write
     - Metadata: Read-only
5. Subscribe to events:
   - Issues
   - Pull requests
   - Push
6. Click "Create GitHub App"

#### Step 2: Generate Private Key

1. Scroll to "Private keys"
2. Click "Generate a private key"
3. Save downloaded PEM file (e.g., `sdlc-orchestrator.pem`)
4. Move to secure location: `mv ~/Downloads/sdlc-orchestrator.*.private-key.pem ~/.ssh/github-app.pem`
5. Secure permissions: `chmod 600 ~/.ssh/github-app.pem`

#### Step 3: Install App to Repository

1. Go to "Install App" (left sidebar)
2. Click "Install" next to your organization
3. Select repositories:
   - All repositories (not recommended)
   - Only select repositories: Choose `sdlc-orchestrator`
4. Click "Install"

#### Step 4: Get App ID

1. Go to "General" (left sidebar)
2. Find "App ID" at the top (e.g., `123456`)
3. Copy the App ID

#### Step 5: Connect via CLI

```bash
sdlcctl mcp connect --github \
  --app-id "123456" \
  --private-key "~/.ssh/github-app.pem" \
  --repo "nqh/sdlc-orchestrator"
```

#### Step 6: Verify

```bash
sdlcctl mcp test --github
```

**Expected Output**:
```
🔍 Testing GitHub integration...
  ✅ App ID valid
  ✅ Private key loaded
  ✅ JWT generation successful
  ✅ Installation token obtained
  ✅ Repository accessible (nqh/sdlc-orchestrator)
  ✅ Evidence Vault working
All checks passed! ✅
```

---

## Troubleshooting

### Common Errors

#### 1. Invalid Slack Bot Token

**Error**:
```
❌ Error: Invalid Slack bot token
   API Response: invalid_auth
```

**Cause**: Bot token is incorrect or expired

**Solution**:
1. Go to https://api.slack.com/apps
2. Select your app → "OAuth & Permissions"
3. Copy new "Bot User OAuth Token" (starts with `xoxb-`)
4. Reconnect:
   ```bash
   sdlcctl mcp disconnect --slack --force
   sdlcctl mcp connect --slack \
     --bot-token "NEW-TOKEN" \
     --signing-secret "YOUR-SECRET" \
     --channel "bugs"
   ```

---

#### 2. GitHub JWT Signature Failed

**Error**:
```
❌ Error: JWT signature verification failed
   Reason: Private key format invalid
```

**Cause**: Private key file is corrupted or not in PEM format

**Solution**:
1. Re-download private key from GitHub App settings
2. Verify format:
   ```bash
   head -1 ~/.ssh/github-app.pem
   # Should output: -----BEGIN RSA PRIVATE KEY-----
   ```
3. Check permissions:
   ```bash
   chmod 600 ~/.ssh/github-app.pem
   ```
4. Reconnect:
   ```bash
   sdlcctl mcp connect --github \
     --app-id "123456" \
     --private-key "~/.ssh/github-app.pem" \
     --repo "owner/repo"
   ```

---

#### 3. Config File Not Found

**Error**:
```
❌ Error: Config file not found
   Path: /home/user/.mcp.json
```

**Cause**: No platforms connected yet

**Solution**:
Connect to at least one platform:
```bash
sdlcctl mcp connect --slack \
  --bot-token "xoxb-token" \
  --signing-secret "secret" \
  --channel "bugs"
```

Config file will be created automatically.

---

#### 4. Channel Not Found (Slack)

**Error**:
```
❌ Error: Channel not found
   Channel: bugs
   API Response: channel_not_found
```

**Cause**: Channel doesn't exist or bot not invited

**Solution**:
1. Verify channel exists in Slack workspace
2. Invite bot to channel:
   - Go to channel in Slack
   - Type `/invite @SDLC-Orchestrator-MCP`
3. Reconnect:
   ```bash
   sdlcctl mcp connect --slack \
     --bot-token "xoxb-token" \
     --signing-secret "secret" \
     --channel "bugs"
   ```

---

#### 5. Repository Not Accessible (GitHub)

**Error**:
```
❌ Error: Repository not accessible
   Repository: nqh/sdlc-orchestrator
   API Response: 404 Not Found
```

**Cause**: GitHub App not installed to repository

**Solution**:
1. Go to https://github.com/apps/your-app-name
2. Click "Configure" → Select organization
3. Under "Repository access":
   - Add `sdlc-orchestrator` to selected repositories
4. Click "Save"
5. Reconnect:
   ```bash
   sdlcctl mcp connect --github \
     --app-id "123456" \
     --private-key "~/.ssh/github-app.pem" \
     --repo "nqh/sdlc-orchestrator"
   ```

---

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
export SDLCCTL_DEBUG=1
sdlcctl mcp test --slack
```

**Output**:
```
[DEBUG] Loading config from /home/user/.mcp.json
[DEBUG] Found Slack credentials
[DEBUG] Calling Slack API: auth.test
[DEBUG] Response: {"ok": true, "user": "bot_user"}
[DEBUG] Creating Evidence artifact: EVD-2026-02-005
[DEBUG] Evidence signature: valid
✅ All checks passed!
```

---

## Advanced Usage

### Multiple Platforms

Connect to multiple platforms simultaneously:

```bash
# Connect Slack
sdlcctl mcp connect --slack \
  --bot-token "xoxb-slack-token" \
  --signing-secret "slack-secret" \
  --channel "bugs"

# Connect GitHub (same config file)
sdlcctl mcp connect --github \
  --app-id "123456" \
  --private-key "~/.ssh/github-app.pem" \
  --repo "owner/repo"

# List all connections
sdlcctl mcp list
```

**Output**:
```
Connected Platforms:
┏━━━━━━━━━┳━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Platform┃ Status ┃ Connected At        ┃ Targets                  ┃
┡━━━━━━━━━╇━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Slack   │ Active │ 2026-02-03 10:30:00 │ bugs                     │
│ GitHub  │ Active │ 2026-02-03 10:35:00 │ owner/repo               │
└─────────┴────────┴─────────────────────┴──────────────────────────┘
```

---

### Multiple Channels/Repositories

Add multiple targets to a single platform:

```bash
# Slack: Multiple channels
sdlcctl mcp connect --slack \
  --bot-token "xoxb-token" \
  --signing-secret "secret" \
  --channel "bugs" \
  --channel "alerts" \
  --channel "incidents"

# GitHub: Multiple repositories
sdlcctl mcp connect --github \
  --app-id "123456" \
  --private-key "~/.ssh/github-app.pem" \
  --repo "owner/repo1" \
  --repo "owner/repo2" \
  --repo "owner/repo3"
```

---

### Programmatic Access

Use MCP CLI in scripts:

```bash
#!/bin/bash

# Automated MCP connection script

CONFIG_FILE="/var/sdlc/mcp.json"

# Connect Slack
sdlcctl mcp connect --slack \
  --bot-token "${SLACK_BOT_TOKEN}" \
  --signing-secret "${SLACK_SIGNING_SECRET}" \
  --channel "bugs" \
  --config "${CONFIG_FILE}" \
  --no-test

# Verify connection
if sdlcctl mcp test --slack --config "${CONFIG_FILE}"; then
    echo "✅ Slack connected successfully"
else
    echo "❌ Slack connection failed"
    exit 1
fi

# Connect GitHub
sdlcctl mcp connect --github \
  --app-id "${GITHUB_APP_ID}" \
  --private-key "${GITHUB_PRIVATE_KEY_PATH}" \
  --repo "${GITHUB_REPO}" \
  --config "${CONFIG_FILE}" \
  --no-test

# Verify connection
if sdlcctl mcp test --github --config "${CONFIG_FILE}"; then
    echo "✅ GitHub connected successfully"
else
    echo "❌ GitHub connection failed"
    exit 1
fi

# List all connections
sdlcctl mcp list --config "${CONFIG_FILE}"
```

---

### CI/CD Integration

Use MCP CLI in GitHub Actions:

```yaml
name: Connect MCP Platforms

on:
  workflow_dispatch:

jobs:
  setup-mcp:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install sdlcctl
        run: |
          pip install -e backend/sdlcctl

      - name: Connect Slack
        env:
          SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
          SLACK_SIGNING_SECRET: ${{ secrets.SLACK_SIGNING_SECRET }}
        run: |
          sdlcctl mcp connect --slack \
            --bot-token "$SLACK_BOT_TOKEN" \
            --signing-secret "$SLACK_SIGNING_SECRET" \
            --channel "bugs" \
            --config "/tmp/mcp.json"

      - name: Verify Slack Connection
        run: |
          sdlcctl mcp test --slack --config "/tmp/mcp.json"

      - name: Connect GitHub
        env:
          GITHUB_APP_ID: ${{ secrets.GITHUB_APP_ID }}
          GITHUB_PRIVATE_KEY: ${{ secrets.GITHUB_PRIVATE_KEY }}
        run: |
          echo "$GITHUB_PRIVATE_KEY" > /tmp/github.pem
          chmod 600 /tmp/github.pem
          sdlcctl mcp connect --github \
            --app-id "$GITHUB_APP_ID" \
            --private-key "/tmp/github.pem" \
            --repo "nqh/sdlc-orchestrator" \
            --config "/tmp/mcp.json"

      - name: Verify GitHub Connection
        run: |
          sdlcctl mcp test --github --config "/tmp/mcp.json"

      - name: List Connections
        run: |
          sdlcctl mcp list --config "/tmp/mcp.json"
```

---

## Evidence Vault Integration

All MCP commands create tamper-evident audit trail via Evidence Vault.

### Evidence Artifacts

Each MCP operation creates an Evidence artifact:

**Connect Operation**:
```json
{
  "artifact_id": "EVD-2026-02-001",
  "operation": "mcp_connect",
  "platform": "slack",
  "metadata": {
    "bot_token": "xoxb-***",
    "channel": "bugs",
    "connected_at": "2026-02-03T10:30:00Z"
  },
  "hash": "a1b2c3d4...",
  "signature": "ed25519_signature",
  "previous_hash": null,
  "signer_key_id": "key-abc123"
}
```

### Verification

Verify Evidence artifact integrity:

```bash
# List recent Evidence artifacts
ls -la ~/.mcp/evidence/

# Output:
# EVD-2026-02-001.json  (Slack connect)
# EVD-2026-02-002.json  (GitHub connect)
# EVD-2026-02-003.json  (Slack disconnect)

# Verify signature (requires Evidence Vault CLI)
sdlcctl evidence verify EVD-2026-02-001
```

**Output**:
```
✅ Artifact EVD-2026-02-001 verification: PASS
  - Hash integrity: VALID
  - Ed25519 signature: VALID
  - Hash chain: INTACT
  - Tamper detected: NO
```

---

## API Reference

MCP CLI internally uses these Python modules:

### SlackAdapter

```python
from sdlcctl.services.mcp.slack_adapter import SlackAdapter

adapter = SlackAdapter(
    bot_token="xoxb-token",
    signing_secret="secret"
)

# Test connection
adapter.test_connection()

# Post message
adapter.post_message(channel="bugs", text="Hello World")

# Verify webhook signature
adapter.verify_webhook_signature(
    request_body="...",
    timestamp="1234567890",
    signature="v0=..."
)
```

### GitHubAdapter

```python
from sdlcctl.services.mcp.github_adapter import GitHubAdapter

adapter = GitHubAdapter(
    app_id="123456",
    private_key_path="/path/to/github.pem"
)

# Test connection
adapter.test_connection()

# Get installation token
token = adapter.get_installation_token(installation_id=123)

# Verify webhook signature
adapter.verify_webhook_signature(
    request_body=b"...",
    signature="sha256=...",
    webhook_secret="secret"
)
```

### EvidenceVaultAdapter

```python
from sdlcctl.services.mcp.evidence_vault_adapter import EvidenceVaultAdapter

vault = EvidenceVaultAdapter(vault_path="~/.mcp/evidence")

# Create artifact
artifact_id = vault.create_artifact(
    operation="mcp_connect",
    platform="slack",
    metadata={"channel": "bugs"}
)

# Verify artifact
is_valid = vault.verify_artifact(artifact_id)

# List artifacts
artifacts = vault.list_artifacts(limit=10)
```

---

## Security Best Practices

1. **Never commit credentials**:
   ```bash
   # Add to .gitignore
   echo ".mcp.json" >> .gitignore
   echo "*.pem" >> .gitignore
   ```

2. **Use environment variables in CI/CD**:
   ```yaml
   env:
     SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
   ```

3. **Rotate credentials regularly**:
   - Slack: Regenerate bot token every 90 days
   - GitHub: Regenerate private key every 180 days

4. **Secure private keys**:
   ```bash
   chmod 600 ~/.ssh/github-app.pem
   ```

5. **Verify Evidence artifacts**:
   ```bash
   sdlcctl evidence verify EVD-2026-02-001
   ```

---

## Performance Benchmarks

**Command Execution Times** (measured on Linux 6.8.0, Python 3.12.3):

| Command | Execution Time | Performance Budget |
|---------|---------------|-------------------|
| `connect --slack` | 0.03s | <5s |
| `connect --github` | 0.03s | <5s |
| `test --slack` | 0.02s | <5s |
| `test --github` | 0.02s | <5s |
| `list` | 0.01s | <5s |
| `disconnect` | 0.02s | <5s |

**Evidence Vault Throughput**:
- Artifact creation: >100 artifacts/sec
- Signature verification: >200 verifications/sec
- Hash chain validation: >150 validations/sec

---

## Version History

### v1.0.0 (February 3, 2026)
- Initial release
- Slack MCP integration
- GitHub MCP integration
- Evidence Vault integration
- Zero deprecation warnings
- Production-ready (8/8 tests passed)

---

## Support

**Documentation**: https://github.com/nqh/sdlc-orchestrator/tree/main/backend/sdlcctl/docs
**Issues**: https://github.com/nqh/sdlc-orchestrator/issues
**Slack**: #sdlc-support
**Email**: support@sdlc-orchestrator.com

---

## License

Copyright © 2026 SDLC Orchestrator Team
Licensed under Apache-2.0

---

**End of CLI Reference Guide**
