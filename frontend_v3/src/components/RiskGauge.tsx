import { Shield, TrendingUp, TrendingDown, Minus, AlertTriangle, CheckCircle } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { RiskAssessment } from '@/types/market';
import { cn } from '@/lib/utils';

interface RiskGaugeProps {
  assessment: RiskAssessment;
}

function GaugeChart({ score }: { score: number }) {
  const rotation = (score / 100) * 180 - 90;
  const getColor = (s: number) => {
    if (s >= 70) return 'text-positive';
    if (s >= 40) return 'text-warning';
    return 'text-adverse';
  };
  const getLabel = (s: number) => {
    if (s >= 70) return 'Low Risk';
    if (s >= 40) return 'Moderate Risk';
    return 'High Risk';
  };
  const getIcon = (s: number) => {
    if (s >= 70) return CheckCircle;
    if (s >= 40) return AlertTriangle;
    return AlertTriangle;
  };

  const RiskIcon = getIcon(score);

  return (
    <div className="relative flex flex-col items-center">
      <svg viewBox="0 0 200 120" className="w-48 h-28">
        {/* Background arc */}
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="hsl(var(--muted))"
          strokeWidth="12"
          strokeLinecap="round"
        />
        {/* Gradient arc segments */}
        <defs>
          <linearGradient id="riskGradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="hsl(var(--adverse))" />
            <stop offset="50%" stopColor="hsl(var(--warning))" />
            <stop offset="100%" stopColor="hsl(var(--positive))" />
          </linearGradient>
        </defs>
        <path
          d="M 20 100 A 80 80 0 0 1 180 100"
          fill="none"
          stroke="url(#riskGradient)"
          strokeWidth="12"
          strokeLinecap="round"
          strokeDasharray={`${(score / 100) * 251.2} 251.2`}
        />
        {/* Needle */}
        <g transform={`rotate(${rotation} 100 100)`}>
          <line
            x1="100"
            y1="100"
            x2="100"
            y2="35"
            stroke="hsl(var(--foreground))"
            strokeWidth="3"
            strokeLinecap="round"
          />
          <circle cx="100" cy="100" r="8" fill="hsl(var(--foreground))" />
          <circle cx="100" cy="100" r="4" fill="hsl(var(--background))" />
        </g>
      </svg>
      <div className="absolute bottom-0 text-center">
        <div className={cn("text-4xl font-bold", getColor(score))}>{score}</div>
        <div className="flex items-center gap-1.5 mt-1">
          <RiskIcon className={cn("h-4 w-4", getColor(score))} />
          <span className={cn("text-sm font-medium", getColor(score))}>{getLabel(score)}</span>
        </div>
      </div>
    </div>
  );
}

const trendIcons = {
  up: TrendingUp,
  down: TrendingDown,
  stable: Minus,
};

export function RiskGauge({ assessment }: RiskGaugeProps) {
  return (
    <Card className="glass-card h-full">
      <CardHeader className="pb-3">
        <CardTitle className="text-lg font-semibold flex items-center gap-2">
          <Shield className="h-5 w-5 text-primary" />
          Risk Assessment
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex justify-center pt-2">
          <GaugeChart score={assessment.overallScore} />
        </div>

        <div className="space-y-2">
          {assessment.factors.map((factor) => {
            const TrendIcon = trendIcons[factor.trend];
            const getTrendColor = () => {
              if (factor.trend === 'up' && factor.name.includes('Risk')) return 'text-adverse';
              if (factor.trend === 'up') return 'text-positive';
              if (factor.trend === 'down' && factor.name.includes('Risk')) return 'text-positive';
              if (factor.trend === 'down') return 'text-adverse';
              return 'text-muted-foreground';
            };

            return (
              <div key={factor.name} className="flex items-center gap-3">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-xs font-medium truncate">{factor.name}</span>
                    <div className="flex items-center gap-1">
                      <span className="text-xs text-muted-foreground">{factor.score}</span>
                      <TrendIcon className={cn("h-3 w-3", getTrendColor())} />
                    </div>
                  </div>
                  <div className="h-1.5 bg-muted rounded-full overflow-hidden">
                    <div
                      className={cn(
                        "h-full rounded-full transition-all",
                        factor.score >= 70 ? 'bg-positive' : factor.score >= 40 ? 'bg-warning' : 'bg-adverse'
                      )}
                      style={{ width: `${factor.score}%` }}
                    />
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        <div className="pt-2 border-t border-border">
          <p className="text-xs text-muted-foreground leading-relaxed">{assessment.summary}</p>
          <p className="text-[10px] text-muted-foreground mt-2">
            Last updated: {new Date(assessment.lastUpdated).toLocaleString()}
          </p>
        </div>
      </CardContent>
    </Card>
  );
}
