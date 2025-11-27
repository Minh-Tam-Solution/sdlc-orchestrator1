/**
 * File: frontend/web/e2e/dashboard.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * E2E tests for dashboard page.
 *
 * Critical Journey #2: Dashboard Overview
 * - View statistics cards
 * - View recent gate activity
 * - Quick actions functionality
 */

import { test, expect } from '@playwright/test'

test.describe('Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 })
  })

  test('should display dashboard statistics', async ({ page }) => {
    // Check stat cards are visible
    await expect(page.getByText(/total projects/i)).toBeVisible()
    await expect(page.getByText(/active gates/i)).toBeVisible()
    await expect(page.getByText(/pending approvals/i)).toBeVisible()
    await expect(page.getByText(/pass rate/i)).toBeVisible()
  })

  test('should display recent gate activity section', async ({ page }) => {
    // Check recent activity section
    await expect(page.getByText(/recent gate activity/i)).toBeVisible()
  })

  test('should display quick actions section', async ({ page }) => {
    // Check quick actions
    await expect(page.getByText(/quick actions/i)).toBeVisible()
    await expect(page.getByText(/create new project/i)).toBeVisible()
    await expect(page.getByText(/upload evidence/i)).toBeVisible()
    await expect(page.getByText(/manage policies/i)).toBeVisible()
  })

  test('should navigate to create project from quick actions', async ({ page }) => {
    // Click create project link
    const createProjectLink = page.getByRole('link', { name: /create new project/i })
    await createProjectLink.click()

    // Should navigate to projects page or open dialog
    await expect(page.url()).toMatch(/\/projects/)
  })

  test('should navigate to policies from quick actions', async ({ page }) => {
    // Click manage policies link
    const policiesLink = page.getByRole('link', { name: /manage policies/i })
    await policiesLink.click()

    // Should navigate to policies page
    await expect(page).toHaveURL(/\/policies/)
    await expect(page.getByRole('heading', { name: /policies/i })).toBeVisible()
  })
})
