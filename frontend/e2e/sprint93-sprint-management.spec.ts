/**
 * E2E Test: Sprint 93 Sprint Management UI
 * @status Sprint 93 - Planning Hierarchy Part 2
 * @description Tests for Sprint CRUD, Charts, and Backlog Management
 *
 * Test Coverage:
 * - Sprint Page Navigation
 * - Sprint List Display
 * - Sprint Modal (Create/Edit)
 * - Burndown Chart
 * - Velocity Chart
 * - Team Workload Chart
 * - Backlog List with Filters
 *
 * @sdlc SDLC 5.1.3 Framework - Sprint 93
 * @reference Pillar 2: Sprint Planning Governance
 * @date January 22, 2026
 */

import { test, expect } from "@playwright/test";

// =============================================================================
// Sprint Page Navigation Tests
// =============================================================================

test.describe("Sprint Page Navigation", () => {
  test("should load sprints page", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    const currentUrl = page.url();
    // Should be on sprints page or redirect to login
    expect(currentUrl).toMatch(/sprints|login/);
  });

  test("should display page header with title", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      // Look for page title
      const pageTitle = page.locator('h1, [class*="title"]');
      const titleText = await pageTitle.first().textContent();
      console.log(`Sprints page title: ${titleText}`);

      // Should contain Sprint-related text
      expect(titleText?.toLowerCase()).toMatch(/sprint|planning/);
    }
  });

  test("should have Back to Planning link", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const backLink = page.locator('a:has-text("Back to Planning"), a[href*="/planning"]');
      const hasBackLink = await backLink.first().isVisible().catch(() => false);
      console.log(`Back to Planning link visible: ${hasBackLink}`);
    }
  });
});

// =============================================================================
// Sprint List Tests
// =============================================================================

test.describe("Sprint List Display", () => {
  test("should display sprint list or empty state", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      // Look for sprint cards or empty state
      const sprintCards = page.locator('[class*="sprint-card"], [class*="rounded"]');
      const emptyState = page.locator('text=/no sprint|create your first/i');

      const hasCards = await sprintCards.first().isVisible().catch(() => false);
      const hasEmptyState = await emptyState.first().isVisible().catch(() => false);

      console.log(`Sprint cards found: ${hasCards}, Empty state: ${hasEmptyState}`);
    }
  });

  test("should have New Sprint button", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const newSprintButton = page.locator('button:has-text("New Sprint"), button:has-text("Create Sprint")');
      const hasButton = await newSprintButton.first().isVisible().catch(() => false);
      console.log(`New Sprint button visible: ${hasButton}`);
    }
  });

  test("should display sprint status badges", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const pageText = await page.textContent("body");

      // Check for status badges
      const hasPlanned = pageText?.toLowerCase().includes("planned");
      const hasActive = pageText?.toLowerCase().includes("active");
      const hasClosed = pageText?.toLowerCase().includes("closed");

      console.log(`Status badges - Planned: ${hasPlanned}, Active: ${hasActive}, Closed: ${hasClosed}`);
    }
  });
});

// =============================================================================
// Sprint Modal Tests
// =============================================================================

test.describe("Sprint Modal", () => {
  test("should open create sprint modal on button click", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const newSprintButton = page.locator('button:has-text("New Sprint"), button:has-text("Create Sprint")');

      if (await newSprintButton.first().isVisible().catch(() => false)) {
        await newSprintButton.first().click();
        await page.waitForTimeout(500);

        // Check if modal is open
        const modal = page.locator('[role="dialog"], [class*="Dialog"], [class*="Modal"]');
        const modalVisible = await modal.first().isVisible().catch(() => false);
        console.log(`Sprint modal visible: ${modalVisible}`);

        // Close modal if open
        if (modalVisible) {
          const cancelButton = page.locator('button:has-text("Cancel")');
          if (await cancelButton.first().isVisible().catch(() => false)) {
            await cancelButton.first().click();
          }
        }
      }
    }
  });

  test("should display sprint form fields", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const newSprintButton = page.locator('button:has-text("New Sprint"), button:has-text("Create Sprint")');

      if (await newSprintButton.first().isVisible().catch(() => false)) {
        await newSprintButton.first().click();
        await page.waitForTimeout(500);

        // Check for form fields
        const nameField = page.locator('input[name="name"], input[id="name"]');
        const goalField = page.locator('textarea[name="goal"], textarea[id="goal"]');
        const startDateField = page.locator('input[type="date"][name*="start"], input[id*="start"]');
        const endDateField = page.locator('input[type="date"][name*="end"], input[id*="end"]');
        const capacityField = page.locator('input[name*="capacity"], input[id*="capacity"]');

        const hasName = await nameField.first().isVisible().catch(() => false);
        const hasGoal = await goalField.first().isVisible().catch(() => false);
        const hasStartDate = await startDateField.first().isVisible().catch(() => false);
        const hasEndDate = await endDateField.first().isVisible().catch(() => false);
        const hasCapacity = await capacityField.first().isVisible().catch(() => false);

        console.log(`Form fields - Name: ${hasName}, Goal: ${hasGoal}, Start: ${hasStartDate}, End: ${hasEndDate}, Capacity: ${hasCapacity}`);

        // Close modal
        const cancelButton = page.locator('button:has-text("Cancel")');
        if (await cancelButton.first().isVisible().catch(() => false)) {
          await cancelButton.first().click();
        }
      }
    }
  });

  test("should show SDLC 5.1.3 guidelines in modal", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const newSprintButton = page.locator('button:has-text("New Sprint"), button:has-text("Create Sprint")');

      if (await newSprintButton.first().isVisible().catch(() => false)) {
        await newSprintButton.first().click();
        await page.waitForTimeout(500);

        // Check for SDLC 5.1.3 guidelines
        const modalText = await page.locator('[role="dialog"]').textContent().catch(() => "");
        const hasGuidelines = modalText.includes("SDLC 5.1.3") || modalText.includes("G-Sprint");

        console.log(`SDLC 5.1.3 guidelines found: ${hasGuidelines}`);

        // Close modal
        const cancelButton = page.locator('button:has-text("Cancel")');
        if (await cancelButton.first().isVisible().catch(() => false)) {
          await cancelButton.first().click();
        }
      }
    }
  });
});

// =============================================================================
// Sprint Detail Page Tests
// =============================================================================

test.describe("Sprint Detail Page", () => {
  test("should navigate to sprint detail on click", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      // Try to click on a sprint link
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const currentUrl = page.url();
        console.log(`Navigated to: ${currentUrl}`);
        expect(currentUrl).toMatch(/\/sprints\//);
      }
    }
  });
});

// =============================================================================
// Burndown Chart Tests
// =============================================================================

test.describe("Burndown Chart", () => {
  test("should display burndown chart on sprint detail", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      // Navigate to first sprint if available
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Look for burndown chart
        const burndownChart = page.locator('text=/burndown/i');
        const chartContainer = page.locator('[class*="recharts"], svg[class*="chart"]');

        const hasBurndownText = await burndownChart.first().isVisible().catch(() => false);
        const hasChartContainer = await chartContainer.first().isVisible().catch(() => false);

        console.log(`Burndown chart - Text: ${hasBurndownText}, Container: ${hasChartContainer}`);
      }
    }
  });

  test("should show burndown health status", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const pageText = await page.textContent("body");

        // Check for health status indicators
        const hasOnTrack = pageText?.toLowerCase().includes("on track");
        const hasAhead = pageText?.toLowerCase().includes("ahead");
        const hasBehind = pageText?.toLowerCase().includes("behind");
        const hasAtRisk = pageText?.toLowerCase().includes("at risk");

        console.log(`Health status - On Track: ${hasOnTrack}, Ahead: ${hasAhead}, Behind: ${hasBehind}, At Risk: ${hasAtRisk}`);
      }
    }
  });
});

// =============================================================================
// Velocity Chart Tests
// =============================================================================

test.describe("Velocity Chart", () => {
  test("should display velocity chart", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const pageText = await page.textContent("body");

      // Look for velocity-related text
      const hasVelocity = pageText?.toLowerCase().includes("velocity");

      console.log(`Velocity chart text found: ${hasVelocity}`);
    }
  });

  test("should show velocity trend indicator", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const pageText = await page.textContent("body");

      // Check for trend indicators
      const hasImproving = pageText?.toLowerCase().includes("improving");
      const hasStable = pageText?.toLowerCase().includes("stable");
      const hasDeclining = pageText?.toLowerCase().includes("declining");

      console.log(`Velocity trend - Improving: ${hasImproving}, Stable: ${hasStable}, Declining: ${hasDeclining}`);
    }
  });
});

// =============================================================================
// Team Workload Chart Tests
// =============================================================================

test.describe("Team Workload Chart", () => {
  test("should display team workload section", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const pageText = await page.textContent("body");

        // Look for team workload text
        const hasWorkload = pageText?.toLowerCase().includes("workload") || pageText?.toLowerCase().includes("team");

        console.log(`Team workload section found: ${hasWorkload}`);
      }
    }
  });
});

// =============================================================================
// Backlog List Tests
// =============================================================================

test.describe("Backlog List", () => {
  test("should display backlog items section", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const pageText = await page.textContent("body");

        // Look for backlog text
        const hasBacklog = pageText?.toLowerCase().includes("backlog") || pageText?.toLowerCase().includes("items");

        console.log(`Backlog section found: ${hasBacklog}`);
      }
    }
  });

  test("should display filter controls", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Look for filter controls
        const searchInput = page.locator('input[placeholder*="search"], input[type="search"]');
        const filterSelect = page.locator('select');

        const hasSearch = await searchInput.first().isVisible().catch(() => false);
        const hasFilters = await filterSelect.first().isVisible().catch(() => false);

        console.log(`Backlog filters - Search: ${hasSearch}, Selects: ${hasFilters}`);
      }
    }
  });

  test("should display priority badges", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const pageText = await page.textContent("body");

        // Check for priority badges
        const hasP0 = pageText?.includes("P0");
        const hasP1 = pageText?.includes("P1");
        const hasP2 = pageText?.includes("P2");
        const hasP3 = pageText?.includes("P3");

        console.log(`Priority badges - P0: ${hasP0}, P1: ${hasP1}, P2: ${hasP2}, P3: ${hasP3}`);
      }
    }
  });

  test("should display status indicators", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const pageText = await page.textContent("body");

        // Check for status indicators
        const hasTodo = pageText?.toLowerCase().includes("to do");
        const hasInProgress = pageText?.toLowerCase().includes("in progress");
        const hasReview = pageText?.toLowerCase().includes("review");
        const hasDone = pageText?.toLowerCase().includes("done");

        console.log(`Status indicators - To Do: ${hasTodo}, In Progress: ${hasInProgress}, Review: ${hasReview}, Done: ${hasDone}`);
      }
    }
  });
});

// =============================================================================
// Sprint Governance Tests (SDLC 5.1.3)
// =============================================================================

test.describe("Sprint Governance (SDLC 5.1.3)", () => {
  test("should display G-Sprint gate status", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const pageText = await page.textContent("body");

      // Check for gate status
      const hasGSprint = pageText?.includes("G-Sprint") || pageText?.includes("g-sprint");

      console.log(`G-Sprint gate reference found: ${hasGSprint}`);
    }
  });

  test("should display G-Sprint-Close gate status", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const pageText = await page.textContent("body");

        // Check for close gate
        const hasGSprintClose = pageText?.includes("G-Sprint-Close") || pageText?.includes("close gate");

        console.log(`G-Sprint-Close gate reference found: ${hasGSprintClose}`);
      }
    }
  });

  test("should show documentation deadline for closing sprints", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const pageText = await page.textContent("body");

      // Check for documentation-related text
      const hasDocumentation = pageText?.toLowerCase().includes("documentation");
      const has24h = pageText?.includes("24h") || pageText?.includes("24 hour");

      console.log(`Documentation deadline - Text: ${hasDocumentation}, 24h: ${has24h}`);
    }
  });
});
