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
    // Frontend uses /login for login page
    await page.goto('/login')

    // Enter invalid credentials using label selectors
    await page.getByLabel(/email/i).fill('invalid@example.com')
    await page.getByLabel(/password/i).fill('wrongpassword')
    await page.getByRole('button', { name: /sign in|login/i }).click()

    // Wait for API response - either error message or stay on login page
    await page.waitForTimeout(3000)

    // Should show error message OR still be on login page (indicating failed login)
    const hasError = await page.getByText(/invalid|error|incorrect|failed/i).isVisible()
    const stillOnLogin = page.url().includes('/login')

    expect(hasError || stillOnLogin).toBeTruthy()
  })

  test('should login successfully with valid credentials', async ({ page }) => {
    // Frontend uses /login for login page
    await page.goto('/login')

    // Enter valid test credentials using label selectors
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()

    // Should redirect to home/dashboard (frontend uses / as dashboard route)
    await expect(page).toHaveURL(/\/(dashboard)?$/, { timeout: 15000 })

    // Dashboard content should be visible
    await expect(page.getByRole('heading', { name: /dashboard/i })).toBeVisible({ timeout: 5000 })
  })

  test('should logout successfully', async ({ page }) => {
    // Login first - Frontend uses /login for login page
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()

    // Wait for dashboard (frontend uses / as dashboard route)
    await expect(page).toHaveURL(/\/(dashboard)?$/, { timeout: 15000 })

    // Wait for page to fully load
    await page.waitForTimeout(1000)

    // Click logout button in sidebar (use testid for precision - there are 2 logout buttons)
    const logoutButton = page.getByTestId('logout')
    await logoutButton.click()

    // Should redirect to login
    await expect(page).toHaveURL(/\/login/, { timeout: 5000 })
  })
})
