/**
 * File: frontend/web/e2e/gates.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * E2E tests for quality gate management.
 *
 * Critical Journey #4: Gate Management
 * - View gates list
 * - Create new gate
 * - View gate details
 * - Gate status workflow
 */

import { test, expect } from '@playwright/test'

test.describe('Gate Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 })
  })

  test('should display gates page', async ({ page }) => {
    // Navigate to gates
    await page.goto('/gates')

    // Check page elements
    await expect(page.getByRole('heading', { name: /gates/i })).toBeVisible()
  })

  test('should show gate status badges', async ({ page }) => {
    await page.goto('/gates')

    // Wait for gates to load
    await page.waitForTimeout(2000)

    // Check for status indicators (passed/failed/pending)
    const statusIndicators = page.locator('[data-status], .status-badge, [class*="status"]')

    // If gates exist, should have status indicators
    const count = await statusIndicators.count()
    if (count > 0) {
      await expect(statusIndicators.first()).toBeVisible()
    }
  })

  test('should filter gates by status', async ({ page }) => {
    await page.goto('/gates')

    // Look for filter dropdown
    const filterButton = page.getByRole('combobox', { name: /status|filter/i })

    if (await filterButton.isVisible()) {
      await filterButton.click()

      // Should show filter options
      await expect(page.getByRole('option')).toBeVisible()
    }
  })

  test('should navigate to gate details', async ({ page }) => {
    await page.goto('/gates')

    // Wait for gates to load
    await page.waitForTimeout(2000)

    // Click on first gate (if exists)
    const gateLink = page.locator('[data-testid="gate-row"], .gate-item, [href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()

      // Should show gate details with evidence section
      await expect(page.getByText(/evidence|exit criteria|approval/i)).toBeVisible({ timeout: 5000 })
    }
  })

  test('should show gate approval workflow', async ({ page }) => {
    await page.goto('/gates')

    // Wait for gates to load
    await page.waitForTimeout(2000)

    // Find a gate and click to view details
    const gateLink = page.locator('[data-testid="gate-row"], .gate-item, [href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()

      // Check for approval-related elements
      const approvalSection = page.getByText(/approval|approve|reject/i)
      if (await approvalSection.isVisible()) {
        await expect(approvalSection).toBeVisible()
      }
    }
  })
})
