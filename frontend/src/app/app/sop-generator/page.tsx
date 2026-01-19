/**
 * SOP Generator Page - Next.js App Router
 * @module frontend/landing/src/app/app/sop-generator/page
 * @status Sprint 67 - SOP Migration
 * @description AI-powered Standard Operating Procedure generator
 */
"use client";

import { useState } from "react";
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
import { Textarea } from "@/components/ui/textarea";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Badge } from "@/components/ui/badge";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Loader2, FileText, Sparkles, Clock, CheckCircle } from "lucide-react";
import { useGenerateSOP } from "@/hooks/useSOP";
import { SOP_TYPE_META, type SOPType, type GeneratedSOPResponse } from "@/lib/types/sop";

export default function SOPGeneratorPage() {
  const router = useRouter();

  // Form state
  const [sopType, setSopType] = useState<SOPType | "">("");
  const [workflowDescription, setWorkflowDescription] = useState("");
  const [additionalContext, setAdditionalContext] = useState("");
  const [targetAudience, setTargetAudience] = useState("");

  // Generated result
  const [generatedSOP, setGeneratedSOP] = useState<GeneratedSOPResponse | null>(null);

  // Mutation
  const generateMutation = useGenerateSOP();

  const canGenerate = sopType && workflowDescription.trim().length >= 50;

  const handleGenerate = async () => {
    if (!canGenerate || !sopType) return;

    try {
      const result = await generateMutation.mutateAsync({
        sop_type: sopType,
        workflow_description: workflowDescription,
        additional_context: additionalContext || undefined,
        target_audience: targetAudience || undefined,
      });

      setGeneratedSOP(result);
    } catch (error) {
      console.error("Failed to generate SOP:", error);
    }
  };

  const handleViewSOP = () => {
    if (generatedSOP) {
      router.push(`/app/sop/${generatedSOP.sop_id}`);
    }
  };

  const handleReset = () => {
    setSopType("");
    setWorkflowDescription("");
    setAdditionalContext("");
    setTargetAudience("");
    setGeneratedSOP(null);
    generateMutation.reset();
  };

  return (
    <div className="space-y-6">
      {/* Breadcrumb */}
      <nav className="flex items-center gap-2 text-sm text-muted-foreground">
        <Link href="/app" className="hover:text-foreground">
          Dashboard
        </Link>
        <span>/</span>
        <span className="text-foreground">SOP Generator</span>
      </nav>

      {/* Page header */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <Sparkles className="h-8 w-8 text-primary" />
            SOP Generator
          </h1>
          <p className="text-muted-foreground mt-1">
            Generate AI-powered Standard Operating Procedures for your workflows.
          </p>
        </div>
        <Link href="/app/sop-history">
          <Button variant="outline">
            <Clock className="h-4 w-4 mr-2" />
            View History
          </Button>
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Input Form */}
        <Card>
          <CardHeader>
            <CardTitle>Workflow Details</CardTitle>
            <CardDescription>
              Describe your workflow and we&apos;ll generate a comprehensive SOP.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* SOP Type */}
            <div className="space-y-2">
              <Label>SOP Type *</Label>
              <Select
                value={sopType}
                onValueChange={(v) => setSopType(v as SOPType)}
                disabled={generateMutation.isPending}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Select SOP type" />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(SOP_TYPE_META).map(([key, meta]) => (
                    <SelectItem key={key} value={key}>
                      <div className="flex items-center gap-2">
                        <span>{meta.label}</span>
                        <span className="text-xs text-muted-foreground">
                          - {meta.description}
                        </span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Workflow Description */}
            <div className="space-y-2">
              <Label>Workflow Description * (min 50 characters)</Label>
              <Textarea
                value={workflowDescription}
                onChange={(e) => setWorkflowDescription(e.target.value)}
                placeholder="Describe the workflow, process, or procedure you want to document. Include key steps, stakeholders, and any critical requirements..."
                className="min-h-[150px]"
                disabled={generateMutation.isPending}
              />
              <p className="text-xs text-muted-foreground">
                {workflowDescription.length}/50 characters minimum
              </p>
            </div>

            {/* Target Audience */}
            <div className="space-y-2">
              <Label>Target Audience (optional)</Label>
              <Input
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
                placeholder="e.g., DevOps Engineers, Security Team, All Staff"
                disabled={generateMutation.isPending}
              />
            </div>

            {/* Additional Context */}
            <div className="space-y-2">
              <Label>Additional Context (optional)</Label>
              <Textarea
                value={additionalContext}
                onChange={(e) => setAdditionalContext(e.target.value)}
                placeholder="Any additional requirements, constraints, or compliance frameworks to consider..."
                className="min-h-[100px]"
                disabled={generateMutation.isPending}
              />
            </div>

            {/* Actions */}
            <div className="flex items-center gap-3">
              <Button
                onClick={handleGenerate}
                disabled={!canGenerate || generateMutation.isPending}
                className="flex-1"
              >
                {generateMutation.isPending ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4 mr-2" />
                    Generate SOP
                  </>
                )}
              </Button>
              {generatedSOP && (
                <Button variant="outline" onClick={handleReset}>
                  Reset
                </Button>
              )}
            </div>

            {/* Error */}
            {generateMutation.error && (
              <div className="p-3 rounded-md bg-red-50 text-red-800 text-sm">
                {generateMutation.error.message}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Preview */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Generated SOP
            </CardTitle>
            <CardDescription>
              Preview of the generated Standard Operating Procedure.
            </CardDescription>
          </CardHeader>
          <CardContent>
            {generatedSOP ? (
              <div className="space-y-4">
                {/* SOP Header */}
                <div className="p-4 rounded-lg bg-muted/50 space-y-2">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-lg">{generatedSOP.title}</h3>
                    <Badge variant="outline">{generatedSOP.version}</Badge>
                  </div>
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <span>Type: {SOP_TYPE_META[generatedSOP.sop_type]?.label}</span>
                    <span>Score: {generatedSOP.completeness_score}%</span>
                    <span>Time: {generatedSOP.generation_time_ms}ms</span>
                  </div>
                </div>

                {/* SOP Content Preview */}
                <ScrollArea className="h-[400px] rounded-lg border p-4">
                  <div className="prose prose-sm max-w-none dark:prose-invert">
                    <h4>Purpose</h4>
                    <p className="text-muted-foreground">{generatedSOP.purpose}</p>

                    <h4>Scope</h4>
                    <p className="text-muted-foreground">{generatedSOP.scope}</p>

                    <h4>Roles & Responsibilities</h4>
                    <p className="text-muted-foreground whitespace-pre-wrap">
                      {generatedSOP.roles}
                    </p>

                    <h4>Procedure</h4>
                    <div className="text-muted-foreground whitespace-pre-wrap">
                      {generatedSOP.procedure}
                    </div>

                    <h4>Quality Criteria</h4>
                    <p className="text-muted-foreground">{generatedSOP.quality_criteria}</p>
                  </div>
                </ScrollArea>

                {/* Actions */}
                <div className="flex items-center gap-3">
                  <Button onClick={handleViewSOP} className="flex-1">
                    <CheckCircle className="h-4 w-4 mr-2" />
                    View Full SOP
                  </Button>
                </div>

                {/* Metadata */}
                <div className="text-xs text-muted-foreground">
                  <p>SOP ID: {generatedSOP.sop_id}</p>
                  <p>AI Model: {generatedSOP.ai_model}</p>
                  <p>Hash: {generatedSOP.sha256_hash.slice(0, 16)}...</p>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-[400px] text-muted-foreground">
                {generateMutation.isPending ? (
                  <>
                    <Loader2 className="h-12 w-12 animate-spin mb-4" />
                    <p>Generating your SOP...</p>
                    <p className="text-xs mt-1">This may take 10-30 seconds</p>
                  </>
                ) : (
                  <>
                    <FileText className="h-12 w-12 mb-4" />
                    <p>Fill in the form and click Generate</p>
                    <p className="text-xs mt-1">Your SOP preview will appear here</p>
                  </>
                )}
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
