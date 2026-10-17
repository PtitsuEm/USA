import { notFound } from 'next/navigation';
import Link from 'next/link';
import Breadcrumbs from '@/components/Breadcrumbs';
import { getOfficeBySlug, getOffices } from '@/lib/data';
import { Building2, User } from 'lucide-react';

interface Props {
  params: { slug: string };
}

export async function generateStaticParams() {
  const offices = await getOffices();
  return offices.slice(0, 20).map((o) => ({ slug: o.slug }));
}

export default async function OfficeDetailPage({ params }: Props) {
  const office = await getOfficeBySlug(params.slug);
  if (!office) notFound();

  return (
    <div className="space-y-8">
      <Breadcrumbs
        items={[
          { label: 'Offices', href: '/offices' },
          { label: office.name },
        ]}
      />

      <div className="border-b border-neutral-200 dark:border-neutral-800 pb-6">
        <span className="capitalize px-2 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-xs font-medium text-neutral-600 dark:text-neutral-300">
          {office.level} · {office.branch} branch
        </span>
        <h1 className="font-serif text-3xl font-bold text-neutral-900 dark:text-white mt-2">
          {office.name}
        </h1>
        {office.description && (
          <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-2">
            {office.description}
          </p>
        )}
      </div>

      {/* Officeholders Timeline */}
      <section className="space-y-4">
        <h2 className="font-serif text-lg font-semibold text-neutral-900 dark:text-white">
          Officeholders Timeline
        </h2>
        <div className="divide-y divide-neutral-200 dark:divide-neutral-800 border border-neutral-200 dark:border-neutral-800 rounded-lg overflow-hidden bg-white dark:bg-neutral-900/40">
          {office.holdersTimeline.map((holder, idx) => (
            <div key={idx} className="p-4 flex items-center justify-between text-xs sm:text-sm">
              <div className="flex items-center gap-3">
                <User className="w-4 h-4 text-neutral-400" />
                <div>
                  <Link
                    href={`/people/${holder.personSlug}`}
                    className="font-medium text-neutral-900 dark:text-white hover:text-accent dark:hover:text-sky-400 hover:underline"
                  >
                    {holder.personName}
                  </Link>
                  {holder.party && (
                    <span className="text-neutral-400 ml-2">({holder.party})</span>
                  )}
                </div>
              </div>
              <div className="font-mono text-neutral-500 text-xs">
                {holder.startDate} — {holder.endDate || 'Present'}
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
