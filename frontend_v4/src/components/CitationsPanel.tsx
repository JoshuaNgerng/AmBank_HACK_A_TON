import { LinkIcon, ExternalLink } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Citation } from '@/types/market';

interface CitationsPanelProps {
  citations: Citation[];
}

export function CitationsPanel({ citations }: CitationsPanelProps) {
  return (
    <Card className="glass-card">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg font-semibold flex items-center gap-2">
            <LinkIcon className="h-5 w-5 text-primary" />
            Evidence & Citations
          </CardTitle>
          <Badge variant="secondary">{citations.length} sources</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[200px] scrollbar-thin">
          <div className="grid gap-2 md:grid-cols-2 lg:grid-cols-3">
            {citations.map((citation, index) => (
              <a
                key={citation.id}
                href={citation.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group flex items-start gap-3 p-3 rounded-lg hover:bg-accent/50 transition-colors border border-transparent hover:border-border"
              >
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-primary/10 text-sm font-medium text-primary">
                  {index + 1}
                </div>
                <div className="flex-1 min-w-0 space-y-1">
                  <div className="flex items-start justify-between gap-2">
                    <h4 className="text-sm font-medium leading-tight group-hover:text-primary transition-colors line-clamp-1">
                      {citation.title}
                    </h4>
                    <ExternalLink className="h-3.5 w-3.5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity shrink-0 mt-0.5" />
                  </div>
                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>{citation.source}</span>
                    <span>·</span>
                    <span>{citation.date}</span>
                  </div>
                </div>
              </a>
            ))}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
