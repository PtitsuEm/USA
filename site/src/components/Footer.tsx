import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="mt-20 border-t border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-950 py-10 text-xs text-neutral-500 dark:text-neutral-400">
      <div className="max-w-content mx-auto px-4 sm:px-6">
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-8 mb-8">
          <div>
            <h4 className="font-serif font-semibold text-neutral-900 dark:text-neutral-200 mb-3">Database</h4>
            <ul className="space-y-2">
              <li><Link href="/people" className="hover:underline">Directory</Link></li>
              <li><Link href="/offices" className="hover:underline">Offices</Link></li>
              <li><Link href="/states/al" className="hover:underline">States & Territories</Link></li>
              <li><Link href="/compare" className="hover:underline">Compare Officials</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="font-serif font-semibold text-neutral-900 dark:text-neutral-200 mb-3">Standards</h4>
            <ul className="space-y-2">
              <li><Link href="/methodology" className="hover:underline">Methodology & Sources</Link></li>
              <li><Link href="/contribute" className="hover:underline">Suggest a Correction</Link></li>
              <li><Link href="/changelog" className="hover:underline">Revision Changelog</Link></li>
            </ul>
          </div>
          <div>
            <h4 className="font-serif font-semibold text-neutral-900 dark:text-neutral-200 mb-3">Open Data</h4>
            <ul className="space-y-2">
              <li><Link href="/data" className="hover:underline">CSV / JSON Downloads</Link></li>
              <li><Link href="/about" className="hover:underline">About Project</Link></li>
              <li><span className="text-neutral-400">Public Domain / ODbL</span></li>
            </ul>
          </div>
          <div>
            <h4 className="font-serif font-semibold text-neutral-900 dark:text-neutral-200 mb-3">Traceability</h4>
            <p className="text-neutral-500 leading-relaxed">
              Every fact is anchored to primary government records (.gov portals, FEC, Congress.gov). No synthetic profiles or inferred mailboxes.
            </p>
            <div className="mt-3 font-mono text-[11px] text-neutral-400">
              Snapshot: 2026-10-15
            </div>
          </div>
        </div>

        <div className="pt-6 border-t border-neutral-200 dark:border-neutral-800/80 flex flex-col sm:flex-row items-center justify-between gap-3 text-[11px]">
          <div>
            © 2026 U.S. Public Officials Reference Database. Built for transparency, speed, and trusted public research.
          </div>
          <div className="flex items-center gap-4">
            <Link href="/methodology" className="hover:underline">Source Hierarchy</Link>
            <Link href="/contribute" className="hover:underline">Report Inaccuracy</Link>
          </div>
        </div>
      </div>
    </footer>
  );
}
