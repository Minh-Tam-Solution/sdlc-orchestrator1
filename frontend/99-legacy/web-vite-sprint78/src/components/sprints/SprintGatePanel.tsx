/**
 * =========================================================================
 * SprintGatePanel - G-Sprint/G-Sprint-Close Gate Management
 * SDLC Orchestrator - Sprint 75 Day 4
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 75 Sprint Dashboard UI
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Display gate evaluation status
 * - Create gate evaluation with checklist
 * - Submit gate for approval (SE4H Coach)
 * - Show approval history
 *
 * SDLC 5.1.3 Compliance:
 * - G-Sprint: Sprint planning approval
 * - G-Sprint-Close: Sprint completion approval (24h Rule #2)
 * - SE4H Coach: Only admin/owner can approve
 * =========================================================================
 */

import { useState } from "react";
import {
  Shield,
  ShieldCheck,
  ShieldX,
  Clock,
  CheckCircle2,
  XCircle,
  AlertCircle,
  ChevronDown,
  ChevronUp,
  Send,
} from "lucide-react";
import {
  SprintGateEvaluation,
  GateType,
  SprintStatus,
  useCreateGateEvaluation,
  useSubmitGateApproval,
  CreateGateEvaluationData,
} from "@/hooks/usePlanning";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";

/**
 * G-Sprint Checklist Items
 * Per SDLC 5.1.3 Sprint Planning Governance
 */
const G_SPRINT_CHECKLIST = [
  {
    key: "previous_sprint_completed",
    label: "Previous sprint completed or closed",
    description: "All items from previous sprint accounted for",
  },
  {
    key: "roadmap_alignment_verified",
    label: "Roadmap alignment verified",
    description: "Sprint goal aligns with phase and roadmap objectives",
  },
  {
    key: "capacity_calculated",
    label: "Team capacity calculated",
    description: "Story points allocated based on team availability",
  },
  {
    key: "backlog_prioritized",
    label: "Backlog prioritized (P0/P1/P2)",
    description: "All items have explicit priority per Rule #8",
  },
  {
    key: "team_committed",
    label: "Team commitment obtained",
    description: "All team members agreed to sprint scope",
  },
  {
    key: "risks_identified",
    label: "Risks and blockers identified",
    description: "Known risks documented with mitigation plans",
  },
];

/**
 * G-Sprint-Close Checklist Items
 * Per SDLC 5.1.3 Sprint Planning Governance
 */
const G_SPRINT_CLOSE_CHECKLIST = [
  {
    key: "all_stories_completed",
    label: "All committed stories completed or deferred",
    description: "Each item marked as done or explicitly carried over",
  },
  {
    key: "demo_conducted",
    label: "Sprint demo conducted",
    description: "Stakeholders reviewed completed work",
  },
  {
    key: "retrospective_completed",
    label: "Retrospective completed",
    description: "Team reviewed what went well and improvements",
  },
  {
    key: "documentation_updated",
    label: "Documentation updated within 24h",
    description: "SDLC 5.1.3 Rule #2: Post-sprint documentation",
  },
  {
    key: "metrics_captured",
    label: "Sprint metrics captured",
    description: "Velocity, completion rate, and quality metrics recorded",
  },
];

/**
 * SprintGatePanel Props
 */
interface SprintGatePanelProps {
  sprintId: string;
  gateType: GateType;
  gateEvaluation?: SprintGateEvaluation;
  sprintStatus: SprintStatus;
  canEvaluate: boolean;
}

/**
 * SprintGatePanel Component
 * Manages G-Sprint or G-Sprint-Close gate evaluation
 */
export default function SprintGatePanel({
  sprintId,
  gateType,
  gateEvaluation,
  sprintStatus,
  canEvaluate,
}: SprintGatePanelProps) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [checklist, setChecklist] = useState<Record<string, boolean>>({});
  const [notes, setNotes] = useState("");

  const createGate = useCreateGateEvaluation(sprintId, gateType);
  const submitGate = useSubmitGateApproval(sprintId);

  // Get checklist items based on gate type
  const checklistItems =
    gateType === "g_sprint" ? G_SPRINT_CHECKLIST : G_SPRINT_CLOSE_CHECKLIST;

  // Gate configuration
  const gateConfig = getGateConfig(gateType);
  const statusConfig = getGateStatusConfig(gateEvaluation?.status);

  /**
   * Handle checklist item change
   */
  const handleChecklistChange = (key: string, checked: boolean) => {
    setChecklist((prev) => ({ ...prev, [key]: checked }));
  };

  /**
   * Create gate evaluation
   */
  const handleCreateEvaluation = async () => {
    const data: CreateGateEvaluationData = {
      checklist,
      notes: notes || undefined,
    };

    await createGate.mutateAsync(data);
    setIsCreating(false);
    setChecklist({});
    setNotes("");
  };

  /**
   * Submit gate for approval
   */
  const handleSubmitApproval = async () => {
    if (!gateEvaluation) return;
    await submitGate.mutateAsync(gateEvaluation.id);
  };

  // Calculate checklist completion
  const completedItems = Object.values(checklist).filter(Boolean).length;
  const totalItems = checklistItems.length;
  const allChecked = completedItems === totalItems;

  return (
    <Card>
      <Collapsible open={isExpanded} onOpenChange={setIsExpanded}>
        <CardHeader className="pb-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {statusConfig.icon}
              <div>
                <CardTitle className="text-base">{gateConfig.title}</CardTitle>
                <CardDescription>{gateConfig.description}</CardDescription>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant={statusConfig.variant} className={statusConfig.className}>
                {statusConfig.label}
              </Badge>
              <CollapsibleTrigger asChild>
                <Button variant="ghost" size="sm">
                  {isExpanded ? (
                    <ChevronUp className="h-4 w-4" />
                  ) : (
                    <ChevronDown className="h-4 w-4" />
                  )}
                </Button>
              </CollapsibleTrigger>
            </div>
          </div>
        </CardHeader>

        <CollapsibleContent>
          <CardContent className="space-y-4">
            {/* Show existing evaluation */}
            {gateEvaluation && !isCreating && (
              <div className="space-y-4">
                {/* Checklist Display */}
                <div className="space-y-2">
                  <Label>Evaluation Checklist</Label>
                  <div className="space-y-2 rounded-lg bg-muted p-3">
                    {checklistItems.map((item) => {
                      const isChecked = gateEvaluation.checklist[item.key];
                      return (
                        <div
                          key={item.key}
                          className="flex items-start gap-2 py-1"
                        >
                          {isChecked ? (
                            <CheckCircle2 className="w-4 h-4 text-green-600 mt-0.5" />
                          ) : (
                            <XCircle className="w-4 h-4 text-red-500 mt-0.5" />
                          )}
                          <div>
                            <div
                              className={`text-sm ${
                                isChecked
                                  ? "text-green-700"
                                  : "text-red-600"
                              }`}
                            >
                              {item.label}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Notes */}
                {gateEvaluation.notes && (
                  <div className="space-y-2">
                    <Label>Notes</Label>
                    <div className="rounded-lg bg-muted p-3 text-sm">
                      {gateEvaluation.notes}
                    </div>
                  </div>
                )}

                {/* Evaluation Info */}
                {gateEvaluation.evaluated_at && (
                  <div className="text-xs text-muted-foreground">
                    Evaluated on{" "}
                    {new Date(gateEvaluation.evaluated_at).toLocaleString()}
                  </div>
                )}

                {/* Submit Button (for pending evaluations) */}
                {gateEvaluation.status === "pending" && (
                  <div className="pt-2 border-t">
                    <div className="flex items-start gap-2 mb-3 p-2 rounded bg-yellow-50 border border-yellow-200">
                      <AlertCircle className="w-4 h-4 text-yellow-600 mt-0.5" />
                      <div className="text-sm text-yellow-700">
                        <strong>SE4H Coach Required:</strong> Only team
                        admin/owner can approve this gate.
                      </div>
                    </div>
                    <Button
                      onClick={handleSubmitApproval}
                      disabled={submitGate.isPending}
                      className="w-full"
                    >
                      <Send className="w-4 h-4 mr-2" />
                      {submitGate.isPending
                        ? "Submitting..."
                        : "Submit for Approval"}
                    </Button>
                  </div>
                )}
              </div>
            )}

            {/* Create new evaluation form */}
            {isCreating && (
              <div className="space-y-4">
                <div className="space-y-3">
                  <Label>Evaluation Checklist</Label>
                  <div className="space-y-3">
                    {checklistItems.map((item) => (
                      <div
                        key={item.key}
                        className="flex items-start gap-3 p-2 rounded hover:bg-muted"
                      >
                        <Checkbox
                          id={item.key}
                          checked={checklist[item.key] || false}
                          onCheckedChange={(checked) =>
                            handleChecklistChange(item.key, checked as boolean)
                          }
                        />
                        <div className="flex-1">
                          <Label
                            htmlFor={item.key}
                            className="text-sm font-medium cursor-pointer"
                          >
                            {item.label}
                          </Label>
                          <p className="text-xs text-muted-foreground">
                            {item.description}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="notes">Notes (optional)</Label>
                  <Textarea
                    id="notes"
                    placeholder="Add any additional notes about this evaluation..."
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                    rows={3}
                  />
                </div>

                <div className="text-sm text-muted-foreground">
                  {completedItems} / {totalItems} items checked
                </div>

                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    onClick={() => {
                      setIsCreating(false);
                      setChecklist({});
                      setNotes("");
                    }}
                    disabled={createGate.isPending}
                  >
                    Cancel
                  </Button>
                  <Button
                    onClick={handleCreateEvaluation}
                    disabled={createGate.isPending || !allChecked}
                    className="flex-1"
                  >
                    {createGate.isPending
                      ? "Creating..."
                      : "Create Evaluation"}
                  </Button>
                </div>

                {!allChecked && (
                  <p className="text-xs text-muted-foreground">
                    All checklist items must be checked to create an evaluation.
                  </p>
                )}
              </div>
            )}

            {/* No evaluation yet - show create button */}
            {!gateEvaluation && !isCreating && (
              <div className="text-center py-4">
                {canEvaluate ? (
                  <>
                    <p className="text-sm text-muted-foreground mb-3">
                      No evaluation created yet. Create one to proceed with the
                      gate.
                    </p>
                    <Button onClick={() => setIsCreating(true)}>
                      Create Evaluation
                    </Button>
                  </>
                ) : (
                  <p className="text-sm text-muted-foreground">
                    {getCannotEvaluateMessage(gateType, sprintStatus)}
                  </p>
                )}
              </div>
            )}
          </CardContent>
        </CollapsibleContent>
      </Collapsible>
    </Card>
  );
}

/**
 * Get gate configuration
 */
function getGateConfig(gateType: GateType) {
  if (gateType === "g_sprint") {
    return {
      title: "G-Sprint Gate",
      description: "Sprint planning approval before start",
    };
  }
  return {
    title: "G-Sprint-Close Gate",
    description: "Sprint completion approval (24h documentation)",
  };
}

/**
 * Get gate status configuration
 */
function getGateStatusConfig(status?: string) {
  switch (status) {
    case "pending":
      return {
        label: "Pending",
        variant: "secondary" as const,
        className: "bg-yellow-100 text-yellow-700",
        icon: <Clock className="w-5 h-5 text-yellow-600" />,
      };
    case "approved":
      return {
        label: "Approved",
        variant: "default" as const,
        className: "bg-green-100 text-green-700",
        icon: <ShieldCheck className="w-5 h-5 text-green-600" />,
      };
    case "rejected":
      return {
        label: "Rejected",
        variant: "destructive" as const,
        className: "bg-red-100 text-red-700",
        icon: <ShieldX className="w-5 h-5 text-red-600" />,
      };
    default:
      return {
        label: "Not Started",
        variant: "outline" as const,
        className: "",
        icon: <Shield className="w-5 h-5 text-muted-foreground" />,
      };
  }
}

/**
 * Get message for why evaluation cannot be created
 */
function getCannotEvaluateMessage(
  gateType: GateType,
  sprintStatus: SprintStatus
): string {
  if (gateType === "g_sprint") {
    if (sprintStatus !== "planning") {
      return "G-Sprint evaluation can only be created during planning phase.";
    }
    return "Cannot create G-Sprint evaluation at this time.";
  }

  // G-Sprint-Close
  if (sprintStatus !== "completed") {
    return "Sprint must be completed before G-Sprint-Close evaluation.";
  }
  return "G-Sprint must be approved before creating G-Sprint-Close evaluation.";
}
