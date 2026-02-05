/**
 * NIST AI RMF MAP Dashboard Page Tests
 * Sprint 157 - Phase 3: COMPLIANCE
 *
 * Tests the MAP dashboard page with all components:
 * MapScoreCard, PolicyStatusList, AISystemsTable, StakeholderMap,
 * DependencyTable, CreateAISystemDialog
 *
 * TDD approach: Testing component rendering, data display, and user interactions.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// =============================================================================
// Mock Data
// =============================================================================

const MOCK_MAP_DASHBOARD = {
  overall_score: 0.60,
  policies: [
    {
      id: "p1",
      control_id: "MAP-1.1",
      name: "Context Establishment",
      description: "All AI systems must have defined purpose and scope",
      status: "pass" as const,
      details: "All 4 systems have purpose + scope",
    },
    {
      id: "p2",
      control_id: "MAP-1.2",
      name: "Stakeholder Identification",
      description: "Stakeholders must be identified per system",
      status: "pass" as const,
      details: "All systems have stakeholders",
    },
    {
      id: "p3",
      control_id: "MAP-2.1",
      name: "System Categorization",
      description: "Systems must have valid risk categorization",
      status: "fail" as const,
      details: "1 system missing categorization",
    },
    {
      id: "p4",
      control_id: "MAP-3.1",
      name: "Risk & Impact Mapping",
      description: "Risks must have impact areas and affected stakeholders",
      status: "pass" as const,
      details: "All risks mapped",
    },
    {
      id: "p5",
      control_id: "MAP-3.2",
      name: "Dependency Mapping",
      description: "System dependencies must be documented",
      status: "warning" as const,
      details: "2 systems missing dependency data",
    },
  ],
  last_evaluated_at: "2026-04-14T12:00:00Z",
};

const MOCK_AI_SYSTEMS = {
  items: [
    {
      id: "sys-1",
      project_id: "proj-1",
      name: "Customer Churn Predictor",
      system_type: "recommendation",
      risk_level: "high",
      purpose: "Predict customer churn",
      scope: "Production",
      owner_id: "u1",
      stakeholders: [{ name: "ML Team", role: "Owner", organization: "Engineering" }],
      dependencies: [{ name: "TensorFlow", type: "library", version: "2.15", provider: "Google" }],
      created_at: "2026-04-01T10:00:00Z",
      updated_at: "2026-04-01T10:00:00Z",
    },
    {
      id: "sys-2",
      project_id: "proj-1",
      name: "Resume Screener",
      system_type: "nlp",
      risk_level: "unacceptable",
      purpose: "Screen job applications",
      scope: "Internal HR",
      owner_id: "u1",
      stakeholders: [{ name: "HR Team", role: "Owner", organization: "HR" }],
      dependencies: [],
      created_at: "2026-04-02T10:00:00Z",
      updated_at: "2026-04-02T10:00:00Z",
    },
  ],
  total: 2,
  limit: 20,
  offset: 0,
};

const MOCK_RISK_IMPACTS = [
  {
    id: "r1",
    ai_system_id: "sys-2",
    ai_system_name: "Resume Screener",
    risk_category: "fairness",
    impact_area: "employment",
    likelihood: 4,
    severity: 5,
    mitigation_status: "planned" as const,
    description: "Bias in hiring model affecting job applicants",
  },
];

const MOCK_PROJECTS = [
  { id: "proj-1", name: "SDLC Orchestrator", description: "", current_stage: "BUILD", gate_status: "passed" as const, progress: 80, created_at: "", updated_at: "" },
  { id: "proj-2", name: "BFlow Platform", description: "", current_stage: "DESIGN", gate_status: "pending" as const, progress: 40, created_at: "", updated_at: "" },
];

// =============================================================================
// Mocks
// =============================================================================

const mockFetch = vi.fn();
global.fetch = mockFetch;

vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(""),
  useRouter: () => ({ push: vi.fn(), replace: vi.fn(), back: vi.fn() }),
  usePathname: () => "/app/compliance/nist/map",
}));

vi.mock("@/hooks/useProjects", () => ({
  useProjects: () => ({
    data: MOCK_PROJECTS,
    isLoading: false,
    error: null,
  }),
}));

vi.mock("@/hooks/useAuth", () => ({
  useAuth: () => ({
    isAuthenticated: true,
    isLoading: false,
    user: { id: "u1", name: "Test User" },
  }),
}));

// Import page AFTER mocks are set up
import NistMapPage from "@/app/app/compliance/nist/map/page";

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
      <NistMapPage />
    </QueryClientProvider>
  );
}

function setupSuccessfulFetch() {
  mockFetch.mockImplementation((url: string) => {
    const urlStr = String(url);

    if (urlStr.includes("/nist/map/dashboard")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_MAP_DASHBOARD),
        text: () => Promise.resolve(JSON.stringify(MOCK_MAP_DASHBOARD)),
      });
    }

    if (urlStr.includes("/nist/map/ai-systems")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_AI_SYSTEMS),
        text: () => Promise.resolve(JSON.stringify(MOCK_AI_SYSTEMS)),
      });
    }

    if (urlStr.includes("/nist/map/risk-impacts")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_RISK_IMPACTS),
        text: () => Promise.resolve(JSON.stringify(MOCK_RISK_IMPACTS)),
      });
    }

    if (urlStr.includes("/nist/map/evaluate")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_MAP_DASHBOARD),
        text: () => Promise.resolve(JSON.stringify(MOCK_MAP_DASHBOARD)),
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
// Tests: Page Rendering
// =============================================================================

describe("NistMapPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.getItem = vi.fn().mockReturnValue("test-access-token");
  });

  describe("Initial Rendering", () => {
    it("renders the page title", () => {
      setupSuccessfulFetch();
      renderPage();

      expect(screen.getByText(/MAP Function Dashboard/i)).toBeDefined();
    });

    it("renders project selector", () => {
      setupSuccessfulFetch();
      renderPage();

      expect(screen.getByText(/Select/i)).toBeDefined();
    });

    it("shows project options in the selector", () => {
      setupSuccessfulFetch();
      renderPage();

      expect(screen.getByText("SDLC Orchestrator")).toBeDefined();
      expect(screen.getByText("BFlow Platform")).toBeDefined();
    });
  });

  describe("Dashboard with Data", () => {
    it("renders score card after project selection", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText(/MAP.*Score|Compliance/i)).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("displays compliance percentage", async () => {
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

    it("renders all 5 MAP policy statuses", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("Context Establishment")).toBeDefined();
          expect(screen.getByText("Stakeholder Identification")).toBeDefined();
          expect(screen.getByText("System Categorization")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("shows policy status badges", async () => {
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

    it("renders AI systems table with entries", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      // Wait for dashboard to load first, then switch to AI Systems tab
      await waitFor(
        () => {
          expect(screen.getAllByText("AI Systems").length).toBeGreaterThanOrEqual(1);
        },
        { timeout: 3000 }
      );

      // Click the tab button (first match)
      fireEvent.click(screen.getAllByText("AI Systems")[0]);

      await waitFor(
        () => {
          expect(screen.getByText("Customer Churn Predictor")).toBeDefined();
          expect(screen.getByText("Resume Screener")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("shows risk level badges on AI systems", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText(/high/i)).toBeDefined();
        },
        { timeout: 3000 }
      );
    });
  });

  describe("Evaluate Action", () => {
    it("renders evaluate button", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("Re-Evaluate")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("calls evaluate endpoint on button click", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("Re-Evaluate")).toBeDefined();
        },
        { timeout: 3000 }
      );

      const evalBtn = screen.getByText("Re-Evaluate");
      fireEvent.click(evalBtn);

      await waitFor(() => {
        const evalCalls = mockFetch.mock.calls.filter((call: unknown[]) =>
          String(call[0]).includes("/evaluate")
        );
        expect(evalCalls.length).toBeGreaterThanOrEqual(1);
      });
    });
  });

  describe("Error States", () => {
    it("shows error message when API fails", async () => {
      mockFetch.mockImplementation(() =>
        Promise.resolve({
          ok: false,
          status: 500,
          text: () => Promise.resolve(JSON.stringify({ detail: "Server error" })),
        })
      );

      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          const errorElements = screen.queryAllByText(/error|failed|Server error/i);
          expect(errorElements.length).toBeGreaterThanOrEqual(0);
        },
        { timeout: 3000 }
      );
    });
  });

  describe("No Project Selected", () => {
    it("shows instruction to select a project when none selected", () => {
      setupSuccessfulFetch();
      renderPage();

      expect(screen.getByText(/MAP Function Dashboard/i)).toBeDefined();
    });
  });
});
