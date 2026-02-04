// Company - simplified with companyId as registration ID
export interface Company {
  id: number;
  name: string;
  industry: string;
  companyId: string; // Registration ID
}

// Executive Summary
export interface ExecutiveSummary {
  overview: string;
  keyPositives: string[];
  keyConcerns: string[];
  confidence: number;
  riskLevel: 'low' | 'moderate' | 'high';
}

// Business Strategy Signal
export interface StrategySignal {
  year: number;
  summary: string;
  source: string;
  confidence: number;
}

// Business Strategy Theme
export interface BusinessStrategy {
  theme: string;
  consistencyScore: number;
  trend: 'up' | 'down' | 'stable';
  signals: StrategySignal[];
}

// Growth Potential
export interface GrowthPotential {
  growthLevel: 'low' | 'medium' | 'high';
  growthScore: number;
  confidence: number;
  growthDrivers: string[];
  constraints: string[];
  summary: string;
}

// Sentiment Analysis
export interface SentimentAnalysis {
  topic: string;
  sentimentLabel: 'positive' | 'negative' | 'neutral';
  sentimentScore: number;
  confidence_level: 'low' | 'medium' | 'high';
  rationale: string;
  supportingSignals: string[];
}

// Risk Factor
export interface RiskFactor {
  name: string;
  score: number;
  trend: 'up' | 'down' | 'stable';
  severity: number;
  managementTone: 'proactive' | 'reactive' | 'neutral';
  keySignals: string[];
  summary: string;
}

// Risk Assessment
export interface RiskAssessment {
  overallScore: number;
  posture: 'low' | 'moderate' | 'high';
  summary: string;
  factors: RiskFactor[];
}

// Methodology
export interface Methodology {
  signalSelection: string;
  ordering: string;
  lookbackYears: number;
}

// Details container
export interface DashboardDetails {
  methodology: Methodology;
  businessStrategy: BusinessStrategy[];
  growthPotential: GrowthPotential[];
  sentimentAnalysis: SentimentAnalysis[];
  riskAssessment: RiskAssessment;
}

// Citation
export interface Citation {
  id: string;
  title: string;
  source: string;
  date: string;
  url: string;
}

// Main Dashboard Data
export interface DashboardData {
  company: Company;
  asOf: string;
  lookbackYears: number;
  executiveSummary: ExecutiveSummary;
  details: DashboardDetails;
  citations: Citation[];
}
