import { ChatContext } from '@/types/chat';
import { API_CONFIG } from './config';
import { apiClient } from './client';
import { ChatRequest, ChatResponse } from './types';
import { generateMockResponse } from '@/lib/mockChatResponses';

/**
 * Send a chat message and get AI response
 * 
 * API Contract:
 * - Endpoint: POST /api/v1/chat
 * - Request Body: { 
 *     message: string,
 *     context: { selectedCompany: { name, stockCode, sector } | null },
 *     conversationHistory?: Array<{ role: 'user' | 'assistant', content: string }>
 *   }
 * - Response: { success: boolean, message: string, error?: string }
 */
export async function sendChatMessage(
  message: string,
  context: ChatContext,
  conversationHistory?: Array<{ role: 'user' | 'assistant'; content: string }>
): Promise<string> {
  // Use mock data if enabled
  if (API_CONFIG.useMockData) {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 800 + Math.random() * 700));
    return generateMockResponse(message, context);
  }

  // Real API call
  const request: ChatRequest = {
    message,
    context: {
      selectedCompany: context.selectedCompany,
    },
    conversationHistory,
  };

  const response = await apiClient.post<ChatResponse>(
    API_CONFIG.chat.send,
    request
  );

  if (!response.success) {
    throw new Error(response.error || 'Failed to get response');
  }

  return response.message;
}

/**
 * Stream chat response (for real-time AI responses)
 * 
 * API Contract:
 * - Endpoint: POST /api/v1/chat/stream
 * - Request Body: Same as sendChatMessage
 * - Response: Server-Sent Events stream
 * 
 * Usage example:
 * ```
 * await streamChatMessage(message, context, history, (chunk) => {
 *   setResponse(prev => prev + chunk);
 * });
 * ```
 */
export async function streamChatMessage(
  message: string,
  context: ChatContext,
  conversationHistory: Array<{ role: 'user' | 'assistant'; content: string }>,
  onChunk: (chunk: string) => void
): Promise<void> {
  // For mock mode, simulate streaming
  if (API_CONFIG.useMockData) {
    const fullResponse = generateMockResponse(message, context);
    const words = fullResponse.split(' ');
    
    for (const word of words) {
      await new Promise((resolve) => setTimeout(resolve, 50));
      onChunk(word + ' ');
    }
    return;
  }

  // Real streaming API call
  const response = await fetch(`${API_CONFIG.baseUrl}/api/v1/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      context: { selectedCompany: context.selectedCompany },
      conversationHistory,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to start stream');
  }

  const reader = response.body?.getReader();
  if (!reader) throw new Error('No response body');

  const decoder = new TextDecoder();
  
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value, { stream: true });
    onChunk(chunk);
  }
}
