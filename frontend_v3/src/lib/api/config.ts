// API Configuration - Replace these with your actual endpoints
export const API_CONFIG = {
  // Base URL for your API
  baseUrl: import.meta.env.VITE_API_BASE_URL || 'https://api.example.com',
  
  // Dashboard endpoints
  dashboard: {
    analyze: '/api/v1/analyze', // POST - Analyze a company
  },
  
  // Chat endpoints  
  chat: {
    send: '/api/v1/chat', // POST - Send chat message
  },
  
  // Enable mock mode (set to false when API is ready)
  useMockData: true,
};
