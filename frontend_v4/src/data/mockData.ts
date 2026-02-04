import { Company, DashboardData } from '@/types/market';

export const malaysianCompanies: Company[] = [
  { id: 1, name: 'Maybank', companyId: 'REG-1155-MY', industry: 'Banking' },
  { id: 2, name: 'Tenaga Nasional', companyId: 'REG-5347-MY', industry: 'Utilities' },
  { id: 3, name: 'Public Bank', companyId: 'REG-1295-MY', industry: 'Banking' },
  { id: 4, name: 'CIMB Group', companyId: 'REG-1023-MY', industry: 'Banking' },
  { id: 5, name: 'Petronas Chemicals', companyId: 'REG-5183-MY', industry: 'Chemicals' },
  { id: 6, name: 'IHH Healthcare', companyId: 'REG-5225-MY', industry: 'Healthcare' },
  { id: 7, name: 'Hong Leong Bank', companyId: 'REG-5819-MY', industry: 'Banking' },
  { id: 8, name: 'Axiata Group', companyId: 'REG-6888-MY', industry: 'Telecommunications' },
  { id: 9, name: 'Digi.Com', companyId: 'REG-6947-MY', industry: 'Telecommunications' },
  { id: 10, name: 'Sime Darby', companyId: 'REG-4197-MY', industry: 'Conglomerate' },
];

export const generateMockDashboard = (company: Company): DashboardData => ({
  company,
  asOf: new Date().toISOString(),
  lookbackYears: 5,

  executiveSummary: {
    overview: `${company.name} has delivered strong financial performance over the past five years driven by digital transformation and regional growth. This positive trajectory is partially offset by elevated regulatory scrutiny and recent management changes.`,
    keyPositives: [
      'Consistent revenue growth with improving profit margins',
      'Clear and sustained digital transformation strategy',
      'Improving ESG profile and governance practices',
    ],
    keyConcerns: [
      'Ongoing regulatory review by Bank Negara Malaysia',
      'CFO resignation during an active transformation phase',
    ],
    confidence: 0.7,
    riskLevel: 'moderate',
  },

  details: {
    methodology: {
      signalSelection: 'Top 10 signals by cosine similarity',
      ordering: 'Latest first',
      lookbackYears: 10,
    },

    businessStrategy: [
      {
        theme: 'Digital Banking & ASEAN Expansion',
        consistencyScore: 0.82,
        trend: 'stable',
        signals: [
          {
            year: 2024,
            summary: 'Accelerating digital banking adoption through fintech partnerships and platform upgrades.',
            source: 'FY2023 Annual Report',
            confidence: 0.91,
          },
          {
            year: 2023,
            summary: 'Expansion of mobile-first banking services across ASEAN markets.',
            source: 'FY2022 Annual Report',
            confidence: 0.88,
          },
          {
            year: 2022,
            summary: 'Investment in digital infrastructure and data-driven customer engagement.',
            source: 'FY2021 Annual Report',
            confidence: 0.86,
          },
        ],
      },
      {
        theme: 'Sustainable Finance Initiatives',
        consistencyScore: 0.75,
        trend: 'up',
        signals: [
          {
            year: 2024,
            summary: 'Launch of green financing products targeting SMEs and renewable energy projects.',
            source: 'Sustainability Report 2023',
            confidence: 0.85,
          },
          {
            year: 2023,
            summary: 'Commitment to net-zero financing portfolio by 2050.',
            source: 'ESG Framework Document',
            confidence: 0.82,
          },
        ],
      },
    ],

    growthPotential: [
      {
        growthLevel: 'high',
        growthScore: 0.74,
        confidence: 0.81,
        growthDrivers: [
          'Rising digital banking adoption',
          'ASEAN market expansion',
          'Cross-selling of fintech services',
        ],
        constraints: [
          'Regulatory approval timelines',
          'Technology execution risk',
        ],
        summary: 'Growth prospects remain strong, supported by scalable digital platforms and regional expansion, though regulatory processes may moderate the pace.',
      },
    ],

    sentimentAnalysis: [
      {
        topic: 'Financial Performance',
        sentimentLabel: 'positive',
        sentimentScore: 0.72,
        confidence_level: 'high',
        rationale: 'Revenue and profitability have shown consistent improvement over the past five years, driven by digital adoption and cost discipline.',
        supportingSignals: ['rev-growth-2020-2024', 'margin-expansion-2022-2024'],
      },
      {
        topic: 'Regulatory Compliance',
        sentimentLabel: 'negative',
        sentimentScore: -0.41,
        confidence_level: 'high',
        rationale: 'Persistent regulatory emphasis on AML compliance and recent external review have increased uncertainty.',
        supportingSignals: ['risk-aml-2020-2024', 'news-bnm-review-2024'],
      },
      {
        topic: 'Corporate Governance',
        sentimentLabel: 'neutral',
        sentimentScore: 0.12,
        confidence_level: 'medium',
        rationale: 'CFO departure balanced by strong internal succession planning. Board composition remains stable with experienced directors.',
        supportingSignals: ['cfo-resignation-2024', 'board-stability-score'],
      },
      {
        topic: 'Strategic Initiatives',
        sentimentLabel: 'positive',
        sentimentScore: 0.78,
        confidence_level: 'high',
        rationale: 'New fintech partnership positions company well for digital transformation. ASEAN expansion aligns with regional growth opportunities.',
        supportingSignals: ['partnership-announcement-2024', 'expansion-pipeline'],
      },
    ],

    riskAssessment: {
      overallScore: 62,
      posture: 'moderate',
      summary: `${company.name} presents a moderate risk profile with strong financial fundamentals offset by elevated regulatory and governance-related risks.`,
      factors: [
        {
          name: 'Regulatory Risk',
          score: 45,
          trend: 'up',
          severity: 0.9,
          managementTone: 'reactive',
          keySignals: ['risk-aml-2020-2024', 'news-bnm-review-2024'],
          summary: 'Ongoing Bank Negara Malaysia review creates compliance uncertainty.',
        },
        {
          name: 'Financial Health',
          score: 82,
          trend: 'stable',
          severity: 0.2,
          managementTone: 'proactive',
          keySignals: ['profit-cagr-3y', 'capital-adequacy'],
          summary: 'Strong capital position and consistent profitability metrics.',
        },
        {
          name: 'Governance',
          score: 68,
          trend: 'down',
          severity: 0.6,
          managementTone: 'neutral',
          keySignals: ['cfo-resignation-2024'],
          summary: 'CFO departure during transformation creates short-term uncertainty.',
        },
        {
          name: 'Market Position',
          score: 75,
          trend: 'up',
          severity: 0.3,
          managementTone: 'proactive',
          keySignals: ['market-share-growth', 'digital-adoption-rate'],
          summary: 'Growing market share in digital banking segment.',
        },
        {
          name: 'ESG Factors',
          score: 71,
          trend: 'up',
          severity: 0.4,
          managementTone: 'proactive',
          keySignals: ['esg-rating-upgrade', 'sustainability-report'],
          summary: 'Improving ESG ratings and sustainability commitments.',
        },
      ],
    },
  },

  citations: [
    {
      id: 'c1',
      title: 'FY2023 Annual Report',
      source: `${company.name} Investor Relations`,
      date: '2024-01-10',
      url: 'https://company.com/reports/fy2023',
    },
    {
      id: 'c2',
      title: 'Q4 Earnings Announcement',
      source: 'Bursa Malaysia',
      date: '2024-01-12',
      url: 'https://bursamalaysia.com/earnings',
    },
    {
      id: 'c3',
      title: 'BNM Regulatory Review Notice',
      source: 'Bank Negara Malaysia',
      date: '2024-01-15',
      url: 'https://bnm.gov.my/notices',
    },
    {
      id: 'c4',
      title: 'Sustainability Report 2023',
      source: `${company.name} ESG`,
      date: '2024-01-08',
      url: 'https://company.com/sustainability',
    },
    {
      id: 'c5',
      title: 'Industry Analysis Report',
      source: 'Bloomberg',
      date: '2024-01-05',
      url: 'https://bloomberg.com/banking-sector',
    },
  ],
});
