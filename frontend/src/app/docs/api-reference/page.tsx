/**
 * API Reference Page - SDLC Orchestrator Landing
 *
 * @module frontend/landing/src/app/docs/api-reference/page
 * @description API documentation with endpoint reference
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

export default function ApiReferencePage() {
  const t = useTranslations("docs");

  const endpoints = [
    {
      category: "Authentication",
      icon: "🔐",
      apis: [
        { method: "POST", path: "/api/v1/auth/login", description: "Login with email/password" },
        { method: "POST", path: "/api/v1/auth/register", description: "Create new account" },
        { method: "POST", path: "/api/v1/auth/refresh", description: "Refresh access token" },
        { method: "POST", path: "/api/v1/auth/logout", description: "Logout and invalidate tokens" },
        { method: "GET", path: "/api/v1/auth/me", description: "Get current user info" },
        { method: "POST", path: "/api/v1/auth/oauth/{provider}", description: "OAuth login (github/google)" },
      ]
    },
    {
      category: "Projects",
      icon: "📁",
      apis: [
        { method: "GET", path: "/api/v1/projects", description: "List all projects" },
        { method: "POST", path: "/api/v1/projects", description: "Create new project" },
        { method: "GET", path: "/api/v1/projects/{id}", description: "Get project details" },
        { method: "PUT", path: "/api/v1/projects/{id}", description: "Update project" },
        { method: "DELETE", path: "/api/v1/projects/{id}", description: "Delete project" },
        { method: "GET", path: "/api/v1/projects/{id}/members", description: "List project members" },
        { method: "POST", path: "/api/v1/projects/{id}/sync", description: "Sync with GitHub" },
      ]
    },
    {
      category: "Gates",
      icon: "🛡️",
      apis: [
        { method: "GET", path: "/api/v1/gates", description: "List all gate definitions" },
        { method: "GET", path: "/api/v1/projects/{id}/gates", description: "Get project gates" },
        { method: "POST", path: "/api/v1/gates/evaluate", description: "Evaluate gate policies (OPA)" },
        { method: "GET", path: "/api/v1/gates/{id}/status", description: "Get gate status" },
        { method: "POST", path: "/api/v1/gates/{id}/approve", description: "Approve gate" },
        { method: "POST", path: "/api/v1/gates/{id}/reject", description: "Reject gate" },
        { method: "POST", path: "/api/v1/gates/{id}/override", description: "Request gate override" },
      ]
    },
    {
      category: "Evidence",
      icon: "📦",
      apis: [
        { method: "GET", path: "/api/v1/evidence", description: "List evidence artifacts" },
        { method: "POST", path: "/api/v1/evidence/upload", description: "Upload evidence file (S3)" },
        { method: "GET", path: "/api/v1/evidence/{id}", description: "Get evidence details" },
        { method: "GET", path: "/api/v1/evidence/{id}/download", description: "Download evidence file" },
        { method: "GET", path: "/api/v1/evidence/{id}/versions", description: "Get version history" },
        { method: "PUT", path: "/api/v1/evidence/{id}/state", description: "Update evidence state" },
      ]
    },
    {
      category: "AI Codegen",
      icon: "🤖",
      apis: [
        { method: "POST", path: "/api/v1/codegen/generate", description: "Generate code from spec (SSE)" },
        { method: "GET", path: "/api/v1/codegen/sessions", description: "List codegen sessions" },
        { method: "GET", path: "/api/v1/codegen/sessions/{id}", description: "Get session details" },
        { method: "POST", path: "/api/v1/codegen/validate", description: "Validate generated code" },
        { method: "POST", path: "/api/v1/codegen/preview", description: "Preview code changes" },
        { method: "POST", path: "/api/v1/codegen/apply", description: "Apply generated code" },
      ]
    },
    {
      category: "Admin",
      icon: "⚙️",
      apis: [
        { method: "GET", path: "/api/v1/admin/users", description: "List all users" },
        { method: "POST", path: "/api/v1/admin/users", description: "Create user" },
        { method: "PUT", path: "/api/v1/admin/users/{id}", description: "Update user" },
        { method: "DELETE", path: "/api/v1/admin/users/{id}", description: "Deactivate user" },
        { method: "GET", path: "/api/v1/admin/audit", description: "View audit logs" },
      ]
    },
  ];

  const getMethodColor = (method: string) => {
    switch (method) {
      case "GET": return "bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300";
      case "POST": return "bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300";
      case "PUT": return "bg-yellow-100 text-yellow-700 dark:bg-yellow-900 dark:text-yellow-300";
      case "DELETE": return "bg-red-100 text-red-700 dark:bg-red-900 dark:text-red-300";
      default: return "bg-gray-100 text-gray-700";
    }
  };

  return (
    <>
      <Header />
      <main className="min-h-screen bg-background">
        <div className="container mx-auto px-4 py-16 md:py-24">
          <div className="max-w-5xl mx-auto">
            {/* Page Header */}
            <div className="mb-12">
              <Badge className="mb-4">{t("apiReference.badge")}</Badge>
              <h1 className="text-display font-bold tracking-tight text-foreground mb-4">
                {t("apiReference.title")}
              </h1>
              <p className="text-body-lg text-muted-foreground">
                {t("apiReference.subtitle")}
              </p>
            </div>

            {/* Base URL */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>{t("apiReference.baseUrl.title")}</CardTitle>
                <CardDescription>{t("apiReference.baseUrl.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg p-4 font-mono text-sm">
                  <code>https://sdlc.nhatquangholding.com/api/v1</code>
                </div>
              </CardContent>
            </Card>

            {/* Authentication */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>{t("apiReference.auth.title")}</CardTitle>
                <CardDescription>{t("apiReference.auth.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="bg-muted rounded-lg p-4 font-mono text-sm overflow-x-auto">
                  <pre>{`Authorization: Bearer <access_token>

# Example cURL request
curl -X GET "https://sdlc.nhatquangholding.com/api/v1/projects" \\
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIs..." \\
  -H "Content-Type: application/json"`}</pre>
                </div>
              </CardContent>
            </Card>

            {/* Endpoints */}
            <div className="space-y-8">
              {endpoints.map((category) => (
                <Card key={category.category}>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <span className="text-2xl">{category.icon}</span>
                      {category.category}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {category.apis.map((api, index) => (
                        <div
                          key={index}
                          className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 p-3 bg-muted/50 rounded-lg"
                        >
                          <span className={`inline-flex items-center justify-center px-2 py-1 rounded text-xs font-bold w-16 ${getMethodColor(api.method)}`}>
                            {api.method}
                          </span>
                          <code className="text-sm font-mono flex-1">{api.path}</code>
                          <span className="text-body-sm text-muted-foreground">{api.description}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            {/* Rate Limits */}
            <Card className="mt-8">
              <CardHeader>
                <CardTitle>{t("apiReference.rateLimits.title")}</CardTitle>
                <CardDescription>{t("apiReference.rateLimits.description")}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid md:grid-cols-3 gap-4">
                  <div className="p-4 bg-muted/50 rounded-lg text-center">
                    <div className="text-2xl font-bold text-foreground">1000</div>
                    <div className="text-body-sm text-muted-foreground">Requests/hour (Free)</div>
                  </div>
                  <div className="p-4 bg-muted/50 rounded-lg text-center">
                    <div className="text-2xl font-bold text-foreground">10,000</div>
                    <div className="text-body-sm text-muted-foreground">Requests/hour (Founder)</div>
                  </div>
                  <div className="p-4 bg-muted/50 rounded-lg text-center">
                    <div className="text-2xl font-bold text-foreground">Unlimited</div>
                    <div className="text-body-sm text-muted-foreground">Enterprise</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* CTA */}
            <div className="mt-12 p-6 bg-secondary/50 rounded-lg text-center">
              <h3 className="text-heading-3 font-semibold text-foreground mb-2">
                {t("apiReference.cta.title")}
              </h3>
              <p className="text-body text-muted-foreground mb-4">
                {t("apiReference.cta.description")}
              </p>
              <div className="flex flex-wrap gap-4 justify-center">
                <Button asChild>
                  <Link href="/register">{t("apiReference.cta.getApiKey")}</Link>
                </Button>
                <Button asChild variant="outline">
                  <Link href="https://sdlc.nhatquangholding.com/api/v1/docs" target="_blank" rel="noopener noreferrer">
                    {t("apiReference.cta.openApiDocs")}
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
