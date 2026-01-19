/**
 * =========================================================================
 * SprintTemplateSelector - Sprint Template Selection & Application
 * SDLC Orchestrator - Sprint 78 Day 5
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 78 Frontend Components
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - List available sprint templates
 * - Show template suggestions based on project context
 * - Apply template to create new sprint
 * - Preview template backlog structure
 *
 * References:
 * - backend/app/services/sprint_template_service.py
 * - docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
 * =========================================================================
 */

import { useState, useMemo } from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import {
  useSprintTemplates,
  useTemplateSuggestions,
  useApplyTemplate,
  SprintTemplate,
  TemplateSuggestion,
} from "@/hooks/usePlanning";
import {
  AlertTriangle,
  Calendar,
  CheckCircle2,
  Clock,
  Copy,
  FileText,
  Layers,
  ListChecks,
  Sparkles,
  Star,
  Target,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";

/** Props for SprintTemplateSelector */
interface SprintTemplateSelectorProps {
  /** Project ID to create sprint for */
  projectId: string;
  /** Team ID for filtering templates */
  teamId?: string;
  /** Optional phase ID for the new sprint */
  phaseId?: string;
  /** Callback when sprint is created */
  onSprintCreated?: (sprintId: string) => void;
}

/** Template type icons */
const TEMPLATE_ICONS: Record<string, React.ElementType> = {
  standard: Calendar,
  feature: Zap,
  bugfix: AlertTriangle,
  release: Target,
  custom: Layers,
};

/** Template type colors */
const TEMPLATE_COLORS: Record<string, string> = {
  standard: "bg-blue-100 text-blue-700 border-blue-300",
  feature: "bg-purple-100 text-purple-700 border-purple-300",
  bugfix: "bg-orange-100 text-orange-700 border-orange-300",
  release: "bg-green-100 text-green-700 border-green-300",
  custom: "bg-gray-100 text-gray-700 border-gray-300",
};

/**
 * Sprint Template Selector Component
 * Allows users to select and apply sprint templates
 */
export default function SprintTemplateSelector({
  projectId,
  teamId,
  phaseId,
  onSprintCreated,
}: SprintTemplateSelectorProps) {
  const { data: templates, isLoading: templatesLoading } =
    useSprintTemplates(teamId);
  const { data: suggestions, isLoading: suggestionsLoading } =
    useTemplateSuggestions(projectId);

  const [selectedTemplate, setSelectedTemplate] =
    useState<SprintTemplate | null>(null);
  const [isApplyDialogOpen, setIsApplyDialogOpen] = useState(false);

  // Sort templates: suggestions first, then by usage
  const sortedTemplates = useMemo(() => {
    if (!templates) return [];

    const suggestionIds = new Set(suggestions?.map((s) => s.template_id) || []);

    return [...templates].sort((a, b) => {
      // Suggested templates first
      const aIsSuggested = suggestionIds.has(a.id);
      const bIsSuggested = suggestionIds.has(b.id);
      if (aIsSuggested && !bIsSuggested) return -1;
      if (!aIsSuggested && bIsSuggested) return 1;

      // Default templates next
      if (a.is_default && !b.is_default) return -1;
      if (!a.is_default && b.is_default) return 1;

      // Then by usage count
      return b.usage_count - a.usage_count;
    });
  }, [templates, suggestions]);

  // Find suggestion data for a template
  const getSuggestion = (templateId: string): TemplateSuggestion | undefined => {
    return suggestions?.find((s) => s.template_id === templateId);
  };

  const isLoading = templatesLoading || suggestionsLoading;

  if (isLoading) {
    return <TemplateSelectorSkeleton />;
  }

  if (!templates || templates.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <Layers className="w-5 h-5 text-muted-foreground" />
            Sprint Templates
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground py-4 text-center">
            No sprint templates available. Create a template to get started.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-base flex items-center gap-2">
          <Layers className="w-5 h-5 text-purple-500" />
          Sprint Templates
        </CardTitle>
        <CardDescription>
          {templates.length} templates available
          {suggestions && suggestions.length > 0 && (
            <span className="ml-2">
              • {suggestions.length} suggested for this project
            </span>
          )}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Suggested Templates Section */}
        {suggestions && suggestions.length > 0 && (
          <div className="space-y-2">
            <h4 className="text-sm font-medium flex items-center gap-2 text-purple-600">
              <Sparkles className="w-4 h-4" />
              Suggested for You
            </h4>
            <div className="grid gap-2">
              {suggestions.slice(0, 3).map((suggestion) => {
                const template = templates.find(
                  (t) => t.id === suggestion.template_id
                );
                if (!template) return null;
                return (
                  <TemplateCard
                    key={template.id}
                    template={template}
                    suggestion={suggestion}
                    onSelect={() => {
                      setSelectedTemplate(template);
                      setIsApplyDialogOpen(true);
                    }}
                    isSuggested
                  />
                );
              })}
            </div>
          </div>
        )}

        {/* All Templates Section */}
        <div className="space-y-2">
          <h4 className="text-sm font-medium">All Templates</h4>
          <div className="grid gap-2">
            {sortedTemplates.map((template) => {
              const suggestion = getSuggestion(template.id);
              // Skip if already shown in suggestions
              if (suggestion && suggestions && suggestions.indexOf(suggestion) < 3)
                return null;
              return (
                <TemplateCard
                  key={template.id}
                  template={template}
                  suggestion={suggestion}
                  onSelect={() => {
                    setSelectedTemplate(template);
                    setIsApplyDialogOpen(true);
                  }}
                />
              );
            })}
          </div>
        </div>

        {/* Apply Template Dialog */}
        {selectedTemplate && (
          <ApplyTemplateDialog
            template={selectedTemplate}
            projectId={projectId}
            phaseId={phaseId}
            open={isApplyDialogOpen}
            onOpenChange={setIsApplyDialogOpen}
            onSuccess={(sprintId) => {
              setIsApplyDialogOpen(false);
              setSelectedTemplate(null);
              onSprintCreated?.(sprintId);
            }}
          />
        )}
      </CardContent>
    </Card>
  );
}

/** Template card component */
function TemplateCard({
  template,
  suggestion,
  onSelect,
  isSuggested = false,
}: {
  template: SprintTemplate;
  suggestion?: TemplateSuggestion;
  onSelect: () => void;
  isSuggested?: boolean;
}) {
  const Icon = TEMPLATE_ICONS[template.template_type] || Layers;
  const colorClass =
    TEMPLATE_COLORS[template.template_type] || TEMPLATE_COLORS.custom;

  return (
    <div
      className={cn(
        "flex items-center gap-3 p-3 rounded-lg border cursor-pointer transition-colors hover:bg-muted/50",
        isSuggested && "border-purple-200 bg-purple-50/50"
      )}
      onClick={onSelect}
    >
      {/* Icon */}
      <div
        className={cn(
          "w-10 h-10 rounded-lg flex items-center justify-center",
          colorClass
        )}
      >
        <Icon className="w-5 h-5" />
      </div>

      {/* Info */}
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2">
          <h5 className="font-medium text-sm truncate">{template.name}</h5>
          {template.is_default && (
            <Star className="w-3 h-3 text-yellow-500 fill-yellow-500" />
          )}
        </div>
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {template.duration_days} days
          </span>
          <span className="flex items-center gap-1">
            <Target className="w-3 h-3" />
            {template.default_capacity_points} SP
          </span>
          {template.backlog_structure && template.backlog_structure.length > 0 && (
            <span className="flex items-center gap-1">
              <ListChecks className="w-3 h-3" />
              {template.backlog_structure.length} items
            </span>
          )}
        </div>
        {suggestion && (
          <div className="text-xs text-purple-600 mt-1 truncate">
            {suggestion.reason}
          </div>
        )}
      </div>

      {/* Match score (if suggested) */}
      {suggestion && (
        <div className="text-right">
          <div className="text-lg font-bold text-purple-600">
            {Math.round(suggestion.match_score * 100)}%
          </div>
          <div className="text-xs text-muted-foreground">match</div>
        </div>
      )}

      {/* Usage count */}
      {!suggestion && (
        <Badge variant="secondary" className="text-xs">
          Used {template.usage_count}x
        </Badge>
      )}
    </div>
  );
}

/** Apply template dialog */
function ApplyTemplateDialog({
  template,
  projectId,
  phaseId,
  open,
  onOpenChange,
  onSuccess,
}: {
  template: SprintTemplate;
  projectId: string;
  phaseId?: string;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onSuccess: (sprintId: string) => void;
}) {
  const applyMutation = useApplyTemplate(template.id);

  const [formData, setFormData] = useState({
    sprint_name: "",
    goal: template.goal_template || "",
    start_date: new Date().toISOString().split("T")[0],
    team_size: "",
    include_backlog: true,
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const result = await applyMutation.mutateAsync({
        project_id: projectId,
        phase_id: phaseId,
        start_date: formData.start_date,
        sprint_name: formData.sprint_name || undefined,
        goal: formData.goal || undefined,
        team_size: formData.team_size ? parseInt(formData.team_size) : undefined,
        include_backlog: formData.include_backlog,
      });

      onSuccess(result.sprint_id);
    } catch (error) {
      // Error handled by mutation
    }
  };

  const Icon = TEMPLATE_ICONS[template.template_type] || Layers;

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg">
        <DialogHeader>
          <DialogTitle className="flex items-center gap-2">
            <Icon className="w-5 h-5 text-purple-500" />
            Create Sprint from Template
          </DialogTitle>
          <DialogDescription>
            Using "{template.name}" template
          </DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit} className="space-y-4">
          {/* Template Preview */}
          <div className="p-3 rounded-lg bg-muted/50 border space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Duration</span>
              <span className="font-medium">{template.duration_days} days</span>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Default Capacity</span>
              <span className="font-medium">
                {template.default_capacity_points} story points
              </span>
            </div>
            {template.backlog_structure &&
              template.backlog_structure.length > 0 && (
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Backlog Items</span>
                  <span className="font-medium">
                    {template.backlog_structure.length} items included
                  </span>
                </div>
              )}
          </div>

          {/* Form Fields */}
          <div className="space-y-3">
            <div className="space-y-2">
              <Label htmlFor="start_date">Start Date *</Label>
              <Input
                id="start_date"
                type="date"
                value={formData.start_date}
                onChange={(e) =>
                  setFormData((f) => ({ ...f, start_date: e.target.value }))
                }
                required
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="sprint_name">
                Sprint Name{" "}
                <span className="text-muted-foreground">(optional)</span>
              </Label>
              <Input
                id="sprint_name"
                placeholder="Auto-generated if empty"
                value={formData.sprint_name}
                onChange={(e) =>
                  setFormData((f) => ({ ...f, sprint_name: e.target.value }))
                }
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="goal">
                Sprint Goal{" "}
                <span className="text-muted-foreground">(optional)</span>
              </Label>
              <Input
                id="goal"
                placeholder="From template if empty"
                value={formData.goal}
                onChange={(e) =>
                  setFormData((f) => ({ ...f, goal: e.target.value }))
                }
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="team_size">
                Team Size{" "}
                <span className="text-muted-foreground">(optional)</span>
              </Label>
              <Input
                id="team_size"
                type="number"
                min={1}
                placeholder="Number of team members"
                value={formData.team_size}
                onChange={(e) =>
                  setFormData((f) => ({ ...f, team_size: e.target.value }))
                }
              />
            </div>

            {/* Include Backlog Checkbox */}
            {template.backlog_structure &&
              template.backlog_structure.length > 0 && (
                <div className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    id="include_backlog"
                    checked={formData.include_backlog}
                    onChange={(e) =>
                      setFormData((f) => ({
                        ...f,
                        include_backlog: e.target.checked,
                      }))
                    }
                    className="rounded border-gray-300"
                  />
                  <Label htmlFor="include_backlog" className="font-normal">
                    Include {template.backlog_structure.length} backlog items
                    from template
                  </Label>
                </div>
              )}
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={applyMutation.isPending}>
              {applyMutation.isPending ? (
                <>
                  <Copy className="w-4 h-4 mr-2 animate-spin" />
                  Creating...
                </>
              ) : (
                <>
                  <CheckCircle2 className="w-4 h-4 mr-2" />
                  Create Sprint
                </>
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}

/** Skeleton loader for template selector */
function TemplateSelectorSkeleton() {
  return (
    <Card>
      <CardHeader>
        <Skeleton className="h-5 w-40 mb-2" />
        <Skeleton className="h-4 w-56" />
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Skeleton className="h-5 w-32" />
          <div className="grid gap-2">
            {[1, 2, 3].map((i) => (
              <Skeleton key={i} className="h-20 w-full rounded-lg" />
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
