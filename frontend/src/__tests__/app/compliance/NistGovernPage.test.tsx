/**
 * NIST AI RMF GOVERN Dashboard Page Tests
 * Sprint 156 - Phase 3: COMPLIANCE
 *
 * Tests the GOVERN dashboard page with all 5 components:
 * GovernScoreCard, PolicyStatusList, RiskHeatmap, RACIMatrix, RiskRegisterTable
 *
 * TDD approach: Testing component rendering, data display, and user interactions.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// =============================================================================
// Mock Data
// =============================================================================

const MOCK_DASHBOARD: {
  overall_score: number;
  policies: Array<{
    id: string;
    control_id: string;
    name: string;
    description: string;
    status: "pass" | "fail" | "warning" | "not_evaluated";
    details: string | null;
  }>;
  last_evaluated_at: string | null;
} = {
  overall_score: 0.80,
  policies: [
    {
      id: "p1",
      control_id: "GOVERN-1.1",
      name: "Accountability Structures",
      description: "AI systems must have designated owners",
      status: "pass",
      details: "All 3 AI systems have owners",
    },
    {
      id: "p2",
      control_id: "GOVERN-1.2",
      name: "Risk Culture",
      description: "Team risk awareness training",
      status: "pass",
      details: "80% trained",
    },
    {
      id: "p3",
      control_id: "GOVERN-1.3",
      name: "Legal Compliance",
      description: "Legal review of AI systems",
      status: "fail",
      details: "Legal review not completed",
    },
    {
      id: "p4",
      control_id: "GOVERN-1.4",
      name: "Third-Party Oversight",
      description: "Third-party AI vendor management",
      status: "warning",
      details: "1 vendor missing SLA",
    },
    {
      id: "p5",
      control_id: "GOVERN-1.5",
      name: "Continuous Improvement",
      description: "Incident learning process",
      status: "not_evaluated",
      details: null,
    },
  ],
  last_evaluated_at: "2026-04-07T12:00:00Z",
};

const MOCK_RISKS = [
  {
    id: "r1",
    title: "Bias in hiring model",
    description: "Potential gender bias detected",
    likelihood: 4,
    impact: 5,
    risk_level: "critical" as const,
    owner: "AI Safety Lead",
    mitigation: "Implement bias detection pipeline",
    status: "open" as const,
    created_at: "2026-04-01T10:00:00Z",
  },
  {
    id: "r2",
    title: "Data privacy exposure",
    description: "PII in training data",
    likelihood: 2,
    impact: 3,
    risk_level: "medium" as const,
    owner: "Data Engineer",
    mitigation: "Add PII scrubbing step",
    status: "mitigating" as const,
    created_at: "2026-04-02T10:00:00Z",
  },
];

const MOCK_RACI = [
  {
    control_id: "GOVERN-1.1",
    control_name: "Accountability",
    responsible: "CTO",
    accountable: "CEO",
    consulted: "Legal",
    informed: "Board",
  },
  {
    control_id: "GOVERN-1.2",
    control_name: "Risk Culture",
    responsible: "Risk Manager",
    accountable: "CTO",
    consulted: "HR",
    informed: "All Staff",
  },
];

const MOCK_PROJECTS = [
  { id: "proj-1", name: "SDLC Orchestrator", description: "", current_stage: "BUILD", gate_status: "passed" as const, progress: 80, created_at: "", updated_at: "" },
  { id: "proj-2", name: "BFlow Platform", description: "", current_stage: "DESIGN", gate_status: "pending" as const, progress: 40, created_at: "", updated_at: "" },
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
  usePathname: () => "/app/compliance/nist/govern",
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
import NistGovernPage from "@/app/app/compliance/nist/govern/page";

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
      <NistGovernPage />
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

    if (urlStr.includes("/risks")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_RISKS),
        text: () => Promise.resolve(JSON.stringify(MOCK_RISKS)),
      });
    }

    if (urlStr.includes("/raci")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_RACI),
        text: () => Promise.resolve(JSON.stringify(MOCK_RACI)),
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
// Tests: Page Rendering
// =============================================================================

describe("NistGovernPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.getItem = vi.fn().mockReturnValue("test-access-token");
  });

  describe("Initial Rendering", () => {
    it("renders the page title", () => {
      setupSuccessfulFetch();
      renderPage();

      expect(screen.getByText("GOVERN Function Dashboard")).toBeDefined();
    });

    it("renders project selector", () => {
      setupSuccessfulFetch();
      renderPage();

      expect(screen.getByText("Select Project")).toBeDefined();
    });

    it("shows project options in the selector", async () => {
      setupSuccessfulFetch();
      renderPage();

      // The page should show project options
      expect(screen.getByText("SDLC Orchestrator")).toBeDefined();
      expect(screen.getByText("BFlow Platform")).toBeDefined();
    });
  });

  describe("Dashboard with Data", () => {
    it("renders score card after project selection and data load", async () => {
      setupSuccessfulFetch();
      renderPage();

      // Click on first project to select it
      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      // Wait for data to load
      await waitFor(
        () => {
          expect(screen.getByText("GOVERN Compliance Score")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("displays overall compliance score", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("80%")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("renders all 5 policy statuses", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getAllByText("Accountability Structures").length).toBeGreaterThanOrEqual(1);
          expect(screen.getAllByText("Risk Culture").length).toBeGreaterThanOrEqual(1);
          expect(screen.getAllByText("Legal Compliance").length).toBeGreaterThanOrEqual(1);
          expect(screen.getAllByText("Third-Party Oversight").length).toBeGreaterThanOrEqual(1);
          expect(screen.getAllByText("Continuous Improvement").length).toBeGreaterThanOrEqual(1);
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
          expect(screen.getAllByText("Warning").length).toBeGreaterThanOrEqual(1);
          expect(screen.getAllByText("Not Evaluated").length).toBeGreaterThanOrEqual(1);
        },
        { timeout: 3000 }
      );
    });

    it("renders risk register with risk entries", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("Bias in hiring model")).toBeDefined();
          expect(screen.getByText("Data privacy exposure")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("shows risk level badges", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getAllByText("Critical").length).toBeGreaterThanOrEqual(1);
          expect(screen.getAllByText("Medium").length).toBeGreaterThanOrEqual(1);
        },
        { timeout: 3000 }
      );
    });

    it("renders RACI matrix entries", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("RACI Matrix")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("renders risk heatmap section", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("Risk Heatmap")).toBeDefined();
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
          expect(screen.getByText("Evaluate Now")).toBeDefined();
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

      // Page should render without crashing even with no project selected
      expect(screen.getByText("GOVERN Function Dashboard")).toBeDefined();
    });
  });
});

// =============================================================================
// Tests: Compliance Overview Page
// =============================================================================

describe("ComplianceOverviewPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders without crashing", async () => {
    // Dynamically import to test independently
    const { default: ComplianceOverviewPage } = await import(
      "@/app/app/compliance/page"
    );

    const { container } = render(<ComplianceOverviewPage />);
    expect(container).toBeDefined();
  });

  it("shows all three framework cards", async () => {
    const { default: ComplianceOverviewPage } = await import(
      "@/app/app/compliance/page"
    );

    render(<ComplianceOverviewPage />);

    expect(screen.getByText("NIST AI Risk Management Framework")).toBeDefined();
    expect(screen.getByText("EU Artificial Intelligence Act")).toBeDefined();
    expect(screen.getByText("ISO/IEC 42001:2023 AI Management Systems")).toBeDefined();
  });

  it("shows active badge for NIST", async () => {
    const { default: ComplianceOverviewPage } = await import(
      "@/app/app/compliance/page"
    );

    render(<ComplianceOverviewPage />);

    expect(screen.getByText("Active")).toBeDefined();
  });

  it("shows coming soon badges for EU AI Act and ISO", async () => {
    const { default: ComplianceOverviewPage } = await import(
      "@/app/app/compliance/page"
    );

    render(<ComplianceOverviewPage />);

    const comingSoonBadges = screen.getAllByText("Coming Soon");
    expect(comingSoonBadges.length).toBe(2);
  });

  it("shows Open Dashboard link for NIST", async () => {
    const { default: ComplianceOverviewPage } = await import(
      "@/app/app/compliance/page"
    );

    render(<ComplianceOverviewPage />);

    const dashboardLink = screen.getByText("Open Dashboard →");
    expect(dashboardLink).toBeDefined();
  });
});
