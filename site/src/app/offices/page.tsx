import Link from 'next/link';
import Breadcrumbs from '@/components/Breadcrumbs';
import { getOffices } from '@/lib/data';
import { Building2, ChevronRight } from 'lucide-react';

export default async function OfficesDirectoryPage() {
  const offices = await getOffices();

  const federalOffices = offices.filter((o) => o.level === 'federal');
  const stateOffices = offices.filter((o) => o.level === 'state').slice(0, 30);
  const localOffices = offices.filter((o) => o.level === 'local').slice(0, 30);

  return (
    <div className="space-y-8">
      <Breadcrumbs items={[{ label: 'Offices' }]} />

      <div>
        <h1 className="font-serif text-3xl font-bold text-neutral-900 dark:text-white">
          Public Offices Directory
        </h1>
        <p className="text-xs text-neutral-500 dark:text-neutral-400 mt-1">
          Explore executive, legislative, and municipal government positions and historical officeholders.
        </p>
      </div>

      {/* Federal Offices */}
      <section>
        <h2 className="font-serif text-lg font-semibold text-neutral-900 dark:text-white mb-3">
          Federal Executive & Constitutional Offices
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
          {federalOffices.map((office) => (
            <Link
              key={office.id}
              href={`/offices/${office.slug}`}
              className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40 hover:border-neutral-300 dark:hover:border-neutral-700 transition-colors flex items-center justify-between group"
            >
              <div>
                <div className="font-medium text-sm text-neutral-900 dark:text-white group-hover:underline">
                  {office.name}
                </div>
                {office.currentHolderName && (
                  <div className="text-xs text-neutral-500 mt-0.5">
                    Current: <span className="text-neutral-700 dark:text-neutral-300 font-medium">{office.currentHolderName}</span>
                  </div>
                )}
              </div>
              <ChevronRight className="w-4 h-4 text-neutral-400 group-hover:text-accent dark:group-hover:text-sky-400" />
            </Link>
          ))}
        </div>
      </section>

      {/* State & Municipal Samples */}
      <section>
        <h2 className="font-serif text-lg font-semibold text-neutral-900 dark:text-white mb-3">
          Sample State & Municipal Offices
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-2.5">
          {stateOffices.concat(localOffices).slice(0, 24).map((office) => (
            <Link
              key={office.id}
              href={`/offices/${office.slug}`}
              className="p-3 rounded border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/30 hover:bg-neutral-50 dark:hover:bg-neutral-800/40 transition-colors block text-xs"
            >
              <div className="font-medium text-neutral-900 dark:text-white truncate">
                {office.name}
              </div>
              <div className="text-[11px] text-neutral-400 mt-0.5 truncate">
                {office.jurisdictionState || 'Local'} · {office.currentHolderName}
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  );
}
