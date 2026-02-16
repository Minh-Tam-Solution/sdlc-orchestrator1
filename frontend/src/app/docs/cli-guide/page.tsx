/**
 * CLI Guide Page - SDLC Orchestrator Landing
 *
 * @module frontend/landing/src/app/docs/cli-guide/page
 * @description CLI tool (sdlcctl) documentation
 * @sdlc SDLC 6.0.6 Universal Framework
 * @status Sprint 60 - Documentation
 */

"use client";

import { Header, Footer } from "@/components/landing";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { useTranslations } from "next-intl";

export default function CliGuidePage() {
  const t = useTranslations("docs");

  const commands = [
    {
      command: "sdlcctl login",
      description: "Authenticate with SDLC Orchestrator",
      example: `sdlcctl login
# Or use API key
sdlcctl login --api-key YOUR_API_KEY
# OAuth login
sdlcctl login --oauth github`
    },
    {
      command: "sdlcctl init",
      description: "Initialize SDLC structure in current directory",
      example: `sdlcctl init
# With classification
sdlcctl init --classification STANDARD
# From template
sdlcctl init --template e-commerce-vi`
    },
    {
      command: "sdlcctl validate",
      description: "Validate project structure against SDLC 6.0.6",
      example: `sdlcctl validate
# Validate specific directory
sdlcctl validate ./docs
# Strict mode (fail on warnings)
sdlcctl validate --strict`
    },
    {
      command: "sdlcctl fix",
      description: "Auto-fix SDLC structure violations",
      example: `sdlcctl fix
# Dry run (preview changes)
sdlcctl fix --dry-run
# Fix specific issues
sdlcctl fix --only missing-folders`
    },
    {
      command: "sdlcctl report",
      description: "Generate compliance report",
      example: `sdlcctl report
# Output formats: json, html, pdf
sdlcctl report --format html --output report.html
# Include AI analysis
sdlcctl report --ai-insights`
    },
    {
      command: "sdlcctl gate",
      description: "Evaluate quality gates",
      example: `# Check gate status
sdlcctl gate status

# Evaluate specific gate
sdlcctl gate evaluate G2

# Request override
sdlcctl gate override G2 --reason "Emergency hotfix"

# List all gates
sdlcctl gate list`
    },
    {
      command: "sdlcctl evidence",
      description: "Manage evidence artifacts",
      example: `# Upload evidence
sdlcctl evidence upload ./brd.pdf --gate G1

# List evidence
sdlcctl evidence list --project my-project

# Download evidence
sdlcctl evidence download <id> --output ./downloads/`
    },
    {
      command: "sdlcctl codegen",
      description: "AI code generation",
      example: `# Generate from spec
sdlcctl codegen ./spec.yaml --output ./src

# Interactive mode (magic mode)
sdlcctl codegen --interactive

# Preview changes
sdlcctl codegen ./spec.yaml --preview`
    },
    {
      command: "sdlcctl sync",
      description: "Sync with remote repository",
      example: `# Sync project
sdlcctl sync

# Force sync (overwrite local)
sdlcctl sync --force

# Sync specific branch
sdlcctl sync --branch develop`
    },
  ];

  return (
    <>
      <Header />
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-4xl mx-auto">
            {/* Page Header */}
            <div className="mb-12">
              <Badge className="mb-4">{t("cliGuide.badge")}</Badge>
              <h1 className="text-display font-bold tracking-tight text-foreground mb-4">
                {t("cliGuide.title")}
              </h1>
              <p className="text-body-lg text-muted-foreground">
                {t("cliGuide.subtitle")}
              </p>
            </div>

            {/* Installation */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="text-2xl">📦</span>
                  {t("cliGuide.installation.title")}
                </CardTitle>
                <CardDescription>{t("cliGuide.installation.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <p className="text-body-sm text-muted-foreground mb-2">pip (Python 3.9+):</p>
                    <div className="bg-muted rounded-lg p-4 font-mono text-sm">
                      <code>pip install sdlcctl</code>
                    </div>
                  </div>
                  <div>
                    <p className="text-body-sm text-muted-foreground mb-2">pipx (isolated):</p>
                    <div className="bg-muted rounded-lg p-4 font-mono text-sm">
                      <code>pipx install sdlcctl</code>
                    </div>
                  </div>
                  <div>
                    <p className="text-body-sm text-muted-foreground mb-2">Verify installation:</p>
                    <div className="bg-muted rounded-lg p-4 font-mono text-sm">
                      <code>sdlcctl --version</code>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Start */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="text-2xl">🚀</span>
                  {t("cliGuide.quickStart.title")}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg p-4 font-mono text-sm overflow-x-auto">
                  <pre>{`# 1. Login to your account
sdlcctl login

# 2. Initialize SDLC structure
cd your-project
sdlcctl init --classification STANDARD

# 3. Validate project structure
sdlcctl validate

# 4. Generate compliance report
sdlcctl report --format html

# 5. Check gate status
sdlcctl gate status`}</pre>
                </div>
              </CardContent>
            </Card>

            {/* Commands */}
            <div className="mb-8">
              <h2 className="text-heading-1 font-bold text-foreground mb-6">
                {t("cliGuide.commands.title")}
              </h2>
              <div className="space-y-4">
                {commands.map((cmd, index) => (
                  <Card key={index}>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-lg font-mono">{cmd.command}</CardTitle>
                      <CardDescription>{cmd.description}</CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="bg-muted rounded-lg p-4 font-mono text-sm overflow-x-auto">
                        <pre>{cmd.example}</pre>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Configuration */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="text-2xl">⚙️</span>
                  {t("cliGuide.config.title")}
                </CardTitle>
                <CardDescription>{t("cliGuide.config.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg p-4 font-mono text-sm overflow-x-auto">
                  <pre>{`# ~/.sdlcctl/config.yaml
api_url: https://sdlc.nhatquangholding.com/api/v1
default_classification: STANDARD
output_format: json

# Project-level: .sdlcctl.yaml
project_id: proj_abc123
classification: PREMIUM
gates:
  G0: required
  G1: required
  G2: required
  G3: optional`}</pre>
                </div>
              </CardContent>
            </Card>

            {/* Pre-commit Hook */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="text-2xl">🔗</span>
                  {t("cliGuide.precommit.title")}
                </CardTitle>
                <CardDescription>{t("cliGuide.precommit.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg p-4 font-mono text-sm overflow-x-auto">
                  <pre>{`# .pre-commit-config.yaml
repos:
  - repo: https://github.com/sdlc-orchestrator/sdlcctl
    rev: v1.0.0
    hooks:
      - id: sdlcctl-validate
        name: SDLC Structure Validation
        entry: sdlcctl validate --strict
        language: system
        pass_filenames: false`}</pre>
                </div>
              </CardContent>
            </Card>

            {/* Help */}
            <div className="p-6 bg-secondary/50 rounded-lg">
              <h3 className="text-heading-3 font-semibold text-foreground mb-2">
                {t("cliGuide.help.title")}
              </h3>
              <p className="text-body text-muted-foreground mb-4">
                {t("cliGuide.help.description")}
              </p>
              <div className="flex flex-wrap gap-4">
                <Button asChild variant="outline">
                  <Link href="https://github.com/sdlc-orchestrator/sdlcctl" target="_blank" rel="noopener noreferrer">
                    GitHub Repository
                  </Link>
                </Button>
                <Button asChild variant="outline">
                  <Link href="https://pypi.org/project/sdlcctl/" target="_blank" rel="noopener noreferrer">
                    PyPI Package
                  </Link>
                </Button>
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
