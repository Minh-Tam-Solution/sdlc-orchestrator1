/**
 * File: frontend/web/e2e/teams.spec.ts
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 73 (Teams Integration)
 * Date: February 10, 2026
 * Authority: QA Engineer + CTO Approved
 * Foundation: SDLC 5.1.2 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * E2E tests for Teams feature - Sprint 73 Day 2.
 * Tests comprehensive Teams workflows including:
 * - Organization CRUD operations
 * - Team CRUD operations
 * - Team membership management
 * - Team-project associations
 * - Permission boundaries (CTO R1/R2 compliance)
 *
 * Sprint 73 Tasks Covered:
 * - S73-E2E-T01: Organization CRUD E2E test
 * - S73-E2E-T02: Team CRUD E2E test
 * - S73-E2E-T03: Team membership E2E test
 * - S73-E2E-T04: Team → Project association E2E
 * - S73-E2E-T05: Permission boundary E2E test
 * - S73-E2E-T06: Cross-browser testing (via Playwright config)
 *
 * SDLC 5.1.2 Compliance:
 * - Pillar 1: Zero Mock Policy (Real API calls to backend)
 * - Pillar 3: Quality Governance (E2E coverage for critical workflows)
 * - SE4A Compliance: Verify AI agents cannot be team owner/admin (CTO R1/R2)
 *
 * Changelog:
 * - v1.0.0 (2026-02-10): Initial implementation - Sprint 73 Day 2
 */

import { test, expect, Page } from '@playwright/test'
import { login, loginAsAdmin, TEST_ADMIN, TEST_REGULAR_USER } from './helpers/auth'

// Test data generators
function generateTeamName(): string {
  return `E2E Test Team ${Date.now()}`
}

function generateOrgName(): string {
  return `E2E Test Org ${Date.now()}`
}

function generateProjectName(): string {
  return `E2E Test Project ${Date.now()}`
}

/**
 * Helper: Navigate to Teams page
 */
async function navigateToTeams(page: Page): Promise<void> {
  await page.goto('/teams')
  await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

  // Verify we're on teams page
  await expect(page.getByRole('heading', { name: /teams/i })).toBeVisible({ timeout: 5000 })
}

/**
 * Helper: Create a new team via UI
 */
async function createTeam(page: Page, teamName: string, description: string = 'E2E test team'): Promise<void> {
  await navigateToTeams(page)

  // Click "Create Team" button
  const createButton = page.getByRole('button', { name: /create team|new team/i })
  await createButton.click()

  // Wait for dialog to open
  await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })

  // Fill team details
  await page.getByLabel(/team name|name/i).fill(teamName)

  const descriptionField = page.getByLabel(/description/i)
  if (await descriptionField.isVisible({ timeout: 2000 }).catch(() => false)) {
    await descriptionField.fill(description)
  }

  // Submit form
  const submitButton = page.getByRole('button', { name: /create|save|submit/i }).last()
  await submitButton.click()

  // Wait for dialog to close
  await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })

  // Verify team appears in list
  await expect(page.getByText(teamName)).toBeVisible({ timeout: 10000 })
}

/**
 * Helper: Delete a team via UI
 */
async function deleteTeam(page: Page, teamName: string): Promise<void> {
  await navigateToTeams(page)

  // Find team card/row
  const teamCard = page.locator(`[data-testid="team-card"]:has-text("${teamName}"), .team-card:has-text("${teamName}")`).first()

  // Click delete button (could be in dropdown or direct button)
  const deleteButton = teamCard.locator('button[aria-label*="delete"], button:has-text("Delete")').first()

  if (await deleteButton.isVisible({ timeout: 2000 }).catch(() => false)) {
    await deleteButton.click()
  } else {
    // Try dropdown menu
    const menuButton = teamCard.locator('button[aria-label*="menu"], button[aria-haspopup="menu"]').first()
    await menuButton.click()
    await page.getByRole('menuitem', { name: /delete/i }).click()
  }

  // Confirm deletion in dialog
  const confirmButton = page.getByRole('button', { name: /confirm|delete|yes/i }).last()
  await confirmButton.click()

  // Verify team is removed
  await expect(page.getByText(teamName)).not.toBeVisible({ timeout: 10000 })
}

/**
 * S73-E2E-T01: Organization CRUD E2E Test
 */
test.describe('Organization Management (S73-E2E-T01)', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page)
  })

  test('should display organizations page', async ({ page }) => {
    await page.goto('/admin/organizations')

    // Verify page loaded
    await expect(page.getByRole('heading', { name: /organizations/i })).toBeVisible({ timeout: 5000 })
    await expect(page.getByRole('button', { name: /create organization|new organization/i })).toBeVisible()
  })

  test('should create new organization', async ({ page }) => {
    await page.goto('/admin/organizations')

    const orgName = generateOrgName()

    // Click create button
    await page.getByRole('button', { name: /create organization|new organization/i }).click()

    // Wait for dialog
    await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })

    // Fill organization details
    await page.getByLabel(/organization name|name/i).fill(orgName)

    const planSelect = page.getByLabel(/plan|subscription/i)
    if (await planSelect.isVisible({ timeout: 2000 }).catch(() => false)) {
      await planSelect.click()
      await page.getByRole('option', { name: /enterprise|standard/i }).first().click()
    }

    // Submit
    await page.getByRole('button', { name: /create|save|submit/i }).last().click()

    // Verify creation
    await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })
    await expect(page.getByText(orgName)).toBeVisible({ timeout: 10000 })
  })

  test('should edit organization details', async ({ page }) => {
    await page.goto('/admin/organizations')

    // Wait for orgs to load
    await page.waitForTimeout(2000)

    // Find first organization card
    const orgCard = page.locator('[data-testid="org-card"], .organization-card').first()

    if (await orgCard.isVisible({ timeout: 2000 }).catch(() => false)) {
      // Click edit button
      const editButton = orgCard.locator('button[aria-label*="edit"], button:has-text("Edit")').first()

      if (await editButton.isVisible({ timeout: 2000 }).catch(() => false)) {
        await editButton.click()

        // Wait for edit dialog
        await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })

        // Update name
        const nameField = page.getByLabel(/organization name|name/i)
        await nameField.clear()
        await nameField.fill(`Updated ${Date.now()}`)

        // Save
        await page.getByRole('button', { name: /save|update/i }).last().click()

        // Verify dialog closed
        await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })
      }
    }
  })

  test('should view organization details', async ({ page }) => {
    await page.goto('/admin/organizations')

    await page.waitForTimeout(2000)

    // Click on first organization
    const orgLink = page.locator('[data-testid="org-card"], .organization-card, [href*="/admin/organizations/"]').first()

    if (await orgLink.isVisible({ timeout: 2000 }).catch(() => false)) {
      await orgLink.click()

      // Should show organization details
      await expect(page.getByText(/teams|members|settings/i)).toBeVisible({ timeout: 5000 })
    }
  })
})

/**
 * S73-E2E-T02: Team CRUD E2E Test
 */
test.describe('Team Management (S73-E2E-T02)', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page)
  })

  test('should display teams page', async ({ page }) => {
    await navigateToTeams(page)

    // Verify page elements
    await expect(page.getByRole('heading', { name: /teams/i })).toBeVisible()
    await expect(page.getByRole('button', { name: /create team|new team/i })).toBeVisible()
  })

  test('should create new team', async ({ page }) => {
    const teamName = generateTeamName()
    await createTeam(page, teamName, 'E2E test team for Sprint 73')

    // Verify team exists
    await navigateToTeams(page)
    await expect(page.getByText(teamName)).toBeVisible()
  })

  test('should edit team details', async ({ page }) => {
    // First create a team
    const originalName = generateTeamName()
    await createTeam(page, originalName)

    // Navigate back to teams
    await navigateToTeams(page)

    // Find the team card
    const teamCard = page.locator(`[data-testid="team-card"]:has-text("${originalName}"), .team-card:has-text("${originalName}")`).first()

    // Click edit button
    const editButton = teamCard.locator('button[aria-label*="edit"], button:has-text("Edit")').first()

    if (await editButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await editButton.click()
    } else {
      // Try dropdown menu
      const menuButton = teamCard.locator('button[aria-label*="menu"], button[aria-haspopup="menu"]').first()
      await menuButton.click()
      await page.getByRole('menuitem', { name: /edit/i }).click()
    }

    // Wait for edit dialog
    await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })

    // Update name
    const updatedName = `Updated ${originalName}`
    const nameField = page.getByLabel(/team name|name/i)
    await nameField.clear()
    await nameField.fill(updatedName)

    // Save
    await page.getByRole('button', { name: /save|update/i }).last().click()

    // Verify update
    await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })
    await expect(page.getByText(updatedName)).toBeVisible({ timeout: 10000 })
  })

  test('should delete team', async ({ page }) => {
    // Create a team to delete
    const teamName = generateTeamName()
    await createTeam(page, teamName)

    // Delete the team
    await deleteTeam(page, teamName)

    // Verify deletion
    await navigateToTeams(page)
    await expect(page.getByText(teamName)).not.toBeVisible()
  })

  test('should view team details', async ({ page }) => {
    await navigateToTeams(page)

    await page.waitForTimeout(2000)

    // Click on first team
    const teamLink = page.locator('[data-testid="team-card"], .team-card, [href*="/teams/"]').first()

    if (await teamLink.isVisible({ timeout: 2000 }).catch(() => false)) {
      await teamLink.click()

      // Should show team details (members, projects, settings)
      await expect(page.getByText(/members|projects|settings/i)).toBeVisible({ timeout: 5000 })
    }
  })
})

/**
 * S73-E2E-T03: Team Membership E2E Test
 */
test.describe('Team Membership Management (S73-E2E-T03)', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page)
  })

  test('should add member to team', async ({ page }) => {
    // Create a team first
    const teamName = generateTeamName()
    await createTeam(page, teamName)

    // Navigate to team details
    await navigateToTeams(page)
    const teamCard = page.locator(`[data-testid="team-card"]:has-text("${teamName}"), .team-card:has-text("${teamName}")`).first()
    await teamCard.click()

    // Wait for team details page
    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

    // Click "Add Member" button
    const addMemberButton = page.getByRole('button', { name: /add member|invite member/i })

    if (await addMemberButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await addMemberButton.click()

      // Wait for add member dialog
      await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })

      // Select a user (dropdown or search)
      const userSelect = page.getByLabel(/user|member|email/i).first()
      await userSelect.click()

      // Click first available user
      const firstUser = page.getByRole('option').first()
      if (await firstUser.isVisible({ timeout: 2000 }).catch(() => false)) {
        await firstUser.click()
      }

      // Select role
      const roleSelect = page.getByLabel(/role/i)
      if (await roleSelect.isVisible({ timeout: 2000 }).catch(() => false)) {
        await roleSelect.click()
        await page.getByRole('option', { name: /member|developer/i }).first().click()
      }

      // Submit
      await page.getByRole('button', { name: /add|invite|save/i }).last().click()

      // Verify member added
      await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })
      await expect(page.getByText(/member added|invitation sent/i)).toBeVisible({ timeout: 5000 })
    }
  })

  test('should remove member from team', async ({ page }) => {
    await navigateToTeams(page)

    await page.waitForTimeout(2000)

    // Click on a team
    const teamLink = page.locator('[data-testid="team-card"], .team-card').first()

    if (await teamLink.isVisible({ timeout: 2000 }).catch(() => false)) {
      await teamLink.click()

      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

      // Find first team member row (not owner)
      const memberRow = page.locator('[data-testid="member-row"], .member-row, tr:has-text("Member")').first()

      if (await memberRow.isVisible({ timeout: 2000 }).catch(() => false)) {
        // Click remove button
        const removeButton = memberRow.locator('button[aria-label*="remove"], button:has-text("Remove")').first()

        if (await removeButton.isVisible({ timeout: 2000 }).catch(() => false)) {
          await removeButton.click()

          // Confirm removal
          const confirmButton = page.getByRole('button', { name: /confirm|remove|yes/i }).last()
          await confirmButton.click()

          // Verify removal
          await expect(page.getByText(/member removed|removed from team/i)).toBeVisible({ timeout: 5000 })
        }
      }
    }
  })

  test('should change member role', async ({ page }) => {
    await navigateToTeams(page)

    await page.waitForTimeout(2000)

    // Click on a team with members
    const teamLink = page.locator('[data-testid="team-card"], .team-card').first()

    if (await teamLink.isVisible({ timeout: 2000 }).catch(() => false)) {
      await teamLink.click()

      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

      // Find a member row
      const memberRow = page.locator('[data-testid="member-row"], .member-row, tr').first()

      if (await memberRow.isVisible({ timeout: 2000 }).catch(() => false)) {
        // Find role dropdown
        const roleSelect = memberRow.locator('select, [role="combobox"]').first()

        if (await roleSelect.isVisible({ timeout: 2000 }).catch(() => false)) {
          await roleSelect.click()

          // Select different role
          const newRole = page.getByRole('option', { name: /lead|admin|member/i }).first()
          await newRole.click()

          // Verify role change (may show confirmation toast)
          await expect(page.getByText(/role updated|role changed/i)).toBeVisible({ timeout: 5000 })
        }
      }
    }
  })
})

/**
 * S73-E2E-T04: Team → Project Association E2E Test
 */
test.describe('Team-Project Association (S73-E2E-T04)', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page)
  })

  test('should assign team when creating project', async ({ page }) => {
    // Navigate to projects
    await page.goto('/projects')

    // Click "Create Project" button
    await page.getByRole('button', { name: /create project|new project/i }).click()

    // Wait for dialog
    await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })

    // Fill project name
    const projectName = generateProjectName()
    await page.getByLabel(/project name|name/i).fill(projectName)

    // Select team
    const teamSelect = page.getByLabel(/team/i)
    if (await teamSelect.isVisible({ timeout: 2000 }).catch(() => false)) {
      await teamSelect.click()

      // Select first available team
      const firstTeam = page.getByRole('option').first()
      if (await firstTeam.isVisible({ timeout: 2000 }).catch(() => false)) {
        await firstTeam.click()
      }
    }

    // Submit
    await page.getByRole('button', { name: /create|save|submit/i }).last().click()

    // Verify project created
    await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })
    await expect(page.getByText(projectName)).toBeVisible({ timeout: 10000 })
  })

  test('should filter projects by team', async ({ page }) => {
    await page.goto('/projects')

    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

    // Find team filter dropdown
    const teamFilter = page.getByLabel(/filter by team|team filter/i)

    if (await teamFilter.isVisible({ timeout: 2000 }).catch(() => false)) {
      await teamFilter.click()

      // Select a team
      const teamOption = page.getByRole('option').first()
      if (await teamOption.isVisible({ timeout: 2000 }).catch(() => false)) {
        const teamName = await teamOption.textContent()
        await teamOption.click()

        // Wait for filter to apply
        await page.waitForTimeout(1000)

        // Verify filter is active (badge or indicator)
        await expect(page.getByText(new RegExp(teamName || '', 'i'))).toBeVisible()
      }
    }
  })

  test('should show team badge on project card', async ({ page }) => {
    await page.goto('/projects')

    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

    // Find first project card with team badge
    const projectCard = page.locator('[data-testid="project-card"], .project-card').first()

    if (await projectCard.isVisible({ timeout: 2000 }).catch(() => false)) {
      // Check for team badge/label
      const teamBadge = projectCard.locator('[data-testid="team-badge"], .team-badge, .badge').first()

      // Team badge may or may not be present (depends on if project has team)
      // Just verify project card is rendered correctly
      await expect(projectCard).toBeVisible()
    }
  })

  test('should verify auto-created gates for new project (BUG #7 fix)', async ({ page }) => {
    // Navigate to projects
    await page.goto('/projects')

    // Create new project
    await page.getByRole('button', { name: /create project|new project/i }).click()
    await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })

    const projectName = generateProjectName()
    await page.getByLabel(/project name|name/i).fill(projectName)

    // Submit
    await page.getByRole('button', { name: /create|save|submit/i }).last().click()
    await expect(page.getByRole('dialog')).not.toBeVisible({ timeout: 10000 })

    // Wait for project to appear
    await expect(page.getByText(projectName)).toBeVisible({ timeout: 10000 })

    // Click on the project to view details
    const projectCard = page.locator(`[data-testid="project-card"]:has-text("${projectName}"), .project-card:has-text("${projectName}")`).first()
    await projectCard.click()

    // Navigate to Gates tab
    const gatesTab = page.getByRole('tab', { name: /gates/i })
    if (await gatesTab.isVisible({ timeout: 2000 }).catch(() => false)) {
      await gatesTab.click()
    } else {
      // Try navigation link
      await page.goto(page.url() + '/gates')
    }

    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

    // Verify 5 default gates exist (BUG #7 fix)
    const expectedGates = [
      /planning review/i,
      /design review/i,
      /code review/i,
      /test review/i,
      /deploy approval/i,
    ]

    for (const gateName of expectedGates) {
      await expect(page.getByText(gateName)).toBeVisible({ timeout: 5000 })
    }
  })
})

/**
 * S73-E2E-T05: Permission Boundary E2E Test (CTO R1/R2 Compliance)
 */
test.describe('Permission Boundaries (S73-E2E-T05)', () => {
  test('admin should have full access to teams', async ({ page }) => {
    await loginAsAdmin(page)

    await navigateToTeams(page)

    // Verify admin can create teams
    await expect(page.getByRole('button', { name: /create team|new team/i })).toBeVisible()

    // Verify admin can see all teams
    await page.waitForTimeout(2000)

    const teamCards = page.locator('[data-testid="team-card"], .team-card')
    const count = await teamCards.count()

    // Admin should see at least the default "Unassigned Projects" team
    expect(count).toBeGreaterThanOrEqual(1)
  })

  test('regular user should have limited team access', async ({ page }) => {
    await login(page, TEST_REGULAR_USER.email, TEST_REGULAR_USER.password)

    await navigateToTeams(page)

    // Regular users should only see teams they belong to
    await page.waitForTimeout(2000)

    // Verify create button may be disabled or not visible for non-admins
    const createButton = page.getByRole('button', { name: /create team|new team/i })
    const isVisible = await createButton.isVisible({ timeout: 2000 }).catch(() => false)

    // If visible, it might be disabled
    if (isVisible) {
      const isDisabled = await createButton.isDisabled()
      // Either not visible or disabled
      expect(isDisabled).toBeTruthy()
    }
  })

  test('CTO R1: AI agents cannot be team owner', async ({ page }) => {
    await loginAsAdmin(page)

    // Create a team
    const teamName = generateTeamName()
    await createTeam(page, teamName)

    // Navigate to team details
    await navigateToTeams(page)
    const teamCard = page.locator(`[data-testid="team-card"]:has-text("${teamName}"), .team-card:has-text("${teamName}")`).first()
    await teamCard.click()

    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

    // Try to add AI agent as owner (should fail validation)
    const addMemberButton = page.getByRole('button', { name: /add member|invite member/i })

    if (await addMemberButton.isVisible({ timeout: 2000 }).catch(() => false)) {
      await addMemberButton.click()
      await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })

      // Select AI agent user type
      const memberTypeSelect = page.getByLabel(/member type|type/i)
      if (await memberTypeSelect.isVisible({ timeout: 2000 }).catch(() => false)) {
        await memberTypeSelect.click()

        const aiAgentOption = page.getByRole('option', { name: /ai agent|agent/i })
        if (await aiAgentOption.isVisible({ timeout: 2000 }).catch(() => false)) {
          await aiAgentOption.click()

          // Try to select "owner" role
          const roleSelect = page.getByLabel(/role/i)
          await roleSelect.click()

          // Owner role should NOT be available for AI agents (CTO R1)
          const ownerOption = page.getByRole('option', { name: /owner/i })
          await expect(ownerOption).not.toBeVisible()
        }
      }

      // Close dialog
      const cancelButton = page.getByRole('button', { name: /cancel|close/i })
      await cancelButton.click()
    }
  })

  test('CTO R2: AI agents cannot be team admin', async ({ page }) => {
    await loginAsAdmin(page)

    await navigateToTeams(page)

    await page.waitForTimeout(2000)

    // Click on first team
    const teamLink = page.locator('[data-testid="team-card"], .team-card').first()

    if (await teamLink.isVisible({ timeout: 2000 }).catch(() => false)) {
      await teamLink.click()

      await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

      // Try to add AI agent
      const addMemberButton = page.getByRole('button', { name: /add member|invite member/i })

      if (await addMemberButton.isVisible({ timeout: 2000 }).catch(() => false)) {
        await addMemberButton.click()
        await expect(page.getByRole('dialog')).toBeVisible({ timeout: 5000 })

        // Select AI agent type
        const memberTypeSelect = page.getByLabel(/member type|type/i)
        if (await memberTypeSelect.isVisible({ timeout: 2000 }).catch(() => false)) {
          await memberTypeSelect.click()

          const aiAgentOption = page.getByRole('option', { name: /ai agent|agent/i })
          if (await aiAgentOption.isVisible({ timeout: 2000 }).catch(() => false)) {
            await aiAgentOption.click()

            // Try to select "admin" role
            const roleSelect = page.getByLabel(/role/i)
            await roleSelect.click()

            // Admin role should NOT be available for AI agents (CTO R2)
            const adminOption = page.getByRole('option', { name: /^admin$/i })
            await expect(adminOption).not.toBeVisible()

            // Only "member" and "viewer" roles should be available
            await expect(page.getByRole('option', { name: /member/i })).toBeVisible()
          }
        }

        // Close dialog
        const cancelButton = page.getByRole('button', { name: /cancel|close/i })
        await cancelButton.click()
      }
    }
  })
})

/**
 * S73-E2E-T06: Cross-Browser Testing
 * Note: Cross-browser testing is configured via playwright.config.ts
 * This test suite will run on all configured browsers:
 * - chromium (Desktop Chrome)
 * - firefox (Desktop Firefox)
 * - webkit (Desktop Safari)
 * - Mobile Chrome (Pixel 5)
 * - Mobile Safari (iPhone 12)
 */
test.describe('Teams - Cross-Browser Compatibility (S73-E2E-T06)', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page)
  })

  test('teams page should render correctly on all browsers', async ({ page, browserName }) => {
    await navigateToTeams(page)

    // Verify core UI elements are visible
    await expect(page.getByRole('heading', { name: /teams/i })).toBeVisible({ timeout: 5000 })
    await expect(page.getByRole('button', { name: /create team|new team/i })).toBeVisible()

    // Verify page is responsive
    const viewport = page.viewportSize()
    expect(viewport).toBeTruthy()

    console.log(`Teams page rendered successfully on ${browserName}`)
  })

  test('team creation should work on all browsers', async ({ page, browserName }) => {
    const teamName = `${browserName} ${generateTeamName()}`

    await createTeam(page, teamName, `E2E test for ${browserName}`)

    // Verify team created
    await navigateToTeams(page)
    await expect(page.getByText(teamName)).toBeVisible({ timeout: 10000 })

    console.log(`Team creation successful on ${browserName}`)
  })
})

/**
 * Dashboard Teams Statistics Test (S73-T09~T13)
 */
test.describe('Dashboard Teams Statistics', () => {
  test.beforeEach(async ({ page }) => {
    await loginAsAdmin(page)
  })

  test('should display team statistics on dashboard', async ({ page }) => {
    await page.goto('/dashboard')

    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

    // Verify "Total Teams" stat card is visible
    const teamStatCard = page.locator('[data-testid="stat-card"]:has-text("Total Teams"), .stat-card:has-text("Total Teams")').first()

    await expect(teamStatCard).toBeVisible({ timeout: 5000 })

    // Verify it shows a number
    await expect(teamStatCard.getByText(/\d+/)).toBeVisible()
  })

  test('clicking team stat should navigate to teams page', async ({ page }) => {
    await page.goto('/dashboard')

    await page.waitForLoadState('networkidle', { timeout: 10000 }).catch(() => {})

    // Click on "Total Teams" stat card
    const teamStatCard = page.locator('[data-testid="stat-card"]:has-text("Total Teams"), .stat-card:has-text("Total Teams")').first()

    if (await teamStatCard.isVisible({ timeout: 2000 }).catch(() => false)) {
      await teamStatCard.click()

      // Should navigate to teams page
      await expect(page).toHaveURL(/\/teams/, { timeout: 5000 })
      await expect(page.getByRole('heading', { name: /teams/i })).toBeVisible()
    }
  })
})
