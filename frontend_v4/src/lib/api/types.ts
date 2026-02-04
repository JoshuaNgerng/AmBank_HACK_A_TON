import { Company, DashboardData } from '@/types/market';
import { ConversationMessage } from '@/types/chat';

// Dashboard API Types
export interface AnalyzeCompanyRequest {
  id: number;
  companyId: string; // Registration ID
  name: string;
  industry: string;
}

export interface AnalyzeCompanyResponse {
  success: boolean;
  data: DashboardData;
  error?: string;
}

// Companies List API Types
export interface CompanyListItem {
  id: number;
  name: string;
  industry: string;
  companyId: string; // Registration ID
}

export interface CompaniesListResponse {
  success: boolean;
  data: CompanyListItem[];
  error?: string;
}

// Chat API Types
export interface ChatRequest {
  message: string;
  context: {
    selectedCompany: {
      name: string;
      companyId: string;
      industry: string;
    } | null;
  };
  conversationHistory: ConversationMessage[];
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
