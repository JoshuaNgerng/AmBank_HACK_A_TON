import { Search, BarChart3, Shield, FileText } from 'lucide-react';

export function EmptyState() {
  return (
    <div className="flex flex-col items-center justify-center py-20 text-center animate-in fade-in duration-500">
      <div className="relative mb-8">
        <div className="absolute inset-0 bg-primary/20 rounded-full blur-3xl scale-150" />
        <div className="relative flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-br from-primary/20 to-primary/5 border border-primary/20">
          <Search className="h-10 w-10 text-primary" />
        </div>
      </div>

      <h2 className="text-2xl font-bold mb-2">Search for a Company</h2>
      <p className="text-muted-foreground max-w-md mb-12">
        Enter a Malaysian company name or stock code above to view comprehensive AI-powered market intelligence and risk analysis.
      </p>

      <div className="grid gap-6 md:grid-cols-3 max-w-3xl">
        <div className="flex flex-col items-center p-6 rounded-2xl bg-card border border-border">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 mb-4">
            <BarChart3 className="h-6 w-6 text-primary" />
          </div>
          <h3 className="font-semibold mb-1">Surface Insights</h3>
          <p className="text-sm text-muted-foreground text-center">
            Adverse events, positive developments, and market trends
          </p>
        </div>

        <div className="flex flex-col items-center p-6 rounded-2xl bg-card border border-border">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 mb-4">
            <FileText className="h-6 w-6 text-primary" />
          </div>
          <h3 className="font-semibold mb-1">Bursa Filings</h3>
          <p className="text-sm text-muted-foreground text-center">
            Official announcements and targeted news coverage
          </p>
        </div>

        <div className="flex flex-col items-center p-6 rounded-2xl bg-card border border-border">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 mb-4">
            <Shield className="h-6 w-6 text-primary" />
          </div>
          <h3 className="font-semibold mb-1">Risk Assessment</h3>
          <p className="text-sm text-muted-foreground text-center">
            AI-powered risk scoring with evidence citations
          </p>
        </div>
      </div>
    </div>
  );
}
