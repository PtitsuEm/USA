'use client';

import { useState, useMemo, useEffect, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import SearchBar from '@/components/SearchBar';
import PersonCard from '@/components/PersonCard';
import FilterPanel from '@/components/FilterPanel';
import Breadcrumbs from '@/components/Breadcrumbs';
import { Person } from '@/types';
import peopleData from '@/data/all_people.json';
import { STATE_MAP } from '@/lib/data';
import { ArrowUpDown, ChevronLeft, ChevronRight } from 'lucide-react';

const allPeople: Person[] = peopleData as Person[];
const stateOptions = Object.values(STATE_MAP);

function DirectoryContent() {
  const searchParams = useSearchParams();
  const router = useRouter();

  const [query, setQuery] = useState(searchParams.get('q') || '');
  const [level, setLevel] = useState(searchParams.get('level') || '');
  const [state, setState] = useState(searchParams.get('state') || '');
  const [status, setStatus] = useState(searchParams.get('status') || '');
  const [verification, setVerification] = useState(searchParams.get('verification') || '');
  const [sortBy, setSortBy] = useState('name');
  const [page, setPage] = useState(1);
  const pageSize = 20;

  // Sync state to URL params
  useEffect(() => {
    const params = new URLSearchParams();
    if (query) params.set('q', query);
    if (level) params.set('level', level);
    if (state) params.set('state', state);
    if (status) params.set('status', status);
    if (verification) params.set('verification', verification);

    const queryString = params.toString();
    const newUrl = queryString ? `/people?${queryString}` : '/people';
    window.history.replaceState(null, '', newUrl);
  }, [query, level, state, status, verification]);

  // Filter and sort people
  const filteredPeople = useMemo(() => {
    return allPeople.filter((p) => {
      if (query.trim()) {
        const q = query.toLowerCase();
        const matchesName = p.fullName.toLowerCase().includes(q);
        const matchesOffice = p.officeName.toLowerCase().includes(q);
        const matchesState = p.jurisdictionState?.toLowerCase().includes(q);
        const matchesParty = p.party?.toLowerCase().includes(q);
        if (!matchesName && !matchesOffice && !matchesState && !matchesParty) {
          return false;
        }
      }
      if (level && p.jurisdictionLevel?.toLowerCase() !== level.toLowerCase()) return false;
      if (state) {
        const matchEntry = Object.values(STATE_MAP).find(
          (s) => s.name.toLowerCase() === state.toLowerCase() || s.code.toLowerCase() === state.toLowerCase()
        );
        const allowed = matchEntry ? [matchEntry.code.toUpperCase(), matchEntry.name.toLowerCase()] : [state.toLowerCase()];
        const pState = (p.jurisdictionState || '').toUpperCase();
        if (!allowed.includes(pState) && !allowed.includes((p.jurisdictionState || '').toLowerCase())) return false;
      }
      if (status && p.status?.toLowerCase() !== status.toLowerCase()) return false;
      if (verification && p.verificationLevel?.toLowerCase() !== verification.toLowerCase()) return false;

      return true;
    }).sort((a, b) => {
      if (sortBy === 'name') return a.fullName.localeCompare(b.fullName);
      if (sortBy === 'office') return a.officeName.localeCompare(b.officeName);
      if (sortBy === 'state') return (a.jurisdictionState || '').localeCompare(b.jurisdictionState || '');
      return 0;
    });
  }, [query, level, state, status, verification, sortBy]);

  const totalPages = Math.ceil(filteredPeople.length / pageSize) || 1;
  const currentItems = useMemo(() => {
    const start = (page - 1) * pageSize;
    return filteredPeople.slice(start, start + pageSize);
  }, [filteredPeople, page]);

  const handleFilterChange = (key: string, value: string) => {
    setPage(1);
    if (key === 'level') setLevel(value);
    if (key === 'state') setState(value);
    if (key === 'status') setStatus(value);
    if (key === 'verification') setVerification(value);
  };

  const handleResetFilters = () => {
    setQuery('');
    setLevel('');
    setState('');
    setStatus('');
    setVerification('');
    setPage(1);
  };

  return (
    <div>
      <Breadcrumbs items={[{ label: 'Directory' }]} />

      <div className="flex flex-col md:flex-row items-baseline justify-between gap-4 mb-6">
        <div>
          <h1 className="font-serif text-2xl sm:text-3xl font-bold text-neutral-900 dark:text-white">
            Directory of Officials
          </h1>
          <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
            Browse and filter {allPeople.length.toLocaleString()} verified federal, state, and local public officials.
          </p>
        </div>

        <div className="flex items-center gap-2 text-xs">
          <ArrowUpDown className="w-3.5 h-3.5 text-neutral-400" />
          <span className="text-neutral-500">Sort by:</span>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="p-1.5 rounded border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-800 dark:text-neutral-200 focus:outline-none"
          >
            <option value="name">Name (A–Z)</option>
            <option value="office">Office Title</option>
            <option value="state">State / Jurisdiction</option>
          </select>
        </div>
      </div>

      <div className="flex flex-col lg:flex-row gap-6 items-start">
        {/* Sticky Sidebar Filter */}
        <FilterPanel
          filters={{ level, state, party: '', status, verification }}
          onChange={handleFilterChange as any}
          onReset={handleResetFilters}
          states={stateOptions}
          totalResults={filteredPeople.length}
        />

        {/* Main Content Area */}
        <div className="flex-1 w-full space-y-4">
          {/* Quick Sector Filter Pills */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 text-xs no-scrollbar">
            {[
              { label: 'All Officials', q: '', levelVal: '' },
              { label: '💾 Data Centers & IT', q: 'Information Technology', levelVal: '' },
              { label: '⚡ Energy & Clean Tech', q: 'Energy', levelVal: '' },
              { label: '🌱 AgriTech & Agriculture', q: 'Agriculture', levelVal: '' },
              { label: '🏭 Advanced Manufacturing', q: 'Manufacturing', levelVal: '' },
              { label: '🚗 EV Infrastructure', q: 'Electric Vehicle', levelVal: '' },
              { label: '🏛️ State Leadership & EDA', q: '', levelVal: 'state' },
              { label: '👥 Congress Delegation', q: '', levelVal: 'federal' },
              { label: '📍 Mayors & Local', q: '', levelVal: 'local' },
            ].map((pill) => {
              const isActive = (pill.q ? query === pill.q : (pill.levelVal ? level === pill.levelVal && !query : !query && !level));
              return (
                <button
                  key={pill.label}
                  onClick={() => {
                    setQuery(pill.q);
                    setLevel(pill.levelVal);
                    setPage(1);
                  }}
                  className={`px-3 py-1.5 rounded-full border whitespace-nowrap transition-colors font-medium text-[11px] ${
                    isActive
                      ? 'bg-neutral-900 text-white dark:bg-sky-500 dark:text-neutral-950 border-neutral-900 dark:border-sky-500 shadow-sm'
                      : 'bg-white dark:bg-neutral-800/80 text-neutral-600 dark:text-neutral-300 border-neutral-200 dark:border-neutral-700 hover:border-neutral-300 dark:hover:border-neutral-600'
                  }`}
                >
                  {pill.label}
                </button>
              );
            })}
          </div>

          <SearchBar
            initialQuery={query}
            onSearch={(q) => {
              setQuery(q);
              setPage(1);
            }}
            placeholder="Filter list by name, title, or agency..."
          />

          <div className="flex items-center justify-between text-xs text-neutral-500">
            <span>
              Showing {currentItems.length > 0 ? (page - 1) * pageSize + 1 : 0}–
              {Math.min(page * pageSize, filteredPeople.length)} of {filteredPeople.length} matching officials
            </span>
            {filteredPeople.length > pageSize && (
              <span>
                Page {page} of {totalPages}
              </span>
            )}
          </div>

          {currentItems.length > 0 ? (
            <div className="grid grid-cols-1 gap-3">
              {currentItems.map((person) => (
                <PersonCard key={person.id} person={person} />
              ))}
            </div>
          ) : (
            <div className="p-12 text-center border border-dashed border-neutral-300 dark:border-neutral-800 rounded-lg">
              <p className="font-serif text-base text-neutral-700 dark:text-neutral-300 mb-1">
                No matching officials found
              </p>
              <p className="text-xs text-neutral-500 mb-4">
                Try loosening your filter criteria or searching with a different term.
              </p>
              <button
                onClick={handleResetFilters}
                className="px-3 py-1.5 text-xs font-medium rounded border border-neutral-300 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-800"
              >
                Reset all filters
              </button>
            </div>
          )}

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="pt-6 border-t border-neutral-200 dark:border-neutral-800 flex items-center justify-between text-xs">
              <button
                disabled={page <= 1}
                onClick={() => {
                  setPage((p) => Math.max(1, p - 1));
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className="px-3 py-1.5 rounded border border-neutral-300 dark:border-neutral-700 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-neutral-100 dark:hover:bg-neutral-800 flex items-center gap-1"
              >
                <ChevronLeft className="w-3.5 h-3.5" />
                Previous
              </button>
              <span className="text-neutral-500 font-mono">
                {page} / {totalPages}
              </span>
              <button
                disabled={page >= totalPages}
                onClick={() => {
                  setPage((p) => Math.min(totalPages, p + 1));
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className="px-3 py-1.5 rounded border border-neutral-300 dark:border-neutral-700 disabled:opacity-40 disabled:cursor-not-allowed hover:bg-neutral-100 dark:hover:bg-neutral-800 flex items-center gap-1"
              >
                Next
                <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function PeoplePage() {
  return (
    <Suspense fallback={<div className="p-12 text-center text-xs text-neutral-500 font-mono">Loading directory...</div>}>
      <DirectoryContent />
    </Suspense>
  );
}
