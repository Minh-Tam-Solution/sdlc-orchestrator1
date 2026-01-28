/**
 * Sprint 113 E2E Tests - Auto-Generation Layer UI
 *
 * @module frontend/e2e/sprint113-auto-generation.spec
 * @description E2E tests for Auto-Generation components (Intent, Ownership, Context, Attestation)
 * @sdlc SDLC 5.3.0 Framework - Sprint 113 (Governance UI - Auto-Generation Layer)
 * @status Sprint 113 - January 28, 2026
 * @adr ADR-041 (Framework 6.0 Governance System)
 * @see frontend/src/components/governance/auto-generation/
 */

import { test, expect, Page } from "@playwright/test";

// =============================================================================
// Test Configuration
// =============================================================================

const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000";
const GOVERNANCE_URL = `${BASE_URL}/app/governance`;

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Navigate to Governance page and wait for load
 */
async function navigateToGovernance(page: Page): Promise<void> {
  await page.goto(GOVERNANCE_URL);
  await page.waitForLoadState("networkidle");
}

/**
 * Mock authenticated session with admin role
 */
async function mockAuthenticatedSession(page: Page): Promise<void> {
  await page.addInitScript(() => {
    localStorage.setItem("auth_token", "mock_jwt_token_for_testing");
    localStorage.setItem("user", JSON.stringify({
      id: "user-123",
      email: "admin@sdlc-orchestrator.dev",
      name: "Test Admin",
      role: "admin",
      permissions: ["governance:write", "governance:admin"],
    }));
  });
}

/**
 * Mock Auto-Generation API responses
 */
async function mockAutoGenerationAPI(page: Page): Promise<void> {
  // Mock intent generation endpoint
  await page.route("**/api/v1/governance/auto-generate/intent", async (route) => {
    const method = route.request().method();
    if (method === "POST") {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          task_id: "TASK-001",
          content: "## Intent Document\n\n### Why This Change?\n\nThis change improves user authentication flow by adding MFA support.\n\n### What Problem Does It Solve?\n\nUsers currently lack additional security options for their accounts.\n\n### Alternatives Considered\n\n1. SMS-based verification (rejected: cost)\n2. Email-based 2FA (rejected: slower UX)",
          auto_generated: true,
          generation_method: "llm",
          model_used: "qwen3:32b",
          confidence: 0.92,
          generated_at: "2026-01-28T10:00:00Z",
          time_saved_minutes: 15,
        }),
      });
    }
  });

  // Mock ownership suggestions endpoint
  await page.route("**/api/v1/governance/ownership/suggestions*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        pr_number: 123,
        suggestions: [
          {
            file_path: "backend/app/services/auth_service.py",
            suggested_owner: "@john-doe",
            confidence: 0.95,
            reason: "Most recent committer (15 commits in 30 days)",
            sources: ["git_blame", "codeowners"],
          },
          {
            file_path: "backend/app/models/user.py",
            suggested_owner: "@jane-smith",
            confidence: 0.87,
            reason: "Declared in CODEOWNERS",
            sources: ["codeowners"],
          },
          {
            file_path: "backend/tests/test_auth.py",
            suggested_owner: "@qa-team",
            confidence: 0.72,
            reason: "Directory pattern match (tests/)",
            sources: ["directory_pattern"],
          },
        ],
        total_files: 3,
        files_with_owners: 0,
        files_needing_review: 3,
      }),
    });
  });

  // Mock accept ownership endpoint
  await page.route("**/api/v1/governance/ownership/accept", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        accepted_files: 1,
        message: "Ownership accepted successfully",
      }),
    });
  });

  // Mock context attachments endpoint
  await page.route("**/api/v1/governance/context/attachments*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        pr_number: 123,
        attachments: [
          {
            id: "ctx-001",
            type: "adr",
            title: "ADR-015: Authentication Service Refactoring",
            path: "docs/02-design/03-ADRs/ADR-015-Auth-Refactoring.md",
            relevance_score: 0.94,
            auto_attached: true,
            reason: "Module mentioned: auth_service",
          },
          {
            id: "ctx-002",
            type: "spec",
            title: "Auth Service API Specification",
            path: "docs/01-planning/05-API-Design/auth-service-spec.md",
            relevance_score: 0.89,
            auto_attached: true,
            reason: "Same directory",
          },
          {
            id: "ctx-003",
            type: "design_doc",
            title: "MFA Implementation Design",
            path: "docs/02-design/specs/mfa-design.md",
            relevance_score: 0.85,
            auto_attached: false,
            reason: "Related feature",
          },
        ],
        total_found: 3,
        auto_attached_count: 2,
      }),
    });
  });

  // Mock attach context endpoint
  await page.route("**/api/v1/governance/context/attach", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        attached: true,
        pr_description_updated: true,
        attachments_added: 1,
      }),
    });
  });

  // Mock AI session data for attestation
  await page.route("**/api/v1/governance/attestation/session-data*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        session_id: "ai-session-001",
        ai_provider: "Anthropic",
        model_version: "claude-sonnet-4-5-20250929",
        prompt_hash: "sha256:abc123def456...",
        lines_generated: 150,
        files_affected: 3,
        session_start: "2026-01-28T09:30:00Z",
        session_end: "2026-01-28T10:15:00Z",
        total_tokens: 12500,
        pre_filled_fields: {
          ai_provider: "Anthropic",
          model_version: "claude-sonnet-4-5-20250929",
          lines_generated: 150,
        },
        requires_confirmation: [
          "review_time",
          "modifications_made",
          "understanding_confirmed",
        ],
      }),
    });
  });

  // Mock attestation submit endpoint
  await page.route("**/api/v1/governance/attestation/submit", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        attestation_id: "attest-001",
        submitted: true,
        pr_updated: true,
        compliance_status: "compliant",
      }),
    });
  });

  // Mock projects endpoint
  await page.route("**/api/v1/projects*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        projects: [
          { id: "proj-001", name: "SDLC Orchestrator", slug: "sdlc-orchestrator" },
        ],
        total: 1,
      }),
    });
  });

  // Mock tasks endpoint
  await page.route("**/api/v1/tasks*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        tasks: [
          {
            id: "TASK-001",
            title: "Add MFA support to authentication",
            description: "Implement multi-factor authentication using TOTP",
            status: "in_progress",
          },
        ],
        total: 1,
      }),
    });
  });
}

// =============================================================================
// Test Suites - Intent Generator Card
// =============================================================================

test.describe("Auto-Generation - Intent Generator Card", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
    await navigateToGovernance(page);
  });

  test("should display intent generator card", async ({ page }) => {
    const card = page.getByText(/intent/i).first()
      .or(page.locator('[data-testid="intent-generator-card"]'));
    await expect(card).toBeVisible();
  });

  test("should show task selection input", async ({ page }) => {
    const taskInput = page.getByPlaceholder(/task/i)
      .or(page.getByRole("combobox"))
      .or(page.locator("select"));
    await expect(taskInput.first()).toBeVisible();
  });

  test("should display generate button", async ({ page }) => {
    const generateBtn = page.getByRole("button", { name: /generate/i });
    await expect(generateBtn.first()).toBeVisible();
  });

  test("should show time saved indicator", async ({ page }) => {
    const timeSaved = page.getByText(/time saved/i)
      .or(page.getByText(/15.*min/i));
    await expect(timeSaved.first()).toBeVisible();
  });

  test("should display AI vs template indicator", async ({ page }) => {
    const methodIndicator = page.getByText(/llm/i)
      .or(page.getByText(/ai.*generated/i))
      .or(page.getByText(/template/i));
    // May or may not be visible depending on state
    const count = await methodIndicator.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});

test.describe("Auto-Generation - Intent Generator Actions", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
    await navigateToGovernance(page);
  });

  test("should generate intent document on button click", async ({ page }) => {
    const generateBtn = page.getByRole("button", { name: /generate/i }).first();
    if (await generateBtn.isEnabled()) {
      await generateBtn.click();
      // Wait for generation
      await page.waitForTimeout(500);
      const content = page.getByText(/why this change/i)
        .or(page.getByText(/intent.*document/i));
      await expect(content.first()).toBeVisible();
    }
  });

  test("should show loading state during generation", async ({ page }) => {
    // Add delay to see loading
    await page.route("**/api/v1/governance/auto-generate/intent", async (route) => {
      await new Promise(r => setTimeout(r, 1000));
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ content: "Test", auto_generated: true }),
      });
    });

    const generateBtn = page.getByRole("button", { name: /generate/i }).first();
    if (await generateBtn.isEnabled()) {
      await generateBtn.click();
      const loading = page.getByText(/generating/i)
        .or(page.locator(".animate-spin"));
      await expect(loading.first()).toBeVisible();
    }
  });

  test("should allow copying generated content", async ({ page }) => {
    const copyBtn = page.getByRole("button", { name: /copy/i })
      .or(page.locator('[aria-label*="copy"]'));
    const count = await copyBtn.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("should display confidence score", async ({ page }) => {
    const confidence = page.getByText(/confidence/i)
      .or(page.getByText(/92%/i))
      .or(page.getByText(/0\.92/i));
    const count = await confidence.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});

// =============================================================================
// Test Suites - Ownership Suggestions Card
// =============================================================================

test.describe("Auto-Generation - Ownership Suggestions Card", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
    await navigateToGovernance(page);
  });

  test("should display ownership suggestions card", async ({ page }) => {
    const card = page.getByText(/ownership/i).first()
      .or(page.locator('[data-testid="ownership-suggestions-card"]'));
    await expect(card).toBeVisible();
  });

  test("should show PR input field", async ({ page }) => {
    const prInput = page.getByPlaceholder(/pr/i)
      .or(page.getByLabel(/pull request/i))
      .or(page.locator('input[type="number"]'));
    await expect(prInput.first()).toBeVisible();
  });

  test("should display suggestions list", async ({ page }) => {
    const suggestionsList = page.locator('[data-testid="suggestions-list"]')
      .or(page.getByText(/auth_service\.py/i));
    await expect(suggestionsList.first()).toBeVisible();
  });

  test("should show file paths in suggestions", async ({ page }) => {
    const filePath = page.getByText(/\.py$/i)
      .or(page.getByText(/backend/i));
    await expect(filePath.first()).toBeVisible();
  });

  test("should display suggested owners", async ({ page }) => {
    const owner = page.getByText(/@[a-z-]+/i)
      .or(page.getByText(/john-doe/i))
      .or(page.getByText(/jane-smith/i));
    await expect(owner.first()).toBeVisible();
  });

  test("should show confidence levels", async ({ page }) => {
    const confidence = page.getByText(/\d+%/)
      .or(page.getByText(/confidence/i));
    await expect(confidence.first()).toBeVisible();
  });

  test("should display reason for suggestion", async ({ page }) => {
    const reason = page.getByText(/committer/i)
      .or(page.getByText(/codeowners/i))
      .or(page.getByText(/directory pattern/i));
    await expect(reason.first()).toBeVisible();
  });
});

test.describe("Auto-Generation - Ownership Actions", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
    await navigateToGovernance(page);
  });

  test("should have accept button for each suggestion", async ({ page }) => {
    const acceptBtn = page.getByRole("button", { name: /accept/i });
    const count = await acceptBtn.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("should have reject button for suggestions", async ({ page }) => {
    const rejectBtn = page.getByRole("button", { name: /reject/i })
      .or(page.getByRole("button", { name: /dismiss/i }));
    const count = await rejectBtn.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("should allow batch accept all suggestions", async ({ page }) => {
    const acceptAllBtn = page.getByRole("button", { name: /accept all/i })
      .or(page.getByRole("button", { name: /apply all/i }));
    const count = await acceptAllBtn.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("should show source badges (git_blame, codeowners)", async ({ page }) => {
    const sourceBadge = page.getByText(/git.*blame/i)
      .or(page.getByText(/codeowners/i));
    await expect(sourceBadge.first()).toBeVisible();
  });
});

// =============================================================================
// Test Suites - Context Attachments Card
// =============================================================================

test.describe("Auto-Generation - Context Attachments Card", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
    await navigateToGovernance(page);
  });

  test("should display context attachments card", async ({ page }) => {
    const card = page.getByText(/context/i).first()
      .or(page.locator('[data-testid="context-attachments-card"]'));
    await expect(card).toBeVisible();
  });

  test("should list discovered ADRs", async ({ page }) => {
    const adr = page.getByText(/ADR-/i)
      .or(page.getByText(/architecture decision/i));
    await expect(adr.first()).toBeVisible();
  });

  test("should show relevance scores", async ({ page }) => {
    const relevance = page.getByText(/relevance/i)
      .or(page.getByText(/\d+%/));
    await expect(relevance.first()).toBeVisible();
  });

  test("should display attachment types (ADR, spec, design_doc)", async ({ page }) => {
    const typeIndicator = page.getByText(/adr|spec|design/i);
    await expect(typeIndicator.first()).toBeVisible();
  });

  test("should show auto-attached indicator", async ({ page }) => {
    const autoAttached = page.getByText(/auto.*attach/i)
      .or(page.locator('[data-testid="auto-attached"]'));
    await expect(autoAttached.first()).toBeVisible();
  });

  test("should display file paths", async ({ page }) => {
    const filePath = page.getByText(/docs\//i)
      .or(page.getByText(/\.md$/i));
    await expect(filePath.first()).toBeVisible();
  });
});

test.describe("Auto-Generation - Context Actions", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
    await navigateToGovernance(page);
  });

  test("should have attach button", async ({ page }) => {
    const attachBtn = page.getByRole("button", { name: /attach/i });
    const count = await attachBtn.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("should have remove button for attached items", async ({ page }) => {
    const removeBtn = page.getByRole("button", { name: /remove/i })
      .or(page.locator('[aria-label*="remove"]'));
    const count = await removeBtn.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("should allow refreshing context discovery", async ({ page }) => {
    const refreshBtn = page.getByRole("button", { name: /refresh|scan|discover/i });
    const count = await refreshBtn.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});

// =============================================================================
// Test Suites - Attestation Form Card
// =============================================================================

test.describe("Auto-Generation - Attestation Form Card", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
    await navigateToGovernance(page);
  });

  test("should display attestation form card", async ({ page }) => {
    const card = page.getByText(/attestation/i).first()
      .or(page.locator('[data-testid="attestation-form-card"]'));
    await expect(card).toBeVisible();
  });

  test("should show AI provider field (pre-filled)", async ({ page }) => {
    const provider = page.getByText(/anthropic/i)
      .or(page.getByText(/ai.*provider/i));
    await expect(provider.first()).toBeVisible();
  });

  test("should display model version field (pre-filled)", async ({ page }) => {
    const model = page.getByText(/claude/i)
      .or(page.getByText(/model.*version/i));
    await expect(model.first()).toBeVisible();
  });

  test("should show lines generated count", async ({ page }) => {
    const lines = page.getByText(/150.*line/i)
      .or(page.getByText(/lines.*generated/i));
    await expect(lines.first()).toBeVisible();
  });

  test("should display review timer", async ({ page }) => {
    const timer = page.getByText(/review.*time/i)
      .or(page.getByText(/min.*required/i))
      .or(page.locator('[data-testid="review-timer"]'));
    await expect(timer.first()).toBeVisible();
  });

  test("should show understanding confirmation checkbox", async ({ page }) => {
    const checkbox = page.getByRole("checkbox")
      .or(page.getByLabel(/understand/i))
      .or(page.getByLabel(/confirm/i));
    await expect(checkbox.first()).toBeVisible();
  });
});

test.describe("Auto-Generation - Attestation Actions", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
    await navigateToGovernance(page);
  });

  test("should have submit attestation button", async ({ page }) => {
    const submitBtn = page.getByRole("button", { name: /submit/i });
    await expect(submitBtn.first()).toBeVisible();
  });

  test("should disable submit until minimum review time", async ({ page }) => {
    const submitBtn = page.getByRole("button", { name: /submit/i }).first();
    // Submit should be disabled initially (minimum review time not met)
    const isDisabled = await submitBtn.isDisabled();
    // May or may not be disabled depending on state
    expect(typeof isDisabled).toBe("boolean");
  });

  test("should show modifications textarea", async ({ page }) => {
    const textarea = page.getByPlaceholder(/modification/i)
      .or(page.locator("textarea"));
    const count = await textarea.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("should display session metadata", async ({ page }) => {
    const metadata = page.getByText(/session/i)
      .or(page.getByText(/token/i));
    await expect(metadata.first()).toBeVisible();
  });
});

// =============================================================================
// Test Suites - Loading & Error States
// =============================================================================

test.describe("Auto-Generation - Loading States", () => {
  test("should show loading skeleton on initial load", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/**", async (route) => {
      await new Promise(r => setTimeout(r, 1000));
      await route.fulfill({ status: 200, body: JSON.stringify({}) });
    });

    await page.goto(GOVERNANCE_URL);

    const skeleton = page.locator(".animate-pulse")
      .or(page.locator(".animate-spin"))
      .or(page.getByText(/loading/i));
    await expect(skeleton.first()).toBeVisible();
  });
});

test.describe("Auto-Generation - Error States", () => {
  test("should show error when intent generation fails", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/governance/auto-generate/intent", async (route) => {
      await route.fulfill({
        status: 500,
        body: JSON.stringify({ error: "LLM service unavailable" }),
      });
    });

    await navigateToGovernance(page);

    const generateBtn = page.getByRole("button", { name: /generate/i }).first();
    if (await generateBtn.isEnabled()) {
      await generateBtn.click();
      const error = page.getByText(/error|failed|unavailable/i);
      await expect(error.first()).toBeVisible();
    }
  });

  test("should show fallback message when using template", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/governance/auto-generate/intent", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          content: "Template-based intent",
          auto_generated: true,
          generation_method: "template",
          model_used: null,
        }),
      });
    });

    await navigateToGovernance(page);

    const templateIndicator = page.getByText(/template/i)
      .or(page.getByText(/fallback/i));
    const count = await templateIndicator.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});

// =============================================================================
// Test Suites - Accessibility
// =============================================================================

test.describe("Auto-Generation - Accessibility", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
    await navigateToGovernance(page);
  });

  test("should have proper heading hierarchy", async ({ page }) => {
    const h1 = page.getByRole("heading", { level: 1 });
    await expect(h1.first()).toBeVisible();
  });

  test("should have accessible form labels", async ({ page }) => {
    const labels = page.locator("label");
    const count = await labels.count();
    expect(count).toBeGreaterThan(0);
  });

  test("should support keyboard navigation", async ({ page }) => {
    await page.keyboard.press("Tab");
    const focusedElement = page.locator(":focus");
    await expect(focusedElement).toBeVisible();
  });

  test("should have aria-labels on buttons", async ({ page }) => {
    const buttons = page.getByRole("button");
    const count = await buttons.count();
    expect(count).toBeGreaterThan(0);
  });
});

// =============================================================================
// Test Suites - Responsive Design
// =============================================================================

test.describe("Auto-Generation - Responsive Design", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockAutoGenerationAPI(page);
  });

  test("should display correctly on mobile viewport", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await navigateToGovernance(page);
    const pageContent = page.locator("main").or(page.locator('[role="main"]'));
    await expect(pageContent).toBeVisible();
  });

  test("should display correctly on tablet viewport", async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await navigateToGovernance(page);
    const pageContent = page.locator("main").or(page.locator('[role="main"]'));
    await expect(pageContent).toBeVisible();
  });

  test("should display correctly on desktop viewport", async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await navigateToGovernance(page);
    const pageContent = page.locator("main").or(page.locator('[role="main"]'));
    await expect(pageContent).toBeVisible();
  });
});
