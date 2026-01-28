import { useState } from 'react';
import { Header } from '@/components/Header';
import { SearchBar } from '@/components/SearchBar';
import { Dashboard } from '@/components/Dashboard';
import { EmptyState } from '@/components/EmptyState';
import { FloatingChatButton } from '@/components/chat/FloatingChatButton';
import { Company, DashboardData } from '@/types/market';
import { generateMockDashboard } from '@/data/mockData';

const Index = () => {
  const [selectedCompany, setSelectedCompany] = useState<Company | null>(null);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSelectCompany = async (company: Company) => {
    setIsLoading(true);
    setSelectedCompany(company);

    // Simulate API call - replace with actual endpoint
    await new Promise((resolve) => setTimeout(resolve, 800));

    const data = generateMockDashboard(company);
    setDashboardData(data);
    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />

      <main className="container py-8">
        {/* Search Section */}
        <div className="flex flex-col items-center mb-10">
          <SearchBar onSelectCompany={handleSelectCompany} selectedCompany={selectedCompany} />
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex flex-col items-center justify-center py-20">
            <div className="relative">
              <div className="h-16 w-16 rounded-full border-4 border-muted animate-spin border-t-primary" />
            </div>
            <p className="mt-4 text-muted-foreground">Analyzing {selectedCompany?.name}...</p>
          </div>
        )}

        {/* Dashboard or Empty State */}
        {!isLoading && dashboardData ? (
          <Dashboard data={dashboardData} />
        ) : !isLoading ? (
          <EmptyState />
        ) : null}
      </main>

      {/* Footer */}
      <footer className="border-t border-border py-6 mt-12">
        <div className="container text-center text-sm text-muted-foreground">
          <p>AQMIS - AI Qualitative Market Intelligence Surveillance</p>
          <p className="text-xs mt-1">Malaysian Stock Market Analysis Platform</p>
        </div>
      </footer>

      {/* Floating Chat Button */}
      <FloatingChatButton
        context={{
          selectedCompany: selectedCompany
            ? {
                name: selectedCompany.name,
                stockCode: selectedCompany.stockCode,
                sector: selectedCompany.sector,
              }
            : null,
        }}
      />
    </div>
  );
};

export default Index;
