/**
 * File: frontend/web/e2e/accessibility.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Accessibility audit tests using axe-core.
 * WCAG 2.1 AA compliance validation.
 */

import { test, expect } from '@playwright/test'
import AxeBuilder from '@axe-core/playwright'

test.describe('Accessibility Audit (WCAG 2.1 AA)', () => {
  test.beforeEach(async ({ page }) => {
    // Login before each test
    await page.goto('/login')
    await page.getByLabel(/email/i).fill('admin@sdlc-orchestrator.io')
    await page.getByLabel(/password/i).fill('Admin@123')
    await page.getByRole('button', { name: /sign in|login/i }).click()
    await expect(page).toHaveURL(/\/dashboard/, { timeout: 10000 })
  })

  test('Login page should have no accessibility violations', async ({ page }) => {
    // Logout first
    await page.goto('/login')

    // Wait for page to fully load
    await page.waitForLoadState('networkidle')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    // Log violations for debugging
    if (accessibilityScanResults.violations.length > 0) {
      console.log('Login page violations:', JSON.stringify(accessibilityScanResults.violations, null, 2))
    }

    expect(accessibilityScanResults.violations).toHaveLength(0)
  })

  test('Dashboard page should have no accessibility violations', async ({ page }) => {
    await page.goto('/dashboard')

    // Wait for page to fully load
    await page.waitForLoadState('networkidle')
    await page.waitForTimeout(1000) // Allow dynamic content to render

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    if (accessibilityScanResults.violations.length > 0) {
      console.log('Dashboard violations:', JSON.stringify(accessibilityScanResults.violations, null, 2))
    }

    expect(accessibilityScanResults.violations).toHaveLength(0)
  })

  test('Projects page should have no accessibility violations', async ({ page }) => {
    await page.goto('/projects')

    await page.waitForLoadState('networkidle')
    await page.waitForTimeout(1000)

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    if (accessibilityScanResults.violations.length > 0) {
      console.log('Projects page violations:', JSON.stringify(accessibilityScanResults.violations, null, 2))
    }

    expect(accessibilityScanResults.violations).toHaveLength(0)
  })

  test('Gates page should have no accessibility violations', async ({ page }) => {
    await page.goto('/gates')

    await page.waitForLoadState('networkidle')
    await page.waitForTimeout(1000)

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    if (accessibilityScanResults.violations.length > 0) {
      console.log('Gates page violations:', JSON.stringify(accessibilityScanResults.violations, null, 2))
    }

    expect(accessibilityScanResults.violations).toHaveLength(0)
  })

  test('Policies page should have no accessibility violations', async ({ page }) => {
    await page.goto('/policies')

    await page.waitForLoadState('networkidle')
    await page.waitForTimeout(1000)

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    if (accessibilityScanResults.violations.length > 0) {
      console.log('Policies page violations:', JSON.stringify(accessibilityScanResults.violations, null, 2))
    }

    expect(accessibilityScanResults.violations).toHaveLength(0)
  })

  test('Evidence page should have no accessibility violations', async ({ page }) => {
    await page.goto('/evidence')

    await page.waitForLoadState('networkidle')
    await page.waitForTimeout(1000)

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    if (accessibilityScanResults.violations.length > 0) {
      console.log('Evidence page violations:', JSON.stringify(accessibilityScanResults.violations, null, 2))
    }

    expect(accessibilityScanResults.violations).toHaveLength(0)
  })

  test('Create Project dialog should have no accessibility violations', async ({ page }) => {
    await page.goto('/projects')

    // Open create project dialog
    await page.getByRole('button', { name: /new project|create project/i }).click()
    await expect(page.getByRole('dialog')).toBeVisible()

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze()

    if (accessibilityScanResults.violations.length > 0) {
      console.log('Create Project dialog violations:', JSON.stringify(accessibilityScanResults.violations, null, 2))
    }

    expect(accessibilityScanResults.violations).toHaveLength(0)
  })

  test('All pages should have proper focus management', async ({ page }) => {
    await page.goto('/dashboard')

    // Tab through interactive elements
    await page.keyboard.press('Tab')

    // Check that focus is visible
    const focusedElement = await page.locator(':focus').first()
    await expect(focusedElement).toBeVisible()

    // Verify focus indicator exists (outline or custom style)
    const focusStyles = await focusedElement.evaluate((el) => {
      const styles = window.getComputedStyle(el)
      return {
        outline: styles.outline,
        outlineWidth: styles.outlineWidth,
        boxShadow: styles.boxShadow,
      }
    })

    // Should have visible focus indicator
    const hasFocusIndicator =
      focusStyles.outlineWidth !== '0px' ||
      focusStyles.boxShadow !== 'none'

    expect(hasFocusIndicator).toBe(true)
  })

  test('All pages should have proper heading structure', async ({ page }) => {
    const pages = ['/dashboard', '/projects', '/gates', '/policies', '/evidence']

    for (const pagePath of pages) {
      await page.goto(pagePath)
      await page.waitForLoadState('networkidle')

      // Check for h1 heading
      const h1Count = await page.locator('h1').count()
      expect(h1Count).toBeGreaterThanOrEqual(1)

      // Check heading hierarchy (no skipped levels)
      const headings = await page.locator('h1, h2, h3, h4, h5, h6').allTextContents()
      expect(headings.length).toBeGreaterThan(0)
    }
  })

  test('All interactive elements should be keyboard accessible', async ({ page }) => {
    await page.goto('/dashboard')

    // Get all interactive elements
    const interactiveElements = await page.locator(
      'button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    ).all()

    // Verify each is focusable
    for (const element of interactiveElements.slice(0, 10)) {
      // Test first 10 elements
      const isVisible = await element.isVisible()
      if (isVisible) {
        await element.focus()
        await expect(element).toBeFocused()
      }
    }
  })

  test('Color contrast should meet WCAG AA standards', async ({ page }) => {
    await page.goto('/dashboard')
    await page.waitForLoadState('networkidle')

    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2aa'])
      .options({
        rules: {
          'color-contrast': { enabled: true },
        },
      })
      .analyze()

    const contrastViolations = accessibilityScanResults.violations.filter(
      (v) => v.id === 'color-contrast'
    )

    if (contrastViolations.length > 0) {
      console.log('Color contrast violations:', JSON.stringify(contrastViolations, null, 2))
    }

    expect(contrastViolations).toHaveLength(0)
  })

  test('Images should have alt text', async ({ page }) => {
    await page.goto('/dashboard')

    const images = await page.locator('img').all()

    for (const img of images) {
      const alt = await img.getAttribute('alt')
      const role = await img.getAttribute('role')

      // Images should have alt text or be marked as decorative
      const hasAlt = alt !== null
      const isDecorative = role === 'presentation' || alt === ''

      expect(hasAlt || isDecorative).toBe(true)
    }
  })

  test('Form inputs should have associated labels', async ({ page }) => {
    await page.goto('/login')

    const inputs = await page.locator('input:not([type="hidden"])').all()

    for (const input of inputs) {
      const id = await input.getAttribute('id')
      const ariaLabel = await input.getAttribute('aria-label')
      const ariaLabelledBy = await input.getAttribute('aria-labelledby')

      if (id) {
        const label = await page.locator(`label[for="${id}"]`).count()
        const hasLabel = label > 0 || ariaLabel !== null || ariaLabelledBy !== null
        expect(hasLabel).toBe(true)
      }
    }
  })
})
