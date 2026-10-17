import { notFound } from 'next/navigation';
import Link from 'next/link';
import type { Metadata } from 'next';
import Breadcrumbs from '@/components/Breadcrumbs';
import VerificationBadge from '@/components/VerificationBadge';
import Timeline from '@/components/Timeline';
import SourceList from '@/components/SourceList';
import { getPersonBySlug, getPeople } from '@/lib/data';
import {
  Building2,
  Calendar,
  GraduationCap,
  Mail,
  Phone,
  ExternalLink,
  ShieldAlert,
  Clock,
  MapPin,
  Share2,
  Printer,
  ChevronRight
} from 'lucide-react';

interface Props {
  params: { slug: string };
}

export async function generateStaticParams() {
  const people = await getPeople();
  return people.slice(0, 50).map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const person = await getPersonBySlug(params.slug);
  if (!person) return { title: 'Person Not Found' };

  return {
    title: `${person.fullName} — ${person.officeName} | U.S. Officials Directory`,
    description: person.bio || `${person.fullName} serves as ${person.officeName}. Verified public record and office profile.`,
    openGraph: {
      title: `${person.fullName} — ${person.officeName}`,
      description: person.bio,
    },
  };
}

export default async function PersonProfilePage({ params }: Props) {
  const person = await getPersonBySlug(params.slug);
  if (!person) notFound();

  // Related officials in same state or office level
  const allPeople = await getPeople();
  const related = allPeople
    .filter((p) => p.id !== person.id && p.jurisdictionState === person.jurisdictionState)
    .slice(0, 3);

  // Schema.org Person JSON-LD
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    name: person.fullName,
    jobTitle: person.officeName,
    url: person.officialWebsite,
    birthDate: person.birthDate,
    birthPlace: person.birthPlace,
    worksFor: {
      '@type': 'GovernmentOrganization',
      name: person.jurisdictionState || 'United States Government',
    },
  };

  return (
    <article className="space-y-8">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />

      <Breadcrumbs
        items={[
          { label: 'Directory', href: '/people' },
          { label: person.jurisdictionState || 'Federal', href: `/people?state=${encodeURIComponent(person.jurisdictionState || '')}` },
          { label: person.fullName },
        ]}
      />

      {/* Profile Header */}
      <div className="border-b border-neutral-200 dark:border-neutral-800 pb-6">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
          <div>
            <div className="flex items-center gap-2.5 flex-wrap mb-1.5">
              <span className="capitalize px-2 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-xs font-medium text-neutral-600 dark:text-neutral-300">
                {person.jurisdictionLevel} level
              </span>
              <VerificationBadge level={person.verificationLevel} />
              {person.status === 'former' && (
                <span className="px-2 py-0.5 rounded text-xs uppercase font-bold tracking-wider bg-neutral-100 dark:bg-neutral-800 text-neutral-500">
                  Former Official
                </span>
              )}
            </div>

            <h1 className="font-serif text-3xl sm:text-4xl font-bold text-neutral-900 dark:text-white">
              {person.fullName}
            </h1>

            <p className="text-base text-neutral-600 dark:text-neutral-400 font-medium mt-1">
              {person.officeName}
              {person.party && <span className="text-neutral-400"> · {person.party}</span>}
              {person.jurisdictionState && <span className="text-neutral-400"> · {person.jurisdictionState}</span>}
            </p>
          </div>

          <div className="flex items-center gap-2 shrink-0">
            <Link
              href={`/contribute?person=${encodeURIComponent(person.fullName)}`}
              className="px-3 py-1.5 text-xs font-medium rounded-md border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 hover:bg-neutral-50 dark:hover:bg-neutral-800 flex items-center gap-1.5 text-neutral-700 dark:text-neutral-300 transition-colors"
            >
              <ShieldAlert className="w-3.5 h-3.5 text-neutral-400" />
              <span>Suggest correction</span>
            </Link>
          </div>
        </div>

        {person.bio && (
          <p className="mt-4 text-sm text-neutral-700 dark:text-neutral-300 leading-relaxed max-w-3xl">
            {person.bio}
          </p>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 items-start">
        {/* Main Details (2 Cols) */}
        <div className="md:col-span-2 space-y-8">
          {/* Career Timeline */}
          {person.timeline && person.timeline.length > 0 && (
            <section className="p-5 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40">
              <h2 className="font-serif text-lg font-semibold text-neutral-900 dark:text-white mb-4">
                Public Career & Positions
              </h2>
              <Timeline items={person.timeline} />
            </section>
          )}

          {/* Committees & Roles */}
          {person.committees && person.committees.length > 0 && (
            <section className="p-5 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40">
              <h2 className="font-serif text-lg font-semibold text-neutral-900 dark:text-white mb-3">
                Committees & Assignments
              </h2>
              <ul className="space-y-1.5 text-xs text-neutral-700 dark:text-neutral-300">
                {person.committees.map((com, idx) => (
                  <li key={idx} className="flex items-center gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-accent dark:bg-sky-500 shrink-0" />
                    <span>{com}</span>
                  </li>
                ))}
              </ul>
            </section>
          )}

          {/* Elections History */}
          {person.elections && person.elections.length > 0 && (
            <section className="p-5 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40">
              <h2 className="font-serif text-lg font-semibold text-neutral-900 dark:text-white mb-3">
                Electoral History
              </h2>
              <div className="divide-y divide-neutral-100 dark:divide-neutral-800 text-xs">
                {person.elections.map((elec, idx) => (
                  <div key={idx} className="py-2.5 flex items-center justify-between">
                    <div>
                      <span className="font-semibold text-neutral-900 dark:text-white">{elec.year}</span>
                      <span className="text-neutral-500 ml-2">{elec.officeName}</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <span className="uppercase text-[10px] font-bold px-1.5 py-0.5 rounded bg-emerald-50 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-400">
                        {elec.result}
                      </span>
                      {elec.votePct && (
                        <span className="text-neutral-500 font-mono">{elec.votePct}%</span>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Sources block */}
          <SourceList sources={person.sources} />
        </div>

        {/* Quick Facts Sidebar (1 Col) */}
        <aside className="space-y-6">
          <div className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-neutral-50/50 dark:bg-neutral-900/60 text-xs space-y-3.5">
            <h3 className="font-serif text-sm font-semibold text-neutral-900 dark:text-white pb-2 border-b border-neutral-200 dark:border-neutral-800">
              Quick Facts
            </h3>

            <div>
              <span className="text-neutral-400 block mb-0.5">Full Official Name</span>
              <span className="font-medium text-neutral-800 dark:text-neutral-200">{person.fullName}</span>
            </div>

            {person.birthDate && (
              <div>
                <span className="text-neutral-400 block mb-0.5">Born</span>
                <span className="font-medium text-neutral-800 dark:text-neutral-200">
                  {person.birthDate} {person.birthPlace ? `(${person.birthPlace})` : ''}
                </span>
              </div>
            )}

            {person.education && person.education.length > 0 && (
              <div>
                <span className="text-neutral-400 block mb-0.5">Education</span>
                <span className="font-medium text-neutral-800 dark:text-neutral-200">
                  {person.education.join(', ')}
                </span>
              </div>
            )}

            <div>
              <span className="text-neutral-400 block mb-0.5">Jurisdiction</span>
              <span className="font-medium text-neutral-800 dark:text-neutral-200">
                {person.jurisdictionState || 'United States Federal'}
              </span>
            </div>

            {/* Contacts & Portals */}
            <div className="pt-2 border-t border-neutral-200 dark:border-neutral-800 space-y-2">
              <span className="text-neutral-400 block">Official Contact</span>
              {person.officialWebsite && (
                <a
                  href={person.officialWebsite}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-1.5 text-accent dark:text-sky-400 hover:underline"
                >
                  <ExternalLink className="w-3.5 h-3.5" />
                  <span>Official government portal</span>
                </a>
              )}
              {person.phone && (
                <div className="flex items-center gap-1.5 text-neutral-700 dark:text-neutral-300">
                  <Phone className="w-3.5 h-3.5 text-neutral-400" />
                  <a href={`tel:${person.phone.replace(/[^0-9+]/g, '')}`} className="hover:underline">
                    {person.phone}
                  </a>
                </div>
              )}
              {person.email && (
                <div className="flex items-center gap-1.5 text-neutral-700 dark:text-neutral-300">
                  <Mail className="w-3.5 h-3.5 text-neutral-400" />
                  <a href={`mailto:${person.email}`} className="hover:underline truncate">
                    {person.email}
                  </a>
                </div>
              )}
            </div>

            <div className="pt-2 border-t border-neutral-200 dark:border-neutral-800 flex items-center justify-between text-[11px] text-neutral-400">
              <span>Last verified:</span>
              <span className="font-mono">{person.lastVerified}</span>
            </div>
          </div>

          {/* Related Officials in same Jurisdiction */}
          {related.length > 0 && (
            <div className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/30 text-xs">
              <h3 className="font-serif text-sm font-semibold text-neutral-900 dark:text-white mb-3">
                Related in {person.jurisdictionState}
              </h3>
              <div className="space-y-2.5">
                {related.map((rel) => (
                  <Link
                    key={rel.id}
                    href={`/people/${rel.slug}`}
                    className="block group hover:bg-neutral-50 dark:hover:bg-neutral-800/40 p-1.5 rounded transition-colors"
                  >
                    <div className="font-medium text-neutral-900 dark:text-white group-hover:underline flex items-center justify-between">
                      <span>{rel.fullName}</span>
                      <ChevronRight className="w-3 h-3 text-neutral-400" />
                    </div>
                    <div className="text-[11px] text-neutral-500 truncate">
                      {rel.officeName}
                    </div>
                  </Link>
                ))}
              </div>
            </div>
          )}
        </aside>
      </div>
    </article>
  );
}
