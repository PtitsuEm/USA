import { notFound } from 'next/navigation';
import Link from 'next/link';
import Breadcrumbs from '@/components/Breadcrumbs';
import StateOfficesView from '@/components/StateOfficesView';
import { getStateByCode, getStates } from '@/lib/data';

interface Props {
  params: { code: string };
}

export async function generateStaticParams() {
  const states = await getStates();
  return states.map((s) => ({ code: s.code.toLowerCase() }));
}

export default async function StatePage({ params }: Props) {
  const result = await getStateByCode(params.code);
  if (!result) notFound();

  const { state, officials } = result;
  const allStates = await getStates();

  return (
    <div className="space-y-8">
      <Breadcrumbs
        items={[
          { label: 'States', href: '/states/al' },
          { label: state.name },
        ]}
      />

      <div className="border-b border-neutral-200 dark:border-neutral-800 pb-6">
        <div className="flex items-center gap-2 mb-1.5">
          <span className="font-mono text-xs px-2 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400 font-semibold">
            {state.code}
          </span>
          <span className="text-xs text-neutral-500 capitalize">{state.type}</span>
        </div>
        <h1 className="font-serif text-3xl font-bold text-neutral-900 dark:text-white">
          {state.name} Public Offices & Leadership
        </h1>
        <p className="text-xs text-neutral-500 mt-1">
          {officials.length} verified public offices across state executive leadership, congressional delegation, state legislature, and municipal governance. Select any office to reveal its current holder.
        </p>

        {/* State Quick Switcher Strip */}
        <div className="mt-4 pt-4 border-t border-neutral-100 dark:border-neutral-800/80 flex items-center gap-1.5 overflow-x-auto pb-1 text-xs font-mono">
          {allStates.map((st) => (
            <Link
              key={st.code}
              href={`/states/${st.code.toLowerCase()}`}
              className={`px-2 py-1 rounded transition-colors whitespace-nowrap ${
                st.code === state.code
                  ? 'bg-accent dark:bg-sky-500 text-white font-bold'
                  : 'bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-white'
              }`}
            >
              {st.code}
            </Link>
          ))}
        </div>
      </div>

      {/* Positions / Offices Explorer with on-demand official card reveal */}
      <StateOfficesView state={state} officials={officials} />
    </div>
  );
}
