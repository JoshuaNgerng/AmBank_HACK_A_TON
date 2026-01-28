import { AlertTriangle, TrendingUp, CheckCircle, ExternalLink } from 'lucide-react';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Insight } from '@/types/market';
import { cn } from '@/lib/utils';

interface InsightCardProps {
  insight: Insight;
}

const insightConfig = {
  adverse: {
    icon: AlertTriangle,
    bgClass: 'bg-adverse/10',
    textClass: 'text-adverse',
    badgeClass: 'bg-adverse/10 text-adverse border-adverse/20',
    label: 'Adverse',
  },
  positive: {
    icon: CheckCircle,
    bgClass: 'bg-positive/10',
    textClass: 'text-positive',
    badgeClass: 'bg-positive/10 text-positive border-positive/20',
    label: 'Positive',
  },
  trend: {
    icon: TrendingUp,
    bgClass: 'bg-primary/10',
    textClass: 'text-primary',
    badgeClass: 'bg-primary/10 text-primary border-primary/20',
    label: 'Trend',
  },
};

export function InsightCard({ insight }: InsightCardProps) {
  const config = insightConfig[insight.type];
  const Icon = config.icon;

  return (
    <Card className="glass-card hover:shadow-[var(--shadow-elevated)] transition-all duration-200 group">
      <CardContent className="p-5">
        <div className="flex items-start gap-4">
          <div className={cn("flex h-10 w-10 shrink-0 items-center justify-center rounded-xl", config.bgClass)}>
            <Icon className={cn("h-5 w-5", config.textClass)} />
          </div>
          <div className="flex-1 min-w-0 space-y-2">
            <div className="flex items-start justify-between gap-3">
              <h4 className="font-medium leading-tight">{insight.title}</h4>
              <Badge variant="outline" className={cn("shrink-0", config.badgeClass)}>
                {config.label}
              </Badge>
            </div>
            <p className="text-sm text-muted-foreground line-clamp-2">{insight.description}</p>
            <div className="flex items-center justify-between pt-1">
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <span>{insight.date}</span>
                <span>·</span>
                <span>{insight.source}</span>
              </div>
              <a
                href={insight.sourceUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 text-xs text-primary hover:underline opacity-0 group-hover:opacity-100 transition-opacity"
              >
                View Source
                <ExternalLink className="h-3 w-3" />
              </a>
            </div>
            <div className="flex items-center gap-2">
              <div className="h-1.5 flex-1 bg-muted rounded-full overflow-hidden">
                <div
                  className={cn("h-full rounded-full transition-all", config.bgClass.replace('/10', ''))}
                  style={{ width: `${insight.confidence * 100}%` }}
                />
              </div>
              <span className="text-xs text-muted-foreground">{Math.round(insight.confidence * 100)}% confidence</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
