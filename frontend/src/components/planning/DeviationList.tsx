/**
 * Deviation List - SDLC Orchestrator
 *
 * @module frontend/src/components/planning/DeviationList
 * @description Table component for displaying pattern deviations
 * @sdlc SDLC 6.0.6 Framework - Sprint 99 (Planning Sub-agent Part 2)
 */

import { cn } from "@/lib/utils";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import type { PatternDeviation, DeviationSeverity } from "@/lib/types/planning-subagent";

interface DeviationListProps {
  deviations: PatternDeviation[];
  showFile?: boolean;
  showSuggestion?: boolean;
  maxItems?: number;
  className?: string;
}

/**
 * Get badge variant for severity
 */
function getSeverityVariant(
  severity: DeviationSeverity
): "destructive" | "default" | "secondary" | "outline" {
  switch (severity) {
    case "CRITICAL":
      return "destructive";
    case "HIGH":
      return "destructive";
    case "MEDIUM":
      return "default";
    case "LOW":
      return "secondary";
  }
}

/**
 * Get severity icon
 */
function getSeverityIcon(severity: DeviationSeverity): string {
  switch (severity) {
    case "CRITICAL":
      return "!!";
    case "HIGH":
      return "!";
    case "MEDIUM":
      return "△";
    case "LOW":
      return "○";
  }
}

export function DeviationList({
  deviations,
  showFile = true,
  showSuggestion = false,
  maxItems,
  className,
}: DeviationListProps) {
  const displayDeviations = maxItems
    ? deviations.slice(0, maxItems)
    : deviations;
  const hasMore = maxItems && deviations.length > maxItems;

  if (deviations.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        No deviations detected
      </div>
    );
  }

  return (
    <div className={cn("space-y-4", className)}>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[100px]">Severity</TableHead>
            <TableHead className="w-[120px]">Rule ID</TableHead>
            <TableHead>Pattern</TableHead>
            <TableHead>Description</TableHead>
            {showFile && <TableHead className="w-[200px]">Location</TableHead>}
          </TableRow>
        </TableHeader>
        <TableBody>
          {displayDeviations.map((deviation, index) => (
            <TableRow key={`${deviation.rule_id}-${index}`}>
              <TableCell>
                <Badge variant={getSeverityVariant(deviation.severity)}>
                  {getSeverityIcon(deviation.severity)} {deviation.severity}
                </Badge>
              </TableCell>
              <TableCell className="font-mono text-sm">
                {deviation.rule_id}
              </TableCell>
              <TableCell className="font-medium">
                {deviation.pattern_name}
              </TableCell>
              <TableCell>
                <div className="space-y-1">
                  <p className="text-sm">{deviation.description}</p>
                  {showSuggestion && deviation.suggestion && (
                    <p className="text-xs text-muted-foreground">
                      💡 {deviation.suggestion}
                    </p>
                  )}
                </div>
              </TableCell>
              {showFile && (
                <TableCell>
                  {deviation.file_path && (
                    <div className="font-mono text-xs">
                      <span className="text-muted-foreground">
                        {deviation.file_path}
                      </span>
                      {deviation.line_number && (
                        <span className="text-blue-600">
                          :{deviation.line_number}
                        </span>
                      )}
                    </div>
                  )}
                </TableCell>
              )}
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {hasMore && (
        <p className="text-center text-sm text-muted-foreground">
          And {deviations.length - maxItems!} more deviations...
        </p>
      )}
    </div>
  );
}

export default DeviationList;
