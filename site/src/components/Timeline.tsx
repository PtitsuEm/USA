import { PositionTimeline } from '@/types';

export default function Timeline({ items }: { items: PositionTimeline[] }) {
  if (!items || items.length === 0) return null;

  return (
    <div className="relative pl-6 space-y-6 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-neutral-200 dark:before:bg-neutral-800">
      {items.map((item, idx) => (
        <div key={idx} className="relative">
          <div className="absolute -left-6 top-1.5 w-2.5 h-2.5 rounded-full border-2 border-white dark:border-neutral-900 bg-accent dark:bg-sky-500" />
          <div className="text-sm font-medium text-neutral-900 dark:text-white">
            {item.officeName}
          </div>
          <div className="text-xs text-neutral-500 dark:text-neutral-400 mt-0.5">
            {item.startDate} — {item.endDate || 'Present'} · {item.appointedOrElected}
          </div>
          {item.notes && (
            <div className="text-xs text-neutral-600 dark:text-neutral-300 mt-1">
              {item.notes}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
