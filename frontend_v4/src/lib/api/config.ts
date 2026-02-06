// API Configuration - Replace these with your actual endpoints
const mockData: boolean = import.meta.env.MOCK_DATA === 'true';

export const API_CONFIG = {
  // Base URL for your API
  baseUrl: import.meta.env.VITE_API_BASE_URL || 'https://api.example.com',
  
  // Dashboard endpoints
  dashboard: {
    base: '/api/dashboard/company' // GET - company
    // analyze: '/api/v1/analyze', // POST - Analyze a company
  },
  
  // Companies endpoints
  companies: {
    list:  '/api/dashboard/company', // GET - List all companies
  },
 
  // Chat endpoints  
  chat: {
    send: '/api/bot/chat', // POST - Send chat message
  },
  
  // Enable mock mode (set to false when API is ready)
  useMockData: mockData
};
