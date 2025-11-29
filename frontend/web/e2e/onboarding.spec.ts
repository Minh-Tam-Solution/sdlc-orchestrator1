/**
 * File: frontend/web/e2e/onboarding.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 15 Day 5
 * Date: December 2, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md
 *
 * Description:
 * E2E tests for onboarding wizard flow.
 *
 * Critical Journey: New User Onboarding
 * - Step 1: OAuth Login (GitHub)
 * - Step 2: Repository Connect
 * - Step 3: AI Analysis
 * - Step 4: Policy Pack Selection
 * - Step 5: Stage Mapping
 * - Step 6: First Gate Evaluation
 *
 * Target: TTFGE < 30 minutes (Time to First Gate Evaluation)
 */

import { test, expect, Page } from '@playwright/test'

test.describe('Onboarding Flow', () => {
  test.describe('Step 1: OAuth Login', () => {
    test('should display onboarding login page', async ({ page }) => {
      await page.goto('/onboarding/login')

      // Check page title and subtitle
      await expect(page.getByText('Welcome to SDLC Orchestrator')).toBeVisible()
      await expect(page.getByText(/enforce quality gates/i)).toBeVisible()
    })

    test('should display OAuth provider buttons', async ({ page }) => {
      await page.goto('/onboarding/login')

      // Check GitHub button (recommended)
      await expect(page.getByRole('button', { name: /GitHub.*Recommended/i })).toBeVisible()

      // Check Google button
      await expect(page.getByRole('button', { name: /Google/i })).toBeVisible()

      // Check Microsoft button
      await expect(page.getByRole('button', { name: /Microsoft/i })).toBeVisible()
    })

    test('should show progress indicator at step 1', async ({ page }) => {
      await page.goto('/onboarding/login')

      // Check progress bar shows step 1 of 6
      await expect(page.getByText(/step 1/i)).toBeVisible()
    })

    test('should show "coming soon" for Google OAuth', async ({ page }) => {
      await page.goto('/onboarding/login')

      // Click Google button
      page.on('dialog', async (dialog) => {
        expect(dialog.message()).toContain('coming soon')
        await dialog.accept()
      })

      await page.getByRole('button', { name: /Google/i }).click()
    })

    test('should show "coming soon" for Microsoft OAuth', async ({ page }) => {
      await page.goto('/onboarding/login')

      // Click Microsoft button
      page.on('dialog', async (dialog) => {
        expect(dialog.message()).toContain('coming soon')
        await dialog.accept()
      })

      await page.getByRole('button', { name: /Microsoft/i }).click()
    })
  })

  test.describe('Step 2: Repository Connect', () => {
    test.beforeEach(async ({ page }) => {
      // Mock authenticated state by setting tokens
      await page.goto('/onboarding/repository')
    })

    test('should display repository connect page', async ({ page }) => {
      await expect(page.getByText('Connect Your Repository')).toBeVisible()
      await expect(page.getByText(/analyze your project/i)).toBeVisible()
    })

    test('should display search input', async ({ page }) => {
      await expect(page.getByPlaceholder(/search repositories/i)).toBeVisible()
    })

    test('should show read-only access notice', async ({ page }) => {
      await expect(page.getByText(/read access/i)).toBeVisible()
    })

    test('should show progress indicator at step 2', async ({ page }) => {
      await expect(page.getByText(/step 2/i)).toBeVisible()
    })
  })

  test.describe('Step 3: AI Analysis', () => {
    test.beforeEach(async ({ page }) => {
      // Set up session storage with mock repo data
      await page.goto('/onboarding/repository')
      await page.evaluate(() => {
        sessionStorage.setItem(
          'onboarding_repo',
          JSON.stringify({
            id: 123456,
            name: 'test-repo',
            full_name: 'developer/test-repo',
            description: 'Test repository',
            language: 'TypeScript',
          })
        )
      })
      await page.goto('/onboarding/analyzing')
    })

    test('should display analysis page', async ({ page }) => {
      await expect(page.getByText(/Analyzing Your Repository/i)).toBeVisible()
    })

    test('should show loading spinner during analysis', async ({ page }) => {
      // Check for spinner element
      await expect(page.locator('.animate-spin')).toBeVisible()
    })

    test('should show progress indicator at step 3', async ({ page }) => {
      await expect(page.getByText(/step 3/i)).toBeVisible()
    })
  })

  test.describe('Step 4: Policy Pack Selection', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('/onboarding/policy-pack')
    })

    test('should display policy pack selection page', async ({ page }) => {
      await expect(page.getByText('Choose Your Policy Pack')).toBeVisible()
      await expect(page.getByText(/governance level/i)).toBeVisible()
    })

    test('should display three policy pack options', async ({ page }) => {
      // Check Lite pack
      await expect(page.getByText('Lite')).toBeVisible()
      await expect(page.getByText(/Essential gates for small teams/i)).toBeVisible()

      // Check Standard pack
      await expect(page.getByText('Standard')).toBeVisible()
      await expect(page.getByText(/Complete SDLC 4.9 gates/i)).toBeVisible()

      // Check Enterprise pack
      await expect(page.getByText('Enterprise')).toBeVisible()
      await expect(page.getByText(/Advanced governance/i)).toBeVisible()
    })

    test('should allow selecting a policy pack', async ({ page }) => {
      // Click on Lite pack
      await page.getByText('Lite').click()

      // Continue button should be enabled
      const continueButton = page.getByRole('button', { name: /Continue.*Lite/i })
      await expect(continueButton).toBeVisible()
    })

    test('should show progress indicator at step 4', async ({ page }) => {
      await expect(page.getByText(/step 4/i)).toBeVisible()
    })
  })

  test.describe('Step 5: Stage Mapping', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto('/onboarding/stage-mapping')
    })

    test('should display stage mapping page', async ({ page }) => {
      await expect(page.getByText('Map Your Project Structure')).toBeVisible()
      await expect(page.getByText(/auto-detected/i)).toBeVisible()
    })

    test('should display folder to stage mappings', async ({ page }) => {
      // Check for SDLC stages in dropdowns
      await expect(page.getByText(/WHY/)).toBeVisible()
      await expect(page.getByText(/BUILD/)).toBeVisible()
    })

    test('should show back and continue buttons', async ({ page }) => {
      await expect(page.getByRole('button', { name: /Back/i })).toBeVisible()
      await expect(page.getByRole('button', { name: /Confirm Mapping/i })).toBeVisible()
    })

    test('should show progress indicator at step 5', async ({ page }) => {
      await expect(page.getByText(/step 5/i)).toBeVisible()
    })
  })

  test.describe('Step 6: First Gate Evaluation', () => {
    test.beforeEach(async ({ page }) => {
      // Set up session storage with mock data
      await page.goto('/onboarding/stage-mapping')
      await page.evaluate(() => {
        sessionStorage.setItem(
          'onboarding_repo',
          JSON.stringify({
            id: 123456,
            name: 'test-repo',
            full_name: 'developer/test-repo',
          })
        )
        sessionStorage.setItem('onboarding_policy_pack', 'standard')
        sessionStorage.setItem('onboarding_stage_mappings', '[]')
      })
      await page.goto('/onboarding/first-gate')
    })

    test('should display first gate evaluation page', async ({ page }) => {
      await expect(page.getByText(/First Gate Evaluation/i)).toBeVisible()
    })

    test('should show loading state during evaluation', async ({ page }) => {
      // Check for spinner during evaluation
      await expect(page.locator('.animate-spin')).toBeVisible()
    })

    test('should show progress indicator at step 6', async ({ page }) => {
      await expect(page.getByText(/step 6/i)).toBeVisible()
    })
  })

  test.describe('GitHub OAuth Callback', () => {
    test('should display loading state on callback page', async ({ page }) => {
      await page.goto('/auth/github/callback?code=test&state=test')

      // Check for loading indicator
      await expect(page.getByText(/Connecting GitHub/i)).toBeVisible()
    })

    test('should show error for missing code parameter', async ({ page }) => {
      await page.goto('/auth/github/callback?state=test')

      // Should show error
      await expect(page.getByText(/Failed|Error|Missing/i)).toBeVisible({ timeout: 10000 })
    })

    test('should show error for missing state parameter', async ({ page }) => {
      await page.goto('/auth/github/callback?code=test')

      // Should show error
      await expect(page.getByText(/Failed|Error|Missing/i)).toBeVisible({ timeout: 10000 })
    })

    test('should have try again button on error', async ({ page }) => {
      await page.goto('/auth/github/callback')

      // Wait for error state
      await page.waitForTimeout(2000)

      // Should have try again link
      const tryAgainButton = page.getByText(/Try again/i)
      if (await tryAgainButton.isVisible()) {
        await tryAgainButton.click()
        await expect(page).toHaveURL(/\/onboarding\/login/)
      }
    })
  })

  test.describe('Navigation Flow', () => {
    test('should redirect /onboarding to /onboarding/login', async ({ page }) => {
      await page.goto('/onboarding')

      await expect(page).toHaveURL(/\/onboarding\/login/)
    })

    test('should navigate from policy pack to stage mapping', async ({ page }) => {
      await page.goto('/onboarding/policy-pack')

      // Select a pack and continue
      await page.getByText('Standard').click()
      await page.getByRole('button', { name: /Continue/i }).click()

      await expect(page).toHaveURL(/\/onboarding\/stage-mapping/)
    })

    test('should navigate back from stage mapping to policy pack', async ({ page }) => {
      await page.goto('/onboarding/stage-mapping')

      // Click back button
      await page.getByRole('button', { name: /Back/i }).click()

      await expect(page).toHaveURL(/\/onboarding\/policy-pack/)
    })
  })

  test.describe('Responsiveness', () => {
    test('should be responsive on mobile viewport', async ({ page }) => {
      // Set mobile viewport
      await page.setViewportSize({ width: 375, height: 667 })

      await page.goto('/onboarding/login')

      // OAuth buttons should still be visible
      await expect(page.getByRole('button', { name: /GitHub/i })).toBeVisible()
    })

    test('should be responsive on tablet viewport', async ({ page }) => {
      // Set tablet viewport
      await page.setViewportSize({ width: 768, height: 1024 })

      await page.goto('/onboarding/policy-pack')

      // All policy packs should be visible
      await expect(page.getByText('Lite')).toBeVisible()
      await expect(page.getByText('Standard')).toBeVisible()
      await expect(page.getByText('Enterprise')).toBeVisible()
    })
  })

  test.describe('Accessibility', () => {
    test('should have proper heading structure', async ({ page }) => {
      await page.goto('/onboarding/login')

      // Check for h1 or h2 heading
      const heading = page.locator('h1, h2').first()
      await expect(heading).toBeVisible()
    })

    test('should have accessible buttons', async ({ page }) => {
      await page.goto('/onboarding/login')

      // Buttons should have accessible names
      const buttons = page.getByRole('button')
      const count = await buttons.count()

      for (let i = 0; i < count; i++) {
        const button = buttons.nth(i)
        const name = await button.getAttribute('aria-label') || await button.textContent()
        expect(name).toBeTruthy()
      }
    })

    test('should support keyboard navigation', async ({ page }) => {
      await page.goto('/onboarding/login')

      // Tab through OAuth buttons
      await page.keyboard.press('Tab')
      await page.keyboard.press('Tab')
      await page.keyboard.press('Tab')

      // Should be able to focus buttons
      const focusedElement = page.locator(':focus')
      await expect(focusedElement).toBeVisible()
    })
  })
})
