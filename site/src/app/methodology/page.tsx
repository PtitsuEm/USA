import Breadcrumbs from '@/components/Breadcrumbs';
import { ShieldCheck, CheckCircle2, AlertCircle, AlertTriangle } from 'lucide-react';

export default function MethodologyPage() {
  return (
    <div className="space-y-8 max-w-2xl">
      <Breadcrumbs items={[{ label: 'Methodology & Sources' }]} />

      <div className="border-b border-neutral-200 dark:border-neutral-800 pb-6">
        <h1 className="font-serif text-3xl font-bold text-neutral-900 dark:text-white">
          Sources Hierarchy & Verification Methodology
        </h1>
        <p className="text-sm text-neutral-600 dark:text-neutral-400 mt-2 leading-relaxed">
          The database operates as a strict factual reference. Every claim, officeholder tenure, and contact method must link directly to an authoritative source.
        </p>
      </div>

      {/* Verification Tiers */}
      <section className="space-y-4">
        <h2 className="font-serif text-xl font-semibold text-neutral-900 dark:text-white">
          Verification Levels
        </h2>

        <div className="space-y-3 text-xs leading-relaxed">
          <div className="p-4 rounded-lg border border-emerald-200 dark:border-emerald-800/60 bg-emerald-50/50 dark:bg-emerald-950/20">
            <div className="flex items-center gap-2 font-semibold text-emerald-800 dark:text-emerald-300 text-sm mb-1">
              <CheckCircle2 className="w-4 h-4" />
              <span>Verified (Primary Source)</span>
            </div>
            <p className="text-emerald-900 dark:text-emerald-200">
              Confirmed by a direct first-party government source: official <code>.gov</code> or <code>.mil</code> websites, Congressional biographical records (Congress.gov), Federal Election Commission filings (FEC), or official state election authority certifications.
            </p>
          </div>

          <div className="p-4 rounded-lg border border-sky-200 dark:border-sky-800/60 bg-sky-50/50 dark:bg-sky-950/20">
            <div className="flex items-center gap-2 font-semibold text-sky-800 dark:text-sky-300 text-sm mb-1">
              <ShieldCheck className="w-4 h-4" />
              <span>Corroborated (2+ Secondary Sources)</span>
            </div>
            <p className="text-sky-900 dark:text-sky-200">
              Confirmed by two or more independent, established secondary sources (e.g. state municipal leagues, Associated Press, university government archives) where a direct .gov portal page is temporarily inaccessible or undergoing redesign.
            </p>
          </div>

          <div className="p-4 rounded-lg border border-amber-200 dark:border-amber-800/60 bg-amber-50/50 dark:bg-amber-950/20">
            <div className="flex items-center gap-2 font-semibold text-amber-800 dark:text-amber-300 text-sm mb-1">
              <AlertCircle className="w-4 h-4" />
              <span>Unverified / Preliminary</span>
            </div>
            <p className="text-amber-900 dark:text-amber-200">
              Listed in a single secondary directory or awaiting manual audit confirmation. Flagged visibly to researchers as preliminary.
            </p>
          </div>

          <div className="p-4 rounded-lg border border-rose-200 dark:border-rose-800/60 bg-rose-50/50 dark:bg-rose-950/20">
            <div className="flex items-center gap-2 font-semibold text-rose-800 dark:text-rose-300 text-sm mb-1">
              <AlertTriangle className="w-4 h-4" />
              <span>Disputed</span>
            </div>
            <p className="text-rose-900 dark:text-rose-200">
              Conflicting official records exist, or an office transition / election challenge is ongoing. Both claims are documented side-by-side with respective source links.
            </p>
          </div>
        </div>
      </section>

      {/* Rules */}
      <section className="space-y-3 text-xs text-neutral-700 dark:text-neutral-300 leading-relaxed">
        <h2 className="font-serif text-xl font-semibold text-neutral-900 dark:text-white">
          Core Editorial Standards
        </h2>
        <ul className="list-disc list-outside ml-4 space-y-2">
          <li><strong>No Inferred Email Addresses:</strong> We never generate pattern emails (e.g. <code>first.last@domain</code>). An email is published only if it appears on an official public agency page.</li>
          <li><strong>No Guessing Phone Deliverability:</strong> Phone numbers are validated against North American Numbering Plan (NANP) syntax, but we do not dial or verify line status.</li>
          <li><strong>No LinkedIn Search URLs:</strong> LinkedIn links are included only when specifically hyperlinked on an official government bio.</li>
          <li><strong>Neutral Tone:</strong> Biographies and descriptions remain strictly factual, nonpartisan, and encyclopedic.</li>
        </ul>
      </section>
    </div>
  );
}
