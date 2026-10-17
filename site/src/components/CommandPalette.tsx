'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Search, X, User, Building, MapPin } from 'lucide-react';
import { Person } from '@/types';

export default function CommandPalette() {
  const [isOpen, setIsOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<Person[]>([]);
  const router = useRouter();

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setIsOpen((prev) => !prev);
      }
      if (e.key === 'Escape' && isOpen) {
        setIsOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen]);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }
    // Perform fast local search
    fetch(`/api/search?q=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => setResults(data.slice(0, 8)))
      .catch(() => {});
  }, [query]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-16 sm:pt-24 px-4 bg-black/50 backdrop-blur-sm animate-in fade-in-0 duration-150">
      <div className="relative w-full max-w-xl rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 shadow-2xl overflow-hidden">
        <div className="flex items-center px-4 py-3 border-b border-neutral-200 dark:border-neutral-800">
          <Search className="w-4 h-4 text-neutral-400 mr-3 shrink-0" />
          <input
            type="text"
            autoFocus
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search officials, offices, states... (Esc to close)"
            className="w-full text-sm bg-transparent text-neutral-900 dark:text-white placeholder:text-neutral-400 focus:outline-none"
          />
          <button
            onClick={() => setIsOpen(false)}
            className="p-1 rounded hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-400"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {results.length > 0 && (
          <ul className="max-h-80 overflow-y-auto py-2 divide-y divide-neutral-100 dark:divide-neutral-800/60">
            {results.map((person) => (
              <li key={person.id}>
                <button
                  onClick={() => {
                    setIsOpen(false);
                    router.push(`/people/${person.slug}`);
                  }}
                  className="w-full px-4 py-2.5 text-left flex items-start gap-3 hover:bg-neutral-50 dark:hover:bg-neutral-800/50 transition-colors"
                >
                  <User className="w-4 h-4 text-neutral-400 mt-0.5 shrink-0" />
                  <div className="min-w-0 flex-1">
                    <div className="text-sm font-medium text-neutral-900 dark:text-neutral-100 truncate">
                      {person.fullName}
                    </div>
                    <div className="text-xs text-neutral-500 truncate">
                      {person.officeName} {person.jurisdictionState ? `· ${person.jurisdictionState}` : ''}
                    </div>
                  </div>
                </button>
              </li>
            ))}
          </ul>
        )}

        {query && results.length === 0 && (
          <div className="p-8 text-center text-xs text-neutral-500">
            No matching officials found. Press Enter to view full directory search.
          </div>
        )}

        <div className="px-4 py-2 bg-neutral-50 dark:bg-neutral-900 border-t border-neutral-100 dark:border-neutral-800 flex items-center justify-between text-[11px] text-neutral-400">
          <span>Navigate with mouse or Tab</span>
          <span>ESC to close</span>
        </div>
      </div>
    </div>
  );
}
