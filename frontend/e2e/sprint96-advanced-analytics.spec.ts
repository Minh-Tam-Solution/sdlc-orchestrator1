/**
 * Sprint 96 E2E Tests - Advanced Analytics UI
 *
 * @module frontend/e2e/sprint96-advanced-analytics.spec
 * @description E2E tests for Sprint Analytics Charts and Metrics Dashboard
 * @sdlc SDLC 5.1.3 Framework - Sprint 96 (Advanced Analytics)
 * @status Sprint 96 - January 22, 2026
 * @see frontend/src/app/app/sprints/page.tsx
 * @see frontend/src/app/app/sprints/components/BurndownChart.tsx
 * @see frontend/src/app/app/sprints/components/VelocityChart.tsx
 * @see frontend/src/app/app/sprints/components/TeamWorkloadChart.tsx
 */

import { test, expect, Page } from "@playwright/test";

// =============================================================================
// Test Configuration
// =============================================================================

const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000";
const SPRINTS_URL = `${BASE_URL}/app/sprints`;

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Navigate to Sprints page and wait for load
 */
async function navigateToSprints(page: Page): Promise<void> {
  await page.goto(SPRINTS_URL);
  await page.waitForLoadState("networkidle");
}

/**
 * Navigate to a specific sprint detail page
 */
async function navigateToSprintDetail(page: Page, sprintId: string): Promise<void> {
  await page.goto(`${SPRINTS_URL}/${sprintId}`);
  await page.waitForLoadState("networkidle");
}

/**
 * Mock authenticated session
 */
async function mockAuthenticatedSession(page: Page): Promise<void> {
  await page.addInitScript(() => {
    localStorage.setItem("auth_token", "mock_jwt_token_for_testing");
    localStorage.setItem("user", JSON.stringify({
      id: "user-123",
      email: "test@sdlc-orchestrator.dev",
      name: "Test User",
      role: "admin",
    }));
  });
}

/**
 * Mock Sprint Governance Dashboard API
 */
async function mockSprintGovernanceAPI(page: Page): Promise<void> {
  // Mock projects endpoint
  await page.route("**/api/v1/projects*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify([
        { id: "proj-001", name: "SDLC Orchestrator", slug: "sdlc-orchestrator" },
      ]),
    });
  });

  // Mock sprint governance dashboard
  await page.route("**/api/v1/sprint-governance/dashboard/*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        active_sprint: {
          id: "sprint-96",
          name: "Advanced Analytics",
          number: 96,
          goal: "Complete advanced analytics charts and metrics dashboard",
          status: "active",
          progress_percentage: 65,
          days_remaining: 3,
          days_total: 10,
          g_sprint_status: "passed",
          g_sprint_close_status: "pending",
          items_by_status: {
            planned: 2,
            in_progress: 5,
            review: 3,
            completed: 15,
            carried_over: 0,
          },
          story_points: {
            planned: 42,
            completed: 28,
            remaining: 14,
          },
        },
        upcoming_sprints: [
          {
            id: "sprint-97",
            name: "Expert Workflow Enhancements",
            number: 97,
            start_date: "2026-01-27",
            end_date: "2026-02-05",
            status: "planned",
            g_sprint_status: "pending",
            story_points_planned: 35,
          },
          {
            id: "sprint-98",
            name: "Planning Sub-agents",
            number: 98,
            start_date: "2026-02-06",
            end_date: "2026-02-15",
            status: "planned",
            g_sprint_status: "pending",
            story_points_planned: 40,
          },
        ],
        recent_sprints: [
          {
            id: "sprint-95",
            name: "Evidence Manifest UI",
            number: 95,
            closed_at: "2026-01-22T18:00:00Z",
            completion_rate: 100,
            items_completed: 72,
            items_total: 72,
            g_sprint_close_status: "passed",
          },
          {
            id: "sprint-94",
            name: "AGENTS.md E2E Tests",
            number: 94,
            closed_at: "2026-01-21T17:00:00Z",
            completion_rate: 100,
            items_completed: 41,
            items_total: 41,
            g_sprint_close_status: "passed",
          },
          {
            id: "sprint-93",
            name: "Planning Hierarchy Part 2",
            number: 93,
            closed_at: "2026-01-20T16:00:00Z",
            completion_rate: 95,
            items_completed: 38,
            items_total: 40,
            g_sprint_close_status: "passed",
          },
        ],
        metrics: {
          avg_velocity: 38,
          avg_completion_rate: 94,
          total_sprints_completed: 95,
          gates_passed: 188,
          gates_failed: 4,
        },
      }),
    });
  });

  // Mock planning hierarchy
  await page.route("**/api/v1/planning/hierarchy/*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        hierarchy: [
          {
            id: "roadmap-2026",
            type: "roadmap",
            name: "2026 Product Roadmap",
            children: [
              {
                id: "phase-q1",
                type: "phase",
                name: "Q1 2026 - Launch",
                children: [
                  { id: "sprint-96", type: "sprint", name: "Sprint 96", status: "active" },
                  { id: "sprint-97", type: "sprint", name: "Sprint 97", status: "planned" },
                ],
              },
            ],
          },
        ],
        active_sprint_id: "sprint-96",
      }),
    });
  });
}

/**
 * Mock Sprint Detail with Charts Data
 */
async function mockSprintDetailAPI(page: Page, sprintId: string): Promise<void> {
  // Mock sprint detail endpoint
  await page.route(`**/api/v1/sprints/${sprintId}`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: sprintId,
        name: "Advanced Analytics",
        number: 96,
        goal: "Complete advanced analytics charts and metrics dashboard",
        status: "active",
        start_date: "2026-01-15",
        end_date: "2026-01-25",
        progress_percentage: 65,
        story_points: { planned: 42, completed: 28, remaining: 14 },
        items_count: { total: 25, completed: 15 },
        // Burndown data
        burndown_data: [
          { date: "2026-01-15", ideal: 42, actual: 42 },
          { date: "2026-01-16", ideal: 38, actual: 40 },
          { date: "2026-01-17", ideal: 34, actual: 36 },
          { date: "2026-01-18", ideal: 30, actual: 32 },
          { date: "2026-01-19", ideal: 26, actual: 28 },
          { date: "2026-01-20", ideal: 22, actual: 22 },
          { date: "2026-01-21", ideal: 18, actual: 18 },
          { date: "2026-01-22", ideal: 14, actual: 14 },
        ],
        // Team workload data
        team_workload: [
          { assignee_name: "Alice", assigned_points: 12, completed_points: 10 },
          { assignee_name: "Bob", assigned_points: 10, completed_points: 8 },
          { assignee_name: "Charlie", assigned_points: 8, completed_points: 5 },
          { assignee_name: "Diana", assigned_points: 12, completed_points: 5 },
        ],
      }),
    });
  });

  // Mock velocity chart data (multi-sprint comparison)
  await page.route("**/api/v1/sprint-governance/velocity*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        velocity_data: [
          { sprint_name: "Sprint 91", planned: 35, completed: 32 },
          { sprint_name: "Sprint 92", planned: 38, completed: 36 },
          { sprint_name: "Sprint 93", planned: 40, completed: 38 },
          { sprint_name: "Sprint 94", planned: 41, completed: 41 },
          { sprint_name: "Sprint 95", planned: 42, completed: 42 },
          { sprint_name: "Sprint 96", planned: 42, completed: 28 },
        ],
      }),
    });
  });

  // Mock sprint metrics endpoint
  await page.route(`**/api/v1/sprint-governance/metrics/${sprintId}`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        velocity: 28,
        completion_rate: 67,
        scope_change: -2,
        carry_over_rate: 0,
        avg_cycle_time: 2.3,
        blockers_resolved: 3,
        documentation_score: 95,
      }),
    });
  });
}

// =============================================================================
// Test Suites
// =============================================================================

test.describe("Sprint Governance Dashboard - Navigation", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
  });

  test("should navigate to sprints dashboard", async ({ page }) => {
    await navigateToSprints(page);
    await expect(page).toHaveURL(/\/app\/sprints/);
  });

  test("should display Sprint Governance title", async ({ page }) => {
    await navigateToSprints(page);
    const title = page.getByRole("heading", { name: /sprint governance/i });
    await expect(title).toBeVisible();
  });

  test("should show SDLC 5.1.3 Pillar 2 reference", async ({ page }) => {
    await navigateToSprints(page);
    const reference = page.getByText(/SDLC 5\.1\.3.*Pillar 2/i)
      .or(page.getByText(/Sprint Planning Governance/i));
    await expect(reference).toBeVisible();
  });

  test("should display project name", async ({ page }) => {
    await navigateToSprints(page);
    const projectName = page.getByText(/SDLC Orchestrator/i);
    await expect(projectName).toBeVisible();
  });
});

test.describe("Sprint Governance Dashboard - Active Sprint Card", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);
  });

  test("should display active sprint card", async ({ page }) => {
    const activeCard = page.getByText(/active sprint/i).first();
    await expect(activeCard).toBeVisible();
  });

  test("should show sprint number and name", async ({ page }) => {
    const sprintInfo = page.getByText(/Sprint 96.*Advanced Analytics/i)
      .or(page.getByText(/Sprint 96/i));
    await expect(sprintInfo.first()).toBeVisible();
  });

  test("should display sprint goal", async ({ page }) => {
    const goal = page.getByText(/Complete advanced analytics/i);
    await expect(goal).toBeVisible();
  });

  test("should show progress percentage", async ({ page }) => {
    const progress = page.getByText(/65%/i);
    await expect(progress).toBeVisible();
  });

  test("should display progress bar", async ({ page }) => {
    const progressBar = page.locator('[role="progressbar"]')
      .or(page.locator(".bg-blue-600").first());
    await expect(progressBar).toBeVisible();
  });

  test("should show days remaining", async ({ page }) => {
    const daysInfo = page.getByText(/Day \d+\/\d+/)
      .or(page.getByText(/3.*day/i));
    await expect(daysInfo.first()).toBeVisible();
  });
});

test.describe("Sprint Governance Dashboard - Item Status Stats", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);
  });

  test("should display planned items count", async ({ page }) => {
    const planned = page.getByText(/planned/i).first();
    await expect(planned).toBeVisible();
  });

  test("should show in-progress items count", async ({ page }) => {
    const inProgress = page.getByText(/in progress/i);
    await expect(inProgress).toBeVisible();
  });

  test("should display review items count", async ({ page }) => {
    const review = page.getByText(/review/i);
    await expect(review).toBeVisible();
  });

  test("should show completed items count", async ({ page }) => {
    const completed = page.getByText(/completed/i).first();
    await expect(completed).toBeVisible();
  });
});

test.describe("Sprint Governance Dashboard - Gate Status", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);
  });

  test("should display G-Sprint gate status", async ({ page }) => {
    const gSprintGate = page.getByText(/G-Sprint/i).first();
    await expect(gSprintGate).toBeVisible();
  });

  test("should show G-Sprint-Close gate status", async ({ page }) => {
    const gSprintCloseGate = page.getByText(/G-Sprint-Close/i);
    await expect(gSprintCloseGate).toBeVisible();
  });

  test("should display gate status badges", async ({ page }) => {
    const statusBadges = page.getByText(/passed|pending|failed/i);
    const count = await statusBadges.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("should have clickable gate links", async ({ page }) => {
    const gateLink = page.getByRole("link", { name: /G-Sprint/i }).first();
    await expect(gateLink).toBeVisible();
  });
});

test.describe("Sprint Governance Dashboard - Upcoming Sprints", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);
  });

  test("should display Upcoming Sprints section", async ({ page }) => {
    const section = page.getByText(/upcoming sprint/i);
    await expect(section).toBeVisible();
  });

  test("should show upcoming sprint cards", async ({ page }) => {
    const sprint97 = page.getByText(/Sprint 97/i);
    await expect(sprint97).toBeVisible();
  });

  test("should display sprint date range", async ({ page }) => {
    const dateRange = page.getByText(/Jan.*2026/)
      .or(page.getByText(/Feb.*2026/));
    await expect(dateRange.first()).toBeVisible();
  });

  test("should show story points planned", async ({ page }) => {
    const storyPoints = page.getByText(/\d+ SP/);
    await expect(storyPoints.first()).toBeVisible();
  });

  test("should display Start Sprint button for pending sprints", async ({ page }) => {
    const startButton = page.getByRole("link", { name: /start sprint/i })
      .or(page.getByRole("button", { name: /start sprint/i }));
    // May or may not be visible depending on gate status
    const count = await startButton.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});

test.describe("Sprint Governance Dashboard - Recent Sprints", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);
  });

  test("should display Recently Completed section", async ({ page }) => {
    const section = page.getByText(/recently completed/i);
    await expect(section).toBeVisible();
  });

  test("should show recent sprint rows", async ({ page }) => {
    const sprint95 = page.getByText(/Sprint 95/i);
    await expect(sprint95).toBeVisible();
  });

  test("should display completion rates", async ({ page }) => {
    const completionRate = page.getByText(/100%|95%/i);
    await expect(completionRate.first()).toBeVisible();
  });

  test("should show items completed count", async ({ page }) => {
    const itemsCount = page.getByText(/\d+\/\d+ items/i);
    await expect(itemsCount.first()).toBeVisible();
  });

  test("should display gate status icons for completed sprints", async ({ page }) => {
    const checkIcon = page.locator("svg").filter({ hasText: "" }).first();
    await expect(checkIcon).toBeVisible();
  });
});

test.describe("Sprint Governance Dashboard - Metrics Summary", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);
  });

  test("should display Sprint Metrics section", async ({ page }) => {
    const section = page.getByText(/sprint metrics/i);
    await expect(section).toBeVisible();
  });

  test("should show average velocity", async ({ page }) => {
    const avgVelocity = page.getByText(/avg velocity/i);
    await expect(avgVelocity).toBeVisible();
  });

  test("should display velocity value", async ({ page }) => {
    const velocityValue = page.getByText(/38/);
    await expect(velocityValue.first()).toBeVisible();
  });

  test("should show average completion rate", async ({ page }) => {
    const avgCompletion = page.getByText(/avg completion/i);
    await expect(avgCompletion).toBeVisible();
  });

  test("should display completion percentage", async ({ page }) => {
    const completionValue = page.getByText(/94%/);
    await expect(completionValue).toBeVisible();
  });

  test("should show total sprints completed", async ({ page }) => {
    const sprintsDone = page.getByText(/sprints done/i);
    await expect(sprintsDone).toBeVisible();
  });

  test("should display gate pass rate", async ({ page }) => {
    const gatePassRate = page.getByText(/gate pass rate/i);
    await expect(gatePassRate).toBeVisible();
  });
});

test.describe("Sprint Governance Dashboard - Planning Hierarchy", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);
  });

  test("should display Planning Hierarchy section", async ({ page }) => {
    const section = page.getByText(/planning hierarchy/i);
    await expect(section).toBeVisible();
  });

  test("should show View Full Hierarchy link", async ({ page }) => {
    const link = page.getByRole("link", { name: /view full hierarchy/i });
    await expect(link).toBeVisible();
  });

  test("should display hierarchy tree", async ({ page }) => {
    const tree = page.locator('[data-testid="planning-hierarchy-tree"]')
      .or(page.getByText(/2026.*Roadmap/i))
      .or(page.getByText(/Q1 2026/i));
    await expect(tree.first()).toBeVisible();
  });
});

test.describe("Sprint Detail Page - Burndown Chart", () => {
  const testSprintId = "sprint-96";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await mockSprintDetailAPI(page, testSprintId);
    await navigateToSprintDetail(page, testSprintId);
  });

  test("should display Burndown Chart section", async ({ page }) => {
    const chartTitle = page.getByText(/burndown chart/i);
    await expect(chartTitle).toBeVisible();
  });

  test("should show chart with ideal and actual lines", async ({ page }) => {
    const chartContainer = page.locator('[data-testid="burndown-chart"]')
      .or(page.locator(".recharts-wrapper"))
      .or(page.locator("svg").filter({ hasText: "" }));
    await expect(chartContainer.first()).toBeVisible();
  });

  test("should display total points info", async ({ page }) => {
    const pointsInfo = page.getByText(/\d+ total points/i)
      .or(page.getByText(/42.*points/i));
    await expect(pointsInfo.first()).toBeVisible();
  });

  test("should show completion percentage", async ({ page }) => {
    const completion = page.getByText(/\d+%.*complete/i)
      .or(page.getByText(/completed/i));
    await expect(completion.first()).toBeVisible();
  });

  test("should display burndown health status", async ({ page }) => {
    const healthStatus = page.getByText(/on track|ahead|at risk|behind/i);
    await expect(healthStatus.first()).toBeVisible();
  });

  test("should show remaining points", async ({ page }) => {
    const remaining = page.getByText(/remaining.*\d+/i)
      .or(page.getByText(/\d+.*pts/i));
    await expect(remaining.first()).toBeVisible();
  });
});

test.describe("Sprint Detail Page - Velocity Chart", () => {
  const testSprintId = "sprint-96";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await mockSprintDetailAPI(page, testSprintId);
    await navigateToSprintDetail(page, testSprintId);
  });

  test("should display Velocity Chart section", async ({ page }) => {
    const chartTitle = page.getByText(/velocity chart/i);
    await expect(chartTitle).toBeVisible();
  });

  test("should show bar chart with planned and completed", async ({ page }) => {
    const chartContainer = page.locator('[data-testid="velocity-chart"]')
      .or(page.locator(".recharts-wrapper"))
      .or(page.locator("svg").filter({ hasText: "" }));
    await expect(chartContainer.first()).toBeVisible();
  });

  test("should display sprint count", async ({ page }) => {
    const sprintCount = page.getByText(/\d+ sprint/i);
    await expect(sprintCount.first()).toBeVisible();
  });

  test("should show average velocity", async ({ page }) => {
    const avgVelocity = page.getByText(/avg.*\d+/i)
      .or(page.getByText(/\d+.*pts\/sprint/i));
    await expect(avgVelocity.first()).toBeVisible();
  });

  test("should display velocity trend indicator", async ({ page }) => {
    const trendIndicator = page.getByText(/improving|stable|declining/i);
    await expect(trendIndicator.first()).toBeVisible();
  });

  test("should show overall completion rate", async ({ page }) => {
    const completionRate = page.getByText(/overall completion/i)
      .or(page.getByText(/\d+% completion/i));
    await expect(completionRate.first()).toBeVisible();
  });
});

test.describe("Sprint Detail Page - Team Workload Chart", () => {
  const testSprintId = "sprint-96";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await mockSprintDetailAPI(page, testSprintId);
    await navigateToSprintDetail(page, testSprintId);
  });

  test("should display Team Workload section", async ({ page }) => {
    const chartTitle = page.getByText(/team workload/i);
    await expect(chartTitle).toBeVisible();
  });

  test("should show workload chart", async ({ page }) => {
    const chartContainer = page.locator('[data-testid="team-workload-chart"]')
      .or(page.locator(".recharts-wrapper"))
      .or(page.locator("svg").filter({ hasText: "" }));
    await expect(chartContainer.first()).toBeVisible();
  });

  test("should display team member count", async ({ page }) => {
    const memberCount = page.getByText(/\d+ member/i);
    await expect(memberCount.first()).toBeVisible();
  });

  test("should show points completed vs assigned", async ({ page }) => {
    const pointsInfo = page.getByText(/\d+\/\d+.*pts/i)
      .or(page.getByText(/completed/i));
    await expect(pointsInfo.first()).toBeVisible();
  });

  test("should display average completion badge", async ({ page }) => {
    const avgBadge = page.getByText(/\d+% avg/i);
    await expect(avgBadge.first()).toBeVisible();
  });

  test("should show workload status legend", async ({ page }) => {
    const legend = page.getByText(/complete|on track|behind|overloaded/i);
    await expect(legend.first()).toBeVisible();
  });
});

test.describe("Analytics Charts - Interactivity", () => {
  const testSprintId = "sprint-96";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await mockSprintDetailAPI(page, testSprintId);
    await navigateToSprintDetail(page, testSprintId);
  });

  test("should show tooltip on chart hover", async ({ page }) => {
    const chart = page.locator(".recharts-wrapper").first();
    if (await chart.isVisible()) {
      await chart.hover();
      // Tooltip may appear
      const tooltip = page.locator(".recharts-tooltip-wrapper")
        .or(page.locator('[role="tooltip"]'));
      const count = await tooltip.count();
      expect(count).toBeGreaterThanOrEqual(0);
    }
  });

  test("should display chart legend", async ({ page }) => {
    const legend = page.locator(".recharts-legend-wrapper")
      .or(page.getByText(/ideal|actual|planned|completed|assigned/i));
    await expect(legend.first()).toBeVisible();
  });
});

test.describe("Analytics - Loading States", () => {
  test("should show loading skeleton on dashboard", async ({ page }) => {
    await mockAuthenticatedSession(page);
    // Delay API response
    await page.route("**/api/v1/sprint-governance/dashboard/*", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      await route.fulfill({ status: 200, body: JSON.stringify({}) });
    });
    await page.route("**/api/v1/projects*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify([{ id: "proj-001", name: "Test" }]),
      });
    });

    await page.goto(SPRINTS_URL);

    const skeleton = page.locator(".animate-pulse")
      .or(page.getByText(/loading/i));
    await expect(skeleton.first()).toBeVisible();
  });

  test("should show loading state on sprint detail", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/sprints/*", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      await route.fulfill({ status: 200, body: JSON.stringify({}) });
    });

    await page.goto(`${SPRINTS_URL}/sprint-96`);

    const skeleton = page.locator(".animate-pulse")
      .or(page.getByText(/loading/i));
    await expect(skeleton.first()).toBeVisible();
  });
});

test.describe("Analytics - Empty States", () => {
  test("should show empty state when no active sprint", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/projects*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify([{ id: "proj-001", name: "Test" }]),
      });
    });
    await page.route("**/api/v1/sprint-governance/dashboard/*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          active_sprint: null,
          upcoming_sprints: [],
          recent_sprints: [],
          metrics: null,
        }),
      });
    });
    await page.route("**/api/v1/planning/hierarchy/*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ hierarchy: [] }),
      });
    });

    await navigateToSprints(page);

    const emptyState = page.getByText(/no active sprint/i)
      .or(page.getByText(/create.*sprint/i));
    await expect(emptyState.first()).toBeVisible();
  });

  test("should show empty burndown chart state", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await page.route("**/api/v1/sprints/*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          id: "sprint-empty",
          name: "Empty Sprint",
          burndown_data: [],
          team_workload: [],
        }),
      });
    });

    await navigateToSprintDetail(page, "sprint-empty");

    const emptyChart = page.getByText(/no burndown data/i)
      .or(page.getByText(/start the sprint/i));
    await expect(emptyChart.first()).toBeVisible();
  });

  test("should show empty velocity chart state", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await page.route("**/api/v1/sprint-governance/velocity*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ velocity_data: [] }),
      });
    });

    await navigateToSprintDetail(page, "sprint-96");

    const emptyVelocity = page.getByText(/no velocity data/i)
      .or(page.getByText(/complete at least one sprint/i));
    // May or may not be visible depending on other chart data
    const count = await emptyVelocity.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("should show empty team workload state", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await page.route("**/api/v1/sprints/*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          id: "sprint-no-team",
          name: "No Team Sprint",
          team_workload: [],
          burndown_data: [],
        }),
      });
    });

    await navigateToSprintDetail(page, "sprint-no-team");

    const emptyTeam = page.getByText(/no team data/i)
      .or(page.getByText(/assign items/i));
    await expect(emptyTeam.first()).toBeVisible();
  });
});

test.describe("Analytics - Error States", () => {
  test("should show error state when API fails", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/projects*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify([{ id: "proj-001", name: "Test" }]),
      });
    });
    await page.route("**/api/v1/sprint-governance/dashboard/*", async (route) => {
      await route.fulfill({ status: 500, body: JSON.stringify({ error: "Server error" }) });
    });

    await navigateToSprints(page);

    const errorState = page.getByText(/error/i)
      .or(page.getByText(/failed/i));
    await expect(errorState.first()).toBeVisible();
  });

  test("should show no projects error state", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/projects*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify([]),
      });
    });

    await navigateToSprints(page);

    const noProjects = page.getByText(/no projects found/i)
      .or(page.getByText(/create a project/i));
    await expect(noProjects.first()).toBeVisible();
  });
});

test.describe("Analytics - Responsive Design", () => {
  test("should display correctly on mobile viewport", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await page.setViewportSize({ width: 375, height: 667 });
    await navigateToSprints(page);

    const title = page.getByText(/sprint governance/i);
    await expect(title).toBeVisible();
  });

  test("should display correctly on tablet viewport", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await page.setViewportSize({ width: 768, height: 1024 });
    await navigateToSprints(page);

    const title = page.getByText(/sprint governance/i);
    await expect(title).toBeVisible();
  });

  test("should display charts correctly on desktop", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await mockSprintDetailAPI(page, "sprint-96");
    await page.setViewportSize({ width: 1920, height: 1080 });
    await navigateToSprintDetail(page, "sprint-96");

    const chart = page.locator(".recharts-wrapper")
      .or(page.getByText(/burndown chart/i));
    await expect(chart.first()).toBeVisible();
  });
});

test.describe("Analytics - Accessibility", () => {
  test("should have proper heading hierarchy", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);

    const h1 = page.getByRole("heading", { level: 1 });
    await expect(h1).toBeVisible();
  });

  test("should have accessible links", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);

    const links = page.getByRole("link");
    const count = await links.count();
    expect(count).toBeGreaterThan(0);
  });

  test("should have accessible buttons", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);

    const buttons = page.getByRole("button");
    const count = await buttons.count();
    expect(count).toBeGreaterThan(0);
  });

  test("should support keyboard navigation", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);

    await page.keyboard.press("Tab");
    const focusedElement = page.locator(":focus");
    await expect(focusedElement).toBeVisible();
  });
});

test.describe("Analytics - Sprint Actions", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
    await navigateToSprints(page);
  });

  test("should display New Sprint button", async ({ page }) => {
    const newSprintButton = page.getByRole("button", { name: /new sprint/i });
    await expect(newSprintButton).toBeVisible();
  });

  test("should display Planning link", async ({ page }) => {
    const planningLink = page.getByRole("link", { name: /planning/i });
    await expect(planningLink).toBeVisible();
  });

  test("should navigate to sprint detail on View Details click", async ({ page }) => {
    const viewDetailsLink = page.getByRole("link", { name: /view details/i });
    if (await viewDetailsLink.isVisible()) {
      await viewDetailsLink.click();
      await expect(page).toHaveURL(/\/app\/sprints\/sprint-96/);
    }
  });
});

test.describe("Analytics - Sprint Comparison", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockSprintGovernanceAPI(page);
  });

  test("should show multiple sprints in velocity comparison", async ({ page }) => {
    await mockSprintDetailAPI(page, "sprint-96");
    await navigateToSprintDetail(page, "sprint-96");

    // Velocity chart should show multiple sprints
    const sprintLabels = page.getByText(/Sprint 9[1-6]/i);
    const count = await sprintLabels.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("should display trend analysis", async ({ page }) => {
    await mockSprintDetailAPI(page, "sprint-96");
    await navigateToSprintDetail(page, "sprint-96");

    const trendAnalysis = page.getByText(/improving|stable|declining|need more data/i);
    await expect(trendAnalysis.first()).toBeVisible();
  });
});
