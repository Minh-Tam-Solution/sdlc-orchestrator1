/**
 * =========================================================================
 * SprintDependencyGraph - Cross-Project Sprint Dependency Visualization
 * SDLC Orchestrator - Sprint 78 Day 5
 *
 * Version: 1.0.0
 * Date: January 18, 2026
 * Status: ACTIVE - Sprint 78 Frontend Components
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Sprint Planning Governance
 *
 * Purpose:
 * - Visualize sprint dependencies as a directed graph
 * - Show blocking/required/related relationships
 * - Highlight critical path and blocked sprints
 * - Interactive node selection and filtering
 *
 * References:
 * - backend/app/services/sprint_dependency_service.py
 * - docs/04-build/02-Sprint-Plans/SPRINT-78-RETROSPECTIVE-CROSS-PROJECT.md
 * =========================================================================
 */

import { useMemo, useState, useCallback } from "react";
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  useDependencyGraph,
  DependencyNode,
  DependencyEdge,
  DependencyType,
  DependencyStatus,
} from "@/hooks/usePlanning";
import {
  AlertTriangle,
  ArrowRight,
  Circle,
  Filter,
  GitBranch,
  Lock,
  RefreshCw,
  Zap,
} from "lucide-react";
import { cn } from "@/lib/utils";

/** Props for SprintDependencyGraph */
interface SprintDependencyGraphProps {
  /** Project ID to show dependencies for */
  projectId: string;
  /** Optional callback when a node is selected */
  onNodeSelect?: (sprintId: string) => void;
}

/** Dependency type configuration */
const DEPENDENCY_TYPES: Record<
  DependencyType,
  { label: string; color: string; icon: React.ElementType }
> = {
  blocks: { label: "Blocks", color: "text-red-500", icon: Lock },
  requires: { label: "Requires", color: "text-orange-500", icon: Zap },
  related: { label: "Related", color: "text-blue-500", icon: GitBranch },
};

/** Dependency status configuration */
const STATUS_COLORS: Record<DependencyStatus, string> = {
  pending: "bg-yellow-100 text-yellow-700 border-yellow-300",
  active: "bg-blue-100 text-blue-700 border-blue-300",
  resolved: "bg-green-100 text-green-700 border-green-300",
  cancelled: "bg-gray-100 text-gray-500 border-gray-300",
};

/**
 * Sprint Dependency Graph Component
 * Visualizes cross-project sprint dependencies
 */
export default function SprintDependencyGraph({
  projectId,
  onNodeSelect,
}: SprintDependencyGraphProps) {
  const { data: graph, isLoading, error, refetch } = useDependencyGraph(projectId);
  const [filter, setFilter] = useState<DependencyType | "all">("all");
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [isRefetching, setIsRefetching] = useState(false);

  const handleRefresh = async () => {
    setIsRefetching(true);
    await refetch();
    setIsRefetching(false);
  };

  const handleNodeClick = useCallback(
    (nodeId: string) => {
      setSelectedNode(nodeId === selectedNode ? null : nodeId);
      if (onNodeSelect) {
        onNodeSelect(nodeId);
      }
    },
    [selectedNode, onNodeSelect]
  );

  // Filter edges based on selected type
  const filteredEdges = useMemo(() => {
    if (!graph) return [];
    if (filter === "all") return graph.edges;
    return graph.edges.filter((e) => e.type === filter);
  }, [graph, filter]);

  // Calculate node positions using simple layered layout
  const nodePositions = useMemo(() => {
    if (!graph) return new Map<string, { x: number; y: number }>();

    const positions = new Map<string, { x: number; y: number }>();
    const visited = new Set<string>();
    const layers: string[][] = [];

    // Build adjacency list for topological sort
    const incoming = new Map<string, Set<string>>();
    const outgoing = new Map<string, Set<string>>();

    graph.nodes.forEach((n) => {
      incoming.set(n.id, new Set());
      outgoing.set(n.id, new Set());
    });

    filteredEdges.forEach((e) => {
      incoming.get(e.target)?.add(e.source);
      outgoing.get(e.source)?.add(e.target);
    });

    // Find root nodes (no incoming edges)
    const queue: string[] = [];
    graph.nodes.forEach((n) => {
      if ((incoming.get(n.id)?.size || 0) === 0) {
        queue.push(n.id);
      }
    });

    // Layered layout via BFS
    while (queue.length > 0) {
      const layer: string[] = [];
      const nextQueue: string[] = [];

      while (queue.length > 0) {
        const nodeId = queue.shift()!;
        if (visited.has(nodeId)) continue;
        visited.add(nodeId);
        layer.push(nodeId);

        outgoing.get(nodeId)?.forEach((targetId) => {
          nextQueue.push(targetId);
        });
      }

      if (layer.length > 0) {
        layers.push(layer);
      }
      queue.push(...nextQueue);
    }

    // Add unvisited nodes (disconnected)
    const unvisited: string[] = [];
    graph.nodes.forEach((n) => {
      if (!visited.has(n.id)) {
        unvisited.push(n.id);
      }
    });
    if (unvisited.length > 0) {
      layers.push(unvisited);
    }

    // Assign positions
    const layerWidth = 180;
    const nodeHeight = 80;

    layers.forEach((layer, layerIdx) => {
      const layerX = 60 + layerIdx * layerWidth;
      layer.forEach((nodeId, nodeIdx) => {
        const layerY = 40 + nodeIdx * nodeHeight;
        positions.set(nodeId, { x: layerX, y: layerY });
      });
    });

    return positions;
  }, [graph, filteredEdges]);

  // Calculate SVG dimensions
  const svgDimensions = useMemo(() => {
    let maxX = 400;
    let maxY = 200;

    nodePositions.forEach((pos) => {
      maxX = Math.max(maxX, pos.x + 150);
      maxY = Math.max(maxY, pos.y + 80);
    });

    return { width: maxX, height: maxY };
  }, [nodePositions]);

  if (isLoading) {
    return <DependencyGraphSkeleton />;
  }

  if (error) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-destructive" />
            Error Loading Dependencies
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Failed to load dependency graph. Please try again.
          </p>
          <Button variant="outline" size="sm" className="mt-3" onClick={handleRefresh}>
            <RefreshCw className="w-4 h-4 mr-2" />
            Retry
          </Button>
        </CardContent>
      </Card>
    );
  }

  if (!graph || graph.nodes.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-muted-foreground" />
            Sprint Dependencies
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground py-4 text-center">
            No sprint dependencies found for this project.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-base flex items-center gap-2">
              <GitBranch className="w-5 h-5 text-purple-500" />
              Sprint Dependencies
            </CardTitle>
            <CardDescription>
              {graph.nodes.length} sprints, {graph.edges.length} dependencies
            </CardDescription>
          </div>
          <div className="flex items-center gap-2">
            <Select
              value={filter}
              onValueChange={(v) => setFilter(v as DependencyType | "all")}
            >
              <SelectTrigger className="w-32">
                <Filter className="w-4 h-4 mr-2" />
                <SelectValue placeholder="Filter" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Types</SelectItem>
                <SelectItem value="blocks">Blocks</SelectItem>
                <SelectItem value="requires">Requires</SelectItem>
                <SelectItem value="related">Related</SelectItem>
              </SelectContent>
            </Select>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleRefresh}
              disabled={isRefetching}
            >
              <RefreshCw
                className={cn("w-4 h-4", isRefetching && "animate-spin")}
              />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {/* Critical Path Alert */}
        {graph.critical_path.length > 0 && (
          <div className="mb-4 p-3 bg-orange-50 border border-orange-200 rounded-lg">
            <div className="flex items-center gap-2 text-sm font-medium text-orange-700">
              <Zap className="w-4 h-4" />
              Critical Path: {graph.critical_path.length} sprints
            </div>
            <p className="text-xs text-orange-600 mt-1">
              These sprints form the longest dependency chain and may impact delivery.
            </p>
          </div>
        )}

        {/* Legend */}
        <div className="flex items-center gap-4 mb-4 text-xs">
          {Object.entries(DEPENDENCY_TYPES).map(([type, config]) => {
            const Icon = config.icon;
            return (
              <div key={type} className="flex items-center gap-1">
                <Icon className={cn("w-3 h-3", config.color)} />
                <span className="text-muted-foreground">{config.label}</span>
              </div>
            );
          })}
        </div>

        {/* Graph SVG */}
        <div className="overflow-auto border rounded-lg bg-muted/30">
          <svg
            width={svgDimensions.width}
            height={svgDimensions.height}
            className="min-w-full"
          >
            <defs>
              {/* Arrow markers for each dependency type */}
              {Object.entries(DEPENDENCY_TYPES).map(([type, config]) => (
                <marker
                  key={type}
                  id={`arrow-${type}`}
                  markerWidth="10"
                  markerHeight="7"
                  refX="9"
                  refY="3.5"
                  orient="auto"
                >
                  <polygon
                    points="0 0, 10 3.5, 0 7"
                    className={config.color.replace("text-", "fill-")}
                  />
                </marker>
              ))}
            </defs>

            {/* Edges */}
            {filteredEdges.map((edge) => {
              const sourcePos = nodePositions.get(edge.source);
              const targetPos = nodePositions.get(edge.target);
              if (!sourcePos || !targetPos) return null;

              const config = DEPENDENCY_TYPES[edge.type];
              const strokeColor = config.color.replace("text-", "stroke-");

              // Calculate edge path
              const x1 = sourcePos.x + 120; // Right side of source node
              const y1 = sourcePos.y + 25; // Middle of node
              const x2 = targetPos.x; // Left side of target node
              const y2 = targetPos.y + 25;

              // Curved path for better visibility
              const midX = (x1 + x2) / 2;

              return (
                <g key={edge.id}>
                  <path
                    d={`M ${x1} ${y1} C ${midX} ${y1}, ${midX} ${y2}, ${x2} ${y2}`}
                    fill="none"
                    className={cn(
                      strokeColor,
                      edge.status === "resolved" && "opacity-40",
                      edge.status === "cancelled" && "opacity-20"
                    )}
                    strokeWidth={edge.status === "active" ? 2 : 1.5}
                    strokeDasharray={edge.type === "related" ? "4 2" : undefined}
                    markerEnd={`url(#arrow-${edge.type})`}
                  />
                </g>
              );
            })}

            {/* Nodes */}
            {graph.nodes.map((node) => {
              const pos = nodePositions.get(node.id);
              if (!pos) return null;

              const isSelected = selectedNode === node.id;
              const isCritical = graph.critical_path.includes(node.id);

              return (
                <g
                  key={node.id}
                  transform={`translate(${pos.x}, ${pos.y})`}
                  onClick={() => handleNodeClick(node.id)}
                  className="cursor-pointer"
                >
                  <rect
                    width={120}
                    height={50}
                    rx={6}
                    className={cn(
                      "fill-background stroke-border transition-all",
                      isSelected && "stroke-primary stroke-2",
                      isCritical && "stroke-orange-400 stroke-2",
                      node.status === "completed" && "fill-green-50",
                      node.status === "in_progress" && "fill-blue-50"
                    )}
                  />
                  <text
                    x={60}
                    y={20}
                    textAnchor="middle"
                    className="text-xs font-medium fill-foreground"
                  >
                    Sprint {node.sprint_number}
                  </text>
                  <text
                    x={60}
                    y={35}
                    textAnchor="middle"
                    className="text-[10px] fill-muted-foreground"
                  >
                    {node.project_name.slice(0, 15)}
                    {node.project_name.length > 15 && "..."}
                  </text>
                  {/* Status indicator */}
                  <circle
                    cx={110}
                    cy={10}
                    r={4}
                    className={cn(
                      node.status === "planning" && "fill-gray-400",
                      node.status === "in_progress" && "fill-blue-500",
                      node.status === "completed" && "fill-green-500",
                      node.status === "closed" && "fill-purple-500"
                    )}
                  />
                </g>
              );
            })}
          </svg>
        </div>

        {/* Selected Node Details */}
        {selectedNode && (
          <SelectedNodeDetails
            node={graph.nodes.find((n) => n.id === selectedNode)!}
            edges={graph.edges.filter(
              (e) => e.source === selectedNode || e.target === selectedNode
            )}
            allNodes={graph.nodes}
          />
        )}
      </CardContent>
    </Card>
  );
}

/** Selected node details panel */
function SelectedNodeDetails({
  node,
  edges,
  allNodes,
}: {
  node: DependencyNode;
  edges: DependencyEdge[];
  allNodes: DependencyNode[];
}) {
  const incoming = edges.filter((e) => e.target === node.id);
  const outgoing = edges.filter((e) => e.source === node.id);

  const getNodeName = (id: string) => {
    const n = allNodes.find((n) => n.id === id);
    return n ? `Sprint ${n.sprint_number}` : "Unknown";
  };

  return (
    <div className="mt-4 p-4 border rounded-lg bg-muted/50">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-medium">Sprint {node.sprint_number}</h4>
        <Badge
          variant="outline"
          className={cn(
            node.status === "in_progress" && "border-blue-300 text-blue-700",
            node.status === "completed" && "border-green-300 text-green-700"
          )}
        >
          {node.status.replace("_", " ")}
        </Badge>
      </div>
      <div className="text-sm text-muted-foreground mb-3">
        {node.project_name}
      </div>

      <div className="grid grid-cols-2 gap-4">
        {/* Dependencies (incoming) */}
        <div>
          <h5 className="text-xs font-medium text-muted-foreground mb-2">
            Depends On ({incoming.length})
          </h5>
          {incoming.length === 0 ? (
            <p className="text-xs text-muted-foreground">No dependencies</p>
          ) : (
            <div className="space-y-1">
              {incoming.map((e) => {
                const config = DEPENDENCY_TYPES[e.type];
                const Icon = config.icon;
                return (
                  <div
                    key={e.id}
                    className="flex items-center gap-2 text-xs"
                  >
                    <Icon className={cn("w-3 h-3", config.color)} />
                    <span>{getNodeName(e.source)}</span>
                    <Badge
                      variant="outline"
                      className={cn("text-[10px] px-1", STATUS_COLORS[e.status])}
                    >
                      {e.status}
                    </Badge>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Dependents (outgoing) */}
        <div>
          <h5 className="text-xs font-medium text-muted-foreground mb-2">
            Blocks ({outgoing.length})
          </h5>
          {outgoing.length === 0 ? (
            <p className="text-xs text-muted-foreground">No dependents</p>
          ) : (
            <div className="space-y-1">
              {outgoing.map((e) => {
                const config = DEPENDENCY_TYPES[e.type];
                const Icon = config.icon;
                return (
                  <div
                    key={e.id}
                    className="flex items-center gap-2 text-xs"
                  >
                    <Icon className={cn("w-3 h-3", config.color)} />
                    <span>{getNodeName(e.target)}</span>
                    <Badge
                      variant="outline"
                      className={cn("text-[10px] px-1", STATUS_COLORS[e.status])}
                    >
                      {e.status}
                    </Badge>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/** Skeleton loader for dependency graph */
function DependencyGraphSkeleton() {
  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <Skeleton className="h-5 w-40 mb-2" />
            <Skeleton className="h-4 w-56" />
          </div>
          <div className="flex items-center gap-2">
            <Skeleton className="h-9 w-32" />
            <Skeleton className="h-8 w-8" />
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Skeleton className="h-[300px] w-full rounded-lg" />
      </CardContent>
    </Card>
  );
}
