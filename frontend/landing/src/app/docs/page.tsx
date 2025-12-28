/**
 * Docs Index Page - SDLC Orchestrator Landing
 *
 * @module frontend/landing/src/app/docs/page
 * @description Documentation index with links to all docs
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 60 - Documentation
 */

"use client";

import { Header, Footer } from "@/components/landing";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { useTranslations } from "next-intl";

export default function DocsIndexPage() {
  const t = useTranslations("docs");

  const docsSections = [
    {
      title: t("index.gettingStarted.title"),
      description: t("index.gettingStarted.description"),
      icon: "🚀",
      href: "/docs/getting-started",
      badge: t("index.gettingStarted.badge")
    },
    {
      title: t("index.apiReference.title"),
      description: t("index.apiReference.description"),
      icon: "📡",
      href: "/docs/api-reference",
      badge: null
    },
    {
      title: t("index.cliGuide.title"),
      description: t("index.cliGuide.description"),
      icon: "💻",
      href: "/docs/cli-guide",
      badge: null
    },
    {
      title: t("index.vscodeExtension.title"),
      description: t("index.vscodeExtension.description"),
      icon: "🔌",
      href: "/docs/vscode-extension",
      badge: null
    },
  ];

  const quickLinks = [
    { label: t("index.quickLinks.register"), href: "/register" },
    { label: t("index.quickLinks.pricing"), href: "/#pricing" },
    { label: t("index.quickLinks.demo"), href: "/demo" },
    { label: t("index.quickLinks.support"), href: "mailto:support@sdlc-orchestrator.com" },
  ];

  return (
    <>
      <Header />
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-4xl mx-auto">
            {/* Page Header */}
            <div className="text-center mb-12">
              <Badge className="mb-4">{t("index.badge")}</Badge>
              <h1 className="text-display font-bold tracking-tight text-foreground mb-4">
                {t("index.title")}
              </h1>
              <p className="text-body-lg text-muted-foreground max-w-2xl mx-auto">
                {t("index.subtitle")}
              </p>
            </div>

            {/* Docs Sections */}
            <div className="grid md:grid-cols-2 gap-6 mb-12">
              {docsSections.map((section) => (
                <Link key={section.href} href={section.href} className="group">
                  <Card className="h-full hover:border-primary/50 transition-colors">
                    <CardHeader>
                      <CardTitle className="flex items-center gap-3">
                        <span className="text-2xl">{section.icon}</span>
                        <span className="group-hover:text-primary transition-colors">
                          {section.title}
                        </span>
                        {section.badge && (
                          <Badge variant="secondary" className="ml-auto">
                            {section.badge}
                          </Badge>
                        )}
                      </CardTitle>
                      <CardDescription>{section.description}</CardDescription>
                    </CardHeader>
                  </Card>
                </Link>
              ))}
            </div>

            {/* SDLC Framework Quick Reference */}
            <Card className="mb-12">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <span className="text-2xl">📋</span>
                  {t("index.framework.title")}
                </CardTitle>
                <CardDescription>{t("index.framework.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
                  {["00 Foundation", "01 Planning", "02 Design", "03 Integrate", "04 Build",
                    "05 Test", "06 Deploy", "07 Operate", "08 Collaborate", "09 Govern"].map((stage) => (
                    <div key={stage} className="bg-muted/50 rounded-lg p-2 text-center text-body-sm">
                      {stage}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Quick Links */}
            <div className="p-6 bg-secondary/50 rounded-lg">
              <h3 className="text-heading-3 font-semibold text-foreground mb-4">
                {t("index.quickLinks.title")}
              </h3>
              <div className="flex flex-wrap gap-4">
                {quickLinks.map((link) => (
                  <Link
                    key={link.href}
                    href={link.href}
                    className="text-body text-primary hover:underline"
                  >
                    {link.label} →
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
