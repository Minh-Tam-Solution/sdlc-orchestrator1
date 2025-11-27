/**
 * File: frontend/web/e2e/projects.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * E2E tests for project management.
 *
 * Critical Journey #3: Project Management
 * - View projects list
 * - Create new project
 * - View project details
 */

import { test, expect } from '@playwright/test'

test.describe('Project Management', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 })
  })

  test('should display projects page', async ({ page }) => {
    // Navigate to projects
    await page.goto('/projects')

    // Check page elements
    await expect(page.getByRole('heading', { name: /projects/i })).toBeVisible()
    await expect(page.getByRole('button', { name: /new project|create project/i })).toBeVisible()
  })

  test('should open create project dialog', async ({ page }) => {
    await page.goto('/projects')

    // Click create project button
    await page.getByRole('button', { name: /new project|create project/i }).click()

    // Dialog should open
    await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })
    await expect(page.getByLabel(/project name|name/i)).toBeVisible()
  })

  test('should create new project', async ({ page }) => {
    await page.goto('/projects')

    // Open create dialog
    await page.getByRole('button', { name: /new project|create project/i }).click()
    await expect(page.getByRole('dialog')).toBeVisible()

    // Fill project details
    const projectName = `Test Project ${Date.now()}`
    await page.getByLabel(/project name|name/i).fill(projectName)

    const descriptionField = page.getByLabel(/description/i)
    if (await descriptionField.isVisible()) {
      await descriptionField.fill('E2E test project description')
    }

    // Submit form
    const createButton = page.getByRole('button', { name: /create|save|submit/i })
    await createButton.click()

    // Dialog should close and project should be created
    await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })

    // Project should appear in list (allow for API response time)
    await expect(page.getByText(projectName)).toBeVisible({ timeout: 10000 })
  })

  test('should show project details', async ({ page }) => {
    await page.goto('/projects')

    // Wait for projects to load
    await page.waitForTimeout(2000)

    // Click on first project (if exists)
    const projectLink = page.locator('[data-testid="project-card"], .project-card, [href*="/projects/"]').first()

    if (await projectLink.isVisible()) {
      await projectLink.click()

      // Should show project details
      await expect(page.getByText(/gates|stage|progress/i)).toBeVisible({ timeout: 5000 })
    }
  })
})
