export default function PrivacyPage() {
  return (
    <div className="container mx-auto p-8">
      <h1 className="text-3xl font-bold mb-4">Privacy Policy</h1>
      <p className="text-muted-foreground">Last updated: January 25, 2026</p>
      
      <section className="mt-6">
        <h2 className="text-2xl font-semibold mb-2">Data Collection</h2>
        <p>SDLC Orchestrator collects minimal data necessary for platform operation.</p>
      </section>

      <section className="mt-6">
        <h2 className="text-2xl font-semibold mb-2">Data Usage</h2>
        <p>Your data is used solely for providing SDLC orchestration services.</p>
      </section>

      <section className="mt-6">
        <h2 className="text-2xl font-semibold mb-2">SOC 2 Compliance</h2>
        <p>We maintain SOC 2 Type II compliance with audit trails and encryption.</p>
      </section>
    </div>
  );
}
