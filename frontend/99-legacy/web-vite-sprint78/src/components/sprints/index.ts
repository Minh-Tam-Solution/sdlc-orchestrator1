/**
 * =========================================================================
 * Sprint Components Index
 * SDLC Orchestrator - Sprint 78 Day 5
 *
 * Version: 1.3.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 78 Frontend Components
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * Export all sprint-related components for easy imports
 *
 * Sprint 77 Additions:
 * - SprintBurndownChart: Burndown visualization
 * - SprintForecastCard: Completion probability
 * - SprintRetrospectivePanel: Auto-retrospective display
 * - SprintAnalyticsTab: Container for analytics
 *
 * Sprint 78 Additions:
 * - SprintDependencyGraph: Cross-project dependency visualization
 * - ResourceAllocationHeatmap: Team capacity heatmap
 * - SprintTemplateSelector: Template selection and application
 * - SprintRetroComparison: Sprint-over-sprint comparison
 * =========================================================================
 */

export { default as CreateSprintDialog } from './CreateSprintDialog';
export { default as SprintGatePanel } from './SprintGatePanel';
export { default as SprintBacklogList } from './SprintBacklogList';
export { default as BacklogKanbanBoard } from './BacklogKanbanBoard';

// Sprint 77: Analytics Components
export { default as SprintBurndownChart } from './SprintBurndownChart';
export { default as SprintForecastCard } from './SprintForecastCard';
export { default as SprintRetrospectivePanel } from './SprintRetrospectivePanel';
export { default as SprintAnalyticsTab } from './SprintAnalyticsTab';

// Sprint 78: Cross-Project & Templates Components
export { default as SprintDependencyGraph } from './SprintDependencyGraph';
export { default as ResourceAllocationHeatmap } from './ResourceAllocationHeatmap';
export { default as SprintTemplateSelector } from './SprintTemplateSelector';
export { default as SprintRetroComparison } from './SprintRetroComparison';
