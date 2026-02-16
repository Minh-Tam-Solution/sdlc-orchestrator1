/**
 * Pattern Summary Card - SDLC Orchestrator
 *
 * @module frontend/src/components/planning/PatternSummaryCard
 * @description Card component for displaying extracted patterns summary
 * @sdlc SDLC 6.0.6 Framework - Sprint 99 (Planning Sub-agent Part 2)
 */

import { cn } from "@/lib/utils";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import type { PatternSummary, PatternCategory } from "@/lib/types/planning-subagent";

interface PatternSummaryCardProps {
  patterns: PatternSummary;
  showConventions?: boolean;
  maxPatterns?: number;
  className?: string;
}

/**
 * Get color for pattern category
 */
function getCategoryColor(category: PatternCategory): string {
  const colors: Record<PatternCategory, string> = {
    ARCHITECTURE: "bg-purple-100 text-purple-800",
    CODE_STYLE: "bg-blue-100 text-blue-800",
    ERROR_HANDLING: "bg-red-100 text-red-800",
    SECURITY: "bg-orange-100 text-orange-800",
    TESTING: "bg-green-100 text-green-800",
    NAMING: "bg-cyan-100 text-cyan-800",
    DOCUMENTATION: "bg-gray-100 text-gray-800",
    API_DESIGN: "bg-indigo-100 text-indigo-800",
    DATABASE: "bg-yellow-100 text-yellow-800",
    PERFORMANCE: "bg-pink-100 text-pink-800",
  };
  return colors[category] || "bg-gray-100 text-gray-800";
}

/**
 * Format category name for display
 */
function formatCategoryName(category: string): string {
  return category
    .toLowerCase()
    .replace(/_/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function PatternSummaryCard({
  patterns,
  showConventions = true,
  maxPatterns = 5,
  className,
}: PatternSummaryCardProps) {
  const displayPatterns = patterns.top_patterns.slice(0, maxPatterns);
  const categoryEntries = Object.entries(patterns.categories).sort(
    ([, a], [, b]) => b - a
  );

  return (
    <Card className={cn("", className)}>
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Extracted Patterns</span>
          <Badge variant="secondary">
            {patterns.total_patterns_found} patterns from{" "}
            {patterns.total_files_scanned} files
          </Badge>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* Categories */}
        <div>
          <h4 className="text-sm font-medium text-muted-foreground mb-3">
            Pattern Categories
          </h4>
          <div className="flex flex-wrap gap-2">
            {categoryEntries.map(([category, count]) => (
              <span
                key={category}
                className={cn(
                  "inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium",
                  getCategoryColor(category as PatternCategory)
                )}
              >
                {formatCategoryName(category)}
                <span className="font-bold">({count})</span>
              </span>
            ))}
          </div>
        </div>

        {/* Top Patterns */}
        {displayPatterns.length > 0 && (
          <div>
            <h4 className="text-sm font-medium text-muted-foreground mb-3">
              Top Patterns Found
            </h4>
            <ul className="space-y-2">
              {displayPatterns.map((pattern, index) => (
                <li
                  key={index}
                  className="flex items-start gap-2 text-sm"
                >
                  <span className="text-muted-foreground font-mono">
                    {index + 1}.
                  </span>
                  <span>{pattern}</span>
                </li>
              ))}
            </ul>
            {patterns.top_patterns.length > maxPatterns && (
              <p className="text-xs text-muted-foreground mt-2">
                And {patterns.top_patterns.length - maxPatterns} more patterns...
              </p>
            )}
          </div>
        )}

        {/* Conventions */}
        {showConventions &&
          Object.keys(patterns.conventions_detected).length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-muted-foreground mb-3">
                Conventions Detected
              </h4>
              <div className="space-y-2">
                {Object.entries(patterns.conventions_detected).map(
                  ([name, description]) => (
                    <div key={name} className="text-sm">
                      <span className="font-medium text-primary">{name}:</span>{" "}
                      <span className="text-muted-foreground">
                        {description.length > 80
                          ? `${description.slice(0, 80)}...`
                          : description}
                      </span>
                    </div>
                  )
                )}
              </div>
            </div>
          )}
      </CardContent>
    </Card>
  );
}

export default PatternSummaryCard;
