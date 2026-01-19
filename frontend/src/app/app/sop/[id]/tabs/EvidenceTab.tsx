/**
 * SOP Evidence Tab - Lazy loaded component
 * @status Sprint 68 - Budget optimization
 */

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Link as LinkIcon } from "lucide-react";
import type { SOPEvidence } from "@/lib/types/sop";

interface EvidenceTabProps {
  evidence?: SOPEvidence[];
}

export default function EvidenceTab({ evidence }: EvidenceTabProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Attached Evidence</CardTitle>
        <CardDescription>Supporting documents and references</CardDescription>
      </CardHeader>
      <CardContent>
        {evidence && evidence.length > 0 ? (
          <div className="space-y-2">
            {evidence.map((ev) => (
              <div
                key={ev.id}
                className="flex items-center justify-between p-3 rounded-lg border"
              >
                <div className="flex items-center gap-3">
                  <FileText className="h-5 w-5 text-muted-foreground" />
                  <div>
                    <p className="font-medium">{ev.title}</p>
                    <p className="text-xs text-muted-foreground">
                      {ev.type} • {new Date(ev.uploaded_at).toLocaleDateString()}
                    </p>
                  </div>
                </div>
                <Button variant="ghost" size="sm">
                  View
                </Button>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center justify-center py-8 text-muted-foreground">
            <LinkIcon className="h-8 w-8 mb-2" />
            <p>No evidence attached</p>
            <Button variant="outline" size="sm" className="mt-2">
              Attach Evidence
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
