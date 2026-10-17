'use client';

import { GovernmentLevel, VerificationLevel } from '@/types';
import { Filter, X } from 'lucide-react';

interface Filters {
  level: string;
  state: string;
  party: string;
  status: string;
  verification: string;
}

interface Props {
  filters: Filters;
  onChange: (key: keyof Filters, value: string) => void;
  onReset: () => void;
  states: { code: string; name: string }[];
  totalResults: number;
}

export default function FilterPanel({ filters, onChange, onReset, states, totalResults }: Props) {
  const hasActiveFilters = Object.values(filters).some(Boolean);

  return (
    <aside className="w-full lg:w-64 shrink-0 p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40 text-xs">
      <div className="flex items-center justify-between pb-3 border-b border-neutral-200 dark:border-neutral-800 mb-4">
        <div className="flex items-center gap-1.5 font-medium text-neutral-900 dark:text-neutral-100">
          <Filter className="w-3.5 h-3.5 text-neutral-500" />
          <span>Filters</span>
          <span className="text-neutral-400 font-normal">({totalResults})</span>
        </div>
        {hasActiveFilters && (
          <button
            onClick={onReset}
            className="text-[11px] text-accent dark:text-sky-400 hover:underline flex items-center gap-0.5"
          >
            <X className="w-3 h-3" />
            <span>Reset</span>
          </button>
        )}
      </div>

      <div className="space-y-4">
        {/* Government Level */}
        <div>
          <label className="block font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
            Government Level
          </label>
          <select
            value={filters.level}
            onChange={(e) => onChange('level', e.target.value)}
            className="w-full p-2 rounded border border-neutral-300 dark:border-neutral-700 bg-neutral-50 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:outline-none focus:border-accent"
          >
            <option value="">All Levels</option>
            <option value="federal">Federal</option>
            <option value="state">State / Territory</option>
            <option value="local">Local / Municipal</option>
          </select>
        </div>

        {/* State */}
        <div>
          <label className="block font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
            State / Jurisdiction
          </label>
          <select
            value={filters.state}
            onChange={(e) => onChange('state', e.target.value)}
            className="w-full p-2 rounded border border-neutral-300 dark:border-neutral-700 bg-neutral-50 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:outline-none focus:border-accent"
          >
            <option value="">All States / Jurisdictions</option>
            {states.map((s) => (
              <option key={s.code} value={s.code}>
                {s.name} ({s.code})
              </option>
            ))}
          </select>
        </div>

        {/* Status */}
        <div>
          <label className="block font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
            Tenure Status
          </label>
          <select
            value={filters.status}
            onChange={(e) => onChange('status', e.target.value)}
            className="w-full p-2 rounded border border-neutral-300 dark:border-neutral-700 bg-neutral-50 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:outline-none focus:border-accent"
          >
            <option value="">All Statuses</option>
            <option value="current">Current in Office</option>
            <option value="former">Former Official</option>
          </select>
        </div>

        {/* Verification Level */}
        <div>
          <label className="block font-medium text-neutral-700 dark:text-neutral-300 mb-1.5">
            Verification Level
          </label>
          <select
            value={filters.verification}
            onChange={(e) => onChange('verification', e.target.value)}
            className="w-full p-2 rounded border border-neutral-300 dark:border-neutral-700 bg-neutral-50 dark:bg-neutral-800 text-neutral-900 dark:text-neutral-100 focus:outline-none focus:border-accent"
          >
            <option value="">All Levels</option>
            <option value="verified">Verified (.gov portal)</option>
            <option value="corroborated">Corroborated</option>
            <option value="unverified">Unverified</option>
          </select>
        </div>
      </div>
    </aside>
  );
}
