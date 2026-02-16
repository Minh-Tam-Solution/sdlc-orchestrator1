/**
 * Privacy Policy Page - SDLC Orchestrator
 *
 * @module frontend/src/app/privacy/page
 * @description Privacy policy page to prevent 404 errors during OAuth flow
 * @sdlc SDLC 6.0.6 Framework
 * @status Sprint 105 - OAuth Fix
 */

import { Header, Footer } from "@/components/landing";

export default function PrivacyPage() {
  return (
    <>
      <Header />
      <main className="min-h-screen bg-secondary/30 py-16">
        <div className="container mx-auto px-4 max-w-4xl">
          <h1 className="text-4xl font-bold mb-6">Privacy Policy</h1>

          <div className="prose prose-lg max-w-none">
            <p className="text-muted-foreground mb-8">
              Last updated: January 25, 2026
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">Introduction</h2>
            <p>
              SDLC Orchestrator (&quot;we&quot;, &quot;our&quot;, or &quot;us&quot;) is committed to protecting
              your privacy. This Privacy Policy explains how we collect, use, and safeguard
              your information when you use our platform.
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">Information We Collect</h2>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Account Information:</strong> Email, name, and authentication data</li>
              <li><strong>OAuth Data:</strong> When you connect GitHub or Google accounts</li>
              <li><strong>Project Data:</strong> Code, evidence, and audit logs you submit</li>
              <li><strong>Usage Data:</strong> Analytics to improve our services</li>
            </ul>

            <h2 className="text-2xl font-semibold mt-8 mb-4">How We Use Your Information</h2>
            <ul className="list-disc pl-6 space-y-2">
              <li>To provide and maintain our services</li>
              <li>To authenticate your identity</li>
              <li>To improve our platform</li>
              <li>To communicate with you about updates</li>
            </ul>

            <h2 className="text-2xl font-semibold mt-8 mb-4">Data Security</h2>
            <p>
              We implement OWASP ASVS Level 2 security controls including encryption
              at-rest (AES-256) and in-transit (TLS 1.3), secure authentication with
              JWT tokens, and immutable audit logs.
            </p>

            <h2 className="text-2xl font-semibold mt-8 mb-4">Contact Us</h2>
            <p>
              For privacy concerns, contact us at: privacy@nhatquangholding.com
            </p>
          </div>
        </div>
      </main>
      <Footer />
    </>
  );
}
