export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export interface ChatContext {
  selectedCompany: {
    name: string;
    stockCode: string;
    sector: string;
  } | null;
}
