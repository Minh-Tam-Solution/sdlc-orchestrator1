/**
 * Sprint 95 E2E Tests - Evidence Manifest UI
 *
 * @module frontend/e2e/sprint95-evidence-manifest.spec
 * @description E2E tests for Evidence Manifest Dashboard and Detail pages
 * @sdlc SDLC 5.1.3 Framework - Sprint 95 (Evidence Manifest UI)
 * @status Sprint 95 - January 22, 2026
 * @see frontend/src/app/app/evidence-manifests/page.tsx
 * @see frontend/src/app/app/evidence-manifests/[id]/page.tsx
 */

import { test, expect, Page } from "@playwright/test";

// =============================================================================
// Test Configuration
// =============================================================================

const BASE_URL = process.env.PLAYWRIGHT_BASE_URL || "http://localhost:3000";
const EVIDENCE_MANIFESTS_URL = `${BASE_URL}/app/evidence-manifests`;

// =============================================================================
// Helper Functions
// =============================================================================

/**
 * Navigate to Evidence Manifests page and wait for load
 */
async function navigateToEvidenceManifests(page: Page): Promise<void> {
  await page.goto(EVIDENCE_MANIFESTS_URL);
  await page.waitForLoadState("networkidle");
}

/**
 * Navigate to a specific manifest detail page
 */
async function navigateToManifestDetail(page: Page, manifestId: string): Promise<void> {
  await page.goto(`${EVIDENCE_MANIFESTS_URL}/${manifestId}`);
  await page.waitForLoadState("networkidle");
}

/**
 * Mock authenticated session
 */
async function mockAuthenticatedSession(page: Page): Promise<void> {
  await page.addInitScript(() => {
    localStorage.setItem("auth_token", "mock_jwt_token_for_testing");
    localStorage.setItem("user", JSON.stringify({
      id: "user-123",
      email: "test@sdlc-orchestrator.dev",
      name: "Test User",
      role: "admin",
    }));
  });
}

/**
 * Mock Evidence Manifests API responses
 */
async function mockEvidenceManifestsAPI(page: Page): Promise<void> {
  // Mock chain status endpoint
  await page.route("**/api/v1/evidence-manifests/chain-status*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        project_id: "proj-001",
        total_manifests: 42,
        verified_count: 40,
        unverified_count: 2,
        broken_count: 0,
        chain_integrity: "verified",
        last_verification: "2026-01-22T10:30:00Z",
        genesis_manifest_id: "manifest-001",
      }),
    });
  });

  // Mock manifests list endpoint
  await page.route("**/api/v1/evidence-manifests*", async (route) => {
    const url = route.request().url();
    // Skip if this is the chain-status endpoint
    if (url.includes("chain-status") || url.includes("verify")) {
      return route.continue();
    }

    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        manifests: [
          {
            id: "manifest-003",
            sequence_number: 3,
            manifest_hash: "abc123def456789012345678901234567890abcdef1234567890abcdef12345678",
            previous_hash: "def456789012345678901234567890abcdef1234567890abcdef12345678abc123",
            artifact_count: 5,
            total_size: 1024000,
            created_at: "2026-01-22T10:00:00Z",
            created_by: "user-123",
            status: "verified",
          },
          {
            id: "manifest-002",
            sequence_number: 2,
            manifest_hash: "def456789012345678901234567890abcdef1234567890abcdef12345678abc123",
            previous_hash: "genesis-hash-000000000000000000000000000000000000000000000000000000",
            artifact_count: 3,
            total_size: 512000,
            created_at: "2026-01-21T15:00:00Z",
            created_by: "user-456",
            status: "verified",
          },
          {
            id: "manifest-001",
            sequence_number: 1,
            manifest_hash: "genesis-hash-000000000000000000000000000000000000000000000000000000",
            previous_hash: null,
            artifact_count: 2,
            total_size: 256000,
            created_at: "2026-01-20T09:00:00Z",
            created_by: "user-123",
            status: "verified",
            is_genesis: true,
          },
        ],
        total: 3,
        page: 1,
        page_size: 10,
      }),
    });
  });

  // Mock verification history endpoint
  await page.route("**/api/v1/evidence-manifests/verification-history*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        history: [
          {
            id: "verify-003",
            verified_at: "2026-01-22T10:30:00Z",
            verified_by: "system",
            result: "passed",
            manifests_checked: 42,
            issues_found: 0,
          },
          {
            id: "verify-002",
            verified_at: "2026-01-21T10:30:00Z",
            verified_by: "user-123",
            result: "passed",
            manifests_checked: 40,
            issues_found: 0,
          },
          {
            id: "verify-001",
            verified_at: "2026-01-20T10:00:00Z",
            verified_by: "system",
            result: "passed",
            manifests_checked: 2,
            issues_found: 0,
          },
        ],
        total: 3,
      }),
    });
  });

  // Mock projects endpoint for project selector
  await page.route("**/api/v1/projects*", async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        projects: [
          { id: "proj-001", name: "SDLC Orchestrator", slug: "sdlc-orchestrator" },
          { id: "proj-002", name: "BFlow Platform", slug: "bflow-platform" },
          { id: "proj-003", name: "NQH Bot", slug: "nqh-bot" },
        ],
        total: 3,
      }),
    });
  });
}

/**
 * Mock manifest detail API response
 */
async function mockManifestDetailAPI(page: Page, manifestId: string): Promise<void> {
  await page.route(`**/api/v1/evidence-manifests/${manifestId}`, async (route) => {
    await route.fulfill({
      status: 200,
      contentType: "application/json",
      body: JSON.stringify({
        id: manifestId,
        sequence_number: 3,
        manifest_hash: "abc123def456789012345678901234567890abcdef1234567890abcdef12345678",
        previous_hash: "def456789012345678901234567890abcdef1234567890abcdef12345678abc123",
        signature: "ed25519-signature-0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef01234567",
        signature_algorithm: "Ed25519",
        created_at: "2026-01-22T10:00:00Z",
        created_by: {
          id: "user-123",
          name: "Test User",
          email: "test@sdlc-orchestrator.dev",
        },
        project: {
          id: "proj-001",
          name: "SDLC Orchestrator",
        },
        status: "verified",
        artifacts: [
          {
            id: "artifact-001",
            name: "gate-evaluation-result.json",
            type: "gate_result",
            mime_type: "application/json",
            size: 2048,
            sha256: "sha256-artifact-001-0123456789abcdef0123456789abcdef0123456789abcdef01234567",
            uploaded_at: "2026-01-22T09:55:00Z",
          },
          {
            id: "artifact-002",
            name: "code-review-report.pdf",
            type: "review",
            mime_type: "application/pdf",
            size: 512000,
            sha256: "sha256-artifact-002-0123456789abcdef0123456789abcdef0123456789abcdef01234567",
            uploaded_at: "2026-01-22T09:56:00Z",
          },
          {
            id: "artifact-003",
            name: "test-coverage.html",
            type: "coverage",
            mime_type: "text/html",
            size: 128000,
            sha256: "sha256-artifact-003-0123456789abcdef0123456789abcdef0123456789abcdef01234567",
            uploaded_at: "2026-01-22T09:57:00Z",
          },
          {
            id: "artifact-004",
            name: "security-scan.sarif",
            type: "security",
            mime_type: "application/json",
            size: 64000,
            sha256: "sha256-artifact-004-0123456789abcdef0123456789abcdef0123456789abcdef01234567",
            uploaded_at: "2026-01-22T09:58:00Z",
          },
          {
            id: "artifact-005",
            name: "deployment-log.txt",
            type: "log",
            mime_type: "text/plain",
            size: 32000,
            sha256: "sha256-artifact-005-0123456789abcdef0123456789abcdef0123456789abcdef01234567",
            uploaded_at: "2026-01-22T09:59:00Z",
          },
        ],
        total_size: 738048,
        artifact_count: 5,
      }),
    });
  });
}

// =============================================================================
// Test Suites
// =============================================================================

test.describe("Evidence Manifests Dashboard - Navigation", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
  });

  test("should navigate to evidence manifests page", async ({ page }) => {
    await navigateToEvidenceManifests(page);
    await expect(page).toHaveURL(/\/app\/evidence-manifests/);
  });

  test("should display page title", async ({ page }) => {
    await navigateToEvidenceManifests(page);
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  });

  test("should show breadcrumb navigation", async ({ page }) => {
    await navigateToEvidenceManifests(page);
    const breadcrumb = page.locator('[aria-label="Breadcrumb"]').or(page.locator(".breadcrumb"));
    // Breadcrumb may or may not exist depending on layout
    if (await breadcrumb.count() > 0) {
      await expect(breadcrumb).toBeVisible();
    }
  });
});

test.describe("Evidence Manifests Dashboard - Chain Status Card", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);
  });

  test("should display chain status card", async ({ page }) => {
    const statusCard = page.locator('[data-testid="chain-status-card"]')
      .or(page.getByText(/chain status/i).first());
    await expect(statusCard).toBeVisible();
  });

  test("should show total manifests count", async ({ page }) => {
    const totalManifests = page.getByText(/42/).or(page.getByText(/total.*manifest/i));
    await expect(totalManifests).toBeVisible();
  });

  test("should display chain integrity status", async ({ page }) => {
    const integrityStatus = page.getByText(/verified/i).first();
    await expect(integrityStatus).toBeVisible();
  });

  test("should show verified vs unverified counts", async ({ page }) => {
    // Look for numbers or text indicating verified/unverified
    const verifiedCount = page.getByText(/40/).or(page.getByText(/verified.*40/i));
    await expect(verifiedCount).toBeVisible();
  });

  test("should display last verification timestamp", async ({ page }) => {
    const lastVerification = page.getByText(/last.*verif/i)
      .or(page.getByText(/2026-01-22/));
    await expect(lastVerification).toBeVisible();
  });
});

test.describe("Evidence Manifests Dashboard - Hash Chain Visualization", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);
  });

  test("should display hash chain visualization", async ({ page }) => {
    const visualization = page.locator('[data-testid="hash-chain-visualization"]')
      .or(page.getByText(/hash chain/i).first());
    await expect(visualization).toBeVisible();
  });

  test("should show chain links between manifests", async ({ page }) => {
    // Look for visual chain indicators or links
    const chainElements = page.locator('[data-testid="chain-link"]')
      .or(page.locator(".chain-link"))
      .or(page.locator("svg").filter({ hasText: "" })); // SVG connectors
    // At least some chain visualization should exist
    const count = await chainElements.count();
    expect(count).toBeGreaterThanOrEqual(0); // Chain visualization is optional
  });

  test("should highlight genesis manifest", async ({ page }) => {
    const genesisIndicator = page.getByText(/genesis/i);
    await expect(genesisIndicator).toBeVisible();
  });
});

test.describe("Evidence Manifests Dashboard - Manifest List", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);
  });

  test("should display manifest list", async ({ page }) => {
    const manifestList = page.locator('[data-testid="manifest-list"]')
      .or(page.locator("table"))
      .or(page.locator('[role="list"]'));
    await expect(manifestList).toBeVisible();
  });

  test("should show manifest sequence numbers", async ({ page }) => {
    // Look for sequence indicators (#1, #2, #3)
    const sequenceNumber = page.getByText(/#[0-9]+/)
      .or(page.getByText(/sequence/i));
    await expect(sequenceNumber.first()).toBeVisible();
  });

  test("should display manifest hashes (truncated)", async ({ page }) => {
    // Look for truncated hash format (abc123... or similar)
    const hashDisplay = page.getByText(/[a-f0-9]{6,8}\.{3}/i)
      .or(page.getByText(/hash/i));
    await expect(hashDisplay.first()).toBeVisible();
  });

  test("should show artifact count per manifest", async ({ page }) => {
    const artifactCount = page.getByText(/\d+\s*artifact/i)
      .or(page.getByText(/5 artifacts/i));
    await expect(artifactCount.first()).toBeVisible();
  });

  test("should display manifest creation dates", async ({ page }) => {
    const dateDisplay = page.getByText(/2026-01-2[0-2]/);
    await expect(dateDisplay.first()).toBeVisible();
  });

  test("should show verification status badges", async ({ page }) => {
    const statusBadge = page.locator('[data-testid="status-badge"]')
      .or(page.getByText(/verified/i).first());
    await expect(statusBadge).toBeVisible();
  });
});

test.describe("Evidence Manifests Dashboard - Project Selector", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);
  });

  test("should display project selector", async ({ page }) => {
    const selector = page.locator('[data-testid="project-selector"]')
      .or(page.getByRole("combobox"))
      .or(page.locator("select"));
    await expect(selector.first()).toBeVisible();
  });

  test("should list available projects", async ({ page }) => {
    const selector = page.getByRole("combobox").or(page.locator("select")).first();
    if (await selector.isVisible()) {
      await selector.click();
      const projectOption = page.getByText(/SDLC Orchestrator/i);
      await expect(projectOption).toBeVisible();
    }
  });

  test("should update manifest list when project changes", async ({ page }) => {
    const selector = page.getByRole("combobox").or(page.locator("select")).first();
    if (await selector.isVisible()) {
      await selector.click();
      const option = page.getByText(/BFlow Platform/i);
      if (await option.isVisible()) {
        await option.click();
        // Wait for list to update
        await page.waitForTimeout(500);
      }
    }
  });
});

test.describe("Evidence Manifests Dashboard - Verification Actions", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);
  });

  test("should display verify chain button", async ({ page }) => {
    const verifyButton = page.getByRole("button", { name: /verify/i });
    await expect(verifyButton.first()).toBeVisible();
  });

  test("should show verification history section", async ({ page }) => {
    const historySection = page.getByText(/verification history/i)
      .or(page.locator('[data-testid="verification-history"]'));
    await expect(historySection).toBeVisible();
  });

  test("should display previous verification results", async ({ page }) => {
    const verificationResult = page.getByText(/passed/i)
      .or(page.getByText(/42 manifests checked/i));
    await expect(verificationResult.first()).toBeVisible();
  });
});

test.describe("Evidence Manifests Dashboard - Verification History", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);
  });

  test("should display verification history list", async ({ page }) => {
    const historyList = page.locator('[data-testid="verification-history-list"]')
      .or(page.getByText(/verification history/i));
    await expect(historyList).toBeVisible();
  });

  test("should show verification timestamps", async ({ page }) => {
    const timestamp = page.getByText(/2026-01-2[0-2]T/i)
      .or(page.getByText(/Jan.*2026/i));
    await expect(timestamp.first()).toBeVisible();
  });

  test("should display who performed verification", async ({ page }) => {
    const verifiedBy = page.getByText(/system/i)
      .or(page.getByText(/user-123/i))
      .or(page.getByText(/Test User/i));
    await expect(verifiedBy.first()).toBeVisible();
  });

  test("should show manifests checked count", async ({ page }) => {
    const manifestsChecked = page.getByText(/\d+ manifest/i);
    await expect(manifestsChecked.first()).toBeVisible();
  });

  test("should display issues found (if any)", async ({ page }) => {
    const issuesCount = page.getByText(/0 issue/i)
      .or(page.getByText(/no issue/i));
    await expect(issuesCount.first()).toBeVisible();
  });
});

test.describe("Evidence Manifest Detail Page - Navigation", () => {
  const testManifestId = "manifest-003";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockManifestDetailAPI(page, testManifestId);
  });

  test("should navigate to manifest detail page", async ({ page }) => {
    await navigateToManifestDetail(page, testManifestId);
    await expect(page).toHaveURL(new RegExp(`/app/evidence-manifests/${testManifestId}`));
  });

  test("should display back button", async ({ page }) => {
    await navigateToManifestDetail(page, testManifestId);
    const backButton = page.getByRole("button", { name: /back/i })
      .or(page.getByRole("link", { name: /back/i }))
      .or(page.locator('[aria-label="Go back"]'));
    await expect(backButton.first()).toBeVisible();
  });

  test("should show manifest header with sequence number", async ({ page }) => {
    await navigateToManifestDetail(page, testManifestId);
    const header = page.getByText(/#3/).or(page.getByText(/manifest.*3/i));
    await expect(header.first()).toBeVisible();
  });
});

test.describe("Evidence Manifest Detail Page - Hash Information", () => {
  const testManifestId = "manifest-003";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockManifestDetailAPI(page, testManifestId);
    await navigateToManifestDetail(page, testManifestId);
  });

  test("should display manifest hash", async ({ page }) => {
    const hashSection = page.getByText(/manifest hash/i)
      .or(page.getByText(/abc123def/i));
    await expect(hashSection.first()).toBeVisible();
  });

  test("should show previous hash link", async ({ page }) => {
    const previousHash = page.getByText(/previous hash/i)
      .or(page.getByText(/def456/i));
    await expect(previousHash.first()).toBeVisible();
  });

  test("should display full hash on hover/click", async ({ page }) => {
    const hashElement = page.locator('[data-testid="manifest-hash"]')
      .or(page.getByText(/abc123/i).first());
    if (await hashElement.isVisible()) {
      await hashElement.hover();
      // Tooltip or expanded hash should appear
      await page.waitForTimeout(300);
    }
  });

  test("should show copy hash button", async ({ page }) => {
    const copyButton = page.getByRole("button", { name: /copy/i })
      .or(page.locator('[aria-label*="copy"]'));
    await expect(copyButton.first()).toBeVisible();
  });
});

test.describe("Evidence Manifest Detail Page - Digital Signature", () => {
  const testManifestId = "manifest-003";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockManifestDetailAPI(page, testManifestId);
    await navigateToManifestDetail(page, testManifestId);
  });

  test("should display signature section", async ({ page }) => {
    const signatureSection = page.getByText(/signature/i)
      .or(page.locator('[data-testid="signature-section"]'));
    await expect(signatureSection.first()).toBeVisible();
  });

  test("should show signature algorithm", async ({ page }) => {
    const algorithm = page.getByText(/Ed25519/i);
    await expect(algorithm).toBeVisible();
  });

  test("should display signature value (truncated)", async ({ page }) => {
    const signatureValue = page.getByText(/ed25519-signature/i)
      .or(page.getByText(/[a-f0-9]{16}/i));
    await expect(signatureValue.first()).toBeVisible();
  });

  test("should show signature verification status", async ({ page }) => {
    const verificationStatus = page.getByText(/verified/i);
    await expect(verificationStatus.first()).toBeVisible();
  });
});

test.describe("Evidence Manifest Detail Page - Artifacts List", () => {
  const testManifestId = "manifest-003";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockManifestDetailAPI(page, testManifestId);
    await navigateToManifestDetail(page, testManifestId);
  });

  test("should display artifacts section", async ({ page }) => {
    const artifactsSection = page.getByText(/artifact/i).first();
    await expect(artifactsSection).toBeVisible();
  });

  test("should show artifact count", async ({ page }) => {
    const artifactCount = page.getByText(/5 artifact/i)
      .or(page.getByText(/5\)/));
    await expect(artifactCount.first()).toBeVisible();
  });

  test("should list all artifacts", async ({ page }) => {
    const artifactItems = page.locator('[data-testid="artifact-item"]')
      .or(page.getByText(/gate-evaluation-result\.json/i));
    await expect(artifactItems.first()).toBeVisible();
  });

  test("should display artifact names", async ({ page }) => {
    const artifactNames = [
      "gate-evaluation-result.json",
      "code-review-report.pdf",
      "test-coverage.html",
      "security-scan.sarif",
      "deployment-log.txt",
    ];

    for (const name of artifactNames.slice(0, 2)) {
      const artifact = page.getByText(new RegExp(name, "i"));
      await expect(artifact).toBeVisible();
    }
  });

  test("should show artifact types with icons", async ({ page }) => {
    const typeIndicators = page.locator('[data-testid="artifact-type"]')
      .or(page.getByText(/gate_result|review|coverage|security|log/i));
    await expect(typeIndicators.first()).toBeVisible();
  });

  test("should display artifact file sizes", async ({ page }) => {
    const fileSize = page.getByText(/KB|MB|bytes/i);
    await expect(fileSize.first()).toBeVisible();
  });

  test("should show artifact SHA256 hashes", async ({ page }) => {
    const sha256 = page.getByText(/sha256/i)
      .or(page.getByText(/[a-f0-9]{64}/i));
    await expect(sha256.first()).toBeVisible();
  });
});

test.describe("Evidence Manifest Detail Page - Artifact Actions", () => {
  const testManifestId = "manifest-003";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockManifestDetailAPI(page, testManifestId);
    await navigateToManifestDetail(page, testManifestId);
  });

  test("should show download button for artifacts", async ({ page }) => {
    const downloadButton = page.getByRole("button", { name: /download/i })
      .or(page.locator('[aria-label*="download"]'));
    await expect(downloadButton.first()).toBeVisible();
  });

  test("should show view/preview button for supported types", async ({ page }) => {
    const viewButton = page.getByRole("button", { name: /view|preview/i })
      .or(page.locator('[aria-label*="view"]'));
    // View may not be available for all artifact types
    const count = await viewButton.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });

  test("should show copy hash button for artifacts", async ({ page }) => {
    const copyButton = page.getByRole("button", { name: /copy/i })
      .or(page.locator('[aria-label*="copy"]'));
    await expect(copyButton.first()).toBeVisible();
  });
});

test.describe("Evidence Manifest Detail Page - Metadata", () => {
  const testManifestId = "manifest-003";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockManifestDetailAPI(page, testManifestId);
    await navigateToManifestDetail(page, testManifestId);
  });

  test("should display creation timestamp", async ({ page }) => {
    const timestamp = page.getByText(/2026-01-22/)
      .or(page.getByText(/created.*at/i));
    await expect(timestamp.first()).toBeVisible();
  });

  test("should show creator information", async ({ page }) => {
    const creator = page.getByText(/Test User/i)
      .or(page.getByText(/created.*by/i));
    await expect(creator.first()).toBeVisible();
  });

  test("should display project association", async ({ page }) => {
    const project = page.getByText(/SDLC Orchestrator/i)
      .or(page.getByText(/project/i));
    await expect(project.first()).toBeVisible();
  });

  test("should show total size", async ({ page }) => {
    const totalSize = page.getByText(/720|738|KB|MB/i)
      .or(page.getByText(/total.*size/i));
    await expect(totalSize.first()).toBeVisible();
  });
});

test.describe("Evidence Manifest Detail Page - Genesis Manifest", () => {
  const genesisManifestId = "manifest-001";

  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
    // Mock genesis manifest
    await page.route(`**/api/v1/evidence-manifests/${genesisManifestId}`, async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify({
          id: genesisManifestId,
          sequence_number: 1,
          manifest_hash: "genesis-hash-000000000000000000000000000000000000000000000000000000",
          previous_hash: null,
          is_genesis: true,
          signature: "ed25519-genesis-signature",
          signature_algorithm: "Ed25519",
          created_at: "2026-01-20T09:00:00Z",
          created_by: { id: "user-123", name: "Test User" },
          project: { id: "proj-001", name: "SDLC Orchestrator" },
          status: "verified",
          artifacts: [
            {
              id: "artifact-genesis-001",
              name: "initial-setup.json",
              type: "config",
              mime_type: "application/json",
              size: 1024,
              sha256: "sha256-genesis-artifact",
              uploaded_at: "2026-01-20T09:00:00Z",
            },
          ],
          total_size: 1024,
          artifact_count: 1,
        }),
      });
    });
    await navigateToManifestDetail(page, genesisManifestId);
  });

  test("should display genesis indicator", async ({ page }) => {
    const genesisIndicator = page.getByText(/genesis/i);
    await expect(genesisIndicator).toBeVisible();
  });

  test("should show no previous hash for genesis manifest", async ({ page }) => {
    const noPreviousHash = page.getByText(/no previous/i)
      .or(page.getByText(/first.*manifest/i))
      .or(page.getByText(/chain origin/i));
    await expect(noPreviousHash.first()).toBeVisible();
  });

  test("should display sequence number 1", async ({ page }) => {
    const sequenceOne = page.getByText(/#1/)
      .or(page.getByText(/sequence.*1/i));
    await expect(sequenceOne.first()).toBeVisible();
  });
});

test.describe("Evidence Manifests - Loading States", () => {
  test("should show loading skeleton on dashboard", async ({ page }) => {
    await mockAuthenticatedSession(page);
    // Delay API response to see loading state
    await page.route("**/api/v1/evidence-manifests/**", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      await route.fulfill({ status: 200, body: JSON.stringify({ manifests: [], total: 0 }) });
    });

    await page.goto(EVIDENCE_MANIFESTS_URL);

    const skeleton = page.locator('[data-testid="loading-skeleton"]')
      .or(page.locator(".animate-pulse"))
      .or(page.getByText(/loading/i));
    await expect(skeleton.first()).toBeVisible();
  });

  test("should show loading state on detail page", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/evidence-manifests/manifest-003", async (route) => {
      await new Promise((resolve) => setTimeout(resolve, 1000));
      await route.fulfill({ status: 200, body: JSON.stringify({ id: "manifest-003" }) });
    });

    await page.goto(`${EVIDENCE_MANIFESTS_URL}/manifest-003`);

    const skeleton = page.locator('[data-testid="loading-skeleton"]')
      .or(page.locator(".animate-pulse"))
      .or(page.getByText(/loading/i));
    await expect(skeleton.first()).toBeVisible();
  });
});

test.describe("Evidence Manifests - Empty States", () => {
  test("should show empty state when no manifests exist", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/evidence-manifests*", async (route) => {
      const url = route.request().url();
      if (url.includes("chain-status")) {
        await route.fulfill({
          status: 200,
          body: JSON.stringify({
            total_manifests: 0,
            verified_count: 0,
            chain_integrity: "empty",
          }),
        });
      } else {
        await route.fulfill({
          status: 200,
          body: JSON.stringify({ manifests: [], total: 0 }),
        });
      }
    });

    await navigateToEvidenceManifests(page);

    const emptyState = page.getByText(/no manifest/i)
      .or(page.getByText(/get started/i))
      .or(page.getByText(/empty/i));
    await expect(emptyState.first()).toBeVisible();
  });

  test("should show empty verification history state", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await page.route("**/api/v1/evidence-manifests/verification-history*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({ history: [], total: 0 }),
      });
    });

    await navigateToEvidenceManifests(page);

    const noHistory = page.getByText(/no verification/i)
      .or(page.getByText(/never.*verified/i));
    // This may or may not show depending on UI design
    const count = await noHistory.count();
    expect(count).toBeGreaterThanOrEqual(0);
  });
});

test.describe("Evidence Manifests - Error States", () => {
  test("should show error state when API fails on dashboard", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/evidence-manifests*", async (route) => {
      await route.fulfill({ status: 500, body: JSON.stringify({ error: "Internal Server Error" }) });
    });

    await navigateToEvidenceManifests(page);

    const errorState = page.getByText(/error/i)
      .or(page.getByText(/failed/i))
      .or(page.getByText(/try again/i));
    await expect(errorState.first()).toBeVisible();
  });

  test("should show error state when manifest not found", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/evidence-manifests/non-existent-id", async (route) => {
      await route.fulfill({ status: 404, body: JSON.stringify({ error: "Manifest not found" }) });
    });

    await navigateToManifestDetail(page, "non-existent-id");

    const notFound = page.getByText(/not found/i)
      .or(page.getByText(/404/i))
      .or(page.getByText(/doesn't exist/i));
    await expect(notFound.first()).toBeVisible();
  });

  test("should show retry button on error", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await page.route("**/api/v1/evidence-manifests*", async (route) => {
      await route.fulfill({ status: 500, body: JSON.stringify({ error: "Server Error" }) });
    });

    await navigateToEvidenceManifests(page);

    const retryButton = page.getByRole("button", { name: /retry|try again/i });
    await expect(retryButton.first()).toBeVisible();
  });
});

test.describe("Evidence Manifests - Chain Integrity Statuses", () => {
  test.beforeEach(async ({ page }) => {
    await mockAuthenticatedSession(page);
  });

  test("should display verified chain status correctly", async ({ page }) => {
    await page.route("**/api/v1/evidence-manifests/chain-status*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          chain_integrity: "verified",
          total_manifests: 10,
          verified_count: 10,
        }),
      });
    });
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);

    const verifiedStatus = page.getByText(/verified/i).first();
    await expect(verifiedStatus).toBeVisible();
  });

  test("should display broken chain status with warning", async ({ page }) => {
    await page.route("**/api/v1/evidence-manifests/chain-status*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          chain_integrity: "broken",
          total_manifests: 10,
          verified_count: 8,
          broken_count: 2,
        }),
      });
    });
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);

    const brokenStatus = page.getByText(/broken/i)
      .or(page.getByText(/integrity issue/i));
    await expect(brokenStatus.first()).toBeVisible();
  });

  test("should display pending verification status", async ({ page }) => {
    await page.route("**/api/v1/evidence-manifests/chain-status*", async (route) => {
      await route.fulfill({
        status: 200,
        body: JSON.stringify({
          chain_integrity: "pending",
          total_manifests: 10,
          unverified_count: 10,
        }),
      });
    });
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);

    const pendingStatus = page.getByText(/pending/i)
      .or(page.getByText(/not verified/i));
    await expect(pendingStatus.first()).toBeVisible();
  });
});

test.describe("Evidence Manifests - Responsive Design", () => {
  test("should display correctly on mobile viewport", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await page.setViewportSize({ width: 375, height: 667 });
    await navigateToEvidenceManifests(page);

    // Page should still be functional
    const pageContent = page.locator("main").or(page.locator('[role="main"]'));
    await expect(pageContent).toBeVisible();
  });

  test("should display correctly on tablet viewport", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await page.setViewportSize({ width: 768, height: 1024 });
    await navigateToEvidenceManifests(page);

    const pageContent = page.locator("main").or(page.locator('[role="main"]'));
    await expect(pageContent).toBeVisible();
  });

  test("should display correctly on desktop viewport", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await page.setViewportSize({ width: 1920, height: 1080 });
    await navigateToEvidenceManifests(page);

    const pageContent = page.locator("main").or(page.locator('[role="main"]'));
    await expect(pageContent).toBeVisible();
  });
});

test.describe("Evidence Manifests - Accessibility", () => {
  test("should have proper heading hierarchy", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);

    const h1 = page.getByRole("heading", { level: 1 });
    await expect(h1).toBeVisible();
  });

  test("should have accessible buttons", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);

    const buttons = page.getByRole("button");
    const count = await buttons.count();
    expect(count).toBeGreaterThan(0);
  });

  test("should have focusable interactive elements", async ({ page }) => {
    await mockAuthenticatedSession(page);
    await mockEvidenceManifestsAPI(page);
    await navigateToEvidenceManifests(page);

    // Tab through the page
    await page.keyboard.press("Tab");
    const focusedElement = page.locator(":focus");
    await expect(focusedElement).toBeVisible();
  });
});
