import { FileText, Newspaper, ExternalLink, ChevronRight } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Filing } from '@/types/market';
import { cn } from '@/lib/utils';

interface FilingsPanelProps {
  filings: Filing[];
}

function FilingItem({ filing }: { filing: Filing }) {
  return (
    <a
      href={filing.sourceUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="group flex items-start gap-3 p-3 rounded-lg hover:bg-accent/50 transition-colors"
    >
      <div className={cn(
        "flex h-9 w-9 shrink-0 items-center justify-center rounded-lg",
        filing.type === 'bursa' ? 'bg-primary/10' : 'bg-warning/10'
      )}>
        {filing.type === 'bursa' ? (
          <FileText className="h-4 w-4 text-primary" />
        ) : (
          <Newspaper className="h-4 w-4 text-warning" />
        )}
      </div>
      <div className="flex-1 min-w-0 space-y-1">
        <div className="flex items-start justify-between gap-2">
          <h4 className="text-sm font-medium leading-tight group-hover:text-primary transition-colors">
            {filing.title}
          </h4>
          <ChevronRight className="h-4 w-4 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
        </div>
        <p className="text-xs text-muted-foreground line-clamp-2">{filing.summary}</p>
        <div className="flex items-center gap-2">
          <Badge variant="secondary" className="text-[10px] px-1.5 py-0">
            {filing.category}
          </Badge>
          <span className="text-xs text-muted-foreground">{filing.date}</span>
        </div>
      </div>
    </a>
  );
}

export function FilingsPanel({ filings }: FilingsPanelProps) {
  const bursaFilings = filings.filter((f) => f.type === 'bursa');
  const newsFilings = filings.filter((f) => f.type === 'news');

  return (
    <Card className="glass-card h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <FileText className="h-5 w-5 text-primary" />
          Filings & News
        </CardTitle>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="bursa" className="w-full">
          <TabsList className="grid w-full grid-cols-2 mb-4">
            <TabsTrigger value="bursa" className="text-sm">
              Bursa Filings ({bursaFilings.length})
            </TabsTrigger>
            <TabsTrigger value="news" className="text-sm">
              News ({newsFilings.length})
            </TabsTrigger>
          </TabsList>
          <TabsContent value="bursa" className="mt-0">
            <ScrollArea className="h-[280px] scrollbar-thin">
              <div className="space-y-1">
                {bursaFilings.map((filing) => (
                  <FilingItem key={filing.id} filing={filing} />
                ))}
              </div>
            </ScrollArea>
          </TabsContent>
          <TabsContent value="news" className="mt-0">
            <ScrollArea className="h-[280px] scrollbar-thin">
              <div className="space-y-1">
                {newsFilings.map((filing) => (
                  <FilingItem key={filing.id} filing={filing} />
                ))}
              </div>
            </ScrollArea>
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
