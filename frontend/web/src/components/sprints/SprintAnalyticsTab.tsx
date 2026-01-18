/**
 * =========================================================================
 * SprintAnalyticsTab - Sprint Analytics Container
 * SDLC Orchestrator - Sprint 77 Day 5
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 77 Frontend & Completion
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Container for sprint analytics components
 * - Combines burndown, forecast, and retrospective views
 * - Responsive layout for all screen sizes
 *
 * References:
 * - SprintBurndownChart.tsx
 * - SprintForecastCard.tsx
 * - SprintRetrospectivePanel.tsx
 * =========================================================================
 */

import SprintBurndownChart from "./SprintBurndownChart";
import SprintForecastCard from "./SprintForecastCard";
import SprintRetrospectivePanel from "./SprintRetrospectivePanel";

/** Props for SprintAnalyticsTab */
interface SprintAnalyticsTabProps {
  /** Sprint ID to show analytics for */
  sprintId: string;
  /** Sprint status for conditional rendering */
  sprintStatus: string;
}

/**
 * Sprint Analytics Tab Component
 * Contains all analytics visualizations for a sprint
 */
export default function SprintAnalyticsTab({
  sprintId,
  sprintStatus,
}: SprintAnalyticsTabProps) {
  return (
    <div className="space-y-6">
      {/* Row 1: Burndown + Forecast */}
      <div className="grid gap-6 lg:grid-cols-2">
        <SprintBurndownChart sprintId={sprintId} height={280} />
        <SprintForecastCard sprintId={sprintId} />
      </div>

      {/* Row 2: Retrospective (only for completed/closed sprints) */}
      {(sprintStatus === "completed" || sprintStatus === "closed") && (
        <SprintRetrospectivePanel sprintId={sprintId} />
      )}

      {/* Message for planning/in_progress sprints */}
      {sprintStatus === "planning" && (
        <div className="p-6 text-center text-muted-foreground bg-muted rounded-lg">
          <p className="text-sm">
            Sprint analytics will be available once the sprint starts.
          </p>
          <p className="text-xs mt-1">
            Complete G-Sprint gate to start the sprint.
          </p>
        </div>
      )}

      {sprintStatus === "in_progress" && (
        <div className="p-6 text-center text-muted-foreground bg-muted rounded-lg">
          <p className="text-sm">
            Retrospective will be generated when the sprint is completed.
          </p>
          <p className="text-xs mt-1">
            Complete all P0 items and close the sprint to generate retrospective.
          </p>
        </div>
      )}
    </div>
  );
}
