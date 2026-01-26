import { Building2, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { DashboardData } from '@/types/market';
import { InsightCard } from './InsightCard';
import { FilingsPanel } from './FilingsPanel';
import { SentimentPanel } from './SentimentPanel';
import { EntityPanel } from './EntityPanel';
import { RiskGauge } from './RiskGauge';
import { CitationsPanel } from './CitationsPanel';

interface DashboardProps {
  data: DashboardData;
}

export function Dashboard({ data }: DashboardProps) {
  const adverseCount = data.insights.filter((i) => i.type === 'adverse').length;
  const positiveCount = data.insights.filter((i) => i.type === 'positive').length;
  const trendCount = data.insights.filter((i) => i.type === 'trend').length;

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
              <Badge variant="secondary">{data.company.stockCode}</Badge>
              <span className="text-sm text-muted-foreground">{data.company.sector}</span>
              <span className="text-sm text-muted-foreground">·</span>
              <span className="text-sm text-muted-foreground">{data.company.marketCap}</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-adverse/10">
            <AlertTriangle className="h-4 w-4 text-adverse" />
            <span className="text-sm font-medium text-adverse">{adverseCount} Adverse</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-positive/10">
            <CheckCircle className="h-4 w-4 text-positive" />
            <span className="text-sm font-medium text-positive">{positiveCount} Positive</span>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-primary/10">
            <TrendingUp className="h-4 w-4 text-primary" />
            <span className="text-sm font-medium text-primary">{trendCount} Trends</span>
          </div>
        </div>
      </div>

      {/* Insights Section */}
      <section>
        <h2 className="text-lg font-semibold mb-4">Surface Insights</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {data.insights.map((insight) => (
            <InsightCard key={insight.id} insight={insight} />
          ))}
        </div>
      </section>

      {/* Analysis Grid */}
      <div className="grid gap-6 lg:grid-cols-3">
        <div className="lg:col-span-1">
          <FilingsPanel filings={data.filings} />
        </div>
        <div className="lg:col-span-1">
          <SentimentPanel analysis={data.sentimentAnalysis} />
        </div>
        <div className="lg:col-span-1">
          <RiskGauge assessment={data.riskAssessment} />
        </div>
      </div>

      {/* Entities and Citations */}
      <div className="grid gap-6 lg:grid-cols-2">
        <EntityPanel entities={data.entities} relationships={data.relationships} />
        <CitationsPanel citations={data.citations} />
      </div>
    </div>
  );
}
