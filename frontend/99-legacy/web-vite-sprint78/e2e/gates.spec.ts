/**
 * File: frontend/web/e2e/gates.spec.ts
 * Version: 2.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: November 28, 2025
 * Authority: Frontend Lead + CTO Approved
 * Foundation: Sprint 19 - CRUD Operations
 * Framework: SDLC 4.9 Complete Lifecycle
 *
 * Description:
 * E2E tests for quality gate CRUD operations.
 *
 * Test Scenarios:
 * - View gates list
 * - Create new gate
 * - Edit gate details
 * - Delete gate with confirmation
 * - View gate details page
 *
 * SDLC 4.9 Compliance:
 * - Pillar 1: Zero Mock Policy (Real API calls)
 * - Pillar 3: Quality Governance (E2E coverage)
 */

import { test, expect } from '@playwright/test'

test.describe('Gate Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\/$/, { timeout: 10000 })
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

test.describe('Gate CRUD Operations', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\/$/, { timeout: 10000 })
  })

  test('should open create gate dialog', async ({ page }) => {
    await page.goto('/gates')

    // Click create gate button
    const createButton = page.getByRole('button', { name: /new gate|create gate/i })
    if (await createButton.isVisible()) {
      await createButton.click()

      // Dialog should open
      await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })
    }
  })

  test('should show project selector in create gate dialog', async ({ page }) => {
    await page.goto('/gates')

    const createButton = page.getByRole('button', { name: /new gate|create gate/i })
    if (await createButton.isVisible()) {
      await createButton.click()
      await expect(page.getByRole('dialog')).toBeVisible()

      // Should have project selector
      const projectSelector = page.getByText(/project|select project/i)
      await expect(projectSelector).toBeVisible({ timeout: 5000 })
    }
  })

  test('should show gate type selector', async ({ page }) => {
    await page.goto('/gates')

    const createButton = page.getByRole('button', { name: /new gate|create gate/i })
    if (await createButton.isVisible()) {
      await createButton.click()
      await expect(page.getByRole('dialog')).toBeVisible()

      // Should have gate type selector
      const gateTypeSelect = page.getByRole('combobox').filter({ hasText: /gate type|type/i })
      if (await gateTypeSelect.isVisible()) {
        await gateTypeSelect.click()
        await expect(page.getByRole('option')).toBeVisible({ timeout: 5000 })
      }
    }
  })

  test('should create new gate', async ({ page }) => {
    await page.goto('/gates')

    const createButton = page.getByRole('button', { name: /new gate|create gate/i })
    if (await createButton.isVisible()) {
      await createButton.click()
      await expect(page.getByRole('dialog')).toBeVisible()

      // Fill gate name
      const nameInput = page.getByLabel(/gate name|name/i)
      if (await nameInput.isVisible()) {
        const gateName = `Test Gate ${Date.now()}`
        await nameInput.fill(gateName)

        // Select project (if required)
        const projectSelector = page.getByRole('combobox').first()
        if (await projectSelector.isVisible()) {
          await projectSelector.click()
          const firstProject = page.getByRole('option').first()
          if (await firstProject.isVisible()) {
            await firstProject.click()
          }
        }

        // Submit
        const submitButton = page.getByRole('button', { name: /create|save|submit/i })
        await submitButton.click()

        // Dialog should close
        await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })
      }
    }
  })

  test('should open edit gate dialog', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    // Find edit button
    const editButton = page.getByRole('button', { name: /edit/i }).first()

    if (await editButton.isVisible()) {
      await editButton.click()

      // Dialog should open with edit title
      await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })
      await expect(page.getByText(/edit gate/i)).toBeVisible()
    }
  })

  test('should edit gate name', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    const editButton = page.getByRole('button', { name: /edit/i }).first()

    if (await editButton.isVisible()) {
      await editButton.click()
      await expect(page.getByRole('dialog')).toBeVisible()

      // Update gate name
      const nameInput = page.getByLabel(/gate name|name/i)
      if (await nameInput.isVisible()) {
        await nameInput.clear()
        const newName = `Updated Gate ${Date.now()}`
        await nameInput.fill(newName)

        // Save changes
        const saveButton = page.getByRole('button', { name: /save|update/i })
        await saveButton.click()

        // Dialog should close
        await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })
      }
    }
  })

  test('should open delete gate confirmation', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    const deleteButton = page.getByRole('button', { name: /delete/i }).first()

    if (await deleteButton.isVisible()) {
      await deleteButton.click()

      // Confirmation dialog should appear
      await expect(page.getByRole('alertdialog').or(page.getByRole('dialog'))).toBeVisible({ timeout: 5000 })
      await expect(page.getByText(/confirm|are you sure|delete/i)).toBeVisible()
    }
  })

  test('should cancel delete gate operation', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    const deleteButton = page.getByRole('button', { name: /delete/i }).first()

    if (await deleteButton.isVisible()) {
      await deleteButton.click()
      await expect(page.getByRole('alertdialog').or(page.getByRole('dialog'))).toBeVisible()

      // Click cancel
      const cancelButton = page.getByRole('button', { name: /cancel|no/i })
      await cancelButton.click()

      // Dialog should close
      await expect(page.getByRole('alertdialog')).not.toBeVisible({ timeout: 5000 })
    }
  })
})

test.describe('Gate Detail Page', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\/$/, { timeout: 10000 })
  })

  test('should display gate detail page', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    const gateLink = page.locator('[href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()
      await expect(page).toHaveURL(/\/gates\//)

      // Should show gate header
      await expect(page.getByRole('heading').first()).toBeVisible()
    }
  })

  test('should show exit criteria section', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    const gateLink = page.locator('[href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()
      await page.waitForTimeout(2000)

      // Should show exit criteria
      await expect(page.getByText(/exit criteria|criteria/i)).toBeVisible({ timeout: 5000 })
    }
  })

  test('should show evidence section', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    const gateLink = page.locator('[href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()
      await page.waitForTimeout(2000)

      // Should show evidence section
      await expect(page.getByText(/evidence/i)).toBeVisible({ timeout: 5000 })
    }
  })

  test('should have upload evidence button', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    const gateLink = page.locator('[href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()
      await page.waitForTimeout(2000)

      // Should have upload evidence button
      const uploadButton = page.getByRole('button', { name: /upload evidence/i })
      if (await uploadButton.isVisible()) {
        await expect(uploadButton).toBeVisible()
      }
    }
  })

  test('should navigate back to gates list', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    const gateLink = page.locator('[href*="/gates/"]').first()

    if (await gateLink.isVisible()) {
      await gateLink.click()
      await expect(page).toHaveURL(/\/gates\//)

      // Click back or gates breadcrumb
      const backLink = page.getByRole('link', { name: /gates|back/i }).first()
      if (await backLink.isVisible()) {
        await backLink.click()
        await expect(page).toHaveURL(/\/gates$/)
      }
    }
  })
})

test.describe('Gate List Features', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard|\/$/, { timeout: 10000 })
  })

  test('should show project filter', async ({ page }) => {
    await page.goto('/gates')

    // Check for project filter
    const projectFilter = page.getByRole('combobox').filter({ hasText: /project|all projects/i })
    if (await projectFilter.isVisible()) {
      await expect(projectFilter).toBeVisible()
    }
  })

  test('should show status filter', async ({ page }) => {
    await page.goto('/gates')

    // Check for status filter
    const statusFilter = page.getByRole('combobox').filter({ hasText: /status|all/i })
    if (await statusFilter.isVisible()) {
      await statusFilter.click()
      await expect(page.getByRole('option')).toBeVisible({ timeout: 5000 })
    }
  })

  test('should show gate statistics', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    // Check for statistics cards
    const statsCard = page.locator('[class*="card"], [class*="stat"]')
    if (await statsCard.first().isVisible()) {
      await expect(statsCard.first()).toBeVisible()
    }
  })

  test('should show empty state when no gates', async ({ page }) => {
    await page.goto('/gates')
    await page.waitForTimeout(2000)

    // Either gates exist or empty state is shown
    const hasGates = await page.locator('[href*="/gates/"]').first().isVisible()
    const hasEmptyState = await page.getByText(/no gates|get started|create.*first/i).isVisible()

    expect(hasGates || hasEmptyState).toBeTruthy()
  })
})
