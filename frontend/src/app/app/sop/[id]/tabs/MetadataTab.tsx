/**
 * SOP Metadata Tab - Lazy loaded component
 * @status Sprint 68 - Budget optimization
 */

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import type { SOPDetail } from "@/lib/types/sop";

interface MetadataTabProps {
  sop: SOPDetail;
}

export default function MetadataTab({ sop }: MetadataTabProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>SOP Metadata</CardTitle>
        <CardDescription>Technical details and identifiers</CardDescription>
      </CardHeader>
      <CardContent>
        <dl className="grid grid-cols-2 gap-4">
          <div>
            <dt className="text-sm font-medium text-muted-foreground">SOP ID</dt>
            <dd className="font-mono text-sm">{sop.sop_id}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-muted-foreground">MRP ID</dt>
            <dd className="font-mono text-sm">{sop.mrp_id}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-muted-foreground">AI Model</dt>
            <dd className="text-sm">{sop.ai_model}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-muted-foreground">Generation Time</dt>
            <dd className="text-sm">{sop.generation_time_ms}ms</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-muted-foreground">Completeness Score</dt>
            <dd className="text-sm">{sop.completeness_score}%</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-muted-foreground">Created</dt>
            <dd className="text-sm">{new Date(sop.created_at).toLocaleString()}</dd>
          </div>
          <div>
            <dt className="text-sm font-medium text-muted-foreground">Updated</dt>
            <dd className="text-sm">{new Date(sop.updated_at).toLocaleString()}</dd>
          </div>
          <div className="col-span-2">
            <dt className="text-sm font-medium text-muted-foreground">SHA256 Hash</dt>
            <dd className="font-mono text-xs break-all">{sop.sha256_hash}</dd>
          </div>
        </dl>
      </CardContent>
    </Card>
  );
}
