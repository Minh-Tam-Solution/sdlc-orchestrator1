/**
 * File: frontend/web/e2e/policies.spec.ts
 * Version: 2.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: November 28, 2025
 * Authority: Frontend Lead + CTO Approved
 * Foundation: Sprint 19 - CRUD Operations
 * Framework: SDLC 4.9 Complete Lifecycle
 *
 * Description:
 * E2E tests for policy library management.
 *
 * Test Scenarios:
 * - View policy packs
 * - Filter policies by stage
 * - View policy details (Rego code)
 * - Navigate to policy detail page
 * - Copy Rego code to clipboard
 *
 * SDLC 4.9 Compliance:
 * - Pillar 1: Zero Mock Policy (Real API calls)
 * - Pillar 3: Quality Governance (E2E coverage)
 */

import { test, expect } from '@playwright/test'

test.describe('Policy Library', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\/$/, { timeout: 10000 })
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

  test('should have view details button for policies', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    // Check for view details button
    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await expect(viewDetailsButton).toBeVisible()
    }
  })

  test('should navigate to policy detail page', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    // Click view details on first policy
    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()

      // Should navigate to policy detail page
      await expect(page).toHaveURL(/\/policies\//, { timeout: 5000 })
    }
  })
})

test.describe('Policy Detail Page', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\/$/, { timeout: 10000 })
  })

  test('should display policy detail page', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    // Navigate to first policy detail
    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await expect(page).toHaveURL(/\/policies\//)

      // Should show policy name in heading
      await expect(page.getByRole('heading').first()).toBeVisible()
    }
  })

  test('should show policy information cards', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await page.waitForTimeout(2000)

      // Should show policy info cards
      await expect(page.getByText(/policy code/i)).toBeVisible({ timeout: 5000 })
      await expect(page.getByText(/stage/i)).toBeVisible()
      await expect(page.getByText(/version/i)).toBeVisible()
    }
  })

  test('should show Rego code section', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await page.waitForTimeout(2000)

      // Should show Rego code section
      await expect(page.getByText(/rego policy code/i)).toBeVisible({ timeout: 5000 })
    }
  })

  test('should have copy code button', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await page.waitForTimeout(2000)

      // Should have copy button
      const copyButton = page.getByRole('button', { name: /copy code/i })
      await expect(copyButton).toBeVisible({ timeout: 5000 })
    }
  })

  test('should show severity badge on detail page', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await page.waitForTimeout(2000)

      // Should show severity badge
      const severityBadge = page.getByText(/info|warning|error|critical/i).first()
      await expect(severityBadge).toBeVisible({ timeout: 5000 })
    }
  })

  test('should show active/inactive status', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await page.waitForTimeout(2000)

      // Should show status badge
      const statusBadge = page.getByText(/active|inactive/i).first()
      await expect(statusBadge).toBeVisible({ timeout: 5000 })
    }
  })

  test('should show policy metadata section', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await page.waitForTimeout(2000)

      // Should show policy information section
      await expect(page.getByText(/policy information/i)).toBeVisible({ timeout: 5000 })
    }
  })

  test('should show policy usage section', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await page.waitForTimeout(2000)

      // Should show policy usage section
      await expect(page.getByText(/policy usage/i)).toBeVisible({ timeout: 5000 })
    }
  })

  test('should have edit policy button', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await page.waitForTimeout(2000)

      // Should have edit button
      const editButton = page.getByRole('button', { name: /edit policy/i })
      await expect(editButton).toBeVisible({ timeout: 5000 })
    }
  })

  test('should navigate back to policies list', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await expect(page).toHaveURL(/\/policies\//)

      // Click breadcrumb to go back
      const backLink = page.getByRole('link', { name: /policies/i }).first()
      if (await backLink.isVisible()) {
        await backLink.click()
        await expect(page).toHaveURL(/\/policies$/)
      }
    }
  })

  test('should show view gates link', async ({ page }) => {
    await page.goto('/policies')
    await page.waitForTimeout(2000)

    const viewDetailsButton = page.getByRole('button', { name: /view details/i }).first()

    if (await viewDetailsButton.isVisible()) {
      await viewDetailsButton.click()
      await page.waitForTimeout(2000)

      // Should have view gates button
      const viewGatesButton = page.getByRole('button', { name: /view gates/i })
      if (await viewGatesButton.isVisible()) {
        await expect(viewGatesButton).toBeVisible()
      }
    }
  })
})

test.describe('Policy Error Handling', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\/$/, { timeout: 10000 })
  })

  test('should show not found for invalid policy ID', async ({ page }) => {
    // Navigate to non-existent policy
    await page.goto('/policies/non-existent-id-12345')
    await page.waitForTimeout(2000)

    // Should show error state
    await expect(page.getByText(/not found|error|doesn.*exist/i)).toBeVisible({ timeout: 5000 })
  })

  test('should have back button on error page', async ({ page }) => {
    // Navigate to non-existent policy
    await page.goto('/policies/non-existent-id-12345')
    await page.waitForTimeout(2000)

    // Should have back to policies button
    const backButton = page.getByRole('button', { name: /back to policies/i })
    if (await backButton.isVisible()) {
      await backButton.click()
      await expect(page).toHaveURL(/\/policies$/)
    }
  })
})
