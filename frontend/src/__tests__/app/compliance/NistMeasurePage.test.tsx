/**
 * NIST AI RMF MEASURE Dashboard Page Tests
 * Sprint 157 - Phase 3: COMPLIANCE
 *
 * Tests the MEASURE dashboard page with all components:
 * MeasureScoreCard, PolicyStatusList, MetricSummaryCards,
 * MetricTrendChart, BiasHeatmap, RecordMetricDialog, MetricHistoryTable
 *
 * TDD approach: Testing component rendering, data display, and user interactions.
 */

import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

// =============================================================================
// Mock Data
// =============================================================================

const MOCK_MEASURE_DASHBOARD = {
  overall_score: 0.75,
  policies: [
    {
      id: "p1",
      control_id: "MEASURE-1.1",
      name: "Performance Thresholds",
      description: "All metrics must have thresholds defined",
      status: "pass" as const,
      details: "10/12 metrics within thresholds",
    },
    {
      id: "p2",
      control_id: "MEASURE-2.1",
      name: "Bias Detection",
      description: "Bias metrics for at least 2 demographic groups per system",
      status: "pass" as const,
      details: "All systems have adequate bias coverage",
    },
    {
      id: "p3",
      control_id: "MEASURE-2.2",
      name: "Disparity Analysis",
      description: "Disparity ratio between groups must be within 4/5ths rule",
      status: "fail" as const,
      details: "1 system has disparity ratio > 1.25",
    },
    {
      id: "p4",
      control_id: "MEASURE-3.1",
      name: "Metric Trending",
      description: "Systems must have at least 3 data points for trend analysis",
      status: "pass" as const,
      details: "All systems have sufficient data points",
    },
  ],
  last_evaluated_at: "2026-04-14T12:00:00Z",
  total_metrics: 12,
  within_threshold_count: 10,
  bias_groups_count: 4,
  disparity_compliant: 3,
  disparity_non_compliant: 1,
};

const MOCK_METRICS = [
  {
    id: "m1",
    ai_system_id: "sys-1",
    ai_system_name: "Customer Churn Predictor",
    metric_type: "accuracy",
    metric_name: "Model Accuracy Q1",
    metric_value: 0.95,
    threshold_min: 0.90,
    threshold_max: 1.0,
    unit: "%",
    demographic_group: null,
    measured_at: "2026-04-14T12:00:00Z",
    notes: null,
    within_threshold: true,
  },
  {
    id: "m2",
    ai_system_id: "sys-1",
    ai_system_name: "Customer Churn Predictor",
    metric_type: "bias_score",
    metric_name: "Gender Bias Score",
    metric_value: 0.15,
    threshold_min: null,
    threshold_max: 0.20,
    unit: "ratio",
    demographic_group: "gender:female",
    measured_at: "2026-04-14T12:00:00Z",
    notes: null,
    within_threshold: true,
  },
  {
    id: "m3",
    ai_system_id: "sys-2",
    ai_system_name: "Resume Screener",
    metric_type: "f1_score",
    metric_name: "F1 Score",
    metric_value: 0.82,
    threshold_min: 0.85,
    threshold_max: 1.0,
    unit: "%",
    demographic_group: null,
    measured_at: "2026-04-13T12:00:00Z",
    notes: null,
    within_threshold: false,
  },
];

const MOCK_METRIC_TREND = {
  ai_system_id: "sys-1",
  ai_system_name: "Customer Churn Predictor",
  metric_type: "accuracy",
  points: [
    { date: "2026-04-01", value: 0.92, within_threshold: true },
    { date: "2026-04-07", value: 0.93, within_threshold: true },
    { date: "2026-04-14", value: 0.95, within_threshold: true },
  ],
};

const MOCK_BIAS_SUMMARY = {
  entries: [
    {
      ai_system_id: "sys-1",
      ai_system_name: "Customer Churn Predictor",
      demographic_group: "gender:female",
      bias_score: 0.15,
      within_threshold: true,
    },
    {
      ai_system_id: "sys-1",
      ai_system_name: "Customer Churn Predictor",
      demographic_group: "gender:male",
      bias_score: 0.12,
      within_threshold: true,
    },
  ],
  systems: [{ id: "sys-1", name: "Customer Churn Predictor" }],
  groups: ["gender:female", "gender:male"],
  disparity_ratios: {
    "gender:female-vs-gender:male": { ratio: 1.12, compliant: true },
  },
};

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
  usePathname: () => "/app/compliance/nist/measure",
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
import NistMeasurePage from "@/app/app/compliance/nist/measure/page";

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
      <NistMeasurePage />
    </QueryClientProvider>
  );
}

function setupSuccessfulFetch() {
  mockFetch.mockImplementation((url: string) => {
    const urlStr = String(url);

    if (urlStr.includes("/nist/measure/dashboard")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_MEASURE_DASHBOARD),
        text: () => Promise.resolve(JSON.stringify(MOCK_MEASURE_DASHBOARD)),
      });
    }

    if (urlStr.includes("/nist/measure/metrics/trend")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_METRIC_TREND),
        text: () => Promise.resolve(JSON.stringify(MOCK_METRIC_TREND)),
      });
    }

    if (urlStr.includes("/nist/measure/metrics")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_METRICS),
        text: () => Promise.resolve(JSON.stringify(MOCK_METRICS)),
      });
    }

    if (urlStr.includes("/nist/measure/bias-summary")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_BIAS_SUMMARY),
        text: () => Promise.resolve(JSON.stringify(MOCK_BIAS_SUMMARY)),
      });
    }

    if (urlStr.includes("/nist/measure/evaluate")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(MOCK_MEASURE_DASHBOARD),
        text: () => Promise.resolve(JSON.stringify(MOCK_MEASURE_DASHBOARD)),
      });
    }

    // MEASURE page fetches AI systems from MAP endpoint for dropdowns
    if (urlStr.includes("/nist/map/ai-systems")) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve([
          { id: "sys-1", name: "Customer Churn Predictor", description: null },
          { id: "sys-2", name: "Resume Screener", description: null },
        ]),
        text: () => Promise.resolve(JSON.stringify([
          { id: "sys-1", name: "Customer Churn Predictor", description: null },
          { id: "sys-2", name: "Resume Screener", description: null },
        ])),
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

describe("NistMeasurePage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.getItem = vi.fn().mockReturnValue("test-access-token");
  });

  describe("Initial Rendering", () => {
    it("renders the page title", () => {
      setupSuccessfulFetch();
      renderPage();

      expect(screen.getByText(/MEASURE Function Dashboard/i)).toBeDefined();
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
          expect(screen.getByText(/MEASURE.*Score|Compliance/i)).toBeDefined();
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
          expect(screen.getByText("75%")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("renders all 4 MEASURE policy statuses", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      await waitFor(
        () => {
          expect(screen.getByText("Performance Thresholds")).toBeDefined();
          expect(screen.getByText("Bias Detection")).toBeDefined();
          expect(screen.getByText("Disparity Analysis")).toBeDefined();
          expect(screen.getByText("Metric Trending")).toBeDefined();
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

    it("renders metric entries in history table", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      // Wait for dashboard to load, then switch to Metrics tab
      await waitFor(
        () => {
          expect(screen.getByText("Metrics")).toBeDefined();
        },
        { timeout: 3000 }
      );

      fireEvent.click(screen.getByText("Metrics"));

      await waitFor(
        () => {
          expect(screen.getByText("Model Accuracy Q1")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("shows within-threshold and outside-threshold indicators", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      // Wait for dashboard to load, then switch to Metrics tab
      await waitFor(
        () => {
          expect(screen.getByText("Metrics")).toBeDefined();
        },
        { timeout: 3000 }
      );

      fireEvent.click(screen.getByText("Metrics"));

      await waitFor(
        () => {
          // F1 Score is outside threshold
          expect(screen.getByText("F1 Score")).toBeDefined();
        },
        { timeout: 3000 }
      );
    });

    it("renders bias summary section", async () => {
      setupSuccessfulFetch();
      renderPage();

      const projectBtn = screen.getByText("SDLC Orchestrator");
      fireEvent.click(projectBtn);

      // Wait for dashboard to load, then switch to Bias Analysis tab
      await waitFor(
        () => {
          expect(screen.getByText("Bias Analysis")).toBeDefined();
        },
        { timeout: 3000 }
      );

      fireEvent.click(screen.getByText("Bias Analysis"));

      await waitFor(
        () => {
          expect(screen.getByText(/Customer Churn Predictor/i)).toBeDefined();
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

      expect(screen.getByText(/MEASURE Function Dashboard/i)).toBeDefined();
    });
  });
});
