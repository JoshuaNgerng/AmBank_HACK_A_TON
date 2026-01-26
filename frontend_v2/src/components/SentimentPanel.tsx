import { Brain, TrendingUp, TrendingDown, Minus, ExternalLink } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { SentimentAnalysis } from '@/types/market';
import { cn } from '@/lib/utils';

interface SentimentPanelProps {
  analysis: SentimentAnalysis[];
}

const sentimentConfig = {
  positive: {
    icon: TrendingUp,
    color: 'text-positive',
    bg: 'bg-positive/10',
    label: 'Positive',
  },
  negative: {
    icon: TrendingDown,
    color: 'text-adverse',
    bg: 'bg-adverse/10',
    label: 'Negative',
  },
  neutral: {
    icon: Minus,
    color: 'text-neutral',
    bg: 'bg-muted',
    label: 'Neutral',
  },
};

export function SentimentPanel({ analysis }: SentimentPanelProps) {
  return (
    <Card className="glass-card h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Brain className="h-5 w-5 text-primary" />
          Sentiment Analysis
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[320px] scrollbar-thin pr-2">
          <Accordion type="single" collapsible className="space-y-2">
            {analysis.map((item) => {
              const config = sentimentConfig[item.sentiment];
              const Icon = config.icon;
              const scorePercent = Math.abs(item.score * 100);

              return (
                <AccordionItem
                  key={item.id}
                  value={item.id}
                  className="border border-border rounded-lg px-4 data-[state=open]:bg-accent/30"
                >
                  <AccordionTrigger className="hover:no-underline py-3">
                    <div className="flex items-center gap-3 text-left">
                      <div className={cn("flex h-8 w-8 items-center justify-center rounded-lg", config.bg)}>
                        <Icon className={cn("h-4 w-4", config.color)} />
                      </div>
                      <div>
                        <p className="font-medium text-sm">{item.topic}</p>
                        <div className="flex items-center gap-2 mt-0.5">
                          <Badge variant="outline" className={cn("text-[10px] px-1.5 py-0", config.color)}>
                            {config.label}
                          </Badge>
                          <span className="text-xs text-muted-foreground">{scorePercent.toFixed(0)}% confidence</span>
                        </div>
                      </div>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="pb-4">
                    <div className="space-y-3 pt-2">
                      <div>
                        <h5 className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-1">Rationale</h5>
                        <p className="text-sm">{item.rationale}</p>
                      </div>
                      {item.citations.length > 0 && (
                        <div>
                          <h5 className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Citations</h5>
                          <div className="space-y-1.5">
                            {item.citations.map((citation) => (
                              <a
                                key={citation.id}
                                href={citation.url}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="flex items-center gap-2 text-xs text-primary hover:underline"
                              >
                                <ExternalLink className="h-3 w-3" />
                                {citation.title} ({citation.source})
                              </a>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </AccordionContent>
                </AccordionItem>
              );
            })}
          </Accordion>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
