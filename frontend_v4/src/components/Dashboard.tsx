import { Building2, Shield, AlertTriangle, CheckCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { DashboardData } from '@/types/market';
import { ExecutiveSummaryPanel } from './ExecutiveSummaryPanel';
import { BusinessStrategyPanel } from './BusinessStrategyPanel';
import { GrowthPotentialPanel } from './GrowthPotentialPanel';
import { SentimentPanel } from './SentimentPanel';
import { RiskGauge } from './RiskGauge';
import { CitationsPanel } from './CitationsPanel';

interface DashboardProps {
  data: DashboardData;
}

export function Dashboard({ data }: DashboardProps) {
  const getRiskBadgeVariant = (riskLevel: string) => {
    switch (riskLevel) {
      case 'low':
        return 'default';
      case 'moderate':
        return 'secondary';
      case 'high':
        return 'destructive';
      default:
        return 'secondary';
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      {/* Company Header */}
      <div className="flex items-center justify-between flex-wrap gap-4">
        <div className="flex items-center gap-4">
          <div className="flex h-14 w-14 items-center justify-center rounded-2xl bg-primary/10">
            <Building2 className="h-7 w-7 text-primary" />
          </div>
          <div>
            <h1 className="text-2xl font-bold">{data.company.name}</h1>
            <div className="flex items-center gap-2 mt-1">
              <Badge variant="secondary">{data.company.companyId}</Badge>
              <span className="text-sm text-muted-foreground">{data.company.industry}</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant={getRiskBadgeVariant(data.executiveSummary.riskLevel)} className="px-3 py-1">
            <Shield className="h-4 w-4 mr-1" />
            {data.executiveSummary.riskLevel.charAt(0).toUpperCase() + data.executiveSummary.riskLevel.slice(1)} Risk
          </Badge>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-muted">
            <span className="text-sm text-muted-foreground">
              Confidence: {Math.round(data.executiveSummary.confidence * 100)}%
            </span>
          </div>
          <div className="text-xs text-muted-foreground">
            As of: {new Date(data.asOf).toLocaleDateString()}
          </div>
        </div>
      </div>

      {/* Executive Summary */}
      <ExecutiveSummaryPanel summary={data.executiveSummary} />

      {/* Strategy & Growth */}
      <div className="grid gap-6 lg:grid-cols-2">
        <BusinessStrategyPanel strategies={data.details.businessStrategy} />
        <GrowthPotentialPanel growth={data.details.growthPotential} />
      </div>

      {/* Analysis Grid */}
      <div className="grid gap-6 lg:grid-cols-2">
        <SentimentPanel analysis={data.details.sentimentAnalysis} />
        <RiskGauge assessment={data.details.riskAssessment} />
      </div>

      {/* Citations */}
      <CitationsPanel citations={data.citations} />
    </div>
  );
}
