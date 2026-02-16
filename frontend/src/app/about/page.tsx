/**
 * About Page - SDLC Orchestrator
 *
 * @module frontend/src/app/about/page
 * @description About page to prevent 404 errors during OAuth flow
 * @sdlc SDLC 6.0.6 Framework
 * @status Sprint 105 - OAuth Fix
 */

import { Header, Footer } from "@/components/landing";

export default function AboutPage() {
  return (
    <>
      <Header />
      <main className="min-h-screen bg-secondary/30 py-16">
        <div className="container mx-auto px-4 max-w-4xl">
          <h1 className="text-4xl font-bold mb-6">About SDLC Orchestrator</h1>

          <div className="prose prose-lg max-w-none">
            <p className="text-xl text-muted-foreground mb-8">
              The Operating System for Software 3.0 - Governance-first AI development platform.
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">Our Mission</h2>
            <p>
              Reduce feature waste from 60-70% to less than 30% by enforcing evidence-based
              development practices and governing AI-generated code through quality gates.
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">Key Features</h2>
            <ul className="list-disc pl-6 space-y-2">
              <li>4-Gate Quality Pipeline for AI code validation</li>
              <li>Evidence Vault with immutable audit trail</li>
              <li>Multi-provider AI integration (Ollama, Claude, GPT-4o)</li>
              <li>SDLC 6.0.6 Framework compliance</li>
              <li>Vietnamese SME focus with domain-specific templates</li>
            </ul>

            <h2 className="text-2xl font-semibold mt-8 mb-4">Framework</h2>
            <p>
              Built on SDLC 6.0.6 with 7-Pillar Architecture and AI Governance Principles.
              We don&apos;t compete with AI coding tools - we orchestrate them.
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
