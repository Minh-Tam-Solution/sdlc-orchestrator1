/**
 * VS Code Extension Page - SDLC Orchestrator Landing
 *
 * @module frontend/landing/src/app/docs/vscode-extension/page
 * @description VS Code extension documentation and features
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 60 - Documentation
 */

"use client";

import { Header, Footer } from "@/components/landing";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { useTranslations } from "next-intl";

export default function VscodeExtensionPage() {
  const t = useTranslations("docs");

  const features = [
    {
      icon: "🎯",
      title: "Project Explorer",
      description: "View and manage projects directly from VS Code sidebar. Quick access to gates, evidence, and settings."
    },
    {
      icon: "🛡️",
      title: "Gate Status",
      description: "Real-time gate status display. See which gates are passed, pending, or blocked at a glance."
    },
    {
      icon: "📤",
      title: "Evidence Upload",
      description: "Upload evidence files with Cmd+Shift+E shortcut. Automatic file type detection and SHA256 hashing."
    },
    {
      icon: "🤖",
      title: "AI Codegen",
      description: "Generate code from specifications using IR-based codegen. Inline suggestions with SSE streaming."
    },
    {
      icon: "📋",
      title: "Template Generator",
      description: "Create BRD, PRD, ADR, and other templates with AI assistance. Vietnamese and English support."
    },
    {
      icon: "⚠️",
      title: "Violation Alerts",
      description: "Real-time notifications for SDLC violations. Quick fixes and auto-remediation suggestions."
    },
    {
      icon: "🔄",
      title: "GitHub Sync",
      description: "Automatic sync with GitHub repository. Track PRs, issues, and CI/CD status in real-time."
    },
    {
      icon: "📊",
      title: "DORA Metrics",
      description: "View deployment frequency, lead time, MTTR, and change failure rate directly in VS Code."
    },
  ];

  const shortcuts = [
    { keys: "Cmd+Shift+P", action: "Open Command Palette" },
    { keys: "Cmd+Shift+E", action: "Upload Evidence" },
    { keys: "Cmd+Shift+G", action: "Open Gates Panel" },
    { keys: "Cmd+Shift+V", action: "Validate SDLC Structure" },
    { keys: "Cmd+Alt+C", action: "Generate Code (AI)" },
    { keys: "Cmd+Alt+T", action: "Generate Template" },
    { keys: "Cmd+Alt+R", action: "Resume Code Generation" },
    { keys: "Cmd+Shift+S", action: "Sync with GitHub" },
  ];

  return (
    <>
      <Header />
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-4xl mx-auto">
            {/* Page Header */}
            <div className="mb-12">
              <Badge className="mb-4">{t("vscodeExtension.badge")}</Badge>
              <h1 className="text-display font-bold tracking-tight text-foreground mb-4">
                {t("vscodeExtension.title")}
              </h1>
              <p className="text-body-lg text-muted-foreground">
                {t("vscodeExtension.subtitle")}
              </p>
            </div>

            {/* Installation */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="text-2xl">📦</span>
                  {t("vscodeExtension.installation.title")}
                </CardTitle>
                <CardDescription>{t("vscodeExtension.installation.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <p className="text-body-sm text-muted-foreground mb-2">Option 1: VS Code Marketplace</p>
                    <div className="flex gap-2">
                      <Button asChild>
                        <Link href="https://marketplace.visualstudio.com/items?itemName=mtsolution.sdlc-orchestrator" target="_blank" rel="noopener noreferrer">
                          Install from Marketplace
                        </Link>
                      </Button>
                    </div>
                  </div>
                  <div>
                    <p className="text-body-sm text-muted-foreground mb-2">Option 2: Command Line</p>
                    <div className="bg-muted rounded-lg p-4 font-mono text-sm">
                      <code>code --install-extension sdlc-orchestrator.sdlc-orchestrator</code>
                    </div>
                  </div>
                  <div>
                    <p className="text-body-sm text-muted-foreground mb-2">Option 3: VSIX File</p>
                    <div className="bg-muted rounded-lg p-4 font-mono text-sm">
                      <code>code --install-extension sdlc-orchestrator-1.0.0.vsix</code>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Quick Setup */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="text-2xl">🚀</span>
                  {t("vscodeExtension.setup.title")}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <ol className="space-y-4 list-decimal list-inside">
                  <li className="text-body text-muted-foreground">
                    <span className="font-medium text-foreground">Install the extension</span> from VS Code Marketplace
                  </li>
                  <li className="text-body text-muted-foreground">
                    <span className="font-medium text-foreground">Open Command Palette</span> (Cmd+Shift+P) and run &quot;SDLC: Login&quot;
                  </li>
                  <li className="text-body text-muted-foreground">
                    <span className="font-medium text-foreground">Authenticate</span> with your SDLC Orchestrator account
                  </li>
                  <li className="text-body text-muted-foreground">
                    <span className="font-medium text-foreground">Select your project</span> from the sidebar
                  </li>
                  <li className="text-body text-muted-foreground">
                    <span className="font-medium text-foreground">Start using</span> gates, evidence, and AI codegen features
                  </li>
                </ol>
              </CardContent>
            </Card>

            {/* Features */}
            <div className="mb-8">
              <h2 className="text-heading-1 font-bold text-foreground mb-6">
                {t("vscodeExtension.features.title")}
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                {features.map((feature, index) => (
                  <Card key={index}>
                    <CardHeader className="pb-2">
                      <CardTitle className="text-lg flex items-center gap-2">
                        <span className="text-2xl">{feature.icon}</span>
                        {feature.title}
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <p className="text-body-sm text-muted-foreground">{feature.description}</p>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            {/* Keyboard Shortcuts */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="text-2xl">⌨️</span>
                  {t("vscodeExtension.shortcuts.title")}
                </CardTitle>
                <CardDescription>{t("vscodeExtension.shortcuts.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  {shortcuts.map((shortcut, index) => (
                    <div key={index} className="flex items-center justify-between p-3 bg-muted/50 rounded-lg">
                      <code className="bg-muted px-2 py-1 rounded text-sm font-mono">{shortcut.keys}</code>
                      <span className="text-body-sm text-muted-foreground">{shortcut.action}</span>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Settings */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="text-2xl">⚙️</span>
                  {t("vscodeExtension.settings.title")}
                </CardTitle>
                <CardDescription>{t("vscodeExtension.settings.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg p-4 font-mono text-sm overflow-x-auto">
                  <pre>{`// settings.json
{
  "sdlc-orchestrator.apiUrl": "https://sdlc.nhatquangholding.com/api/v1",
  "sdlc-orchestrator.autoValidate": true,
  "sdlc-orchestrator.showGateStatus": true,
  "sdlc-orchestrator.showViolations": true,
  "sdlc-orchestrator.language": "vi",
  "sdlc-orchestrator.codegen.model": "qwen3-coder:30b",
  "sdlc-orchestrator.codegen.maxTokens": 4096
}`}</pre>
                </div>
              </CardContent>
            </Card>

            {/* Screenshot Preview */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>{t("vscodeExtension.preview.title")}</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="aspect-video bg-gradient-to-br from-primary/10 to-accent/10 rounded-lg flex items-center justify-center border-2 border-dashed border-muted-foreground/20">
                  <div className="text-center p-8">
                    <div className="text-4xl mb-4">🖥️</div>
                    <p className="text-body text-muted-foreground">
                      Extension screenshots coming soon
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Help */}
            <div className="p-6 bg-secondary/50 rounded-lg">
              <h3 className="text-heading-3 font-semibold text-foreground mb-2">
                {t("vscodeExtension.help.title")}
              </h3>
              <p className="text-body text-muted-foreground mb-4">
                {t("vscodeExtension.help.description")}
              </p>
              <div className="flex flex-wrap gap-4">
                <Button asChild variant="outline">
                  <Link href="https://github.com/sdlc-orchestrator/vscode-extension" target="_blank" rel="noopener noreferrer">
                    GitHub Repository
                  </Link>
                </Button>
                <Button asChild variant="outline">
                  <Link href="https://marketplace.visualstudio.com/items?itemName=sdlc-orchestrator" target="_blank" rel="noopener noreferrer">
                    VS Code Marketplace
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
