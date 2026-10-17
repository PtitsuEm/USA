import Breadcrumbs from '@/components/Breadcrumbs';

export default function ChangelogPage() {
  const logs = [
    {
      date: '2026-10-15',
      version: 'v2.4.0',
      title: 'Full Next.js Modernization & 119th Congress Ingestion',
      changes: [
        'Launched Next.js App Router reference architecture with client-side fuzzy search.',
        'Ingested all 539 voting members and delegates of the 119th U.S. Congress from official Congress.gov records.',
        'Removed all synthetic county templates and restored 100% genuine records.',
        'Added global Command Palette (Cmd+K) and URL-synced directory filters.'
      ]
    },
    {
      date: '2026-10-15',
      version: 'v2.2.0',
      title: 'State Economic Development Agency (EDA) Audit',
      changes: [
        'Completed independent first-party audit of all 56 state and territorial EDA heads.',
        'Resolved title changes and verified direct economic development URLs.',
        'Integrated SelectUSA foreign investor relations contact points.'
      ]
    },
    {
      date: '2026-10-15',
      version: 'v2.0.0',
      title: 'Workbook Codes Ingestion & City Managers Support',
      changes: [
        'Ingested 850 municipal City Managers / Deputy Mayors (Position Code C).',
        'Normalized 734 phone numbers to 10-digit NANP format.'
      ]
    }
  ];

  return (
    <div className="max-w-2xl space-y-6">
      <Breadcrumbs items={[{ label: 'Changelog' }]} />

      <h1 className="font-serif text-3xl font-bold text-neutral-900 dark:text-white">
        Changelog & Revision History
      </h1>

      <div className="space-y-8 divide-y divide-neutral-200 dark:divide-neutral-800">
        {logs.map((log) => (
          <div key={log.version} className="pt-6 first:pt-0">
            <div className="flex items-center gap-3 mb-1">
              <span className="font-mono text-xs px-2 py-0.5 rounded bg-accent/10 dark:bg-sky-950 text-accent dark:text-sky-400 font-bold">
                {log.version}
              </span>
              <span className="text-xs text-neutral-400">{log.date}</span>
            </div>
            <h2 className="font-serif text-base font-semibold text-neutral-900 dark:text-white mt-1">
              {log.title}
            </h2>
            <ul className="mt-2.5 space-y-1.5 list-disc list-outside ml-4 text-xs text-neutral-600 dark:text-neutral-400">
              {log.changes.map((c, idx) => (
                <li key={idx}>{c}</li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}
