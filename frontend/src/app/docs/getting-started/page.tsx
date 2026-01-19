/**
 * Getting Started Docs Page - SDLC Orchestrator Landing
 *
 * @module frontend/landing/src/app/docs/getting-started/page
 * @description Comprehensive getting started guide with i18n support
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 60 - i18n Localization
 */

"use client";

import { Header, Footer } from "@/components/landing";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { useTranslations } from "next-intl";

export default function GettingStartedPage() {
  const t = useTranslations("docs");

  // Success stories from SDLC 5.1.3
  const successStories = [
    { name: "BFlow", result: "$43M revenue, 827:1 ROI", industry: "SaaS" },
    { name: "NQH-Bot", result: "15B+ VND value", industry: "AI Assistant" },
    { name: "MTEP", result: "<30 min PaaS deployment", industry: "DevOps" },
  ];

  return (
    <>
      <Header />
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-4xl mx-auto">
            {/* Page Header */}
            <div className="mb-12">
              <Badge className="mb-4">{t("gettingStarted.badge")}</Badge>
              <h1 className="text-display font-bold tracking-tight text-foreground mb-4">
                {t("gettingStarted.title")}
              </h1>
              <p className="text-body-lg text-muted-foreground">
                {t("gettingStarted.subtitle")}
              </p>
            </div>

            {/* Success Stories */}
            <div className="grid grid-cols-3 gap-4 mb-12">
              {successStories.map((story) => (
                <div key={story.name} className="bg-muted/50 rounded-lg p-4 text-center">
                  <div className="font-bold text-foreground">{story.name}</div>
                  <div className="text-body-sm text-primary">{story.result}</div>
                  <div className="text-body-sm text-muted-foreground">{story.industry}</div>
                </div>
              ))}
            </div>

            {/* Quick Start Steps */}
            <div className="space-y-8 mb-16">
              {/* Step 1 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-3">
                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-bold">
                      1
                    </span>
                    {t("gettingStarted.step1.title")}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-body text-muted-foreground mb-4">
                    {t("gettingStarted.step1.description")}
                  </p>
                  <div className="bg-muted/50 rounded-lg p-4 mb-4 font-mono text-sm">
                    <code>https://sdlc.nhatquangholding.com/register</code>
                  </div>
                  <Button asChild>
                    <Link href="/register">{t("gettingStarted.step1.cta")}</Link>
                  </Button>
                </CardContent>
              </Card>

              {/* Step 2 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-3">
                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-bold">
                      2
                    </span>
                    {t("gettingStarted.step2.title")}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-body text-muted-foreground mb-4">
                    {t("gettingStarted.step2.description")}
                  </p>
                  <ul className="space-y-2 text-body-sm text-muted-foreground">
                    <li className="flex items-start gap-2">
                      <span className="text-success font-bold">✓</span>
                      {t("gettingStarted.step2.feature1")}
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-success font-bold">✓</span>
                      {t("gettingStarted.step2.feature2")}
                    </li>
                    <li className="flex items-start gap-2">
                      <span className="text-success font-bold">✓</span>
                      {t("gettingStarted.step2.feature3")}
                    </li>
                  </ul>
                </CardContent>
              </Card>

              {/* Step 3 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-3">
                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-bold">
                      3
                    </span>
                    {t("gettingStarted.step3.title")}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-body text-muted-foreground mb-4">
                    {t("gettingStarted.step3.description")}
                  </p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-muted/50 rounded-lg p-3 text-center">
                      <div className="text-2xl mb-1">🛡️</div>
                      <div className="text-body-sm font-medium">G0</div>
                      <div className="text-body-sm text-muted-foreground">Foundation</div>
                    </div>
                    <div className="bg-muted/50 rounded-lg p-3 text-center">
                      <div className="text-2xl mb-1">📋</div>
                      <div className="text-body-sm font-medium">G1</div>
                      <div className="text-body-sm text-muted-foreground">Planning</div>
                    </div>
                    <div className="bg-muted/50 rounded-lg p-3 text-center">
                      <div className="text-2xl mb-1">🏗️</div>
                      <div className="text-body-sm font-medium">G2</div>
                      <div className="text-body-sm text-muted-foreground">Design</div>
                    </div>
                    <div className="bg-muted/50 rounded-lg p-3 text-center">
                      <div className="text-2xl mb-1">🚀</div>
                      <div className="text-body-sm font-medium">G3-G4</div>
                      <div className="text-body-sm text-muted-foreground">Build</div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {/* Step 4 */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-3">
                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-bold">
                      4
                    </span>
                    {t("gettingStarted.step4.title")}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-body text-muted-foreground mb-4">
                    {t("gettingStarted.step4.description")}
                  </p>
                  <div className="bg-muted/50 rounded-lg p-4 font-mono text-sm overflow-x-auto">
                    <pre>{`# VS Code Extension
code --install-extension sdlc-orchestrator

# CLI Tool
pip install sdlcctl

# Verify installation
sdlcctl --version`}</pre>
                  </div>
                </CardContent>
              </Card>

              {/* Step 5 */}
              <Card className="border-accent">
                <CardHeader>
                  <CardTitle className="flex items-center gap-3">
                    <span className="flex items-center justify-center w-8 h-8 rounded-full bg-accent text-accent-foreground text-sm font-bold">
                      5
                    </span>
                    {t("gettingStarted.step5.title")}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-body text-muted-foreground mb-4">
                    {t("gettingStarted.step5.description")}
                  </p>
                  <Button asChild size="lg" className="w-full sm:w-auto">
                    <Link href="/checkout?plan=founder">{t("gettingStarted.step5.cta")}</Link>
                  </Button>
                </CardContent>
              </Card>
            </div>

            {/* SDLC Framework Overview */}
            <div className="mb-16">
              <h2 className="text-heading-1 font-bold text-foreground mb-6">
                {t("gettingStarted.framework.title")}
              </h2>
              <div className="bg-muted/30 rounded-lg p-6 overflow-x-auto mb-6">
                <pre className="text-body-sm text-muted-foreground whitespace-pre">
{`┌────────────────────────────────────────────────────────────────────┐
│                    SDLC 5.1.2 - 10 STAGES                          │
├────────────────────────────────────────────────────────────────────┤
│  00 FOUNDATION  → Why are we building this?                        │
│  01 PLANNING    → What exactly do we need?                         │
│  02 DESIGN      → How will we build it?                            │
│  03 INTEGRATE   → How does it connect?                             │
│  04 BUILD       → Are we building right?                           │
│  05 TEST        → Does it work correctly?                          │
│  06 DEPLOY      → Can we ship safely?                              │
│  07 OPERATE     → Is it running reliably?                          │
│  08 COLLABORATE → Is the team effective?                           │
│  09 GOVERN      → Are we compliant?                                │
├────────────────────────────────────────────────────────────────────┤
│  CLASSIFICATION: LITE | STANDARD | PREMIUM | ENTERPRISE            │
└────────────────────────────────────────────────────────────────────┘`}
                </pre>
              </div>

              {/* 4-Tier Classification */}
              <div className="grid md:grid-cols-4 gap-4">
                <Card className="border-l-4 border-l-blue-500">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">LITE</CardTitle>
                  </CardHeader>
                  <CardContent className="text-body-sm text-muted-foreground">
                    <p>1-2 weeks</p>
                    <p>1-3 people</p>
                    <p>Essential gates</p>
                  </CardContent>
                </Card>
                <Card className="border-l-4 border-l-green-500">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">STANDARD</CardTitle>
                  </CardHeader>
                  <CardContent className="text-body-sm text-muted-foreground">
                    <p>1-3 months</p>
                    <p>3-7 people</p>
                    <p>Core gates (G0-G6)</p>
                  </CardContent>
                </Card>
                <Card className="border-l-4 border-l-yellow-500">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">PREMIUM</CardTitle>
                  </CardHeader>
                  <CardContent className="text-body-sm text-muted-foreground">
                    <p>3-6 months</p>
                    <p>7-15 people</p>
                    <p>All gates (G0-G9)</p>
                  </CardContent>
                </Card>
                <Card className="border-l-4 border-l-purple-500">
                  <CardHeader className="pb-2">
                    <CardTitle className="text-sm">ENTERPRISE</CardTitle>
                  </CardHeader>
                  <CardContent className="text-body-sm text-muted-foreground">
                    <p>6+ months</p>
                    <p>15+ people</p>
                    <p>Enhanced reviews</p>
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Key Features */}
            <div className="mb-16">
              <h2 className="text-heading-1 font-bold text-foreground mb-6">
                {t("gettingStarted.features.title")}
              </h2>
              <div className="grid md:grid-cols-2 gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span className="text-2xl">🛡️</span>
                      {t("gettingStarted.features.gates.title")}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-body-sm text-muted-foreground">
                    {t("gettingStarted.features.gates.description")}
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span className="text-2xl">📦</span>
                      {t("gettingStarted.features.vault.title")}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-body-sm text-muted-foreground">
                    {t("gettingStarted.features.vault.description")}
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span className="text-2xl">🤖</span>
                      {t("gettingStarted.features.ai.title")}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-body-sm text-muted-foreground">
                    {t("gettingStarted.features.ai.description")}
                  </CardContent>
                </Card>
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span className="text-2xl">📊</span>
                      {t("gettingStarted.features.reports.title")}
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="text-body-sm text-muted-foreground">
                    {t("gettingStarted.features.reports.description")}
                  </CardContent>
                </Card>
              </div>
            </div>

            {/* Help Section */}
            <div className="p-6 bg-secondary/50 rounded-lg">
              <h3 className="text-heading-3 font-semibold text-foreground mb-2">
                {t("gettingStarted.help.title")}
              </h3>
              <p className="text-body text-muted-foreground mb-4">
                {t("gettingStarted.help.description")}
              </p>
              <div className="flex flex-wrap gap-4">
                <Button asChild variant="outline">
                  <Link href="https://discord.gg/sdlc-orchestrator" target="_blank" rel="noopener noreferrer">
                    {t("gettingStarted.help.discord")}
                  </Link>
                </Button>
                <Button asChild variant="outline">
                  <Link href="https://calendly.com/sdlc-orchestrator" target="_blank" rel="noopener noreferrer">
                    {t("gettingStarted.help.call")}
                  </Link>
                </Button>
                <Button asChild variant="outline">
                  <Link href="mailto:support@sdlc-orchestrator.com">
                    {t("gettingStarted.help.email")}
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
