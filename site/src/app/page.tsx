import Link from 'next/link';
import SearchBar from '@/components/SearchBar';
import PersonCard from '@/components/PersonCard';
import { getStats, getStates, getPeople } from '@/lib/data';
import { Building2, Landmark, Scale, Users, Award, ShieldCheck, MapPin, Zap, Sprout, Factory, BatteryCharging, Server } from 'lucide-react';

export default async function HomePage() {
  const stats = await getStats();
  const states = await getStates();
  const allPeople = await getPeople();
  const samplePeople = allPeople.slice(0, 4);

  const quickBrowse = [
    { label: 'Data Centers & AI Cloud', href: '/people?q=Information+Technology', count: stats.datacenter, icon: Server },
    { label: 'Energy & Clean Tech', href: '/people?q=Energy', count: stats.energy, icon: Zap },
    { label: 'AgriTech & Agriculture', href: '/people?q=Agriculture', count: stats.agri, icon: Sprout },
    { label: 'Advanced Manufacturing', href: '/people?q=Manufacturing', count: stats.manufacturing, icon: Factory },
    { label: 'EV Infrastructure & NEVI', href: '/people?q=Electric+Vehicle', count: stats.ev, icon: BatteryCharging },
    { label: 'State Leadership & EDA', href: '/people?level=state', count: stats.stateLeadership, icon: Landmark },
    { label: 'Governors & Lt. Govs', href: '/people?level=state', count: stats.governors, icon: Award },
    { label: 'State Legislatures', href: '/people?level=state', count: stats.stateLegislatures, icon: Building2 },
    { label: 'Local Mayors & Managers', href: '/people?level=local', count: stats.local, icon: MapPin },
    { label: 'Senate & House (Congress)', href: '/people?level=federal', count: stats.congress, icon: Users },
  ];

  return (
    <div className="space-y-12">
      {/* Hero & Search */}
      <section className="text-center pt-6 pb-2 space-y-5">
        <h1 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight text-neutral-900 dark:text-white">
          U.S. Public Officials Database
        </h1>
        <p className="max-w-xl mx-auto text-sm sm:text-base text-neutral-600 dark:text-neutral-400 font-normal leading-relaxed">
          A minimalist, verifiable reference database of federal, state, and municipal leadership. Every fact is cited to an official primary source.
        </p>

        <div className="max-w-2xl mx-auto pt-2">
          <SearchBar autoFocus className="shadow-sm" />
        </div>

        {/* Small stats line */}
        <div className="flex items-center justify-center gap-4 text-xs text-neutral-500 dark:text-neutral-400 font-mono pt-1">
          <span>{stats.total.toLocaleString()} total records</span>
          <span>·</span>
          <span className="inline-flex items-center gap-1 text-emerald-600 dark:text-emerald-400 font-medium">
            <ShieldCheck className="w-3.5 h-3.5" />
            {stats.verifiedPct}% primary verified
          </span>
          <span>·</span>
          <span>Updated {stats.lastUpdated}</span>
        </div>
      </section>

      {/* Quick Browse Tiles */}
      <section>
        <div className="text-xs font-semibold uppercase tracking-wider text-neutral-400 dark:text-neutral-500 mb-3">
          Quick Browse by Branch & Level
        </div>
        <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
          {quickBrowse.map((tile) => {
            const Icon = tile.icon;
            return (
              <Link
                key={tile.label}
                href={tile.href}
                className="p-3.5 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/60 hover:border-neutral-300 dark:hover:border-neutral-700 hover:shadow-sm transition-all duration-150 flex items-center justify-between group"
              >
                <div className="flex items-center gap-2.5">
                  <Icon className="w-4 h-4 text-neutral-400 group-hover:text-accent dark:group-hover:text-sky-400 transition-colors" />
                  <span className="text-sm font-medium text-neutral-900 dark:text-neutral-100 group-hover:underline">
                    {tile.label}
                  </span>
                </div>
                <span className="text-xs font-mono text-neutral-400 dark:text-neutral-500">
                  {tile.count.toLocaleString()}
                </span>
              </Link>
            );
          })}
        </div>
      </section>

      {/* Browse by State Grid */}
      <section>
        <div className="flex items-center justify-between mb-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
            Browse by State & Territory (50 States + DC + Territories)
          </div>
          <Link href="/states/al" className="text-xs text-accent dark:text-sky-400 hover:underline">
            View all
          </Link>
        </div>

        <div className="grid grid-cols-4 sm:grid-cols-8 md:grid-cols-10 gap-1.5 text-center text-xs">
          {states.map((st) => (
            <Link
              key={st.code}
              href={`/states/${st.code.toLowerCase()}`}
              className="p-2 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40 hover:bg-neutral-50 dark:hover:bg-neutral-800 hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors"
              title={`${st.name} (${st.officialsCount} officials)`}
            >
              <div className="font-semibold text-neutral-900 dark:text-neutral-100 font-mono">
                {st.code}
              </div>
              <div className="text-[10px] text-neutral-400 truncate">
                {st.officialsCount}
              </div>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Verified Entries */}
      <section>
        <div className="flex items-center justify-between mb-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-neutral-400 dark:text-neutral-500">
            Sample Traceable Profiles
          </div>
          <Link href="/people" className="text-xs text-accent dark:text-sky-400 hover:underline">
            View full directory →
          </Link>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          {samplePeople.map((person) => (
            <PersonCard key={person.id} person={person} />
          ))}
        </div>
      </section>
    </div>
  );
}
