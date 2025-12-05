/**
 * File: frontend/web/e2e/helpers/auth.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Authentication helper functions for E2E tests.
 * Provides reusable login/logout utilities.
 */

import { Page, expect } from '@playwright/test'

export const TEST_USER = {
  email: 'admin@sdlc-orchestrator.io',
  password: 'Admin@123',
}

/**
 * Login to the application with test credentials.
 * Uses flexible selectors to handle different input implementations.
<<<<<<< HEAD
 * Includes retry logic for parallel test stability.
 */
export async function login(page: Page, email = TEST_USER.email, password = TEST_USER.password): Promise<void> {
  const maxRetries = 3
  let lastError: Error | null = null

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      // Navigate to login page
      await page.goto('/login', { waitUntil: 'domcontentloaded' })

      // Wait for page to be ready
      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {
        // Continue even if networkidle times out
      })

      // Check if already logged in (redirected to dashboard)
      if (!page.url().includes('/login')) {
        return // Already logged in
      }

      // Find and fill email input (try multiple selectors)
      const emailInput = page.locator('input[type="email"], input#email, input[name="email"]').first()
      await emailInput.waitFor({ state: 'visible', timeout: 10000 })
      await emailInput.clear()
      await emailInput.fill(email)

      // Find and fill password input
      const passwordInput = page.locator('input[type="password"], input#password, input[name="password"]').first()
      await passwordInput.waitFor({ state: 'visible', timeout: 5000 })
      await passwordInput.clear()
      await passwordInput.fill(password)

      // Click login button
      const loginButton = page.getByRole('button', { name: /sign in|login|submit/i })
      await loginButton.click()

      // Wait for navigation away from login page
      // Use Promise.race to handle both redirect and error scenarios
      await Promise.race([
        page.waitForURL((url) => !url.pathname.includes('/login'), { timeout: 15000 }),
        page.waitForSelector('.error, [role="alert"]', { timeout: 15000 }).then(() => {
          throw new Error('Login error displayed')
        }).catch(() => {
          // No error displayed, continue waiting for redirect
        })
      ])

      // Verify we're not on login page
      if (!page.url().includes('/login')) {
        return // Success
      }

      throw new Error('Still on login page after submit')
    } catch (error) {
      lastError = error as Error
      if (attempt < maxRetries) {
        // Wait before retry with exponential backoff
        await page.waitForTimeout(1000 * attempt)
      }
    }
  }

  throw lastError || new Error('Login failed after max retries')
=======
 */
export async function login(page: Page, email = TEST_USER.email, password = TEST_USER.password): Promise<void> {
  // Navigate to login page
  await page.goto('/login')

  // Wait for page to be ready
  await page.waitForLoadState('networkidle')

  // Find and fill email input (try multiple selectors)
  const emailInput = page.locator('input[type="email"], input#email, input[name="email"]').first()
  await emailInput.waitFor({ state: 'visible', timeout: 10000 })
  await emailInput.fill(email)

  // Find and fill password input
  const passwordInput = page.locator('input[type="password"], input#password, input[name="password"]').first()
  await passwordInput.waitFor({ state: 'visible', timeout: 5000 })
  await passwordInput.fill(password)

  // Click login button
  const loginButton = page.getByRole('button', { name: /sign in|login|submit/i })
  await loginButton.click()

  // Wait for login to complete - button changes to "Signing in..." then redirects
  // Wait for the button to not be disabled (loading finished)
  await page.waitForFunction(
    () => {
      const btn = document.querySelector('button[type="submit"], button:has-text("Sign in"), button:has-text("Login")')
      return !btn || !btn.hasAttribute('disabled')
    },
    { timeout: 20000 }
  ).catch(() => {
    // Ignore if button is gone (redirected)
  })

  // Wait for redirect - dashboard is at / or /dashboard
  // After login, we should NOT be on /login anymore
  await page.waitForTimeout(1000)
  await page.waitForURL((url) => !url.pathname.includes('/login'), { timeout: 20000 })
>>>>>>> e4e08a4422114f82896f50256a793810a38a0c5b
}

/**
 * Logout from the application.
 * Handles different logout implementations (button, menu item).
 */
export async function logout(page: Page): Promise<void> {
  // Try direct logout button first
  const logoutButton = page.getByRole('button', { name: /logout|sign out/i })

  if (await logoutButton.isVisible({ timeout: 2000 }).catch(() => false)) {
    await logoutButton.click()
  } else {
    // Try user menu dropdown
    const userMenuTrigger = page.locator('[data-testid="user-menu"], button:has-text("Account"), .user-menu-trigger').first()

    if (await userMenuTrigger.isVisible({ timeout: 2000 }).catch(() => false)) {
      await userMenuTrigger.click()
      await page.getByRole('menuitem', { name: /logout|sign out/i }).click()
    } else {
      // Last resort - find any logout link
      const logoutLink = page.locator('a[href*="logout"], button:has-text("Log out")').first()
      if (await logoutLink.isVisible({ timeout: 2000 }).catch(() => false)) {
        await logoutLink.click()
      }
    }
  }

  // Wait for redirect to auth page
  await expect(page).toHaveURL(/\/(login|auth)/, { timeout: 5000 })
}

/**
 * Check if user is logged in by verifying dashboard access.
 */
export async function isLoggedIn(page: Page): Promise<boolean> {
  try {
    await page.goto('/dashboard')
    await page.waitForURL(/\/dashboard/, { timeout: 5000 })
    return true
  } catch {
    return false
  }
}
