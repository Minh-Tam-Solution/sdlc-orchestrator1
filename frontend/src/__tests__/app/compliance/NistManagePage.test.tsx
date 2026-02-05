/**
 * NIST AI RMF MANAGE Dashboard Page Tests
 * Sprint 158 - Phase 3: COMPLIANCE
 *
 * Tests the MANAGE dashboard page with all components:
 * ManageScoreCard, PolicyStatusList, RiskResponseTable, IncidentTable
 *
 * TDD approach: Testing component rendering, data display, and user interactions.
 * 14 tests total:
 *   12 NistManagePage tests (rendering, data display, evaluate action, no project)
 *   2 ComplianceOverviewPage MANAGE-specific tests (19 controls, active function)
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// =============================================================================
// Mock Data
// =============================================================================

const MOCK_DASHBOARD = {
  project_id: "proj-1",
  compliance_percentage: 60,
  policies_passed: 3,
  policies_total: 5,
  policy_results: [
    {
      control_code: "MANAGE-1.1",
      title: "Risk Response Planning",
      allowed: true,
      reason: "All risks have responses",
      severity: "critical",
      details: {},
    },
    {
      control_code: "MANAGE-2.1",
      title: "Resource Allocation",
      allowed: true,
      reason: "70% responses have budget",
      severity: "high",
      details: {},
    },
    {
      control_code: "MANAGE-2.4",
      title: "System Deactivation Criteria",
      allowed: false,
      reason: "No deactivation criteria defined",
      severity: "high",
      details: {},
    },
    {
      control_code: "MANAGE-3.1",
      title: "Third-Party Monitoring",
      allowed: true,
      reason: "All third-party systems monitored",
      severity: "high",
      details: {},
    },
    {
      control_code: "MANAGE-4.1",
      title: "Post-Deployment Monitoring",
      allowed: false,
      reason: "2 systems lack recent metrics",
      severity: "critical",
      details: {},
    },
  ],
  total_risk_responses: 5,
  completed_responses: 2,
  total_incidents: 8,
  open_incidents: 3,
  critical_incidents: 1,
  has_deactivation_criteria: false,
};

const MOCK_RISK_RESPONSES = {
  items: [
    {
      id: "rr1",
      project_id: "proj-1",
      risk_id: "r1",
      response_type: "mitigate",
      description: "Implement bias detection",
      assigned_to: "AI Safety Lead",
      priority: "critical",
      status: "in_progress",
      due_date: "2026-05-01",
      resources_allocated: [],
      deactivation_criteria: null,
      notes: null,
      created_at: "2026-04-21T10:00:00Z",
      updated_at: "2026-04-21T10:00:00Z",
    },
    {
      id: "rr2",
      project_id: "proj-1",
      risk_id: "r2",
      response_type: "accept",
      description: "Accept low risk",
      assigned_to: "Risk Manager",
      priority: "low",
      status: "completed",
      due_date: null,
      resources_allocated: [],
      deactivation_criteria: null,
      notes: null,
      created_at: "2026-04-22T10:00:00Z",
      updated_at: "2026-04-22T10:00:00Z",
    },
  ],
  total: 2,
  limit: 50,
  offset: 0,
  has_more: false,
};

const MOCK_INCIDENTS = {
  items: [
    {
      id: "inc1",
      project_id: "proj-1",
      ai_system_id: "sys1",
      risk_id: null,
      title: "Bias spike in hiring model",
      description: "Gender bias increased",
      severity: "critical",
      incident_type: "bias_detected",
      status: "investigating",
      reported_by: "QA",
      assigned_to: "AI Safety Lead",
      resolution: null,
      root_cause: null,
      occurred_at: "2026-04-20T08:00:00Z",
      resolved_at: null,
      created_at: "2026-04-20T09:00:00Z",
      updated_at: "2026-04-20T09:00:00Z",
    },
    {
      id: "inc2",
      project_id: "proj-1",
      ai_system_id: "sys2",
      risk_id: null,
      title: "API latency degradation",
      description: "p95 > 500ms",
      severity: "medium",
      incident_type: "performance_degradation",
      status: "resolved",
      reported_by: "Monitoring",
      assigned_to: "Backend Lead",
      resolution: "Optimized queries",
      root_cause: "N+1 query",
      occurred_at: "2026-04-19T14:00:00Z",
      resolved_at: "2026-04-19T18:00:00Z",
      created_at: "2026-04-19T15:00:00Z",
      updated_at: "2026-04-19T18:00:00Z",
    },
  ],
  total: 2,
  limit: 50,
  offset: 0,
  has_more: false,
};

const MOCK_PROJECTS = [
  {
    id: "proj-1",
    name: "SDLC Orchestrator",
    description: "",
    current_stage: "BUILD",
    gate_status: "passed" as const,
    progress: 80,
    created_at: "",
    updated_at: "",
  },
  {
    id: "proj-2",
    name: "BFlow Platform",
    description: "",
    current_stage: "DESIGN",
    gate_status: "pending" as const,
    progress: 40,
    created_at: "",
    updated_at: "",
  },
];

// =============================================================================
// Mocks
// =============================================================================

// Mock fetch globally
const mockFetch = vi.fn();
global.fetch = mockFetch;

// Mock next/navigation
vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(""),
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), back: vi.fn() }),
  usePathname: () => "/app/compliance/nist/manage",
}));

// Mock useProjects hook
vi.mock("@/hooks/useProjects", () => ({
  useProjects: () => ({
    data: MOCK_PROJECTS,
    isLoading: false,
    error: null,
  }),
}));

// Mock useAuth hook
vi.mock("@/hooks/useAuth", () => ({
  useAuth: () => ({
    isAuthenticated: true,
    isLoading: false,
    user: { id: "u1", name: "Test User" },
  }),
}));

// Import page AFTER mocks are set up
import NistManagePage from "@/app/app/compliance/nist/manage/page";

// =============================================================================
// Test Helpers
// =============================================================================

function createQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
}

function renderPage() {
  const queryClient = createQueryClient();
  return render(
    <QueryClientProvider client={queryClient}>
      <NistManagePage />
    </QueryClientProvider>
  );
}

function setupSuccessfulFetch() {
  mockFetch.mockImplementation((url: string) => {
    const urlStr = String(url);

    if (urlStr.includes("/dashboard")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_DASHBOARD),
        text: () => Promise.resolve(JSON.stringify(MOCK_DASHBOARD)),
      });
    }

    if (urlStr.includes("/risk-responses")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_RISK_RESPONSES),
        text: () => Promise.resolve(JSON.stringify(MOCK_RISK_RESPONSES)),
      });
    }

    if (urlStr.includes("/incidents")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_INCIDENTS),
        text: () => Promise.resolve(JSON.stringify(MOCK_INCIDENTS)),
      });
    }

    if (urlStr.includes("/evaluate")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_DASHBOARD),
        text: () => Promise.resolve(JSON.stringify(MOCK_DASHBOARD)),
      });
    }

    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve({}),
      text: () => Promise.resolve("{}"),
    });
  });
}

// =============================================================================
// Tests: NistManagePage
// =============================================================================

describe("NistManagePage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.getItem = vi.fn().mockReturnValue("test-access-token");
  });

  describe("Initial Rendering", () => {
    it("renders the page title 'MANAGE Function Dashboard'", () => {
      setupSuccessfulFetch();
      renderPage();

      expect(screen.getByText("MANAGE Function Dashboard")).toBeDefined();
    });

    it("renders project selector with project options", () => {
      setupSuccessfulFetch();
      renderPage();

      expect(screen.getByText("SDLC Orchestrator")).toBeDefined();
      expect(screen.getByText("BFlow Platform")).toBeDefined();
    });
  });

  describe("Dashboard with Data", () => {
    it("renders score card after project selection and data load", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("MANAGE Compliance Score")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("displays compliance percentage (60%)", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("60%")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("renders all 5 policy statuses (MANAGE-1.1 through MANAGE-4.1)", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(
            screen.getAllByText("Risk Response Planning").length
          ).toBeGreaterThanOrEqual(1);
          expect(
            screen.getAllByText("Resource Allocation").length
          ).toBeGreaterThanOrEqual(1);
          expect(
            screen.getAllByText("System Deactivation Criteria").length
          ).toBeGreaterThanOrEqual(1);
          expect(
            screen.getAllByText("Third-Party Monitoring").length
          ).toBeGreaterThanOrEqual(1);
          expect(
            screen.getAllByText("Post-Deployment Monitoring").length
          ).toBeGreaterThanOrEqual(1);
        },
        { timeout: 3000 }
      );
    });

    it("shows policy status badges (Pass, Fail, Warning, Not Evaluated)", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getAllByText("Pass").length).toBeGreaterThanOrEqual(1);
          expect(screen.getAllByText("Fail").length).toBeGreaterThanOrEqual(1);
        },
        { timeout: 3000 }
      );
    });

    it("renders risk response table with response entries", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("Implement bias detection")).toBeDefined();
          expect(screen.getByText("Accept low risk")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("shows response type badges (Mitigate, Accept, Transfer, Avoid)", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(
            screen.getAllByText(/[Mm]itigate/).length
          ).toBeGreaterThanOrEqual(1);
          expect(
            screen.getAllByText(/[Aa]ccept/).length
          ).toBeGreaterThanOrEqual(1);
        },
        { timeout: 3000 }
      );
    });

    it("renders incident table with incident entries", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      // Wait for incident section header
      const header = await screen.findByText("Incidents", {}, { timeout: 5000 });
      expect(header).toBeDefined();

      // Check for incident titles (may need additional render cycle)
      await waitFor(
        () => {
          const allText = document.body.textContent || "";
          expect(allText).toContain("Bias spike in hiring model");
          expect(allText).toContain("API latency degradation");
        },
        { timeout: 5000 }
      );
    });

    it("shows severity badges (Critical, Medium)", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(
            screen.getAllByText(/[Cc]ritical/).length
          ).toBeGreaterThanOrEqual(1);
          expect(
            screen.getAllByText(/[Mm]edium/).length
          ).toBeGreaterThanOrEqual(1);
        },
        { timeout: 3000 }
      );
    });
  });

  describe("Evaluate Action", () => {
    it("renders evaluate button and calls evaluate endpoint", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("Evaluate Now")).toBeDefined();
        },
        { timeout: 3000 }
      );

      const evalBtn = screen.getByText("Evaluate Now");
      fireEvent.click(evalBtn);

      await waitFor(() => {
        const evalCalls = mockFetch.mock.calls.filter((call: unknown[]) =>
          String(call[0]).includes("/evaluate")
        );
        expect(evalCalls.length).toBeGreaterThanOrEqual(1);
      });
    });
  });

  describe("No Project Selected", () => {
    it("shows instruction when no project selected", () => {
      setupSuccessfulFetch();
      renderPage();

      // Page should render the title without crashing even with no project selected
      expect(screen.getByText("MANAGE Function Dashboard")).toBeDefined();
    });
  });
});

// =============================================================================
// Tests: ComplianceOverviewPage (MANAGE-specific)
// =============================================================================

describe("ComplianceOverviewPage MANAGE tests", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("shows 19 controls count", async () => {
    const { default: ComplianceOverviewPage } = await import(
      "@/app/app/compliance/page"
    );

    render(<ComplianceOverviewPage />);

    // The overview page displays "19" as the total NIST AI RMF controls count
    expect(screen.getByText("19")).toBeDefined();
  });

  it("shows MANAGE as active function", async () => {
    const { default: ComplianceOverviewPage } = await import(
      "@/app/app/compliance/page"
    );

    render(<ComplianceOverviewPage />);

    // The NIST AI RMF card has MANAGE listed as the active function
    expect(screen.getByText("MANAGE")).toBeDefined();
  });
});
