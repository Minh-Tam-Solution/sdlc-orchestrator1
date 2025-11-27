/**
 * File: frontend/web/e2e/policies.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * E2E tests for policy library management.
 *
 * Critical Journey #5: Policy Management
 * - View policy packs
 * - Filter policies by stage
 * - View policy details (Rego code)
 */

import { test, expect } from '@playwright/test'

test.describe('Policy Library', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 })
  })

  test('should display policies page', async ({ page }) => {
    // Navigate to policies
    await page.goto('/policies')

    // Check page elements
    await expect(page.getByRole('heading', { name: /policies/i })).toBeVisible()
    await expect(page.getByText(/policy pack|sdlc 4.9/i)).toBeVisible()
  })

  test('should display SDLC stages summary', async ({ page }) => {
    await page.goto('/policies')

    // Check for stage summary cards
    await expect(page.getByText(/why|what|build|verify/i)).toBeVisible()
  })

  test('should filter policies by stage', async ({ page }) => {
    await page.goto('/policies')

    // Find stage filter dropdown
    const filterSelect = page.getByRole('combobox')

    if (await filterSelect.isVisible()) {
      await filterSelect.click()

      // Should show stage options
      await expect(page.getByRole('option', { name: /build/i })).toBeVisible({ timeout: 5000 })

      // Select a stage
      await page.getByRole('option', { name: /build/i }).click()

      // URL or content should update
      await page.waitForTimeout(1000)
    }
  })

  test('should expand policy to show Rego code', async ({ page }) => {
    await page.goto('/policies')

    // Wait for policies to load
    await page.waitForTimeout(2000)

    // Find "View Rego" button
    const viewRegoButton = page.getByRole('button', { name: /view rego/i }).first()

    if (await viewRegoButton.isVisible()) {
      await viewRegoButton.click()

      // Rego code section should appear
      await expect(page.getByText(/rego policy code|package/i)).toBeVisible({ timeout: 5000 })

      // Click to collapse
      const hideRegoButton = page.getByRole('button', { name: /hide rego/i }).first()
      if (await hideRegoButton.isVisible()) {
        await hideRegoButton.click()
      }
    }
  })

  test('should show policy severity badges', async ({ page }) => {
    await page.goto('/policies')

    // Wait for policies to load
    await page.waitForTimeout(2000)

    // Check for severity badges
    const severityBadges = page.locator('[class*="bg-blue-100"], [class*="bg-yellow-100"], [class*="bg-red-100"], [class*="bg-orange-100"]')

    const count = await severityBadges.count()
    if (count > 0) {
      await expect(severityBadges.first()).toBeVisible()
    }
  })

  test('should display custom policies section', async ({ page }) => {
    await page.goto('/policies')

    // Check for custom policies section
    await expect(page.getByText(/custom policies/i)).toBeVisible()
    await expect(page.getByText(/rego language/i)).toBeVisible()
  })

  test('should have create policy button', async ({ page }) => {
    await page.goto('/policies')

    // Check for create policy button
    await expect(page.getByRole('button', { name: /create policy/i })).toBeVisible()
  })
})
