import Link from 'next/link';
import { ChevronRight } from 'lucide-react';

interface Crumb {
  label: string;
  href?: string;
}

export default function Breadcrumbs({ items }: { items: Crumb[] }) {
  return (
    <nav aria-label="Breadcrumb" className="mb-6 flex items-center space-x-1.5 text-xs text-neutral-500 dark:text-neutral-400">
      <Link href="/" className="hover:text-neutral-900 dark:hover:text-white transition-colors">
        Home
      </Link>
      {items.map((item, idx) => (
        <span key={idx} className="flex items-center space-x-1.5">
          <ChevronRight className="w-3 h-3 text-neutral-400 dark:text-neutral-600" />
          {item.href ? (
            <Link href={item.href} className="hover:text-neutral-900 dark:hover:text-white transition-colors">
              {item.label}
            </Link>
          ) : (
            <span className="font-medium text-neutral-800 dark:text-neutral-200" aria-current="page">
              {item.label}
            </span>
          )}
        </span>
      ))}
    </nav>
  );
}
