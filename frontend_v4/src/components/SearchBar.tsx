import { useState, useRef, useEffect } from 'react';
import { Search, Building2, X, Loader2 } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Company } from '@/types/market';
import { fetchCompanies } from '@/lib/api';
import { cn } from '@/lib/utils';

interface SearchBarProps {
  onSelectCompany: (company: Company) => void;
  selectedCompany?: Company | null;
}

export function SearchBar({ onSelectCompany, selectedCompany }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);

  // Fetch companies when query changes
  useEffect(() => {
    const fetchData = async () => {
      if (query.length > 0) {
        setIsLoading(true);
        try {
          const results = await fetchCompanies(query);
          setCompanies(results);
          setIsOpen(true);
        } catch (error) {
          console.error('Failed to fetch companies:', error);
          setCompanies([]);
        } finally {
          setIsLoading(false);
        }
      } else {
        setCompanies([]);
        setIsOpen(false);
      }
    };

    const debounceTimer = setTimeout(fetchData, 300);
    return () => clearTimeout(debounceTimer);
  }, [query]);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleSelect = (company: Company) => {
    onSelectCompany(company);
    setQuery('');
    setIsOpen(false);
  };

  const handleClear = () => {
    setQuery('');
    setIsOpen(false);
    inputRef.current?.focus();
  };

  return (
    <div ref={containerRef} className="relative w-full max-w-2xl">
      <div className="relative">
        <Search className="absolute left-4 top-1/2 h-5 w-5 -translate-y-1/2 text-muted-foreground" />
        <Input
          ref={inputRef}
          type="text"
          placeholder="Search Malaysian companies by name or registration ID..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="h-14 pl-12 pr-12 text-base bg-card border-border shadow-[var(--shadow-card)] focus:shadow-[var(--shadow-elevated)] transition-shadow"
        />
        {query && (
          <Button
            variant="ghost"
            size="icon"
            className="absolute right-2 top-1/2 -translate-y-1/2 h-8 w-8"
            onClick={handleClear}
          >
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      {isOpen && (
        <div className="absolute top-full left-0 right-0 mt-2 bg-card border border-border rounded-lg shadow-[var(--shadow-overlay)] overflow-hidden z-50">
          {isLoading ? (
            <div className="flex items-center justify-center p-6">
              <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
              <span className="ml-2 text-muted-foreground">Searching...</span>
            </div>
          ) : companies.length > 0 ? (
            <ul className="max-h-80 overflow-auto scrollbar-thin">
              {companies.map((company) => (
                <li key={company.id}>
                  <button
                    onClick={() => handleSelect(company)}
                    className={cn(
                      "w-full px-4 py-3 flex items-center gap-4 hover:bg-accent transition-colors text-left",
                      selectedCompany?.id === company.id && "bg-accent"
                    )}
                  >
                    <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                      <Building2 className="h-5 w-5 text-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium truncate">{company.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {company.companyId} · {company.industry}
                      </p>
                    </div>
                  </button>
                </li>
              ))}
            </ul>
          ) : (
            <div className="p-6 text-center">
              <p className="text-muted-foreground">No companies found matching "{query}"</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
