import { Company } from '@/types/market';
import { API_CONFIG } from './config';
import { apiClient } from './client';
import { CompaniesListResponse } from './types';
import { malaysianCompanies } from '@/data/mockData';

/**
 * Fetch list of companies
 * 
 * API Contract:
 * - Endpoint: GET /api/v1/companies
 * - Query Params: ?search=query (optional)
 * - Response: { success: boolean, data: Company[], error?: string }
 */
export async function fetchCompanies(searchQuery?: string): Promise<Company[]> {
  // Use mock data if enabled
  if (API_CONFIG.useMockData) {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 200));
    
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      return malaysianCompanies.filter(
        (company) =>
          company.name.toLowerCase().includes(query) ||
          company.companyId.toLowerCase().includes(query) ||
          company.industry.toLowerCase().includes(query)
      );
    }
    
    return malaysianCompanies;
  }

  // Real API call
  const endpoint = searchQuery 
    ? `${API_CONFIG.companies.list}?name=${encodeURIComponent(searchQuery)}`
    : API_CONFIG.companies.list;

  const response = await apiClient.get<CompaniesListResponse>(endpoint);

  if (!response.success || !response.data) {
    throw new Error(response.error || 'Failed to fetch companies');
  }

  return response.data;
}
