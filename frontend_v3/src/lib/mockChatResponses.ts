import { ChatContext } from '@/types/chat';

const generalResponses = [
  "The Malaysian stock market (Bursa Malaysia) has shown resilience with key sectors like technology, healthcare, and banking leading recent gains.",
  "Based on current market trends, the KLCI has been trading within a consolidation range. Key support levels are being monitored by analysts.",
  "Recent regulatory changes by Bank Negara Malaysia may impact banking sector valuations. I recommend monitoring quarterly earnings reports for updates.",
  "The palm oil sector continues to be influenced by global commodity prices and ESG considerations from international investors.",
  "Technology stocks on Bursa Malaysia have attracted attention due to the semiconductor supply chain developments in the region.",
];

const companySpecificResponses = (companyName: string, stockCode: string) => [
  `Based on my analysis of ${companyName} (${stockCode}), recent filings indicate stable operational performance with some notable developments in their quarterly announcements.`,
  `${companyName} has shown mixed sentiment in recent news coverage. Key topics include their expansion plans and regulatory compliance updates.`,
  `The risk assessment for ${companyName} considers factors like management changes, sector headwinds, and financial health indicators from recent filings.`,
  `Entity extraction from ${companyName}'s filings reveals key relationships with subsidiaries and notable board member activities worth monitoring.`,
  `Recent Bursa announcements for ${companyName} (${stockCode}) include material disclosures that may impact investor sentiment in the short term.`,
];

export function generateMockResponse(userMessage: string, context: ChatContext): string {
  const lowerMessage = userMessage.toLowerCase();
  
  // Simulate processing delay response
  if (context.selectedCompany) {
    const { name, stockCode } = context.selectedCompany;
    
    // Company-specific queries
    if (lowerMessage.includes('risk') || lowerMessage.includes('assessment')) {
      return `For ${name} (${stockCode}), the current risk assessment indicates moderate concern based on recent filing patterns and sentiment analysis. Key risk factors include sector volatility and pending regulatory reviews.`;
    }
    
    if (lowerMessage.includes('sentiment') || lowerMessage.includes('news')) {
      return `Sentiment analysis for ${name} shows a mixed outlook. Recent news coverage has been 60% neutral, 25% positive, and 15% negative. Key topics driving sentiment include quarterly earnings and market positioning.`;
    }
    
    if (lowerMessage.includes('filing') || lowerMessage.includes('announcement') || lowerMessage.includes('bursa')) {
      return `Recent Bursa filings for ${name} (${stockCode}) include quarterly reports and material announcements. Notable disclosures involve changes in substantial shareholding and corporate governance updates.`;
    }
    
    if (lowerMessage.includes('entity') || lowerMessage.includes('relationship')) {
      return `Entity extraction for ${name} reveals key relationships: Board members, subsidiary companies, and major shareholders. Notable connections include institutional investors and cross-holdings with related entities.`;
    }
    
    // General company query
    const responses = companySpecificResponses(name, stockCode);
    return responses[Math.floor(Math.random() * responses.length)];
  }
  
  // General market queries (no company selected)
  if (lowerMessage.includes('klci') || lowerMessage.includes('index')) {
    return "The KLCI (FTSE Bursa Malaysia KLCI) tracks the top 30 companies by market capitalization. Current market conditions show moderate trading volumes with sector rotation patterns.";
  }
  
  if (lowerMessage.includes('sector')) {
    return "Key sectors on Bursa Malaysia include Financial Services, Plantation, Technology, Healthcare, and Consumer Products. Each sector has unique risk profiles and growth drivers.";
  }
  
  if (lowerMessage.includes('help') || lowerMessage.includes('can you')) {
    return "I can help you with:\n• Company-specific analysis (select a company first)\n• Risk assessment insights\n• Sentiment analysis of news and filings\n• Entity and relationship mapping\n• General Malaysian market intelligence\n\nTry searching for a company above to get detailed analysis!";
  }
  
  // Default general response
  return generalResponses[Math.floor(Math.random() * generalResponses.length)];
}
