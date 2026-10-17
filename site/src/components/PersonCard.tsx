import Link from 'next/link';
import { Person } from '@/types';
import VerificationBadge from './VerificationBadge';
import { Building2, MapPin, Mail, Phone, ExternalLink } from 'lucide-react';

export default function PersonCard({ person }: { person: Person }) {
  return (
    <article className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/50 hover:border-neutral-300 dark:hover:border-neutral-700 hover:shadow-sm transition-all duration-150">
      <div className="flex items-start justify-between gap-3">
        <div>
          <Link
            href={`/people/${person.slug}`}
            className="font-serif text-base font-semibold text-neutral-900 dark:text-neutral-100 hover:text-accent dark:hover:text-sky-400 hover:underline inline-block"
          >
            {person.fullName}
          </Link>
          <div className="text-xs text-neutral-600 dark:text-neutral-400 font-medium mt-0.5 flex items-center gap-1.5 flex-wrap">
            <span>{person.officeName}</span>
            {person.party && (
              <>
                <span className="text-neutral-300 dark:text-neutral-700">·</span>
                <span className="text-neutral-500">{person.party}</span>
              </>
            )}
          </div>
        </div>
        <div className="shrink-0 flex items-center gap-1.5">
          <VerificationBadge level={person.verificationLevel} />
          {person.status === 'former' && (
            <span className="px-1.5 py-0.5 rounded text-[10px] uppercase font-bold tracking-wider bg-neutral-100 dark:bg-neutral-800 text-neutral-500">
              Former
            </span>
          )}
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-neutral-100 dark:border-neutral-800/80 flex items-center justify-between text-xs text-neutral-500 dark:text-neutral-400">
        <div className="flex items-center gap-3 flex-wrap">
          {(person.jurisdictionState || person.jurisdictionDistrict) && (
            <span className="inline-flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-neutral-400 shrink-0" />
              <span>{person.jurisdictionState || person.jurisdictionDistrict}</span>
            </span>
          )}
          <span className="capitalize px-1.5 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-[11px] text-neutral-600 dark:text-neutral-300">
            {person.jurisdictionLevel}
          </span>
        </div>

        <div className="flex items-center gap-2">
          {person.phone && (
            <a
              href={`tel:${person.phone.replace(/[^0-9+]/g, '')}`}
              className="p-1 hover:text-neutral-900 dark:hover:text-white"
              title={`Call ${person.phone}`}
            >
              <Phone className="w-3.5 h-3.5" />
            </a>
          )}
          {person.email && (
            <a
              href={`mailto:${person.email}`}
              className="p-1 hover:text-neutral-900 dark:hover:text-white"
              title={`Email ${person.email}`}
            >
              <Mail className="w-3.5 h-3.5" />
            </a>
          )}
          {person.officialWebsite && (
            <a
              href={person.officialWebsite}
              target="_blank"
              rel="noopener noreferrer"
              className="p-1 hover:text-neutral-900 dark:hover:text-white"
              title="Official portal"
            >
              <ExternalLink className="w-3.5 h-3.5" />
            </a>
          )}
        </div>
      </div>
    </article>
  );
}
