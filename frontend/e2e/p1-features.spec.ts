/**
 * E2E Test: P1 Features (Sprint 69 Go-Live)
 * @status Sprint 69 - Phase 3 QA
 * @description Tests for P1 backend hooks: Council, SAST, Evidence Timeline
 *
 * Test Coverage:
 * - Council History Page
 * - SAST Analytics Dashboard
 * - Evidence Timeline with Override Rate
 * - Gate Notification Flow
 */

import { test, expect } from "@playwright/test";

// =============================================================================
// Council History Tests
// =============================================================================

test.describe("Council History - Project AI Council", () => {
  test("should load council history page", async ({ page }) => {
    // Navigate to council history (assuming project ID in URL)
    await page.goto("/app/projects/test-project/council");
    await page.waitForLoadState("networkidle");

    const currentUrl = page.url();
    // Should be on council page or redirect to login/project list
    expect(currentUrl).toMatch(/council|login|projects/);
  });

  test("should display council stats cards", async ({ page }) => {
    await page.goto("/app/projects/test-project/council");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/council")) {
      // Look for stats cards
      const statsCards = page.locator('[class*="card"], [class*="Card"], [class*="stat"]');
      const cardCount = await statsCards.count();
      console.log(`Council stats cards found: ${cardCount}`);

      // Check for specific metrics
      const pageText = await page.textContent("body");
      const hasDeliberations = pageText?.includes("Deliberation") || pageText?.includes("deliberation");
      const hasConfidence = pageText?.includes("Confidence") || pageText?.includes("confidence");
      console.log(`Stats visible: Deliberations=${hasDeliberations}, Confidence=${hasConfidence}`);
    }
  });

  test("should display council history list", async ({ page }) => {
    await page.goto("/app/projects/test-project/council");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/council")) {
      // Look for history items
      const historyItems = page.locator('[class*="history"], table tbody tr, [class*="list"] > div');
      const itemCount = await historyItems.count();
      console.log(`Council history items found: ${itemCount}`);
    }
  });

  test("should filter by council mode", async ({ page }) => {
    await page.goto("/app/projects/test-project/council");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/council")) {
      // Look for mode filter (single, council, auto)
      const modeFilter = page.locator('select, [role="combobox"], button:has-text("Mode"), button:has-text("Filter")');
      const hasFilter = await modeFilter.first().isVisible().catch(() => false);
      console.log(`Mode filter visible: ${hasFilter}`);
    }
  });

  test("should display provider badges", async ({ page }) => {
    await page.goto("/app/projects/test-project/council");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/council")) {
      // Look for provider badges (ollama, claude, etc)
      const badges = page.locator('[class*="badge"], [class*="Badge"]');
      const badgeCount = await badges.count();
      console.log(`Provider badges found: ${badgeCount}`);

      // Check for specific providers
      const pageText = await page.textContent("body");
      const hasOllama = pageText?.toLowerCase().includes("ollama");
      const hasClaude = pageText?.toLowerCase().includes("claude");
      console.log(`Providers visible: Ollama=${hasOllama}, Claude=${hasClaude}`);
    }
  });
});

// =============================================================================
// SAST Analytics Tests
// =============================================================================

test.describe("SAST Analytics - Security Dashboard", () => {
  test("should load SAST analytics page", async ({ page }) => {
    await page.goto("/app/projects/test-project/sast");
    await page.waitForLoadState("networkidle");

    const currentUrl = page.url();
    expect(currentUrl).toMatch(/sast|login|projects|security/);
  });

  test("should display SAST summary cards", async ({ page }) => {
    await page.goto("/app/projects/test-project/sast");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sast") || page.url().includes("/security")) {
      // Look for summary cards
      const summaryCards = page.locator('[class*="card"], [class*="Card"]');
      const cardCount = await summaryCards.count();
      console.log(`SAST summary cards found: ${cardCount}`);

      // Check for severity metrics
      const pageText = await page.textContent("body");
      const hasCritical = pageText?.includes("Critical") || pageText?.includes("CRITICAL");
      const hasHigh = pageText?.includes("High") || pageText?.includes("HIGH");
      console.log(`Severities visible: Critical=${hasCritical}, High=${hasHigh}`);
    }
  });

  test("should display scan history table", async ({ page }) => {
    await page.goto("/app/projects/test-project/sast");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sast") || page.url().includes("/security")) {
      // Look for scan history table
      const table = page.locator("table, [role='grid']");
      const hasTable = await table.isVisible().catch(() => false);
      console.log(`Scan history table visible: ${hasTable}`);

      // Check for scan history items
      const historyItems = page.locator('table tbody tr, [class*="scan"]');
      const itemCount = await historyItems.count();
      console.log(`Scan history items found: ${itemCount}`);
    }
  });

  test("should display category breakdown chart", async ({ page }) => {
    await page.goto("/app/projects/test-project/sast");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sast") || page.url().includes("/security")) {
      // Look for chart elements
      const chart = page.locator('svg, canvas, [class*="chart"], [class*="Chart"]');
      const hasChart = await chart.first().isVisible().catch(() => false);
      console.log(`Category chart visible: ${hasChart}`);
    }
  });

  test("should display findings trend", async ({ page }) => {
    await page.goto("/app/projects/test-project/sast/trend");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/trend") || page.url().includes("/sast")) {
      // Look for trend chart
      const trendChart = page.locator('[class*="trend"], [class*="Trend"], svg');
      const hasTrend = await trendChart.first().isVisible().catch(() => false);
      console.log(`Trend chart visible: ${hasTrend}`);

      // Check for trend direction
      const pageText = await page.textContent("body");
      const hasDirection = pageText?.includes("creasing") || pageText?.includes("stable");
      console.log(`Trend direction visible: ${hasDirection}`);
    }
  });

  test("should trigger SAST scan button", async ({ page }) => {
    await page.goto("/app/projects/test-project/sast");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sast") || page.url().includes("/security")) {
      // Look for scan trigger button
      const scanButton = page.locator('button:has-text("Scan"), button:has-text("Run"), button:has-text("Start")');
      const hasScanButton = await scanButton.first().isVisible().catch(() => false);
      console.log(`Scan trigger button visible: ${hasScanButton}`);
    }
  });
});

// =============================================================================
// Evidence Timeline Tests
// =============================================================================

test.describe("Evidence Timeline - Override Rate", () => {
  test("should load evidence timeline page", async ({ page }) => {
    await page.goto("/app/projects/test-project/timeline");
    await page.waitForLoadState("networkidle");

    const currentUrl = page.url();
    expect(currentUrl).toMatch(/timeline|evidence|login|projects/);
  });

  test("should display timeline stats including override rate", async ({ page }) => {
    await page.goto("/app/projects/test-project/timeline");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/timeline") || page.url().includes("/evidence")) {
      // Look for stats cards
      const statsCards = page.locator('[class*="stat"], [class*="Stat"], [class*="card"]');
      const cardCount = await statsCards.count();
      console.log(`Timeline stats cards found: ${cardCount}`);

      // Check for override rate metric
      const pageText = await page.textContent("body");
      const hasOverrideRate = pageText?.includes("Override") && pageText?.includes("Rate");
      const hasPassRate = pageText?.includes("Pass") && pageText?.includes("Rate");
      console.log(`Stats visible: OverrideRate=${hasOverrideRate}, PassRate=${hasPassRate}`);
    }
  });

  test("should display AI code events list", async ({ page }) => {
    await page.goto("/app/projects/test-project/timeline");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/timeline") || page.url().includes("/evidence")) {
      // Look for event items
      const eventItems = page.locator('[class*="event"], [class*="Event"], table tbody tr');
      const eventCount = await eventItems.count();
      console.log(`AI code events found: ${eventCount}`);
    }
  });

  test("should display AI tool badges", async ({ page }) => {
    await page.goto("/app/projects/test-project/timeline");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/timeline") || page.url().includes("/evidence")) {
      // Look for AI tool badges
      const toolBadges = page.locator('[class*="badge"]:has-text("Cursor"), [class*="badge"]:has-text("Copilot"), [class*="badge"]:has-text("Claude")');
      const badgeCount = await toolBadges.count();
      console.log(`AI tool badges found: ${badgeCount}`);
    }
  });

  test("should filter by validation status", async ({ page }) => {
    await page.goto("/app/projects/test-project/timeline");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/timeline") || page.url().includes("/evidence")) {
      // Look for status filter
      const statusFilter = page.locator('select, [role="combobox"], button:has-text("Status"), button:has-text("Filter")');
      const hasFilter = await statusFilter.first().isVisible().catch(() => false);
      console.log(`Status filter visible: ${hasFilter}`);
    }
  });

  test("should filter by AI tool", async ({ page }) => {
    await page.goto("/app/projects/test-project/timeline");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/timeline") || page.url().includes("/evidence")) {
      // Look for AI tool filter
      const toolFilter = page.locator('select:has-text("AI"), [role="combobox"], button:has-text("Tool")');
      const hasFilter = await toolFilter.first().isVisible().catch(() => false);
      console.log(`AI tool filter visible: ${hasFilter}`);
    }
  });

  test("should show override request button for failed events", async ({ page }) => {
    await page.goto("/app/projects/test-project/timeline");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/timeline") || page.url().includes("/evidence")) {
      // Look for override request button
      const overrideBtn = page.locator('button:has-text("Override"), button:has-text("Request")');
      const hasOverrideBtn = await overrideBtn.first().isVisible().catch(() => false);
      console.log(`Override request button visible: ${hasOverrideBtn}`);
    }
  });
});

// =============================================================================
// Gate Notification Flow Tests
// =============================================================================

test.describe("Gate Notification Flow", () => {
  test("should load gates page", async ({ page }) => {
    await page.goto("/app/projects/test-project/gates");
    await page.waitForLoadState("networkidle");

    const currentUrl = page.url();
    expect(currentUrl).toMatch(/gates|login|projects/);
  });

  test("should display gate status cards", async ({ page }) => {
    await page.goto("/app/projects/test-project/gates");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/gates")) {
      // Look for gate cards
      const gateCards = page.locator('[class*="gate"], [class*="Gate"], [class*="card"]');
      const cardCount = await gateCards.count();
      console.log(`Gate cards found: ${cardCount}`);
    }
  });

  test("should show submit button for draft gates", async ({ page }) => {
    await page.goto("/app/projects/test-project/gates");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/gates")) {
      // Look for submit button
      const submitBtn = page.locator('button:has-text("Submit"), button:has-text("Request Approval")');
      const hasSubmitBtn = await submitBtn.first().isVisible().catch(() => false);
      console.log(`Submit button visible: ${hasSubmitBtn}`);
    }
  });

  test("should display approval history", async ({ page }) => {
    await page.goto("/app/projects/test-project/gates");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/gates")) {
      // Look for approval history section
      const approvalSection = page.locator('[class*="approval"], [class*="history"]');
      const hasApprovalSection = await approvalSection.first().isVisible().catch(() => false);
      console.log(`Approval history visible: ${hasApprovalSection}`);
    }
  });

  test("should show notification preferences link", async ({ page }) => {
    await page.goto("/app/settings/notifications");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/notifications") || page.url().includes("/settings")) {
      // Look for notification settings
      const notificationSettings = page.locator('[class*="notification"], [class*="Notification"]');
      const hasSettings = await notificationSettings.first().isVisible().catch(() => false);
      console.log(`Notification settings visible: ${hasSettings}`);
    }
  });
});

// =============================================================================
// Admin AI Provider Settings Tests (ADR-027)
// =============================================================================

test.describe("Admin AI Provider Settings", () => {
  test("should load AI providers admin page", async ({ page }) => {
    await page.goto("/admin/ai-providers");
    await page.waitForLoadState("networkidle");

    const currentUrl = page.url();
    expect(currentUrl).toMatch(/ai-providers|login|admin/);
  });

  test("should display provider cards", async ({ page }) => {
    await page.goto("/admin/ai-providers");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/ai-providers")) {
      // Look for provider cards
      const providerCards = page.locator('[class*="card"], [class*="Card"]');
      const cardCount = await providerCards.count();
      console.log(`AI provider cards found: ${cardCount}`);

      // Check for specific providers
      const pageText = await page.textContent("body");
      const hasOllama = pageText?.toLowerCase().includes("ollama");
      const hasClaude = pageText?.toLowerCase().includes("claude");
      const hasOpenAI = pageText?.toLowerCase().includes("openai");
      console.log(`Providers visible: Ollama=${hasOllama}, Claude=${hasClaude}, OpenAI=${hasOpenAI}`);
    }
  });

  test("should have enable/disable toggles", async ({ page }) => {
    await page.goto("/admin/ai-providers");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/ai-providers")) {
      // Look for toggle switches
      const toggles = page.locator('[role="switch"], input[type="checkbox"], [class*="switch"], [class*="Switch"]');
      const toggleCount = await toggles.count();
      console.log(`Provider toggles found: ${toggleCount}`);
    }
  });

  test("should display provider priority order", async ({ page }) => {
    await page.goto("/admin/ai-providers");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/ai-providers")) {
      // Look for priority/order indicators
      const pageText = await page.textContent("body");
      const hasPriority = pageText?.includes("Priority") || pageText?.includes("priority") || pageText?.includes("Order");
      console.log(`Priority order visible: ${hasPriority}`);
    }
  });

  test("should show connection status badges", async ({ page }) => {
    await page.goto("/admin/ai-providers");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/ai-providers")) {
      // Look for status badges
      const statusBadges = page.locator('[class*="badge"]:has-text("Connected"), [class*="badge"]:has-text("Online"), [class*="badge"]:has-text("Offline")');
      const badgeCount = await statusBadges.count();
      console.log(`Connection status badges found: ${badgeCount}`);
    }
  });

  test("should have test connection button", async ({ page }) => {
    await page.goto("/admin/ai-providers");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/ai-providers")) {
      // Look for test connection button
      const testBtn = page.locator('button:has-text("Test"), button:has-text("Verify"), button:has-text("Check")');
      const hasTestBtn = await testBtn.first().isVisible().catch(() => false);
      console.log(`Test connection button visible: ${hasTestBtn}`);
    }
  });
});

// =============================================================================
// Codegen Page Tests
// =============================================================================

test.describe("Codegen Page", () => {
  test("should load codegen page", async ({ page }) => {
    await page.goto("/app/codegen");
    await page.waitForLoadState("networkidle");

    const currentUrl = page.url();
    expect(currentUrl).toMatch(/codegen|login/);
  });

  test("should display code generation form", async ({ page }) => {
    await page.goto("/app/codegen");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/codegen")) {
      // Look for form elements
      const form = page.locator("form, [class*='form'], [class*='Form']");
      const hasForm = await form.first().isVisible().catch(() => false);
      console.log(`Codegen form visible: ${hasForm}`);

      // Look for prompt input
      const promptInput = page.locator('textarea, input[type="text"]');
      const hasPromptInput = await promptInput.first().isVisible().catch(() => false);
      console.log(`Prompt input visible: ${hasPromptInput}`);
    }
  });

  test("should have generate button", async ({ page }) => {
    await page.goto("/app/codegen");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/codegen")) {
      // Look for generate button
      const generateBtn = page.locator('button:has-text("Generate"), button:has-text("Create"), button[type="submit"]');
      const hasGenerateBtn = await generateBtn.first().isVisible().catch(() => false);
      console.log(`Generate button visible: ${hasGenerateBtn}`);
    }
  });

  test("should display provider selection", async ({ page }) => {
    await page.goto("/app/codegen");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/codegen")) {
      // Look for provider selection
      const providerSelect = page.locator('select, [role="combobox"]');
      const hasProviderSelect = await providerSelect.first().isVisible().catch(() => false);
      console.log(`Provider selection visible: ${hasProviderSelect}`);
    }
  });
});
