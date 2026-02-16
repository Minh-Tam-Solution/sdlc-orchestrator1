/**
 * Demo Page - SDLC Orchestrator Landing
 *
 * @module frontend/landing/src/app/demo/page
 * @description Interactive demo showcasing platform features with i18n support
 * @sdlc SDLC 6.0.6 Universal Framework
 * @status Sprint 60 - i18n Localization
 */

"use client";

import { Header, Footer } from "@/components/landing";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { useTranslations } from "next-intl";

export default function DemoPage() {
  const t = useTranslations("demo");

  const demoSections = [
    {
      key: "gateEngine",
      icon: "🛡️",
      href: "/demo/gate-engine"
    },
    {
      key: "evidenceVault",
      icon: "📦",
      href: "/demo/evidence-vault"
    },
    {
      key: "aiCodegen",
      icon: "🤖",
      href: "/demo/ai-codegen"
    },
    {
      key: "dashboard",
      icon: "📊",
      href: "/demo/dashboard"
    }
  ];

  return (
    <>
      <Header />
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-4xl mx-auto">
            {/* Page Header */}
            <div className="text-center mb-12">
              <Badge className="mb-4">{t("badge")}</Badge>
              <h1 className="text-display font-bold tracking-tight text-foreground mb-4">
                {t("title")}
              </h1>
              <p className="text-body-lg text-muted-foreground max-w-2xl mx-auto">
                {t("subtitle")}
              </p>
            </div>

            {/* Video Preview Section */}
            <div className="mb-16">
              <div className="aspect-video bg-gradient-to-br from-primary/10 to-accent/10 rounded-lg flex items-center justify-center border-2 border-dashed border-muted-foreground/20">
                <div className="text-center p-8">
                  <div className="w-20 h-20 rounded-full bg-primary/20 flex items-center justify-center mx-auto mb-4">
                    <svg
                      className="w-10 h-10 text-primary"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path d="M8 5v14l11-7z" />
                    </svg>
                  </div>
                  <p className="text-lg font-medium text-foreground mb-2">
                    Demo Video Coming Soon
                  </p>
                  <p className="text-body-sm text-muted-foreground">
                    Explore the interactive demos below while we prepare the full video walkthrough.
                  </p>
                </div>
              </div>
            </div>

            {/* Demo Sections Grid */}
            <div className="grid md:grid-cols-2 gap-6 mb-16">
              {demoSections.map((section) => (
                <Card key={section.key} className="hover:border-primary/50 transition-colors">
                  <CardHeader>
                    <CardTitle className="flex items-center gap-3">
                      <span className="text-2xl">{section.icon}</span>
                      {t(`sections.${section.key}.title`)}
                    </CardTitle>
                    <CardDescription>
                      {t(`sections.${section.key}.description`)}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Button asChild variant="outline" className="w-full">
                      <Link href={section.href}>
                        {t(`sections.${section.key}.cta`)}
                      </Link>
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* SDLC Framework Preview */}
            <div className="mb-16">
              <h2 className="text-heading-1 font-bold text-foreground text-center mb-6">
                SDLC 6.0.6 Framework
              </h2>
              <div className="bg-muted/30 rounded-lg p-6 overflow-x-auto">
                <pre className="text-body-sm text-muted-foreground whitespace-pre font-mono">
{`┌────────────────────────────────────────────────────────────────────┐
│                    SDLC 6.0.6 - 10 STAGES                          │
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
            </div>

            {/* Quality Gates Preview */}
            <div className="mb-16">
              <h2 className="text-heading-1 font-bold text-foreground text-center mb-6">
                4-Gate Quality Pipeline
              </h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gradient-to-br from-blue-500/10 to-blue-600/20 rounded-lg p-4 text-center border border-blue-500/20">
                  <div className="text-3xl mb-2">G0</div>
                  <div className="font-medium text-foreground">Foundation</div>
                  <div className="text-body-sm text-muted-foreground">Problem Definition</div>
                </div>
                <div className="bg-gradient-to-br from-green-500/10 to-green-600/20 rounded-lg p-4 text-center border border-green-500/20">
                  <div className="text-3xl mb-2">G1</div>
                  <div className="font-medium text-foreground">Planning</div>
                  <div className="text-body-sm text-muted-foreground">Requirements</div>
                </div>
                <div className="bg-gradient-to-br from-yellow-500/10 to-yellow-600/20 rounded-lg p-4 text-center border border-yellow-500/20">
                  <div className="text-3xl mb-2">G2</div>
                  <div className="font-medium text-foreground">Design</div>
                  <div className="text-body-sm text-muted-foreground">Architecture</div>
                </div>
                <div className="bg-gradient-to-br from-purple-500/10 to-purple-600/20 rounded-lg p-4 text-center border border-purple-500/20">
                  <div className="text-3xl mb-2">G3</div>
                  <div className="font-medium text-foreground">Build</div>
                  <div className="text-body-sm text-muted-foreground">Implementation</div>
                </div>
              </div>
            </div>

            {/* CTA Section */}
            <div className="bg-gradient-to-r from-primary/10 via-accent/10 to-primary/10 rounded-lg p-8 text-center">
              <h2 className="text-heading-1 font-bold text-foreground mb-2">
                {t("cta.title")}
              </h2>
              <p className="text-body text-muted-foreground mb-6">
                {t("cta.description")}
              </p>
              <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Button asChild size="lg">
                  <Link href="/register">{t("cta.primary")}</Link>
                </Button>
                <Button asChild variant="outline" size="lg">
                  <Link href="/#pricing">{t("cta.secondary")}</Link>
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
