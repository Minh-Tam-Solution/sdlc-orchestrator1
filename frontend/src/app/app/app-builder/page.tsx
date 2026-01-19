/**
 * App Builder Page - Next.js App Router
 * @module frontend/landing/src/app/app/app-builder/page
 * @status Sprint 66 - EP-06 Migration
 * @description Vietnamese SME onboarding wizard to generate AppBlueprint (IR)
 */
"use client";

import { useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { useRouter } from "next/navigation";
import Link from "next/link";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Checkbox } from "@/components/ui/checkbox";
import { ScrollArea } from "@/components/ui/scroll-area";

// Dynamic import for bundle optimization (Sprint 66 - P0 fix)
const BlueprintJsonViewer = dynamic(
  () => import("@/components/codegen/BlueprintJsonViewer").then((mod) => mod.BlueprintJsonViewer),
  {
    loading: () => (
      <div className="h-64 animate-pulse bg-muted rounded-lg flex items-center justify-center">
        <span className="text-muted-foreground">Loading blueprint viewer...</span>
      </div>
    ),
    ssr: false,
  }
);
import {
  useStartOnboarding,
  useDomainOptions,
  useFeatureOptions,
  useScaleOptions,
  useSubmitWizard,
} from "@/hooks/useOnboarding";
import type { AppBlueprint, DomainOption } from "@/lib/types/onboarding";

export default function AppBuilderPage() {
  const router = useRouter();

  // Session state
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [locale] = useState<"vi" | "en">("vi");

  // Form state
  const [domain, setDomain] = useState<string>("");
  const [appName, setAppName] = useState<string>("");
  const [scale, setScale] = useState<string>("");
  const [selectedFeatures, setSelectedFeatures] = useState<string[]>([]);

  // Generated blueprint
  const [generatedBlueprint, setGeneratedBlueprint] = useState<AppBlueprint | null>(null);
  const [generatedStats, setGeneratedStats] = useState<Record<string, unknown> | null>(null);

  // Mutations
  const startMutation = useStartOnboarding();
  const submitMutation = useSubmitWizard(sessionId);

  // Queries
  const { data: domainOptions = [], isLoading: domainsLoading } = useDomainOptions(sessionId);
  const { data: featureOptions = [], isLoading: featuresLoading } = useFeatureOptions(sessionId, domain);
  const { data: scaleOptions = [], isLoading: scalesLoading } = useScaleOptions(sessionId);

  const selectedDomainMeta = useMemo(() => {
    return domainOptions.find((d: DomainOption) => d.key === domain);
  }, [domain, domainOptions]);

  const canGenerate =
    !!sessionId &&
    !!domain &&
    !!appName.trim() &&
    selectedFeatures.length > 0 &&
    !!scale;

  const handleStartSession = async () => {
    try {
      const session = await startMutation.mutateAsync(locale);
      setSessionId(session.session_id);
      // Reset form
      setDomain("");
      setAppName("");
      setScale("");
      setSelectedFeatures([]);
      setGeneratedBlueprint(null);
      setGeneratedStats(null);
    } catch (error) {
      console.error("Failed to start session:", error);
    }
  };

  const handleGenerate = async () => {
    try {
      const result = await submitMutation.mutateAsync({
        domain,
        appName,
        features: selectedFeatures,
        scale,
      });

      if (result.success && result.blueprint) {
        setGeneratedBlueprint(result.blueprint);
        setGeneratedStats(result.stats);
      }
    } catch (error) {
      console.error("Failed to generate blueprint:", error);
    }
  };

  const handleContinueToCodegen = () => {
    // Store blueprint in sessionStorage for the code generation page
    if (generatedBlueprint) {
      sessionStorage.setItem("appBlueprint", JSON.stringify(generatedBlueprint));
      sessionStorage.setItem("blueprintStats", JSON.stringify(generatedStats));
      router.push("/app/code-generation");
    }
  };

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-muted-foreground">
        <Link href="/app" className="hover:text-foreground">
          Dashboard
        </Link>
        <span>/</span>
        <span className="text-foreground">App Builder</span>
      </nav>

      {/* Page header */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Vietnamese IR Onboarding</h1>
        <p className="text-muted-foreground mt-1">
          Minimal flow to generate a schema-valid AppBlueprint for Vietnamese SME domains.
        </p>
      </div>

      {/* Start Session Card */}
      <Card>
        <CardHeader>
          <CardTitle>Start Session</CardTitle>
          <CardDescription>
            Creates an onboarding session and loads available domains, features, and scale tiers.
          </CardDescription>
        </CardHeader>
        <CardContent className="flex items-center gap-3">
          <Button
            onClick={handleStartSession}
            disabled={startMutation.isPending}
          >
            {startMutation.isPending ? "Starting..." : "Start Vietnamese Onboarding"}
          </Button>
          {sessionId && (
            <div className="text-sm text-muted-foreground">
              Session: <span className="font-mono text-xs">{sessionId}</span>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Questionnaire Card */}
      <Card>
        <CardHeader>
          <CardTitle>Questionnaire</CardTitle>
          <CardDescription>
            Provide domain + app name + features + scale, then generate IR.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Domain */}
          <div className="space-y-2">
            <Label>Domain</Label>
            <Select
              value={domain}
              onValueChange={(v) => {
                setDomain(v);
                setSelectedFeatures([]);
              }}
              disabled={!sessionId || domainsLoading}
            >
              <SelectTrigger>
                <SelectValue
                  placeholder={!sessionId ? "Start session first" : "Select a domain"}
                />
              </SelectTrigger>
              <SelectContent>
                {domainOptions.map((d: DomainOption) => (
                  <SelectItem key={d.key} value={d.key}>
                    {d.icon} {d.name} ({d.name_en})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            {selectedDomainMeta && (
              <p className="text-sm text-muted-foreground">
                {selectedDomainMeta.description}
              </p>
            )}
          </div>

          {/* App Name */}
          <div className="space-y-2">
            <Label>App name (Vietnamese OK)</Label>
            <Input
              value={appName}
              onChange={(e) => setAppName(e.target.value)}
              placeholder={!sessionId ? "Start session first" : "e.g., Quán Phở Ngon"}
              disabled={!sessionId}
            />
          </div>

          {/* Features */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <Label>Features</Label>
              {sessionId && domain && featureOptions.length > 0 && (
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setSelectedFeatures(featureOptions.map((f) => f.key))}
                    disabled={selectedFeatures.length === featureOptions.length}
                  >
                    Select All
                  </Button>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setSelectedFeatures([])}
                    disabled={selectedFeatures.length === 0}
                  >
                    Clear
                  </Button>
                </div>
              )}
            </div>
            <Card className="border">
              <CardContent className="p-3">
                {!sessionId ? (
                  <p className="text-sm text-muted-foreground">Start session first.</p>
                ) : !domain ? (
                  <p className="text-sm text-muted-foreground">
                    Select a domain to see features.
                  </p>
                ) : featuresLoading ? (
                  <p className="text-sm text-muted-foreground">Loading features...</p>
                ) : featureOptions.length === 0 ? (
                  <p className="text-sm text-muted-foreground">
                    No features found for this domain.
                  </p>
                ) : (
                  <ScrollArea className="h-40">
                    <div className="space-y-2 pr-3">
                      {featureOptions.map((f) => {
                        const checked = selectedFeatures.includes(f.key);
                        return (
                          <div
                            key={f.key}
                            className="flex items-start gap-3 rounded-md p-2 hover:bg-muted"
                          >
                            <Checkbox
                              checked={checked}
                              onCheckedChange={(nextChecked) => {
                                const isChecked = nextChecked === true;
                                setSelectedFeatures((prev) => {
                                  if (isChecked)
                                    return prev.includes(f.key) ? prev : [...prev, f.key];
                                  return prev.filter((x) => x !== f.key);
                                });
                              }}
                              aria-label={f.name}
                            />
                            <div className="space-y-0.5">
                              <div className="text-sm font-medium">{f.name}</div>
                              <div className="text-xs text-muted-foreground">
                                {f.description}
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </ScrollArea>
                )}
              </CardContent>
            </Card>
            {selectedFeatures.length > 0 && (
              <p className="text-sm text-muted-foreground">
                Selected: <span className="font-mono text-xs">{selectedFeatures.join(", ")}</span>
              </p>
            )}
          </div>

          {/* Scale */}
          <div className="space-y-2">
            <Label>Company scale</Label>
            <Select
              value={scale}
              onValueChange={setScale}
              disabled={!sessionId || scalesLoading}
            >
              <SelectTrigger>
                <SelectValue
                  placeholder={!sessionId ? "Start session first" : "Select a scale"}
                />
              </SelectTrigger>
              <SelectContent>
                {scaleOptions.map((s) => (
                  <SelectItem key={s.key} value={s.key}>
                    {s.label} ({s.employee_min}-{s.employee_max} employees) • {s.cgf_tier}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Generate Button */}
          <div className="flex items-center gap-3">
            <Button
              onClick={handleGenerate}
              disabled={!canGenerate || submitMutation.isPending}
            >
              {submitMutation.isPending ? "Generating..." : "Generate AppBlueprint (IR)"}
            </Button>
            {!sessionId && (
              <span className="text-sm text-muted-foreground">
                Start a session to begin.
              </span>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Generated Blueprint */}
      {generatedBlueprint ? (
        <Card>
          <CardHeader>
            <div className="flex items-center justify-between">
              <div>
                <CardTitle>Generated IR (AppBlueprint)</CardTitle>
                <CardDescription>
                  Blueprint is ready for code generation.
                </CardDescription>
              </div>
              <Button onClick={handleContinueToCodegen} className="gap-2">
                Continue to Code Generation
                <span aria-hidden="true">&rarr;</span>
              </Button>
            </div>
          </CardHeader>
          <CardContent>
            <BlueprintJsonViewer blueprint={generatedBlueprint} />
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardHeader>
            <CardTitle>Generated IR (AppBlueprint)</CardTitle>
            <CardDescription>
              Copy/export this IR to use with backend IR generation endpoints.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-3">
            <Textarea
              value=""
              readOnly
              placeholder="IR will appear here after generation"
              className="min-h-[280px] font-mono text-xs"
            />
          </CardContent>
        </Card>
      )}

      {/* Stats */}
      {generatedStats && (
        <Card>
          <CardHeader>
            <CardTitle>Generation Stats</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold">
                  {(generatedStats.modules_count as number) || 0}
                </div>
                <div className="text-sm text-muted-foreground">Modules</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">
                  {(generatedStats.entities_count as number) || 0}
                </div>
                <div className="text-sm text-muted-foreground">Entities</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">
                  {(generatedStats.endpoints_count as number) || 0}
                </div>
                <div className="text-sm text-muted-foreground">Endpoints</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold">
                  {(generatedStats.generation_time_ms as number) || 0}ms
                </div>
                <div className="text-sm text-muted-foreground">Generation Time</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
