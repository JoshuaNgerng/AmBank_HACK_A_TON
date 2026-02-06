import { Target, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion';
import { BusinessStrategy } from '@/types/market';
import { cn } from '@/lib/utils';

interface BusinessStrategyPanelProps {
  strategies: BusinessStrategy[];
}

const trendIcons = {
  up: TrendingUp,
  down: TrendingDown,
  stable: Minus,
};

const trendColors = {
  up: 'text-positive',
  down: 'text-adverse',
  stable: 'text-muted-foreground',
};

const mapDegreeToKey = (val: string): string => {
  switch (val) {
    case 'up':
      return 'up';
    case 'down':
      return 'down';
    case 'stable':
      return 'stable';
    default:
      return 'down'
  }
};

export function BusinessStrategyPanel({ strategies }: BusinessStrategyPanelProps) {
  return (
    <Card className="glass-card h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Target className="h-5 w-5 text-primary" />
          Business Strategy
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[320px] scrollbar-thin pr-2">
          <Accordion type="single" collapsible className="space-y-2">
            {strategies.map((strategy, index) => {
              const TrendIcon = trendIcons[mapDegreeToKey(strategy.trend)];
            if (strategies.length === 0) {
              return (
                <Card className="glass-card h-full">
                  <CardHeader className="pb-3">
                    <CardTitle className="text-lg font-semibold flex items-center gap-2">
                      <Target className="h-5 w-5 text-primary" />
                      Business Strategy
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="flex items-center justify-center h-[320px]">
                    <p className="text-sm text-muted-foreground">
                      No business strategies available
                    </p>
                  </CardContent>
                </Card>
              );
            }
              return (
                <AccordionItem
                  key={index}
                  value={`strategy-${index}`}
                  className="border border-border rounded-lg px-4 data-[state=open]:bg-accent/30"
                >
                  <AccordionTrigger className="hover:no-underline py-3">
                    <div className="flex items-center gap-3 text-left flex-1">
                      <div className="flex-1 min-w-0">
                        <p className="font-medium text-sm truncate">{strategy.theme}</p>
                        <div className="flex items-center gap-2 mt-0.5">
                          <Badge variant="outline" className="text-[10px] px-1.5 py-0">
                            {Math.round(strategy.consistencyScore * 100)}% consistent
                          </Badge>
                          {/* console.log(strategy.trend) */}
                          <div className={cn("flex items-center gap-1", trendColors[mapDegreeToKey(strategy.trend)])}>
                            <TrendIcon className="h-3 w-3" />
                            <span className="text-xs capitalize">{strategy.trend}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </AccordionTrigger>
                  <AccordionContent className="pb-4">
                    <div className="space-y-3 pt-2">
                      <h5 className="text-xs font-medium text-muted-foreground uppercase tracking-wide">
                        Signals ({strategy.signals.length})
                      </h5>
                      <div className="space-y-2">
                        {strategy.signals.map((signal, signalIndex) => (
                          <div
                            key={signalIndex}
                            className="p-3 rounded-lg bg-muted/50 space-y-1"
                          >
                            <div className="flex items-center justify-between">
                              <Badge variant="secondary" className="text-[10px]">
                                {signal.year}
                              </Badge>
                              <span className="text-xs text-muted-foreground">
                                {Math.round(signal.confidence * 100)}% confidence
                              </span>
                            </div>
                            <p className="text-sm">{signal.summary}</p>
                            <p className="text-xs text-muted-foreground">
                              Source: {signal.source}
                            </p>
                          </div>
                        ))}
                      </div>
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
