import Breadcrumbs from '@/components/Breadcrumbs';

export default function AboutPage() {
  return (
    <div className="max-w-2xl space-y-6 text-xs text-neutral-700 dark:text-neutral-300 leading-relaxed">
      <Breadcrumbs items={[{ label: 'About' }]} />

      <h1 className="font-serif text-3xl font-bold text-neutral-900 dark:text-white">
        About the Project
      </h1>

      <p className="text-sm text-neutral-800 dark:text-neutral-200">
        The U.S. Public Officials Database is an open reference tool documenting executive, legislative, and economic governance leadership across the United States.
      </p>

      <section className="space-y-2">
        <h2 className="font-serif text-base font-semibold text-neutral-900 dark:text-white">Core Principles</h2>
        <p>
          Unlike social graphs or lead-generation scrapers, this directory prioritizes public transparency, source traceability, and strict non-inferencing. We do not generate predictive emails, test email deliverability via spam probes, or use unverified third-party aggregators.
        </p>
      </section>

      <section className="space-y-2">
        <h2 className="font-serif text-base font-semibold text-neutral-900 dark:text-white">Coverage Scope</h2>
        <p>
          Coverage spans all 50 states, 5 territories, the District of Columbia, federal constitutional officers, members of Congress, and municipal executives in incorporated cities and towns.
        </p>
      </section>
    </div>
  );
}
