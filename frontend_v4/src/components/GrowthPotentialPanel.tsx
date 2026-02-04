import { Rocket, TrendingUp, AlertCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { ScrollArea } from '@/components/ui/scroll-area';
import { GrowthPotential } from '@/types/market';
import { cn } from '@/lib/utils';

interface GrowthPotentialPanelProps {
  growth: GrowthPotential[];
}

const levelConfig = {
  low: { color: 'text-adverse', bg: 'bg-adverse/10', label: 'Low' },
  medium: { color: 'text-warning', bg: 'bg-warning/10', label: 'Medium' },
  high: { color: 'text-positive', bg: 'bg-positive/10', label: 'High' },
};

export function GrowthPotentialPanel({ growth }: GrowthPotentialPanelProps) {
  return (
    <Card className="glass-card h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Rocket className="h-5 w-5 text-primary" />
          Growth Potential
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-[320px] scrollbar-thin pr-2">
          <div className="space-y-4">
            {growth.map((item, index) => {
              const config = levelConfig[item.growthLevel];

              return (
                <div key={index} className="space-y-4">
                  {/* Score Header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className={cn("flex h-10 w-10 items-center justify-center rounded-lg", config.bg)}>
                        <TrendingUp className={cn("h-5 w-5", config.color)} />
                      </div>
                      <div>
                        <p className={cn("font-semibold", config.color)}>
                          {config.label} Growth Potential
                        </p>
                        <p className="text-xs text-muted-foreground">
                          Score: {Math.round(item.growthScore * 100)}% | Confidence: {Math.round(item.confidence * 100)}%
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Summary */}
                  <p className="text-sm text-muted-foreground">{item.summary}</p>

                  {/* Drivers & Constraints */}
                  <div className="grid gap-4 md:grid-cols-2">
                    {/* Growth Drivers */}
                    <div className="space-y-2">
                      <h5 className="text-xs font-medium text-muted-foreground uppercase tracking-wide flex items-center gap-1">
                        <TrendingUp className="h-3 w-3 text-positive" />
                        Growth Drivers
                      </h5>
                      <ul className="space-y-1">
                        {item.growthDrivers.map((driver, driverIndex) => (
                          <li key={driverIndex} className="flex items-start gap-2 text-sm">
                            <span className="text-positive mt-1">+</span>
                            <span>{driver}</span>
                          </li>
                        ))}
                      </ul>
                    </div>

                    {/* Constraints */}
                    <div className="space-y-2">
                      <h5 className="text-xs font-medium text-muted-foreground uppercase tracking-wide flex items-center gap-1">
                        <AlertCircle className="h-3 w-3 text-adverse" />
                        Constraints
                      </h5>
                      <ul className="space-y-1">
                        {item.constraints.map((constraint, constraintIndex) => (
                          <li key={constraintIndex} className="flex items-start gap-2 text-sm">
                            <span className="text-adverse mt-1">-</span>
                            <span>{constraint}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}
