export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatContext {
  selectedCompany: {
    name: string;
    companyId: string; // Changed from stockCode
    industry: string; // Changed from sector
  } | null;
}

// Conversation history for API
export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
}
