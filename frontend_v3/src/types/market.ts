export interface Company {
  id: string;
  name: string;
  stockCode: string;
  sector: string;
  marketCap: string;
}

export interface Insight {
  id: string;
  type: 'adverse' | 'positive' | 'trend';
  title: string;
  description: string;
  date: string;
  source: string;
  sourceUrl: string;
  confidence: number;
}

export interface Filing {
  id: string;
  type: 'bursa' | 'news';
  title: string;
  summary: string;
  date: string;
  source: string;
  sourceUrl: string;
  category: string;
}

export interface SentimentAnalysis {
  id: string;
  topic: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  score: number;
  rationale: string;
  citations: Citation[];
}

export interface Entity {
  id: string;
  name: string;
  type: 'person' | 'organization' | 'location' | 'event';
  mentions: number;
}

export interface Relationship {
  sourceId: string;
  targetId: string;
  type: string;
  description: string;
}

export interface Citation {
  id: string;
  title: string;
  url: string;
  source: string;
  date: string;
  relevance: number;
}

export interface RiskAssessment {
  overallScore: number;
  factors: {
    name: string;
    score: number;
    weight: number;
    trend: 'up' | 'down' | 'stable';
  }[];
  summary: string;
  lastUpdated: string;
}

export interface DashboardData {
  company: Company;
  insights: Insight[];
  filings: Filing[];
  sentimentAnalysis: SentimentAnalysis[];
  entities: Entity[];
  relationships: Relationship[];
  riskAssessment: RiskAssessment;
  citations: Citation[];
}
