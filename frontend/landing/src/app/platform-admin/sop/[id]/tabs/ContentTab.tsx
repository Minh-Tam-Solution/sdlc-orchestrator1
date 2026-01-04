/**
 * SOP Content Tab - Lazy loaded component
 * @status Sprint 68 - Budget optimization
 */

import { Card, CardContent } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { SOPDetail } from "@/lib/types/sop";

interface ContentTabProps {
  sop: SOPDetail;
}

export default function ContentTab({ sop }: ContentTabProps) {
  return (
    <Card>
      <CardContent className="pt-6">
        <ScrollArea className="h-[600px]">
          <div className="prose prose-sm max-w-none dark:prose-invert">
            <h2>Purpose</h2>
            <p>{sop.purpose}</p>

            <h2>Scope</h2>
            <p>{sop.scope}</p>

            <h2>Roles & Responsibilities</h2>
            <div className="whitespace-pre-wrap">{sop.roles}</div>

            <h2>Procedure</h2>
            <div className="whitespace-pre-wrap">{sop.procedure}</div>

            <h2>Quality Criteria</h2>
            <p>{sop.quality_criteria}</p>
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
