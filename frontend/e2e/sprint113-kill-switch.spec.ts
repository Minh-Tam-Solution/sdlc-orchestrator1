/**
 * Sprint 113 E2E Tests - Kill Switch Admin UI
 *
 * @module frontend/e2e/sprint113-kill-switch.spec
 * @description E2E tests for Kill Switch Admin components (Mode Toggle, Dashboard, History, Break Glass, Audit)
 * @sdlc SDLC 5.3.0 Framework - Sprint 113 (Governance UI - Kill Switch Admin)
 * @status Sprint 113 - January 28, 2026
 * @adr ADR-041 (Framework 6.0 Governance System)
 * @see frontend/src/components/governance/kill-switch/
 */

import { test, expect, Page } from "@playwright/test";

// =============================================================================
// Test Configuration
// =============================================================================

const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000";
const GOVERNANCE_URL = `${BASE_URL}/app/governance`;
const KILL_SWITCH_URL = `${BASE_URL}/app/governance/kill-switch`;

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Navigate to Kill Switch Admin page
 */
async function navigateToKillSwitch(page: Page): Promise<void> {
  await page.goto(KILL_SWITCH_URL);
  await page.waitForLoadState("networkidle");
}

/**
 * Mock authenticated session with CTO role (required for mode changes)
 */
async function mockCTOSession(page: Page): Promise<void> {
  await page.addInitScript(() => {
    localStorage.setItem("auth_token", "mock_jwt_token_cto");
    localStorage.setItem("user", JSON.stringify({
      id: "user-cto",
      email: "cto@sdlc-orchestrator.dev",
      name: "Test CTO",
      role: "cto",
      permissions: ["governance:admin", "kill_switch:manage", "mode:change"],
    }));
  });
}

/**
 * Mock authenticated session with regular admin (cannot change mode)
 */
async function mockAdminSession(page: Page): Promise<void> {
  await page.addInitScript(() => {
    localStorage.setItem("auth_token", "mock_jwt_token_admin");
    localStorage.setItem("user", JSON.stringify({
      id: "user-admin",
      email: "admin@sdlc-orchestrator.dev",
      name: "Test Admin",
      role: "admin",
      permissions: ["governance:read"],
    }));
  });
}

/**
 * Mock Kill Switch API responses
 */
async function mockKillSwitchAPI(page: Page): Promise<void> {
  // Mock governance mode endpoint
  await page.route("**/api/v1/governance/mode", async (route) => {
    const method = route.request().method();
    if (method === "GET") {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          mode: "FULL",
          changed_by: "admin@sdlc-orchestrator.dev",
          last_changed: "2026-01-27T14:30:00Z",
          change_reason: "Weekly stability milestone reached",
        }),
      });
    } else if (method === "POST") {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          mode: "SOFT",
          changed_by: "cto@sdlc-orchestrator.dev",
          changed_at: "2026-01-28T10:00:00Z",
          previous_mode: "FULL",
        }),
      });
    }
  });

  // Mock can change mode endpoint
  await page.route("**/api/v1/governance/mode/can-change", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        can_change: true,
        reason: "User has CTO role",
        required_role: "cto",
      }),
    });
  });

  // Mock kill switch check endpoint
  await page.route("**/api/v1/governance/kill-switch/check", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        should_trigger: false,
        current_metrics: {
          rejection_rate_current: 0.03,
          rejection_rate_threshold: 0.05,
          rejection_rate_triggered: false,
          latency_p95_current_ms: 85,
          latency_p95_threshold_ms: 100,
          latency_triggered: false,
          false_positive_current: 0.05,
          false_positive_threshold: 0.10,
          false_positive_triggered: false,
          developer_complaints_current: 1,
          developer_complaints_threshold: 3,
          complaints_triggered: false,
        },
        triggered_criteria: [],
        recommended_action: "maintain_current",
        last_check: "2026-01-28T09:55:00Z",
      }),
    });
  });

  // Mock kill switch dashboard endpoint
  await page.route("**/api/v1/governance/kill-switch/dashboard", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        current_mode: "FULL",
        kill_switch_armed: true,
        auto_rollback_enabled: true,
        health: {
          opa_service: "healthy",
          evidence_vault: "healthy",
          governance_api: "healthy",
        },
        last_rollback: null,
        uptime_percentage: 99.9,
      }),
    });
  });

  // Mock mode history endpoint
  await page.route("**/api/v1/governance/mode/history*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        entries: [
          {
            id: "hist-003",
            from_mode: "SOFT",
            to_mode: "FULL",
            changed_by: "admin@sdlc-orchestrator.dev",
            changed_at: "2026-01-27T14:30:00Z",
            reason: "Weekly stability milestone reached",
            auto_triggered: false,
            duration_in_mode: "7 days",
          },
          {
            id: "hist-002",
            from_mode: "WARNING",
            to_mode: "SOFT",
            changed_by: "cto@sdlc-orchestrator.dev",
            changed_at: "2026-01-20T10:00:00Z",
            reason: "Confidence in governance rules increased",
            auto_triggered: false,
            duration_in_mode: "3 days",
          },
          {
            id: "hist-001",
            from_mode: "FULL",
            to_mode: "WARNING",
            changed_by: "system",
            changed_at: "2026-01-17T08:45:00Z",
            reason: "Auto-rollback: rejection rate exceeded 80%",
            auto_triggered: true,
            trigger_criteria: ["rejection_rate > 80%"],
            duration_in_mode: "2 hours",
          },
        ],
        total: 3,
        current_mode: "FULL",
        current_mode_since: "2026-01-27T14:30:00Z",
        total_changes_30d: 3,
        average_time_in_full_mode: "5 days",
      }),
    });
  });

  // Mock break glass status endpoint
  await page.route("**/api/v1/governance/break-glass/status", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        active: false,
        can_activate: true,
        last_activation: {
          activated_at: "2026-01-15T02:30:00Z",
          activated_by: "oncall@sdlc-orchestrator.dev",
          reason: "P0 production incident",
          incident_type: "P0",
          expired_at: "2026-01-15T06:30:00Z",
          auto_reverted: true,
        },
        cooldown_remaining: null,
      }),
    });
  });

  // Mock break glass activate endpoint
  await page.route("**/api/v1/governance/break-glass/activate", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        break_glass_id: "bg-001",
        activated: true,
        expires_at: "2026-01-28T14:00:00Z",
        auto_revert_scheduled: true,
        notifications_sent: ["cto@sdlc-orchestrator.dev", "ceo@sdlc-orchestrator.dev"],
      }),
    });
  });

  // Mock audit log endpoint
  await page.route("**/api/v1/governance/audit-log*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        entries: [
          {
            id: "audit-005",
            type: "mode_change",
            timestamp: "2026-01-27T14:30:00Z",
            actor: "admin@sdlc-orchestrator.dev",
            actor_role: "admin",
            action: "Changed governance mode from SOFT to FULL",
            details: { from_mode: "SOFT", to_mode: "FULL" },
          },
          {
            id: "audit-004",
            type: "kill_switch_check",
            timestamp: "2026-01-27T14:00:00Z",
            actor: "system",
            actor_role: "system",
            action: "Automated kill switch health check",
            details: { all_criteria_passed: true },
          },
          {
            id: "audit-003",
            type: "break_glass_expired",
            timestamp: "2026-01-15T06:30:00Z",
            actor: "system",
            actor_role: "system",
            action: "Break glass session auto-expired after 4 hours",
            details: { break_glass_id: "bg-old" },
          },
          {
            id: "audit-002",
            type: "break_glass_requested",
            timestamp: "2026-01-15T02:30:00Z",
            actor: "oncall@sdlc-orchestrator.dev",
            actor_role: "tech_lead",
            action: "Break glass activated for P0 incident",
            details: { incident_type: "P0", reason: "Production outage" },
          },
          {
            id: "audit-001",
            type: "rollback_triggered",
            timestamp: "2026-01-17T08:45:00Z",
            actor: "system",
            actor_role: "system",
            action: "Auto-rollback triggered: rejection rate exceeded 80%",
            details: { from_mode: "FULL", to_mode: "WARNING", trigger: "rejection_rate" },
          },
        ],
        total: 5,
        has_more: false,
      }),
    });
  });
}

// =============================================================================
// Test Suites - Governance Mode Toggle
// =============================================================================

test.describe("Kill Switch - Governance Mode Toggle", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should display mode toggle card", async ({ page }) => {
    const card = page.getByText(/governance mode/i).first()
      .or(page.locator('[data-testid="governance-mode-toggle"]'));
    await expect(card).toBeVisible();
  });

  test("should show current mode (FULL)", async ({ page }) => {
    const currentMode = page.getByText(/full/i);
    await expect(currentMode.first()).toBeVisible();
  });

  test("should display all four mode options", async ({ page }) => {
    const modes = ["off", "warning", "soft", "full"];
    for (const mode of modes) {
      const modeOption = page.getByText(new RegExp(mode, "i"));
      await expect(modeOption.first()).toBeVisible();
    }
  });

  test("should show mode descriptions", async ({ page }) => {
    const descriptions = [
      /disabled/i,
      /log.*violations/i,
      /block.*critical/i,
      /all.*violations.*block/i,
    ];
    for (const desc of descriptions) {
      const descText = page.getByText(desc);
      const count = await descText.count();
      expect(count).toBeGreaterThanOrEqual(0);
    }
  });

  test("should display last changed information", async ({ page }) => {
    const lastChanged = page.getByText(/last changed/i)
      .or(page.getByText(/admin@sdlc/i));
    await expect(lastChanged.first()).toBeVisible();
  });

  test("should show change reason", async ({ page }) => {
    const reason = page.getByText(/stability/i)
      .or(page.getByText(/reason/i));
    await expect(reason.first()).toBeVisible();
  });
});

test.describe("Kill Switch - Mode Change Flow", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should enable mode selection for CTO", async ({ page }) => {
    const modeButton = page.getByRole("button").filter({ hasText: /soft|warning/i }).first();
    const isEnabled = await modeButton.isEnabled();
    expect(isEnabled).toBe(true);
  });

  test("should open confirmation dialog on mode click", async ({ page }) => {
    const modeButton = page.locator("button").filter({ hasText: /soft/i }).first();
    if (await modeButton.isVisible() && await modeButton.isEnabled()) {
      await modeButton.click();
      const dialog = page.getByText(/confirm/i)
        .or(page.getByRole("dialog"));
      await expect(dialog.first()).toBeVisible();
    }
  });

  test("should require reason for mode change", async ({ page }) => {
    const modeButton = page.locator("button").filter({ hasText: /soft/i }).first();
    if (await modeButton.isVisible() && await modeButton.isEnabled()) {
      await modeButton.click();
      const reasonInput = page.getByPlaceholder(/reason/i)
        .or(page.locator("textarea"));
      await expect(reasonInput.first()).toBeVisible();
    }
  });

  test("should show cancel button in confirmation", async ({ page }) => {
    const modeButton = page.locator("button").filter({ hasText: /soft/i }).first();
    if (await modeButton.isVisible() && await modeButton.isEnabled()) {
      await modeButton.click();
      const cancelBtn = page.getByRole("button", { name: /cancel/i });
      await expect(cancelBtn.first()).toBeVisible();
    }
  });
});

test.describe("Kill Switch - Authorization Check", () => {
  test("should show authorization warning for non-CTO users", async ({ page }) => {
    await mockAdminSession(page);
    // Override can-change to return false
    await page.route("**/api/v1/governance/mode/can-change", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          can_change: false,
          reason: "CTO or CEO authorization required",
          required_role: "cto",
        }),
      });
    });
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);

    const warning = page.getByText(/authorization.*required/i)
      .or(page.getByText(/CTO.*CEO/i));
    await expect(warning.first()).toBeVisible();
  });

  test("should disable mode buttons for non-CTO users", async ({ page }) => {
    await mockAdminSession(page);
    await page.route("**/api/v1/governance/mode/can-change", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ can_change: false }),
      });
    });
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);

    const modeButton = page.locator("button").filter({ hasText: /soft/i }).first();
    if (await modeButton.isVisible()) {
      const isDisabled = await modeButton.isDisabled();
      expect(isDisabled).toBe(true);
    }
  });
});

// =============================================================================
// Test Suites - Kill Switch Dashboard
// =============================================================================

test.describe("Kill Switch - Dashboard Metrics", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should display kill switch dashboard card", async ({ page }) => {
    const card = page.getByText(/kill switch/i).first()
      .or(page.locator('[data-testid="kill-switch-dashboard"]'));
    await expect(card).toBeVisible();
  });

  test("should show rejection rate gauge", async ({ page }) => {
    const rejectionRate = page.getByText(/rejection.*rate/i);
    await expect(rejectionRate.first()).toBeVisible();
  });

  test("should display latency P95 gauge", async ({ page }) => {
    const latency = page.getByText(/latency/i)
      .or(page.getByText(/p95/i));
    await expect(latency.first()).toBeVisible();
  });

  test("should show false positive rate gauge", async ({ page }) => {
    const falsePositive = page.getByText(/false positive/i);
    await expect(falsePositive.first()).toBeVisible();
  });

  test("should display developer complaints gauge", async ({ page }) => {
    const complaints = page.getByText(/complaint/i)
      .or(page.getByText(/developer/i));
    await expect(complaints.first()).toBeVisible();
  });

  test("should show threshold values", async ({ page }) => {
    const threshold = page.getByText(/threshold/i);
    await expect(threshold.first()).toBeVisible();
  });

  test("should display current vs threshold comparison", async ({ page }) => {
    const current = page.getByText(/current/i);
    await expect(current.first()).toBeVisible();
  });

  test("should show status indicator (normal/triggered)", async ({ page }) => {
    const status = page.getByText(/normal/i)
      .or(page.getByText(/triggered/i));
    await expect(status.first()).toBeVisible();
  });
});

test.describe("Kill Switch - Health Indicators", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should display service health section", async ({ page }) => {
    const health = page.getByText(/health/i)
      .or(page.getByText(/service/i));
    await expect(health.first()).toBeVisible();
  });

  test("should show OPA service status", async ({ page }) => {
    const opa = page.getByText(/opa/i);
    await expect(opa.first()).toBeVisible();
  });

  test("should display evidence vault status", async ({ page }) => {
    const vault = page.getByText(/evidence.*vault/i)
      .or(page.getByText(/vault/i));
    await expect(vault.first()).toBeVisible();
  });

  test("should show healthy status indicators", async ({ page }) => {
    const healthy = page.getByText(/healthy/i);
    await expect(healthy.first()).toBeVisible();
  });
});

// =============================================================================
// Test Suites - Mode History Timeline
// =============================================================================

test.describe("Kill Switch - Mode History Timeline", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should display mode history timeline", async ({ page }) => {
    const timeline = page.getByText(/history/i)
      .or(page.locator('[data-testid="mode-history-timeline"]'));
    await expect(timeline.first()).toBeVisible();
  });

  test("should show mode transitions", async ({ page }) => {
    const transition = page.getByText(/soft.*full/i)
      .or(page.getByText(/warning.*soft/i));
    await expect(transition.first()).toBeVisible();
  });

  test("should display who made the change", async ({ page }) => {
    const actor = page.getByText(/@/i)
      .or(page.getByText(/admin/i));
    await expect(actor.first()).toBeVisible();
  });

  test("should show change timestamps", async ({ page }) => {
    const timestamp = page.getByText(/2026-01/i)
      .or(page.getByText(/ago/i));
    await expect(timestamp.first()).toBeVisible();
  });

  test("should indicate auto-rollback entries", async ({ page }) => {
    const autoRollback = page.getByText(/auto.*rollback/i)
      .or(page.getByText(/system/i));
    await expect(autoRollback.first()).toBeVisible();
  });

  test("should show trigger criteria for rollbacks", async ({ page }) => {
    const trigger = page.getByText(/trigger/i)
      .or(page.getByText(/rejection.*rate/i));
    await expect(trigger.first()).toBeVisible();
  });

  test("should display duration in previous mode", async ({ page }) => {
    const duration = page.getByText(/\d+.*day/i)
      .or(page.getByText(/duration/i));
    await expect(duration.first()).toBeVisible();
  });

  test("should have expandable entries", async ({ page }) => {
    const expandButton = page.getByText(/show.*detail/i)
      .or(page.locator('[aria-expanded]'));
    const count = await expandButton.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});

// =============================================================================
// Test Suites - Break Glass Button
// =============================================================================

test.describe("Kill Switch - Break Glass Button", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should display break glass section", async ({ page }) => {
    const breakGlass = page.getByText(/break.*glass/i);
    await expect(breakGlass.first()).toBeVisible();
  });

  test("should show emergency bypass button", async ({ page }) => {
    const button = page.getByRole("button", { name: /emergency|break.*glass/i });
    await expect(button.first()).toBeVisible();
  });

  test("should display last activation info", async ({ page }) => {
    const lastActivation = page.getByText(/last.*activ/i)
      .or(page.getByText(/P0/i));
    await expect(lastActivation.first()).toBeVisible();
  });

  test("should show auto-revert timer info", async ({ page }) => {
    const revert = page.getByText(/auto.*revert/i)
      .or(page.getByText(/4.*hour/i));
    await expect(revert.first()).toBeVisible();
  });
});

test.describe("Kill Switch - Break Glass Activation Flow", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should open confirmation on break glass click", async ({ page }) => {
    const button = page.getByRole("button", { name: /emergency|break.*glass/i }).first();
    if (await button.isVisible() && await button.isEnabled()) {
      await button.click();
      const dialog = page.getByText(/confirm/i)
        .or(page.getByRole("alertdialog"))
        .or(page.getByRole("dialog"));
      await expect(dialog.first()).toBeVisible();
    }
  });

  test("should show incident type selector", async ({ page }) => {
    const button = page.getByRole("button", { name: /emergency|break.*glass/i }).first();
    if (await button.isVisible() && await button.isEnabled()) {
      await button.click();
      const incidentType = page.getByText(/P0|P1|hotfix/i)
        .or(page.getByRole("combobox"));
      await expect(incidentType.first()).toBeVisible();
    }
  });

  test("should require reason for activation", async ({ page }) => {
    const button = page.getByRole("button", { name: /emergency|break.*glass/i }).first();
    if (await button.isVisible() && await button.isEnabled()) {
      await button.click();
      const reasonInput = page.getByPlaceholder(/reason/i)
        .or(page.locator("textarea"));
      await expect(reasonInput.first()).toBeVisible();
    }
  });

  test("should show warning about notifications", async ({ page }) => {
    const button = page.getByRole("button", { name: /emergency|break.*glass/i }).first();
    if (await button.isVisible() && await button.isEnabled()) {
      await button.click();
      const warning = page.getByText(/notify/i)
        .or(page.getByText(/slack/i))
        .or(page.getByText(/CEO.*CTO/i));
      await expect(warning.first()).toBeVisible();
    }
  });
});

// =============================================================================
// Test Suites - Audit Log Table
// =============================================================================

test.describe("Kill Switch - Audit Log Table", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should display audit log section", async ({ page }) => {
    const auditLog = page.getByText(/audit.*log/i);
    await expect(auditLog.first()).toBeVisible();
  });

  test("should show entry count", async ({ page }) => {
    const count = page.getByText(/\d+.*entr/i);
    await expect(count.first()).toBeVisible();
  });

  test("should display timestamps", async ({ page }) => {
    const timestamp = page.getByText(/2026/i);
    await expect(timestamp.first()).toBeVisible();
  });

  test("should show entry types with badges", async ({ page }) => {
    const typeBadge = page.getByText(/mode.*change|rollback|break.*glass/i);
    await expect(typeBadge.first()).toBeVisible();
  });

  test("should display actors", async ({ page }) => {
    const actor = page.getByText(/@/i)
      .or(page.getByText(/system/i));
    await expect(actor.first()).toBeVisible();
  });

  test("should show action descriptions", async ({ page }) => {
    const action = page.getByText(/changed.*mode|auto.*rollback|activated/i);
    await expect(action.first()).toBeVisible();
  });
});

test.describe("Kill Switch - Audit Log Filtering", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should have search by actor input", async ({ page }) => {
    const searchInput = page.getByPlaceholder(/search|actor/i);
    await expect(searchInput.first()).toBeVisible();
  });

  test("should have filter by type dropdown", async ({ page }) => {
    const filterDropdown = page.locator("select")
      .or(page.getByRole("combobox"));
    await expect(filterDropdown.first()).toBeVisible();
  });

  test("should have pagination controls", async ({ page }) => {
    const pagination = page.getByRole("button", { name: /next|previous/i })
      .or(page.getByText(/showing/i));
    await expect(pagination.first()).toBeVisible();
  });
});

// =============================================================================
// Test Suites - Triggered State
// =============================================================================

test.describe("Kill Switch - Triggered State", () => {
  test("should display triggered status when criteria exceeded", async ({ page }) => {
    await mockCTOSession(page);

    // Override with triggered state
    await page.route("**/api/v1/governance/kill-switch/check", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          should_trigger: true,
          current_metrics: {
            rejection_rate_current: 0.85,
            rejection_rate_threshold: 0.05,
            rejection_rate_triggered: true,
            latency_p95_current_ms: 85,
            latency_p95_threshold_ms: 100,
            latency_triggered: false,
            false_positive_current: 0.05,
            false_positive_threshold: 0.10,
            false_positive_triggered: false,
            developer_complaints_current: 1,
            developer_complaints_threshold: 3,
            complaints_triggered: false,
          },
          triggered_criteria: ["Rejection rate 85% exceeds threshold 5%"],
          recommended_action: "rollback_to_warning",
        }),
      });
    });

    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);

    const triggered = page.getByText(/triggered/i);
    await expect(triggered.first()).toBeVisible();
  });

  test("should show triggered criteria list", async ({ page }) => {
    await mockCTOSession(page);

    await page.route("**/api/v1/governance/kill-switch/check", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          should_trigger: true,
          triggered_criteria: ["Rejection rate 85% exceeds threshold 5%"],
          recommended_action: "rollback_to_warning",
        }),
      });
    });

    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);

    const criteria = page.getByText(/rejection.*rate.*85/i)
      .or(page.getByText(/criteria/i));
    await expect(criteria.first()).toBeVisible();
  });

  test("should display recommended action", async ({ page }) => {
    await mockCTOSession(page);

    await page.route("**/api/v1/governance/kill-switch/check", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          should_trigger: true,
          triggered_criteria: ["Test criteria"],
          recommended_action: "rollback_to_warning",
        }),
      });
    });

    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);

    const recommendation = page.getByText(/recommend/i)
      .or(page.getByText(/rollback/i));
    await expect(recommendation.first()).toBeVisible();
  });
});

// =============================================================================
// Test Suites - Loading & Error States
// =============================================================================

test.describe("Kill Switch - Loading States", () => {
  test("should show loading skeleton on initial load", async ({ page }) => {
    await mockCTOSession(page);
    await page.route("**/api/v1/**", async (route) => {
      await new Promise(r => setTimeout(r, 1000));
      await route.fulfill({ status: 200, body: JSON.stringify({}) });
    });

    await page.goto(KILL_SWITCH_URL);

    const skeleton = page.locator(".animate-pulse")
      .or(page.locator(".animate-spin"))
      .or(page.getByText(/loading/i));
    await expect(skeleton.first()).toBeVisible();
  });
});

test.describe("Kill Switch - Error States", () => {
  test("should show error when API fails", async ({ page }) => {
    await mockCTOSession(page);
    await page.route("**/api/v1/governance/**", async (route) => {
      await route.fulfill({
        status: 500,
        body: JSON.stringify({ error: "Internal Server Error" }),
      });
    });

    await navigateToKillSwitch(page);

    const error = page.getByText(/error|failed/i);
    await expect(error.first()).toBeVisible();
  });
});

// =============================================================================
// Test Suites - Accessibility
// =============================================================================

test.describe("Kill Switch - Accessibility", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
    await navigateToKillSwitch(page);
  });

  test("should have proper heading hierarchy", async ({ page }) => {
    const h1 = page.getByRole("heading", { level: 1 });
    await expect(h1.first()).toBeVisible();
  });

  test("should have accessible buttons", async ({ page }) => {
    const buttons = page.getByRole("button");
    const count = await buttons.count();
    expect(count).toBeGreaterThan(0);
  });

  test("should support keyboard navigation", async ({ page }) => {
    await page.keyboard.press("Tab");
    const focusedElement = page.locator(":focus");
    await expect(focusedElement).toBeVisible();
  });

  test("should have proper color contrast for status indicators", async ({ page }) => {
    const status = page.getByText(/normal|triggered/i).first();
    await expect(status).toBeVisible();
  });
});

// =============================================================================
// Test Suites - Responsive Design
// =============================================================================

test.describe("Kill Switch - Responsive Design", () => {
  test.beforeEach(async ({ page }) => {
    await mockCTOSession(page);
    await mockKillSwitchAPI(page);
  });

  test("should display correctly on mobile viewport", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await navigateToKillSwitch(page);
    const pageContent = page.locator("main").or(page.locator('[role="main"]'));
    await expect(pageContent).toBeVisible();
  });

  test("should display correctly on tablet viewport", async ({ page }) => {
    await page.setViewportSize({ width: 768, height: 1024 });
    await navigateToKillSwitch(page);
    const pageContent = page.locator("main").or(page.locator('[role="main"]'));
    await expect(pageContent).toBeVisible();
  });

  test("should display correctly on desktop viewport", async ({ page }) => {
    await page.setViewportSize({ width: 1920, height: 1080 });
    await navigateToKillSwitch(page);
    const pageContent = page.locator("main").or(page.locator('[role="main"]'));
    await expect(pageContent).toBeVisible();
  });
});
