import React, { useState, useEffect } from 'react';
import { Upload, Send, FileText, TrendingUp, AlertCircle, Check, LayoutDashboard, Newspaper, Activity, DollarSign, BarChart3, RefreshCw } from 'lucide-react';

export default function FinancialAnalysisApp() {
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState('');
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [news, setNews] = useState([]);
  const [newsLoading, setNewsLoading] = useState(false);

// Original API_CONFIG
/*
  // Configure your Azure endpoints here
  const API_CONFIG = {
    chatEndpoint: 'https://your-api.azurewebsites.net/api/chat',
    uploadEndpoint: 'https://your-api.azurewebsites.net/api/upload',
    newsEndpoint: 'https://your-api.azurewebsites.net/api/news', // Add your news API endpoint
    apiKey: ''
  };
*/
  const API_CONFIG = {
  chatEndpoint: 'https://your-api.azurewebsites.net/api/chat',
  uploadEndpoint: 'https://your-api.azurewebsites.net/api/upload',
  newsEndpoint: 'https://your-api.azurewebsites.net/api/news', // ← Add your news API
  marketDataEndpoint: 'https://your-api.azurewebsites.net/api/market-data', // For indices
  commoditiesEndpoint: 'https://your-api.azurewebsites.net/api/commodities', // For commodities
  watchlistEndpoint: 'https://your-api.azurewebsites.net/api/watchlist', // For stocks
  apiKey: 'YOUR_API_KEY'
  }; 

  // Fetch news when dashboard loads
  useEffect(() => {
    if (activeTab === 'dashboard') {
      fetchNews();
    }
  }, [activeTab]);

  const fetchNews = async () => {
    setNewsLoading(true);
    try {
      const response = await fetch(API_CONFIG.newsEndpoint, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          ...(API_CONFIG.apiKey && { 'Authorization': `Bearer ${API_CONFIG.apiKey}` })
        }
      });

      if (!response.ok) throw new Error(`API Error: ${response.status}`);

      const data = await response.json();
      // Expecting API to return: { news: [{title, description, source, url, publishedAt}] }
      setNews(data.news || data.articles || data);
    } catch (error) {
      console.error('Error fetching news:', error);
      // Fallback mock data for development
      setNews([
        {
          title: "Stock Markets Hit Record Highs Amid Tech Rally",
          description: "Major indices surge as technology stocks lead the market upward...",
          source: "Financial Times",
          url: "#",
          publishedAt: "2 hours ago"
        },
        {
          title: "Federal Reserve Signals Potential Rate Changes",
          description: "Central bank officials hint at policy adjustments in upcoming meeting...",
          source: "Wall Street Journal",
          url: "#",
          publishedAt: "5 hours ago"
        },
        {
          title: "Emerging Markets Show Strong Growth Potential",
          description: "Analysts identify key opportunities in developing economies...",
          source: "Bloomberg",
          url: "#",
          publishedAt: "1 day ago"
        }
      ]);
    } finally {
      setNewsLoading(false);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'application/pdf') {
      setUploadedFile(file);
    } else {
      alert('Please upload a PDF file only.');
    }
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputText,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString()
    };

    setMessages([...messages, userMessage]);
    setInputText('');
    setIsLoading(true);

    try {
      const response = await fetch(API_CONFIG.chatEndpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(API_CONFIG.apiKey && { 'Authorization': `Bearer ${API_CONFIG.apiKey}` })
        },
        body: JSON.stringify({
          prompt: inputText,
          conversationHistory: messages.slice(-5)
        })
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      
      const aiResponse = {
        id: Date.now() + 1,
        text: data.response || data.message || data.text || 'No response from AI',
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString()
      };
      
      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      console.error('Error calling AI endpoint:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: `Error: Unable to get response. ${error.message}`,
        sender: 'ai',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUploadToDatabase = async () => {
    if (!uploadedFile) return;
    
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append('file', uploadedFile);
      formData.append('fileName', uploadedFile.name);
      formData.append('fileSize', uploadedFile.size);

      const response = await fetch(API_CONFIG.uploadEndpoint, {
        method: 'POST',
        headers: {
          ...(API_CONFIG.apiKey && { 'Authorization': `Bearer ${API_CONFIG.apiKey}` })
        },
        body: formData
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.status}`);
      }

      const result = await response.json();
      alert(`✓ ${uploadedFile.name} has been uploaded successfully!`);
      setUploadedFile(null);
      document.getElementById('fileUpload').value = '';
    } catch (error) {
      console.error('Error uploading file:', error);
      alert(`✗ Upload failed: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const quickQuestions = [
    "What's the company's revenue trend?",
    "Analyze profit margins",
    "Is the debt level concerning?",
    "Should I invest in this company?"
  ];

  return (
    <div className="h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Header */}
      <div className="bg-white shadow-md px-6 py-4 border-b-2 border-indigo-500">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <TrendingUp className="text-indigo-600" size={32} />
            <div>
              <h1 className="text-2xl font-bold text-gray-800">Financial Analysis AI</h1>
              <p className="text-sm text-gray-600">Investment Decision Support System</p>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-4 py-2 rounded-lg font-medium transition flex items-center gap-2 ${
                activeTab === 'dashboard'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              <LayoutDashboard size={18} />
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab('chat')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'chat'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Chat Analysis
            </button>
            <button
              onClick={() => setActiveTab('upload')}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                activeTab === 'upload'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
              }`}
            >
              Upload Reports
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-hidden">
        {/* Dashboard Screen */}
        {activeTab === 'dashboard' && (
          <div className="h-full overflow-y-auto p-6">
            <div className="max-w-7xl mx-auto">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Market Overview</h2>
              
              {/* Dashboard Grid - Easy to add more blocks */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                {/* Top News Block */}
                <div className="lg:col-span-2 bg-white rounded-lg shadow-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-2">
                      <Newspaper className="text-indigo-600" size={24} />
                      <h3 className="text-xl font-semibold text-gray-800">Top Market News</h3>
                    </div>
                    <button
                      onClick={fetchNews}
                      disabled={newsLoading}
                      className="p-2 hover:bg-gray-100 rounded-lg transition"
                      title="Refresh news"
                    >
                      <RefreshCw className={`text-gray-600 ${newsLoading ? 'animate-spin' : ''}`} size={20} />
                    </button>
                  </div>

                  {newsLoading ? (
                    <div className="space-y-4">
                      {[1, 2, 3].map(i => (
                        <div key={i} className="animate-pulse">
                          <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                          <div className="h-3 bg-gray-200 rounded w-full"></div>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="space-y-4 max-h-96 overflow-y-auto">
                      {news.map((article, idx) => (
                        <div key={idx} className="border-b border-gray-200 pb-4 last:border-0">
                          <a href={article.url} target="_blank" rel="noopener noreferrer" className="group">
                            <h4 className="font-semibold text-gray-900 group-hover:text-indigo-600 transition mb-1">
                              {article.title}
                            </h4>
                            <p className="text-sm text-gray-600 mb-2">{article.description}</p>
                            <div className="flex items-center gap-3 text-xs text-gray-500">
                              <span>{article.source}</span>
                              <span>•</span>
                              <span>{article.publishedAt}</span>
                            </div>
                          </a>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Quick Stats Block - Ready for API integration */}
                <div className="space-y-6">
                  <div className="bg-white rounded-lg shadow-lg p-6">
                    <div className="flex items-center gap-2 mb-4">
                      <Activity className="text-green-600" size={24} />
                      <h3 className="text-lg font-semibold text-gray-800">Market Indices</h3>
                    </div>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">S&P 500</span>
                        <span className="font-semibold text-green-600">+1.2%</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">NASDAQ</span>
                        <span className="font-semibold text-green-600">+1.8%</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">DOW</span>
                        <span className="font-semibold text-red-600">-0.3%</span>
                      </div>
                    </div>
                    <p className="text-xs text-gray-500 mt-4">Connect to API in API_CONFIG</p>
                  </div>

                  <div className="bg-white rounded-lg shadow-lg p-6">
                    <div className="flex items-center gap-2 mb-4">
                      <DollarSign className="text-yellow-600" size={24} />
                      <h3 className="text-lg font-semibold text-gray-800">Commodities</h3>
                    </div>
                    <div className="space-y-3">
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">Gold</span>
                        <span className="font-semibold">$2,043</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">Oil (WTI)</span>
                        <span className="font-semibold">$73.52</span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-gray-600">Silver</span>
                        <span className="font-semibold">$23.15</span>
                      </div>
                    </div>
                    <p className="text-xs text-gray-500 mt-4">Connect to API in API_CONFIG</p>
                  </div>
                </div>
              </div>

              {/* Additional Dashboard Blocks - Easy to add more */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Watchlist Block - Ready for customization */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <div className="flex items-center gap-2 mb-4">
                    <BarChart3 className="text-purple-600" size={24} />
                    <h3 className="text-lg font-semibold text-gray-800">Markets to Watch</h3>
                  </div>
                  <div className="space-y-3">
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-medium text-gray-800">AAPL</span>
                        <span className="text-green-600 font-semibold">+2.4%</span>
                      </div>
                      <p className="text-sm text-gray-600">Apple Inc.</p>
                    </div>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-medium text-gray-800">MSFT</span>
                        <span className="text-green-600 font-semibold">+1.8%</span>
                      </div>
                      <p className="text-sm text-gray-600">Microsoft Corporation</p>
                    </div>
                    <div className="p-3 bg-gray-50 rounded-lg">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-medium text-gray-800">TSLA</span>
                        <span className="text-red-600 font-semibold">-0.9%</span>
                      </div>
                      <p className="text-sm text-gray-600">Tesla, Inc.</p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 mt-4">Connect to API in API_CONFIG</p>
                </div>

                {/* AI Insights Block */}
                <div className="bg-white rounded-lg shadow-lg p-6">
                  <div className="flex items-center gap-2 mb-4">
                    <TrendingUp className="text-indigo-600" size={24} />
                    <h3 className="text-lg font-semibold text-gray-800">AI Insights</h3>
                  </div>
                  <div className="space-y-3">
                    <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
                      <p className="text-sm text-gray-700">
                        <span className="font-semibold">Market Sentiment:</span> Bullish trend detected in tech sector with strong momentum indicators.
                      </p>
                    </div>
                    <div className="p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                      <p className="text-sm text-gray-700">
                        <span className="font-semibold">Risk Alert:</span> Increased volatility expected in energy sector due to geopolitical factors.
                      </p>
                    </div>
                    <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
                      <p className="text-sm text-gray-700">
                        <span className="font-semibold">Opportunity:</span> Emerging markets showing strong growth potential in Q1.
                      </p>
                    </div>
                  </div>
                  <p className="text-xs text-gray-500 mt-4">Connect to API in API_CONFIG</p>
                </div>
              </div>

              {/* Instructions for Adding More Blocks */}
              <div className="mt-6 bg-indigo-50 border-2 border-dashed border-indigo-300 rounded-lg p-6">
                <h4 className="font-semibold text-indigo-900 mb-2">Add More Dashboard Blocks</h4>
                <p className="text-sm text-indigo-700 mb-3">
                  To add more widgets to your dashboard, simply copy any of the existing blocks above and customize:
                </p>
                <ul className="text-sm text-indigo-700 space-y-1 list-disc list-inside">
                  <li>Change the icon and colors</li>
                  <li>Update the API endpoint in API_CONFIG</li>
                  <li>Modify the data structure to match your API response</li>
                  <li>Add to the grid layout above</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Chat Screen */}
        {activeTab === 'chat' && (
          <div className="h-full flex flex-col max-w-5xl mx-auto p-4">
            {messages.length === 0 && (
              <div className="mb-4">
                <p className="text-sm text-gray-600 mb-2 font-medium">Quick Questions:</p>
                <div className="grid grid-cols-2 gap-2">
                  {quickQuestions.map((question, idx) => (
                    <button
                      key={idx}
                      onClick={() => setInputText(question)}
                      className="text-left px-4 py-2 bg-white rounded-lg border border-gray-300 hover:border-indigo-400 hover:bg-indigo-50 transition text-sm"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            )}

            <div className="flex-1 bg-white rounded-lg shadow-lg overflow-y-auto p-4 mb-4">
              {messages.length === 0 ? (
                <div className="h-full flex items-center justify-center">
                  <div className="text-center">
                    <TrendingUp className="mx-auto text-indigo-300 mb-4" size={64} />
                    <h3 className="text-xl font-semibold text-gray-700 mb-2">
                      Welcome to Financial Analysis AI
                    </h3>
                    <p className="text-gray-600">
                      Ask me about company financials, investment decisions, or upload reports for analysis
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  {messages.map((message) => (
                    <div
                      key={message.id}
                      className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div
                        className={`max-w-xl px-4 py-3 rounded-lg ${
                          message.sender === 'user'
                            ? 'bg-indigo-600 text-white'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        <p className="text-sm whitespace-pre-wrap">{message.text}</p>
                        <p className={`text-xs mt-1 ${
                          message.sender === 'user' ? 'text-indigo-200' : 'text-gray-500'
                        }`}>
                          {message.timestamp}
                        </p>
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-gray-100 px-4 py-3 rounded-lg">
                        <div className="flex gap-2">
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                          <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="bg-white rounded-lg shadow-lg p-4">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSendMessage()}
                  placeholder="Ask about financial metrics, investment decisions..."
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  disabled={isLoading}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!inputText.trim() || isLoading}
                  className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition flex items-center gap-2"
                >
                  <Send size={20} />
                  Send
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Upload Screen */}
        {activeTab === 'upload' && (
          <div className="h-full flex items-center justify-center p-4">
            <div className="bg-white rounded-lg shadow-lg p-8 max-w-2xl w-full">
              <div className="text-center mb-6">
                <FileText className="mx-auto text-indigo-600 mb-4" size={64} />
                <h2 className="text-2xl font-bold text-gray-800 mb-2">Upload Financial Reports</h2>
                <p className="text-gray-600">
                  Upload PDF financial reports to add them to the AI database for analysis
                </p>
              </div>

              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-400 transition mb-4">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handleFileUpload}
                  className="hidden"
                  id="fileUpload"
                  disabled={isLoading}
                />
                <label htmlFor="fileUpload" className="cursor-pointer">
                  <Upload className="mx-auto text-gray-400 mb-4" size={48} />
                  <p className="text-gray-700 font-medium mb-1">
                    Click to upload or drag and drop
                  </p>
                  <p className="text-sm text-gray-500">PDF files only</p>
                </label>
              </div>

              {uploadedFile && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Check className="text-green-600" size={24} />
                      <div>
                        <p className="font-medium text-gray-800">{uploadedFile.name}</p>
                        <p className="text-sm text-gray-600">
                          {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                        </p>
                      </div>
                    </div>
                    <button
                      onClick={() => setUploadedFile(null)}
                      className="text-red-600 hover:text-red-800 font-medium text-sm"
                      disabled={isLoading}
                    >
                      Remove
                    </button>
                  </div>
                </div>
              )}

              <button
                onClick={handleUploadToDatabase}
                disabled={!uploadedFile || isLoading}
                className="w-full py-3 bg-indigo-600 text-white rounded-lg font-medium hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition"
              >
                {isLoading ? 'Uploading...' : 'Upload to Database'}
              </button>

              <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
                <div className="flex gap-3">
                  <AlertCircle className="text-blue-600 flex-shrink-0" size={20} />
                  <div className="text-sm text-gray-700">
                    <p className="font-medium mb-1">Supported Documents:</p>
                    <ul className="list-disc list-inside space-y-1 text-gray-600">
                      <li>Annual Reports (10-K)</li>
                      <li>Quarterly Reports (10-Q)</li>
                      <li>Financial Statements</li>
                      <li>Earnings Reports</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}