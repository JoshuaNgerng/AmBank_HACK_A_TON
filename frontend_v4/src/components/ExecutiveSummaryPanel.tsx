import { FileText, CheckCircle, AlertTriangle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { ExecutiveSummary } from '@/types/market';
import { cn } from '@/lib/utils';

interface ExecutiveSummaryPanelProps {
  summary: ExecutiveSummary;
}

export function ExecutiveSummaryPanel({ summary }: ExecutiveSummaryPanelProps) {
  return (
    <Card className="glass-card">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <FileText className="h-5 w-5 text-primary" />
          Executive Summary
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground leading-relaxed">{summary.overview}</p>

        <div className="grid gap-4 md:grid-cols-2">
          {/* Key Positives */}
          <div className="space-y-2">
            <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide flex items-center gap-2">
              <CheckCircle className="h-4 w-4 text-positive" />
              Key Positives
            </h4>
            <ul className="space-y-1.5">
              {summary.keyPositives.map((positive, index) => (
                <li key={index} className="flex items-start gap-2 text-sm">
                  <span className="text-positive mt-1">•</span>
                  <span>{positive}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Key Concerns */}
          <div className="space-y-2">
            <h4 className="text-xs font-medium text-muted-foreground uppercase tracking-wide flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-adverse" />
              Key Concerns
            </h4>
            <ul className="space-y-1.5">
              {summary.keyConcerns.map((concern, index) => (
                <li key={index} className="flex items-start gap-2 text-sm">
                  <span className="text-adverse mt-1">•</span>
                  <span>{concern}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
