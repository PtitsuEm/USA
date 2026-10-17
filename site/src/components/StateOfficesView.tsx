'use client';

import { useState, useMemo } from 'react';
import { Person, StateInfo } from '@/types';
import PersonCard from '@/components/PersonCard';
import {
  Landmark,
  Users,
  Building2,
  MapPin,
  Search,
  ChevronRight,
  X,
  UserCheck,
  Zap,
  Sprout,
  Factory,
  BatteryCharging,
  Server
} from 'lucide-react';

interface Props {
  state: StateInfo;
  officials: Person[];
}

type CategoryKey =
  | 'executive'
  | 'datacenter'
  | 'energy'
  | 'agri'
  | 'manufacturing'
  | 'ev'
  | 'congress'
  | 'senate'
  | 'house'
  | 'municipal';

interface CategoryConfig {
  key: CategoryKey;
  label: string;
  shortLabel: string;
  icon: any;
  description: string;
}

const CATEGORIES: CategoryConfig[] = [
  {
    key: 'executive',
    label: 'State Executive & EDA Leadership',
    shortLabel: 'Executive & EDA',
    icon: Landmark,
    description: 'Governors, Lt. Governors, Commerce Secretaries, SelectUSA Leads, and Deputy Directors.'
  },
  {
    key: 'datacenter',
    label: 'Data Centers & Computing Infrastructure',
    shortLabel: 'Data Centers & IT',
    icon: Server,
    description: 'State CIOs, CTOs, enterprise computing, AI cloud infrastructure, and data center attraction leads.'
  },
  {
    key: 'energy',
    label: 'Energy & Clean Technology',
    shortLabel: 'Energy & Clean Tech',
    icon: Zap,
    description: 'State Energy Office Directors, clean energy divisions, power grid, and renewable energy leads.'
  },
  {
    key: 'agri',
    label: 'Agriculture & AgriTech',
    shortLabel: 'AgriTech & Farming',
    icon: Sprout,
    description: 'Secretaries of Agriculture, commissioners, sustainable food systems, and agritech leads.'
  },
  {
    key: 'manufacturing',
    label: 'Advanced Manufacturing & Production',
    shortLabel: 'Manufacturing',
    icon: Factory,
    description: 'NIST MEP Center Directors, industrial production, supply chain, and factory expansion leads.'
  },
  {
    key: 'ev',
    label: 'Electric Vehicles & Infrastructure',
    shortLabel: 'EV Infrastructure',
    icon: BatteryCharging,
    description: 'Designated State NEVI Program coordinators, EV charging buildout, and clean mobility leads.'
  },
  {
    key: 'congress',
    label: 'U.S. Congressional Delegation',
    shortLabel: 'Congress',
    icon: Users,
    description: 'Federal U.S. Senators and Representatives representing this state in Washington D.C.'
  },
  {
    key: 'senate',
    label: 'State Senate Districts',
    shortLabel: 'State Senate',
    icon: Building2,
    description: 'Upper chamber state senators elected to the state legislature.'
  },
  {
    key: 'house',
    label: 'State House / Assembly Districts',
    shortLabel: 'State House',
    icon: Building2,
    description: 'Lower chamber state representatives or assembly members.'
  },
  {
    key: 'municipal',
    label: 'Municipal Mayors & City Managers',
    shortLabel: 'Municipal',
    icon: MapPin,
    description: 'Local city mayors, city managers, and municipal economic development heads.'
  }
];

export default function StateOfficesView({ state, officials }: Props) {
  // Partition officials into structured positions by category
  const categorized = useMemo(() => {
    const isEnergy = (p: Person) =>
      p.id.includes('energy') ||
      p.officeName.toLowerCase().includes('energy') ||
      p.officeName.toLowerCase().includes('power') ||
      (p.bio && p.bio.toLowerCase().includes('energy commission'));

    const isAgri = (p: Person) =>
      p.id.includes('agriculture') ||
      p.id.includes('agri-') ||
      p.officeName.toLowerCase().includes('agriculture') ||
      p.officeName.toLowerCase().includes('food & agriculture') ||
      p.officeName.toLowerCase().includes('farming');

    const isMfg = (p: Person) =>
      p.id.includes('manufacturing') ||
      p.id.includes('mfg-') ||
      p.officeName.toLowerCase().includes('mep') ||
      p.officeName.toLowerCase().includes('manufacturing');

    const isEv = (p: Person) =>
      p.id.includes('ev-') ||
      p.id.includes('sec-ev') ||
      p.officeName.toLowerCase().includes('electric vehicle') ||
      p.officeName.toLowerCase().includes('nevi') ||
      p.officeName.toLowerCase().includes('mobility');

    const isDataCenter = (p: Person) =>
      p.id.includes('data-center') ||
      p.officeName.toLowerCase().includes('information technology') ||
      p.officeName.toLowerCase().includes('cio') ||
      p.officeName.toLowerCase().includes('cto') ||
      p.officeName.toLowerCase().includes('technology services') ||
      p.officeName.toLowerCase().includes('digital service') ||
      p.officeName.toLowerCase().includes('data center');

    return {
      executive: officials.filter(
        (p) =>
          p.jurisdictionLevel === 'state' &&
          p.branch === 'executive' &&
          !isEnergy(p) &&
          !isAgri(p) &&
          !isMfg(p) &&
          !isEv(p) &&
          !isDataCenter(p)
      ),
      datacenter: officials.filter(isDataCenter),
      energy: officials.filter(isEnergy),
      agri: officials.filter(isAgri),
      manufacturing: officials.filter(isMfg),
      ev: officials.filter(isEv),
      congress: officials.filter((p) => p.jurisdictionLevel === 'federal'),
      senate: officials.filter(
        (p) => p.id.startsWith('leg-') && p.officeName.toLowerCase().includes('senat')
      ),
      house: officials.filter(
        (p) =>
          p.id.startsWith('leg-') &&
          (p.officeName.toLowerCase().includes('represent') || p.officeName.toLowerCase().includes('assembl'))
      ),
      municipal: officials.filter((p) => p.jurisdictionLevel === 'local'),
    };
  }, [officials]);

  // Find first category with records as default active tab
  const defaultTab = useMemo<CategoryKey>(() => {
    for (const cat of CATEGORIES) {
      if (categorized[cat.key] && categorized[cat.key].length > 0) {
        return cat.key;
      }
    }
    return 'executive';
  }, [categorized]);

  const [activeTab, setActiveTab] = useState<CategoryKey>(defaultTab);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPersonId, setSelectedPersonId] = useState<string | null>(null);

  // Current category officials
  const activeOfficials = categorized[activeTab] || [];

  // Filter within active category
  const filteredOfficials = useMemo(() => {
    if (!searchQuery.trim()) return activeOfficials;
    const q = searchQuery.toLowerCase();
    return activeOfficials.filter((p) => {
      const matchOffice = p.officeName.toLowerCase().includes(q);
      const matchName = p.fullName.toLowerCase().includes(q);
      const matchParty = p.party?.toLowerCase().includes(q);
      const matchDistrict = p.jurisdictionDistrict?.toLowerCase().includes(q);
      return matchOffice || matchName || matchParty || matchDistrict;
    });
  }, [activeOfficials, searchQuery]);

  // The currently selected official to display
  const selectedOfficial = useMemo(() => {
    if (!selectedPersonId) return null;
    return officials.find((p) => p.id === selectedPersonId) || null;
  }, [selectedPersonId, officials]);

  const activeCategoryConfig = CATEGORIES.find((c) => c.key === activeTab)!;

  return (
    <div className="space-y-6">
      {/* Category Tabs */}
      <div>
        <div className="text-xs font-semibold uppercase tracking-wider text-neutral-400 dark:text-neutral-500 mb-2">
          Select Government Branch, Chamber, or Sector
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2">
          {CATEGORIES.map((cat) => {
            const count = categorized[cat.key]?.length || 0;
            if (count === 0) return null;
            const Icon = cat.icon;
            const isActive = activeTab === cat.key;

            return (
              <button
                key={cat.key}
                onClick={() => {
                  setActiveTab(cat.key);
                  setSearchQuery('');
                  setSelectedPersonId(null);
                }}
                className={`p-3 rounded-lg border text-left transition-all duration-150 flex flex-col justify-between ${
                  isActive
                    ? 'border-accent dark:border-sky-500 bg-neutral-900 text-white dark:bg-neutral-800 shadow-sm'
                    : 'border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/50 text-neutral-700 dark:text-neutral-300 hover:border-neutral-300 dark:hover:border-neutral-700'
                }`}
              >
                <div className="flex items-center justify-between w-full mb-1">
                  <Icon className={`w-4 h-4 ${isActive ? 'text-sky-300' : 'text-neutral-400'}`} />
                  <span className={`text-xs font-mono font-semibold ${isActive ? 'text-sky-300' : 'text-neutral-500'}`}>
                    {count.toLocaleString()}
                  </span>
                </div>
                <div className="font-serif text-xs font-bold leading-tight">
                  {cat.shortLabel}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Selected Category Header & Search */}
      <div className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-neutral-50/70 dark:bg-neutral-900/40 space-y-3">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
          <div>
            <h2 className="font-serif text-lg font-bold text-neutral-900 dark:text-white">
              {activeCategoryConfig.label}
            </h2>
            <p className="text-xs text-neutral-500 mt-0.5">
              {activeCategoryConfig.description} ({filteredOfficials.length} positions)
            </p>
          </div>

          {/* Position Search */}
          <div className="relative w-full sm:w-64">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-neutral-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search positions or names..."
              className="w-full pl-8 pr-3 py-1.5 text-xs rounded border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white placeholder-neutral-400 focus:outline-none focus:border-accent dark:focus:border-sky-400"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery('')}
                className="absolute right-2 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600"
              >
                <X className="w-3 h-3" />
              </button>
            )}
          </div>
        </div>

        {/* Selected Official Drawer / Spotlight */}
        {selectedOfficial ? (
          <div className="pt-3 border-t border-neutral-200 dark:border-neutral-800">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-accent dark:text-sky-400 uppercase tracking-wide">
                <UserCheck className="w-4 h-4" />
                <span>Selected Office Holder: {selectedOfficial.officeName}</span>
              </div>
              <button
                onClick={() => setSelectedPersonId(null)}
                className="text-xs text-neutral-500 hover:text-neutral-900 dark:hover:text-white flex items-center gap-1 font-mono"
              >
                <X className="w-3.5 h-3.5" />
                <span>Close preview</span>
              </button>
            </div>
            <div className="max-w-xl">
              <PersonCard person={selectedOfficial} />
            </div>
          </div>
        ) : (
          <div className="pt-2 text-xs text-neutral-500 font-mono flex items-center gap-1.5">
            <span>👉</span>
            <span>Click any position below to view official credentials, contact info, and verifiable sources.</span>
          </div>
        )}
      </div>

      {/* Grid of Positions / Offices */}
      <div>
        <div className="text-xs font-semibold uppercase tracking-wider text-neutral-400 dark:text-neutral-500 mb-2.5 flex items-center justify-between">
          <span>Positions in this Chamber / Level</span>
          <span className="text-neutral-400 font-normal">Click a position to reveal official</span>
        </div>

        {filteredOfficials.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5 max-h-[620px] overflow-y-auto p-1 border border-neutral-200 dark:border-neutral-800 rounded-lg">
            {filteredOfficials.map((person) => {
              const isSelected = selectedPersonId === person.id;
              return (
                <button
                  key={person.id}
                  onClick={() => setSelectedPersonId(isSelected ? null : person.id)}
                  className={`p-3 rounded-lg border text-left transition-all duration-150 flex flex-col justify-between group ${
                    isSelected
                      ? 'border-accent dark:border-sky-400 bg-neutral-100 dark:bg-neutral-800/90 shadow-sm'
                      : 'border-neutral-200 dark:border-neutral-800/80 bg-white dark:bg-neutral-900/60 hover:border-neutral-300 dark:hover:border-neutral-700 hover:bg-neutral-50 dark:hover:bg-neutral-800/40'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2 w-full">
                    <span className="font-serif text-xs font-semibold text-neutral-900 dark:text-neutral-100 group-hover:text-accent dark:group-hover:text-sky-400 leading-snug">
                      {person.officeName}
                    </span>
                    <ChevronRight
                      className={`w-3.5 h-3.5 shrink-0 transition-transform ${
                        isSelected
                          ? 'rotate-90 text-accent dark:text-sky-400'
                          : 'text-neutral-300 dark:text-neutral-600 group-hover:text-neutral-500'
                      }`}
                    />
                  </div>

                  <div className="mt-2 pt-2 border-t border-neutral-100 dark:border-neutral-800/60 flex items-center justify-between text-[11px] text-neutral-500 w-full">
                    <span className="truncate text-neutral-700 dark:text-neutral-300 font-medium">
                      {person.fullName}
                    </span>
                    {person.party && (
                      <span className="text-[10px] font-mono px-1 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-500">
                        {person.party.slice(0, 3).toUpperCase()}
                      </span>
                    )}
                  </div>
                </button>
              );
            })}
          </div>
        ) : (
          <div className="p-8 text-center border border-dashed border-neutral-200 dark:border-neutral-800 rounded-lg text-xs text-neutral-500">
            No positions matching &quot;{searchQuery}&quot; found in this category.
          </div>
        )}
      </div>
    </div>
  );
}
