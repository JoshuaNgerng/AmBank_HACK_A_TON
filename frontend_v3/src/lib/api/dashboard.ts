import { Company, DashboardData } from '@/types/market';
import { API_CONFIG } from './config';
import { apiClient } from './client';
import { AnalyzeCompanyRequest, AnalyzeCompanyResponse } from './types';
import { generateMockDashboard } from '@/data/mockData';

/**
 * Analyze a company and get dashboard data
 * 
 * API Contract:
 * - Endpoint: POST /api/v1/analyze
 * - Request Body: { companyId, stockCode, name, sector }
 * - Response: { success: boolean, data: DashboardData, error?: string }
 */
export async function analyzeCompany(company: Company): Promise<DashboardData> {
  // Use mock data if enabled
  if (API_CONFIG.useMockData) {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 800));
    return generateMockDashboard(company);
  }

  // Real API call
  const request: AnalyzeCompanyRequest = {
    companyId: company.id,
    stockCode: company.stockCode,
    name: company.name,
    sector: company.sector,
  };

  const response = await apiClient.post<AnalyzeCompanyResponse>(
    API_CONFIG.dashboard.analyze,
    request
  );

  if (!response.success || !response.data) {
    throw new Error(response.error || 'Failed to analyze company');
  }

  return response.data;
}
