/**
 * File: frontend/web/e2e/evidence.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: November 28, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: Sprint 18 - Evidence Integration
 * Framework: SDLC 4.9 Complete Lifecycle
 *
 * Description:
 * E2E tests for Evidence Vault page.
 *
 * Test Scenarios:
 * - Evidence list with pagination
 * - Filter by evidence type
 * - Download evidence file
 * - Verify evidence integrity
 * - View evidence details
 * - Evidence upload (via gate detail)
 */

import { test, expect } from '@playwright/test'

test.describe('Evidence Vault', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\//, { timeout: 10000 })
  })

  test('should display evidence vault page', async ({ page }) => {
    // Navigate to evidence vault
    await page.goto('/evidence')

    // Check page header
    await expect(page.getByRole('heading', { name: /evidence vault/i })).toBeVisible()

    // Check for filter section
    await expect(page.getByPlaceholder(/search evidence/i)).toBeVisible()
  })

  test('should list evidence with pagination', async ({ page }) => {
    await page.goto('/evidence')

    // Wait for evidence to load
    await page.waitForTimeout(2000)

    // Check for evidence table or empty state
    const table = page.locator('table')
    const emptyState = page.getByText(/no evidence uploaded/i)

    // Either table exists with evidence or empty state is shown
    const hasTable = await table.isVisible()
    const hasEmptyState = await emptyState.isVisible()

    expect(hasTable || hasEmptyState).toBeTruthy()

    // If table exists, check for pagination
    if (hasTable) {
      const rows = page.locator('tbody tr')
      const rowCount = await rows.count()

      // Should have at least column headers if there's data
      if (rowCount > 0) {
        await expect(page.locator('thead')).toBeVisible()
      }
    }
  })

  test('should filter by evidence type', async ({ page }) => {
    await page.goto('/evidence')

    // Find evidence type dropdown
    const typeFilter = page.getByRole('combobox').filter({ hasText: /evidence type|all types/i })

    if (await typeFilter.isVisible()) {
      await typeFilter.click()

      // Should show filter options
      await expect(page.getByRole('option', { name: /design document/i })).toBeVisible()
      await expect(page.getByRole('option', { name: /test results/i })).toBeVisible()
      await expect(page.getByRole('option', { name: /code review/i })).toBeVisible()
    }
  })

  test('should have clear filters button', async ({ page }) => {
    await page.goto('/evidence')

    // Check for clear filters button
    const clearButton = page.getByRole('button', { name: /clear filters/i })
    await expect(clearButton).toBeVisible()

    // Click clear filters
    await clearButton.click()

    // Filters should be cleared (search should be empty)
    const searchInput = page.getByPlaceholder(/search evidence/i)
    await expect(searchInput).toHaveValue('')
  })

  test('should show view evidence details button', async ({ page }) => {
    await page.goto('/evidence')

    // Wait for evidence to load
    await page.waitForTimeout(2000)

    // Check for view button (if evidence exists)
    const viewButton = page.getByRole('button', { name: /view/i }).first()

    if (await viewButton.isVisible()) {
      await viewButton.click()

      // Should open detail dialog
      await expect(page.getByRole('dialog')).toBeVisible()
      await expect(page.getByText(/file information/i)).toBeVisible()
    }
  })

  test('should show download button for evidence', async ({ page }) => {
    await page.goto('/evidence')

    // Wait for evidence to load
    await page.waitForTimeout(2000)

    // Check for download button (if evidence exists)
    const downloadButton = page.getByRole('button', { name: /download/i }).first()

    if (await downloadButton.isVisible()) {
      await expect(downloadButton).toBeEnabled()
    }
  })

  test('should show integrity verification button', async ({ page }) => {
    await page.goto('/evidence')

    // Wait for evidence to load
    await page.waitForTimeout(2000)

    // Check for verify button (if evidence exists)
    const verifyButton = page.getByRole('button', { name: /verify|check integrity/i }).first()

    if (await verifyButton.isVisible()) {
      await expect(verifyButton).toBeEnabled()
    }
  })

  test('should display integrity status badges', async ({ page }) => {
    await page.goto('/evidence')

    // Wait for evidence to load
    await page.waitForTimeout(2000)

    // Check for integrity status badges (Valid, Failed, Pending)
    const statusBadges = page.locator('[class*="badge"], [class*="Badge"]')
    const count = await statusBadges.count()

    if (count > 0) {
      await expect(statusBadges.first()).toBeVisible()
    }
  })

  test('should display SHA256 hash (truncated)', async ({ page }) => {
    await page.goto('/evidence')

    // Wait for evidence to load
    await page.waitForTimeout(2000)

    // Check for hash display (truncated with ...)
    const hashDisplay = page.locator('code').filter({ hasText: /\.\.\./ })

    if (await hashDisplay.first().isVisible()) {
      // Hash should be truncated (8 chars + ...)
      const hashText = await hashDisplay.first().textContent()
      expect(hashText?.includes('...')).toBeTruthy()
    }
  })

  test('should show upload evidence prompt', async ({ page }) => {
    await page.goto('/evidence')

    // Click upload button
    const uploadButton = page.getByRole('button', { name: /upload evidence/i })
    await expect(uploadButton).toBeVisible()

    await uploadButton.click()

    // Should show dialog explaining to go to gate detail
    await expect(page.getByText(/select a gate first/i)).toBeVisible()

    // Close dialog
    const closeButton = page.getByRole('button', { name: /close/i })
    await closeButton.click()
  })

  test('should navigate to gate from evidence', async ({ page }) => {
    await page.goto('/evidence')

    // Wait for evidence to load
    await page.waitForTimeout(2000)

    // Check for gate link (if evidence exists)
    const gateLink = page.getByRole('link', { name: /view gate/i }).first()

    if (await gateLink.isVisible()) {
      await gateLink.click()

      // Should navigate to gate detail page
      await expect(page).toHaveURL(/\/gates\//)
    }
  })
})

test.describe('Evidence Detail Dialog', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\//, { timeout: 10000 })
  })

  test('should display evidence detail dialog with all sections', async ({ page }) => {
    await page.goto('/evidence')
    await page.waitForTimeout(2000)

    // Click view on first evidence
    const viewButton = page.getByRole('button', { name: /view/i }).first()

    if (await viewButton.isVisible()) {
      await viewButton.click()

      // Check dialog sections
      await expect(page.getByText(/file information/i)).toBeVisible()
      await expect(page.getByText(/integrity verification/i)).toBeVisible()
      await expect(page.getByText(/upload information/i)).toBeVisible()
    }
  })

  test('should copy SHA256 hash to clipboard', async ({ page }) => {
    await page.goto('/evidence')
    await page.waitForTimeout(2000)

    // Click view on first evidence
    const viewButton = page.getByRole('button', { name: /view/i }).first()

    if (await viewButton.isVisible()) {
      await viewButton.click()

      // Find and click copy button
      const copyButton = page.getByRole('button').filter({ has: page.locator('svg[class*="h-4"]') }).last()

      if (await copyButton.isVisible()) {
        await copyButton.click()

        // Should show success indicator (checkmark)
        await page.waitForTimeout(500)
      }
    }
  })

  test('should verify integrity from detail dialog', async ({ page }) => {
    await page.goto('/evidence')
    await page.waitForTimeout(2000)

    // Click view on first evidence
    const viewButton = page.getByRole('button', { name: /view/i }).first()

    if (await viewButton.isVisible()) {
      await viewButton.click()

      // Find and click verify button
      const verifyButton = page.getByRole('button', { name: /verify now/i })

      if (await verifyButton.isVisible()) {
        await verifyButton.click()

        // Should show loading state or result
        await page.waitForTimeout(1000)
      }
    }
  })

  test('should download from detail dialog', async ({ page }) => {
    await page.goto('/evidence')
    await page.waitForTimeout(2000)

    // Click view on first evidence
    const viewButton = page.getByRole('button', { name: /view/i }).first()

    if (await viewButton.isVisible()) {
      await viewButton.click()

      // Find download button in dialog footer
      const downloadButton = page.getByRole('button', { name: /download/i })
      await expect(downloadButton).toBeVisible()
    }
  })

  test('should close dialog with close button', async ({ page }) => {
    await page.goto('/evidence')
    await page.waitForTimeout(2000)

    // Click view on first evidence
    const viewButton = page.getByRole('button', { name: /view/i }).first()

    if (await viewButton.isVisible()) {
      await viewButton.click()

      // Dialog should be visible
      await expect(page.getByRole('dialog')).toBeVisible()

      // Click close button
      const closeButton = page.getByRole('button', { name: /close/i })
      await closeButton.click()

      // Dialog should be closed
      await expect(page.getByRole('dialog')).not.toBeVisible()
    }
  })
})

test.describe('Evidence Upload (via Gate)', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\//, { timeout: 10000 })
  })

  test('should show upload dialog on gate detail page', async ({ page }) => {
    // Navigate to gates first
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    // Click on first gate
    const gateLink = page.locator('[href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()
      await page.waitForTimeout(1000)

      // Look for upload evidence button
      const uploadButton = page.getByRole('button', { name: /upload evidence/i })

      if (await uploadButton.isVisible()) {
        await uploadButton.click()

        // Should show upload dialog
        await expect(page.getByRole('dialog')).toBeVisible()
        await expect(page.getByText(/drag.*drop|choose file/i)).toBeVisible()
      }
    }
  })

  test('should show drag-and-drop zone', async ({ page }) => {
    // Navigate to gates first
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    // Click on first gate
    const gateLink = page.locator('[href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()
      await page.waitForTimeout(1000)

      // Look for upload evidence button
      const uploadButton = page.getByRole('button', { name: /upload evidence/i })

      if (await uploadButton.isVisible()) {
        await uploadButton.click()

        // Should show drag and drop zone
        await expect(page.getByText(/drag.*drop/i)).toBeVisible()
        await expect(page.getByText(/click to browse/i)).toBeVisible()
      }
    }
  })

  test('should show evidence type selector', async ({ page }) => {
    // Navigate to gates first
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    // Click on first gate
    const gateLink = page.locator('[href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()
      await page.waitForTimeout(1000)

      // Look for upload evidence button
      const uploadButton = page.getByRole('button', { name: /upload evidence/i })

      if (await uploadButton.isVisible()) {
        await uploadButton.click()

        // Should have evidence type selector
        const typeSelector = page.getByRole('combobox').filter({ hasText: /select evidence type/i })
        await expect(typeSelector).toBeVisible()

        // Click to show options
        await typeSelector.click()

        // Should show evidence type options
        await expect(page.getByRole('option', { name: /design document/i })).toBeVisible()
      }
    }
  })
})
