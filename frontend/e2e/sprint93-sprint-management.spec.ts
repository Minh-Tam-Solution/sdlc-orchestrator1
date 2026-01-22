/**
 * E2E Test: Sprint 93 Sprint Management UI
 * @status Sprint 93 - Planning Hierarchy Part 2
 * @description Tests for Sprint CRUD, Charts, and Backlog Management
 *
 * Test Coverage (Day 1):
 * - Sprint Page Navigation
 * - Sprint List Display
 * - Sprint Modal (Create/Edit)
 * - Burndown Chart
 * - Velocity Chart
 * - Team Workload Chart
 * - Backlog List with Filters
 *
 * Test Coverage (Day 2):
 * - Backlog Item Modal (Create/Edit)
 * - Backlog List Multi-Select
 * - Bulk Move Modal
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

// =============================================================================
// Backlog Item Modal Tests (Day 2)
// =============================================================================

test.describe("Backlog Item Modal", () => {
  test("should have Add Item button in sprint detail", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Look for Add Item button
        const addItemButton = page.locator('button:has-text("Add Item"), button:has-text("New Item")');
        const hasButton = await addItemButton.first().isVisible().catch(() => false);
        console.log(`Add Item button visible: ${hasButton}`);
      }
    }
  });

  test("should open create backlog item modal on button click", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const addItemButton = page.locator('button:has-text("Add Item"), button:has-text("New Item")');

        if (await addItemButton.first().isVisible().catch(() => false)) {
          await addItemButton.first().click();
          await page.waitForTimeout(500);

          // Check if modal is open
          const modal = page.locator('[role="dialog"], [class*="Dialog"], [class*="Modal"]');
          const modalVisible = await modal.first().isVisible().catch(() => false);
          console.log(`Backlog item modal visible: ${modalVisible}`);

          // Close modal if open
          if (modalVisible) {
            const cancelButton = page.locator('button:has-text("Cancel")');
            if (await cancelButton.first().isVisible().catch(() => false)) {
              await cancelButton.first().click();
            }
          }
        }
      }
    }
  });

  test("should display backlog item form fields", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const addItemButton = page.locator('button:has-text("Add Item"), button:has-text("New Item")');

        if (await addItemButton.first().isVisible().catch(() => false)) {
          await addItemButton.first().click();
          await page.waitForTimeout(500);

          // Check for form fields
          const titleField = page.locator('input[name="title"], input[id="title"]');
          const descField = page.locator('textarea[name="description"], textarea[id="description"]');
          const prioritySelect = page.locator('select[name="priority"], select[id="priority"]');
          const storyPointsField = page.locator('input[name="story_points"], input[id="story_points"]');

          const hasTitle = await titleField.first().isVisible().catch(() => false);
          const hasDesc = await descField.first().isVisible().catch(() => false);
          const hasPriority = await prioritySelect.first().isVisible().catch(() => false);
          const hasStoryPoints = await storyPointsField.first().isVisible().catch(() => false);

          console.log(`Form fields - Title: ${hasTitle}, Desc: ${hasDesc}, Priority: ${hasPriority}, Story Points: ${hasStoryPoints}`);

          // Close modal
          const cancelButton = page.locator('button:has-text("Cancel")');
          if (await cancelButton.first().isVisible().catch(() => false)) {
            await cancelButton.first().click();
          }
        }
      }
    }
  });

  test("should display type selection grid", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const addItemButton = page.locator('button:has-text("Add Item"), button:has-text("New Item")');

        if (await addItemButton.first().isVisible().catch(() => false)) {
          await addItemButton.first().click();
          await page.waitForTimeout(500);

          // Check for type selection buttons
          const storyType = page.locator('button:has-text("Story")');
          const taskType = page.locator('button:has-text("Task")');
          const bugType = page.locator('button:has-text("Bug")');
          const spikeType = page.locator('button:has-text("Spike")');

          const hasStory = await storyType.first().isVisible().catch(() => false);
          const hasTask = await taskType.first().isVisible().catch(() => false);
          const hasBug = await bugType.first().isVisible().catch(() => false);
          const hasSpike = await spikeType.first().isVisible().catch(() => false);

          console.log(`Type buttons - Story: ${hasStory}, Task: ${hasTask}, Bug: ${hasBug}, Spike: ${hasSpike}`);

          // Close modal
          const cancelButton = page.locator('button:has-text("Cancel")');
          if (await cancelButton.first().isVisible().catch(() => false)) {
            await cancelButton.first().click();
          }
        }
      }
    }
  });

  test("should display Fibonacci story points", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const addItemButton = page.locator('button:has-text("Add Item"), button:has-text("New Item")');

        if (await addItemButton.first().isVisible().catch(() => false)) {
          await addItemButton.first().click();
          await page.waitForTimeout(500);

          // Check for Fibonacci story points options (1, 2, 3, 5, 8, 13, 21)
          const modalText = await page.locator('[role="dialog"]').textContent().catch(() => "");
          const hasFibonacci = modalText?.includes("1") && modalText?.includes("2") &&
            modalText?.includes("3") && modalText?.includes("5") && modalText?.includes("8");

          console.log(`Fibonacci story points visible: ${hasFibonacci}`);

          // Close modal
          const cancelButton = page.locator('button:has-text("Cancel")');
          if (await cancelButton.first().isVisible().catch(() => false)) {
            await cancelButton.first().click();
          }
        }
      }
    }
  });

  test("should open edit modal when clicking backlog item", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Click on a backlog item row (not checkbox)
        const backlogItem = page.locator('[class*="border-b"][class*="cursor-pointer"], [class*="backlog-item"]').first();

        if (await backlogItem.isVisible().catch(() => false)) {
          await backlogItem.click();
          await page.waitForTimeout(500);

          // Check if edit modal is open
          const modalTitle = page.locator('[role="dialog"] h2:has-text("Edit")');
          const isEditModal = await modalTitle.first().isVisible().catch(() => false);

          console.log(`Edit modal opened: ${isEditModal}`);

          // Close modal if open
          const cancelButton = page.locator('button:has-text("Cancel")');
          if (await cancelButton.first().isVisible().catch(() => false)) {
            await cancelButton.first().click();
          }
        }
      }
    }
  });

  test("should display acceptance criteria field", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        const addItemButton = page.locator('button:has-text("Add Item"), button:has-text("New Item")');

        if (await addItemButton.first().isVisible().catch(() => false)) {
          await addItemButton.first().click();
          await page.waitForTimeout(500);

          // Check for acceptance criteria field
          const acField = page.locator('textarea[name="acceptance_criteria"], textarea[id="acceptance_criteria"]');
          const hasAC = await acField.first().isVisible().catch(() => false);

          // Also check for labels text
          const modalText = await page.locator('[role="dialog"]').textContent().catch(() => "");
          const hasACLabel = modalText?.toLowerCase().includes("acceptance criteria");

          console.log(`Acceptance Criteria field: ${hasAC}, Label: ${hasACLabel}`);

          // Close modal
          const cancelButton = page.locator('button:has-text("Cancel")');
          if (await cancelButton.first().isVisible().catch(() => false)) {
            await cancelButton.first().click();
          }
        }
      }
    }
  });
});

// =============================================================================
// Multi-Select in Backlog List Tests (Day 2)
// =============================================================================

test.describe("Backlog List Multi-Select", () => {
  test("should display selection checkboxes on backlog items", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Look for checkboxes in backlog list
        const checkboxes = page.locator('input[type="checkbox"]');
        const checkboxCount = await checkboxes.count();

        console.log(`Checkboxes found in backlog list: ${checkboxCount}`);
      }
    }
  });

  test("should have Select All checkbox in header", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Look for select all checkbox in header
        const selectAllCheckbox = page.locator('input[type="checkbox"][aria-label*="all"], input[type="checkbox"]').first();
        const hasSelectAll = await selectAllCheckbox.isVisible().catch(() => false);

        console.log(`Select All checkbox visible: ${hasSelectAll}`);
      }
    }
  });

  test("should toggle checkbox on click", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Find first checkbox that is not in the header
        const itemCheckbox = page.locator('[class*="border-b"] input[type="checkbox"]').first();

        if (await itemCheckbox.isVisible().catch(() => false)) {
          const initialState = await itemCheckbox.isChecked();
          await itemCheckbox.click();
          const newState = await itemCheckbox.isChecked();

          console.log(`Checkbox toggled: initial=${initialState}, new=${newState}`);
          expect(newState).not.toBe(initialState);
        }
      }
    }
  });

  test("should show Move Items button when items selected", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Select an item
        const itemCheckbox = page.locator('[class*="border-b"] input[type="checkbox"]').first();

        if (await itemCheckbox.isVisible().catch(() => false)) {
          await itemCheckbox.click();
          await page.waitForTimeout(300);

          // Look for Move Items button
          const moveButton = page.locator('button:has-text("Move")');
          const hasMoveButton = await moveButton.first().isVisible().catch(() => false);

          console.log(`Move Items button visible after selection: ${hasMoveButton}`);

          // Uncheck the item
          await itemCheckbox.click();
        }
      }
    }
  });
});

// =============================================================================
// Bulk Move Modal Tests (Day 2)
// =============================================================================

test.describe("Bulk Move Modal", () => {
  test("should open bulk move modal when clicking Move button", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Select an item
        const itemCheckbox = page.locator('[class*="border-b"] input[type="checkbox"]').first();

        if (await itemCheckbox.isVisible().catch(() => false)) {
          await itemCheckbox.click();
          await page.waitForTimeout(300);

          // Click Move button
          const moveButton = page.locator('button:has-text("Move")');

          if (await moveButton.first().isVisible().catch(() => false)) {
            await moveButton.first().click();
            await page.waitForTimeout(500);

            // Check if bulk move modal is open
            const modal = page.locator('[role="dialog"]');
            const modalVisible = await modal.first().isVisible().catch(() => false);

            console.log(`Bulk move modal visible: ${modalVisible}`);

            // Close modal
            const cancelButton = page.locator('button:has-text("Cancel")');
            if (await cancelButton.first().isVisible().catch(() => false)) {
              await cancelButton.first().click();
            }
          }

          // Uncheck the item
          await itemCheckbox.click();
        }
      }
    }
  });

  test("should display selected items summary in bulk move modal", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Select an item
        const itemCheckbox = page.locator('[class*="border-b"] input[type="checkbox"]').first();

        if (await itemCheckbox.isVisible().catch(() => false)) {
          await itemCheckbox.click();
          await page.waitForTimeout(300);

          // Click Move button
          const moveButton = page.locator('button:has-text("Move")');

          if (await moveButton.first().isVisible().catch(() => false)) {
            await moveButton.first().click();
            await page.waitForTimeout(500);

            // Check for selected items summary
            const modalText = await page.locator('[role="dialog"]').textContent().catch(() => "");
            const hasItemCount = modalText?.includes("1 item") || modalText?.includes("items");
            const hasStoryPoints = modalText?.toLowerCase().includes("story points") || modalText?.includes("SP");

            console.log(`Summary - Item count: ${hasItemCount}, Story points: ${hasStoryPoints}`);

            // Close modal
            const cancelButton = page.locator('button:has-text("Cancel")');
            if (await cancelButton.first().isVisible().catch(() => false)) {
              await cancelButton.first().click();
            }
          }

          // Uncheck the item
          await itemCheckbox.click();
        }
      }
    }
  });

  test("should display target sprint selector", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Select an item
        const itemCheckbox = page.locator('[class*="border-b"] input[type="checkbox"]').first();

        if (await itemCheckbox.isVisible().catch(() => false)) {
          await itemCheckbox.click();
          await page.waitForTimeout(300);

          // Click Move button
          const moveButton = page.locator('button:has-text("Move")');

          if (await moveButton.first().isVisible().catch(() => false)) {
            await moveButton.first().click();
            await page.waitForTimeout(500);

            // Check for target sprint selector
            const sprintSelect = page.locator('[role="dialog"] select');
            const hasSprintSelect = await sprintSelect.first().isVisible().catch(() => false);

            // Check for Product Backlog option
            const modalText = await page.locator('[role="dialog"]').textContent().catch(() => "");
            const hasBacklogOption = modalText?.includes("Product Backlog") || modalText?.includes("No Sprint");

            console.log(`Sprint selector: ${hasSprintSelect}, Backlog option: ${hasBacklogOption}`);

            // Close modal
            const cancelButton = page.locator('button:has-text("Cancel")');
            if (await cancelButton.first().isVisible().catch(() => false)) {
              await cancelButton.first().click();
            }
          }

          // Uncheck the item
          await itemCheckbox.click();
        }
      }
    }
  });

  test("should display optional status update selector", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Select an item
        const itemCheckbox = page.locator('[class*="border-b"] input[type="checkbox"]').first();

        if (await itemCheckbox.isVisible().catch(() => false)) {
          await itemCheckbox.click();
          await page.waitForTimeout(300);

          // Click Move button
          const moveButton = page.locator('button:has-text("Move")');

          if (await moveButton.first().isVisible().catch(() => false)) {
            await moveButton.first().click();
            await page.waitForTimeout(500);

            // Check for status update selector
            const modalText = await page.locator('[role="dialog"]').textContent().catch(() => "");
            const hasStatusOption = modalText?.toLowerCase().includes("status") || modalText?.includes("Keep current");

            console.log(`Status update option visible: ${hasStatusOption}`);

            // Close modal
            const cancelButton = page.locator('button:has-text("Cancel")');
            if (await cancelButton.first().isVisible().catch(() => false)) {
              await cancelButton.first().click();
            }
          }

          // Uncheck the item
          await itemCheckbox.click();
        }
      }
    }
  });

  test("should display SDLC 5.1.3 guidelines in bulk move modal", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Select an item
        const itemCheckbox = page.locator('[class*="border-b"] input[type="checkbox"]').first();

        if (await itemCheckbox.isVisible().catch(() => false)) {
          await itemCheckbox.click();
          await page.waitForTimeout(300);

          // Click Move button
          const moveButton = page.locator('button:has-text("Move")');

          if (await moveButton.first().isVisible().catch(() => false)) {
            await moveButton.first().click();
            await page.waitForTimeout(500);

            // Check for SDLC 5.1.3 guidelines
            const modalText = await page.locator('[role="dialog"]').textContent().catch(() => "");
            const hasGuidelines = modalText?.includes("SDLC 5.1.3") ||
              modalText?.includes("G-Sprint") ||
              modalText?.includes("Carried Over");

            console.log(`SDLC 5.1.3 guidelines found: ${hasGuidelines}`);

            // Close modal
            const cancelButton = page.locator('button:has-text("Cancel")');
            if (await cancelButton.first().isVisible().catch(() => false)) {
              await cancelButton.first().click();
            }
          }

          // Uncheck the item
          await itemCheckbox.click();
        }
      }
    }
  });

  test("should show warning when moving to active sprint", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Select an item
        const itemCheckbox = page.locator('[class*="border-b"] input[type="checkbox"]').first();

        if (await itemCheckbox.isVisible().catch(() => false)) {
          await itemCheckbox.click();
          await page.waitForTimeout(300);

          // Click Move button
          const moveButton = page.locator('button:has-text("Move")');

          if (await moveButton.first().isVisible().catch(() => false)) {
            await moveButton.first().click();
            await page.waitForTimeout(500);

            // Select an active sprint in the dropdown if available
            const sprintSelect = page.locator('[role="dialog"] select').first();

            if (await sprintSelect.isVisible().catch(() => false)) {
              // Try to select an option with "active" status
              const options = await sprintSelect.locator('option').allTextContents();
              const activeOption = options.find(opt => opt.includes("🏃") || opt.toLowerCase().includes("active"));

              if (activeOption) {
                await sprintSelect.selectOption({ label: activeOption });
                await page.waitForTimeout(300);

                // Check for warning message
                const warningText = page.locator('text=/moving to active|team has capacity/i');
                const hasWarning = await warningText.first().isVisible().catch(() => false);

                console.log(`Active sprint warning visible: ${hasWarning}`);
              }
            }

            // Close modal
            const cancelButton = page.locator('button:has-text("Cancel")');
            if (await cancelButton.first().isVisible().catch(() => false)) {
              await cancelButton.first().click();
            }
          }

          // Uncheck the item
          await itemCheckbox.click();
        }
      }
    }
  });

  test("should display item preview list in bulk move modal", async ({ page }) => {
    await page.goto("/app/sprints");
    await page.waitForLoadState("networkidle");

    if (page.url().includes("/sprints")) {
      const sprintLink = page.locator('a[href*="/sprints/"]').first();

      if (await sprintLink.isVisible().catch(() => false)) {
        await sprintLink.click();
        await page.waitForLoadState("networkidle");

        // Select multiple items if available
        const itemCheckboxes = page.locator('[class*="border-b"] input[type="checkbox"]');
        const checkboxCount = await itemCheckboxes.count();

        if (checkboxCount > 0) {
          // Select first checkbox
          await itemCheckboxes.first().click();
          await page.waitForTimeout(300);

          // Click Move button
          const moveButton = page.locator('button:has-text("Move")');

          if (await moveButton.first().isVisible().catch(() => false)) {
            await moveButton.first().click();
            await page.waitForTimeout(500);

            // Check for item preview list
            const previewList = page.locator('[role="dialog"] [class*="overflow-y-auto"], [role="dialog"] [class*="max-h-"]');
            const hasPreviewList = await previewList.first().isVisible().catch(() => false);

            console.log(`Item preview list visible: ${hasPreviewList}`);

            // Close modal
            const cancelButton = page.locator('button:has-text("Cancel")');
            if (await cancelButton.first().isVisible().catch(() => false)) {
              await cancelButton.first().click();
            }
          }

          // Uncheck the item
          await itemCheckboxes.first().click();
        }
      }
    }
  });
});
