import Breadcrumbs from '@/components/Breadcrumbs';
import { Download, FileSpreadsheet, Code2 } from 'lucide-react';
import { getStats } from '@/lib/data';

export default async function DataExportPage() {
  const stats = await getStats();

  return (
    <div className="max-w-2xl space-y-6 text-xs text-neutral-700 dark:text-neutral-300">
      <Breadcrumbs items={[{ label: 'Data Export' }]} />

      <h1 className="font-serif text-3xl font-bold text-neutral-900 dark:text-white">
        Open Data & Downloads
      </h1>
      <p className="text-sm text-neutral-600 dark:text-neutral-400">
        Download complete public records of U.S. government officials for research, analysis, and civic applications.
      </p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
        <div className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40 space-y-3">
          <div className="flex items-center gap-2 font-semibold text-neutral-900 dark:text-white text-sm">
            <FileSpreadsheet className="w-4 h-4 text-emerald-600" />
            <span>CSV Dataset</span>
          </div>
          <p className="text-neutral-500 leading-relaxed">
            Standard UTF-8 comma-separated file containing all {stats.total.toLocaleString()} public officials, roles, verified URLs, and contact endpoints.
          </p>
          <a
            href="/data/contacts.csv"
            download
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded border border-neutral-300 dark:border-neutral-700 font-medium hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-900 dark:text-white"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download contacts.csv</span>
          </a>
        </div>

        <div className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40 space-y-3">
          <div className="flex items-center gap-2 font-semibold text-neutral-900 dark:text-white text-sm">
            <Code2 className="w-4 h-4 text-sky-600" />
            <span>JSON Structured Feed</span>
          </div>
          <p className="text-neutral-500 leading-relaxed">
            Typed JSON array with nested career timelines, source citations, verification tiers, and election records.
          </p>
          <a
            href="/data/officials.json"
            download
            className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded border border-neutral-300 dark:border-neutral-700 font-medium hover:bg-neutral-100 dark:hover:bg-neutral-800 text-neutral-900 dark:text-white"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download officials.json</span>
          </a>
        </div>
      </div>
    </div>
  );
}
