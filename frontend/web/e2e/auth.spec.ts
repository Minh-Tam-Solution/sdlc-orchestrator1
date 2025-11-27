/**
 * File: frontend/web/e2e/auth.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * E2E tests for authentication flows.
 *
 * Critical Journey #1: User Authentication
 * - Login with valid credentials
 * - Login error handling
 * - Logout flow
 * - Protected route access
 */

import { test, expect } from '@playwright/test'

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
  })

  test('should redirect to login when not authenticated', async ({ page }) => {
    // Attempt to access dashboard
    await page.goto('/dashboard')

    // Should redirect to auth page (login or /auth with redirect)
    await expect(page).toHaveURL(/\/(login|auth)/)
  })

  test('should display login form', async ({ page }) => {
    // Frontend uses /auth for login page
    await page.goto('/auth')

    // Check form elements exist using input type selectors for specificity
    await expect(page.locator('input[type="email"], input#email, input[name="email"]')).toBeVisible()
    await expect(page.locator('input[type="password"], input#password, input[name="password"]')).toBeVisible()
    await expect(page.getByRole('button', { name: /sign in|login/i })).toBeVisible()
  })

  test('should show error with invalid credentials', async ({ page }) => {
    // Frontend uses /auth for login page
    await page.goto('/auth')

    // Enter invalid credentials using specific input selectors
    const emailInput = page.locator('input[type="email"], input#email, input[name="email"]')
    const passwordInput = page.locator('input[type="password"], input#password, input[name="password"]')
    await emailInput.fill('invalid@example.com')
    await passwordInput.fill('wrongpassword')
    await page.getByRole('button', { name: /sign in|login/i }).click()

    // Should show error message
    await expect(page.getByText(/invalid|error|incorrect/i)).toBeVisible({ timeout: 10000 })
  })

  test('should login successfully with valid credentials', async ({ page }) => {
    // Frontend uses /auth for login page
    await page.goto('/auth')

    // Enter valid test credentials using specific input selectors
    const emailInput = page.locator('input[type="email"], input#email, input[name="email"]')
    const passwordInput = page.locator('input[type="password"], input#password, input[name="password"]')
    await emailInput.fill('admin@sdlc-orchestrator.io')
    await passwordInput.fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()

    // Should redirect to dashboard
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 15000 })

    // Dashboard should be visible
    await expect(page.getByText(/dashboard/i).first()).toBeVisible({ timeout: 5000 })
  })

  test('should logout successfully', async ({ page }) => {
    // Login first - Frontend uses /auth for login page
    await page.goto('/auth')
    const emailInput = page.locator('input[type="email"], input#email, input[name="email"]')
    const passwordInput = page.locator('input[type="password"], input#password, input[name="password"]')
    await emailInput.fill('admin@sdlc-orchestrator.io')
    await passwordInput.fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()

    // Wait for dashboard
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 15000 })

    // Find and click logout (may be in dropdown menu)
    const logoutButton = page.getByRole('button', { name: /logout|sign out/i })
    if (await logoutButton.isVisible()) {
      await logoutButton.click()
    } else {
      // Try opening user menu first
      const userMenu = page.getByRole('button', { name: /user|profile|menu/i })
      if (await userMenu.isVisible()) {
        await userMenu.click()
        await page.getByRole('menuitem', { name: /logout|sign out/i }).click()
      }
    }

    // Should redirect to login/auth
    await expect(page).toHaveURL(/\/(login|auth)/, { timeout: 5000 })
  })
})
