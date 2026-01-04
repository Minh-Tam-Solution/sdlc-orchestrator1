/**
 * BlueprintJsonViewer Component - Next.js App Router
 * @module frontend/landing/src/components/codegen/BlueprintJsonViewer
 * @status Sprint 66 - EP-06 Migration
 * @description AppBlueprint JSON viewer with collapsible sections and copy functionality
 */
"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight, Copy, Check, Eye, Code } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CopyableCodeBlock } from "./CopyableCodeBlock";
import { cn } from "@/lib/utils";
import type { AppBlueprint, AppModule } from "@/lib/types/onboarding";

interface BlueprintJsonViewerProps {
  /** AppBlueprint object to display */
  blueprint: AppBlueprint;
  /** Additional CSS classes */
  className?: string;
}

/**
 * CollapsibleSection Component
 * Reusable collapsible section for structured view
 */
function CollapsibleSection({
  title,
  badge,
  children,
  defaultOpen = false,
}: {
  title: string;
  badge?: string | number;
  children: React.ReactNode;
  defaultOpen?: boolean;
}) {
  const [isOpen, setIsOpen] = useState(defaultOpen);

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen}>
      <CollapsibleTrigger asChild>
        <Button
          variant="ghost"
          className="w-full justify-between px-4 py-2 hover:bg-muted/50"
        >
          <div className="flex items-center gap-2">
            {isOpen ? (
              <ChevronDown className="h-4 w-4" />
            ) : (
              <ChevronRight className="h-4 w-4" />
            )}
            <span className="font-medium">{title}</span>
          </div>
          {badge !== undefined && <Badge variant="secondary">{badge}</Badge>}
        </Button>
      </CollapsibleTrigger>
      <CollapsibleContent className="px-4 pb-4">{children}</CollapsibleContent>
    </Collapsible>
  );
}

/**
 * BlueprintJsonViewer Component
 *
 * Displays AppBlueprint with two view modes:
 * 1. Structured View - Collapsible sections for modules, entities, etc.
 * 2. JSON View - Full JSON with syntax highlighting and copy button
 */
export function BlueprintJsonViewer({
  blueprint,
  className,
}: BlueprintJsonViewerProps) {
  const [copiedSection, setCopiedSection] = useState<string | null>(null);

  const handleCopySection = async (section: string, content: unknown) => {
    try {
      await navigator.clipboard.writeText(JSON.stringify(content, null, 2));
      setCopiedSection(section);
      setTimeout(() => setCopiedSection(null), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  // Calculate statistics
  const totalModules = blueprint.modules?.length || 0;
  const totalEntities =
    blueprint.modules?.reduce((sum, m) => sum + (m.entities?.length || 0), 0) ||
    0;
  const totalEndpoints =
    blueprint.modules?.reduce(
      (sum, m) => sum + (m.endpoints?.length || 0),
      0
    ) || 0;

  return (
    <Card className={cn("w-full", className)}>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              {blueprint.app_name_display || blueprint.app_name}
              <Badge variant="outline">{blueprint.sdlc_tier}</Badge>
            </CardTitle>
            <p className="text-sm text-muted-foreground mt-1">
              {blueprint.domain} • v{blueprint.version}
            </p>
          </div>
          <div className="flex items-center gap-4 text-sm">
            <div className="text-center">
              <div className="font-bold text-lg">{totalModules}</div>
              <div className="text-muted-foreground">Modules</div>
            </div>
            <div className="text-center">
              <div className="font-bold text-lg">{totalEntities}</div>
              <div className="text-muted-foreground">Entities</div>
            </div>
            <div className="text-center">
              <div className="font-bold text-lg">{totalEndpoints}</div>
              <div className="text-muted-foreground">Endpoints</div>
            </div>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="structured" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-4">
            <TabsTrigger value="structured" className="flex items-center gap-2">
              <Eye className="h-4 w-4" />
              Structured View
            </TabsTrigger>
            <TabsTrigger value="json" className="flex items-center gap-2">
              <Code className="h-4 w-4" />
              JSON View
            </TabsTrigger>
          </TabsList>

          {/* Structured View */}
          <TabsContent value="structured" className="space-y-2">
            {/* Modules Section */}
            <CollapsibleSection
              title="Modules"
              badge={totalModules}
              defaultOpen={true}
            >
              <div className="space-y-3 mt-2">
                {blueprint.modules?.map((module: AppModule, idx: number) => (
                  <Card key={idx} className="border-dashed">
                    <CardContent className="p-3">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="font-medium">{module.name}</p>
                          <p className="text-sm text-muted-foreground">
                            {module.description}
                          </p>
                          <div className="flex gap-2 mt-2">
                            <Badge variant="secondary">
                              {module.entities?.length || 0} entities
                            </Badge>
                            <Badge variant="secondary">
                              {module.endpoints?.length || 0} endpoints
                            </Badge>
                          </div>
                        </div>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() =>
                            handleCopySection(`module-${idx}`, module)
                          }
                        >
                          {copiedSection === `module-${idx}` ? (
                            <Check className="h-4 w-4 text-green-500" />
                          ) : (
                            <Copy className="h-4 w-4" />
                          )}
                        </Button>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </CollapsibleSection>

            {/* Config Section */}
            <CollapsibleSection title="System Configuration">
              <div className="space-y-3 mt-2">
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-3 rounded-lg bg-muted/50">
                    <p className="font-medium text-sm">Database</p>
                    <p className="text-sm text-muted-foreground">
                      {blueprint.config?.database?.type || "PostgreSQL"}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      Pool: {blueprint.config?.database?.connection_pool_size || 10}
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-muted/50">
                    <p className="font-medium text-sm">Cache</p>
                    <p className="text-sm text-muted-foreground">
                      {blueprint.config?.cache?.type || "Redis"}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      TTL: {blueprint.config?.cache?.ttl_seconds || 300}s
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-muted/50">
                    <p className="font-medium text-sm">Authentication</p>
                    <p className="text-sm text-muted-foreground">
                      {blueprint.config?.security?.authentication || "JWT"}
                    </p>
                  </div>
                  <div className="p-3 rounded-lg bg-muted/50">
                    <p className="font-medium text-sm">Rate Limit</p>
                    <p className="text-sm text-muted-foreground">
                      {blueprint.config?.security?.rate_limit?.requests_per_minute || 100}/min
                    </p>
                  </div>
                </div>
              </div>
            </CollapsibleSection>

            {/* Metadata Section */}
            <CollapsibleSection title="Metadata">
              <div className="mt-2 p-3 rounded-lg bg-muted/50 text-sm space-y-1">
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Generated:</span>
                  <span>
                    {new Date(
                      blueprint.metadata?.generated_at || Date.now()
                    ).toLocaleString()}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Generator:</span>
                  <span>v{blueprint.metadata?.generator_version || "1.0.0"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Est. Files:</span>
                  <span>{blueprint.metadata?.estimated_files || "~50"}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-muted-foreground">Est. Lines:</span>
                  <span>
                    {blueprint.metadata?.estimated_lines?.toLocaleString() ||
                      "~5,000"}
                  </span>
                </div>
              </div>
            </CollapsibleSection>
          </TabsContent>

          {/* JSON View */}
          <TabsContent value="json">
            <CopyableCodeBlock
              code={JSON.stringify(blueprint, null, 2)}
              language="json"
              title="AppBlueprint.json"
              maxHeight="500px"
            />
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}

export default BlueprintJsonViewer;
