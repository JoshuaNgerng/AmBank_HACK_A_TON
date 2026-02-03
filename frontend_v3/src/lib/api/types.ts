import { Company, DashboardData } from '@/types/market';

// Dashboard API Types
export interface AnalyzeCompanyRequest {
  companyId: string;
  stockCode: string;
  name: string;
  sector: string;
}

export interface AnalyzeCompanyResponse {
  success: boolean;
  data: DashboardData;
  error?: string;
}

// Chat API Types
export interface ChatRequest {
  message: string;
  context: {
    selectedCompany: {
      name: string;
      stockCode: string;
      sector: string;
    } | null;
  };
  conversationHistory?: Array<{
    role: 'user' | 'assistant';
    content: string;
  }>;
}

export interface ChatResponse {
  success: boolean;
  message: string;
  error?: string;
}

// Generic API Response wrapper
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}
