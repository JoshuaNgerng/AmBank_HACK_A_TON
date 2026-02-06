import { Brain, TrendingUp, TrendingDown, Minus, Info } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
import { SentimentAnalysis, DegreeLevel } from '@/types/market';
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

const mapDegreeToKey = (degree: DegreeLevel): keyof typeof levelConfig => {
  const normalized = degree.toLowerCase(); // convert input to lowercase

  switch (normalized) {
    case 'very low':
      return 'very_low';
    case 'low':
      return 'low';
    case 'moderate':
      return 'medium';
    case 'high':
      return 'high';
    case 'very high':
      return 'very_high';
    default:
      return 'medium';
  }
};

const confidenceConfig = {
  very_low: { color: 'text-adverse', bg: 'bg-adverse/10', label: 'Very low confidence' },
  low: { color: 'text-adverse', label: 'Low confidence' },
  medium: { color: 'text-warning', label: 'Medium confidence' },
  high: { color: 'text-positive', label: 'High confidence' },
  very_high: { color: 'text-positive', bg: 'bg-positive/10', label: 'Very high confidence' },
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
            {analysis.map((item, index) => {
              console.log(item.sentimentLabel)
              console.log(item.confidenceLevel)
              const config = sentimentConfig[item.sentimentLabel];
              const confConfig = confidenceConfig[mapDegreeToKey(item.confidenceLevel)];
              const Icon = config.icon;
              const scorePercent = Math.abs(item.sentimentScore * 100);

              return (
                <AccordionItem
                  key={index}
                  value={`sentiment-${index}`}
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
                          <span className="text-xs text-muted-foreground">{scorePercent.toFixed(0)}%</span>
                          <TooltipProvider>
                            <Tooltip>
                              <TooltipTrigger>
                                <Badge variant="outline" className={cn("text-[10px] px-1.5 py-0", confConfig.color)}>
                                  {confConfig.label}
                                </Badge>
                              </TooltipTrigger>
                              <TooltipContent>
                                <p>Analysis confidence level</p>
                              </TooltipContent>
                            </Tooltip>
                          </TooltipProvider>
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
                      {item.supportingSignals.length > 0 && (
                        <div>
                          <h5 className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">Supporting Signals</h5>
                          <div className="flex flex-wrap gap-1">
                            {item.supportingSignals.map((signal, signalIndex) => (
                              <Badge key={signalIndex} variant="secondary" className="text-[10px]">
                                {signal}
                              </Badge>
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
