/**
 * SOP Revisions Tab - Lazy loaded component
 * @status Sprint 68 - Budget optimization
 */

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { History } from "lucide-react";
import type { SOPRevision } from "@/lib/types/sop";

interface RevisionsTabProps {
  revisions?: SOPRevision[];
}

export default function RevisionsTab({ revisions }: RevisionsTabProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Revision History</CardTitle>
        <CardDescription>Track changes made to this SOP</CardDescription>
      </CardHeader>
      <CardContent>
        {revisions && revisions.length > 0 ? (
          <div className="space-y-4">
            {revisions.map((rev) => (
              <div
                key={rev.revision}
                className="flex items-start gap-4 p-4 rounded-lg border"
              >
                <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary text-primary-foreground text-sm font-medium">
                  {rev.revision}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between">
                    <p className="font-medium">v{rev.version}</p>
                    <p className="text-sm text-muted-foreground">
                      {new Date(rev.created_at).toLocaleString()}
                    </p>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    by {rev.author_name}
                  </p>
                  <p className="text-sm mt-1">{rev.change_summary}</p>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
            <History className="h-8 w-8 mb-2" />
            <p>No revisions yet</p>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
