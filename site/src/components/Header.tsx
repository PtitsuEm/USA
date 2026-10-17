'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import ThemeToggle from './ThemeToggle';
import { Search } from 'lucide-react';

export default function Header() {
  const pathname = usePathname();

  const navLinks = [
    { label: 'Directory', href: '/people' },
    { label: 'Offices', href: '/offices' },
    { label: 'States', href: '/states/al' },
    { label: 'Methodology', href: '/methodology' },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-neutral-200 dark:border-neutral-800 bg-white/95 dark:bg-neutral-950/95 backdrop-blur">
      <div className="max-w-content mx-auto px-4 sm:px-6 h-14 flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Link href="/" className="flex items-center gap-2 group">
            <span className="font-serif font-bold text-lg tracking-tight text-neutral-900 dark:text-white group-hover:text-accent dark:group-hover:text-sky-400 transition-colors">
              U.S. Officials
            </span>
            <span className="hidden sm:inline-block text-[11px] uppercase font-mono px-1.5 py-0.5 rounded bg-neutral-100 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400 font-semibold tracking-wider">
              Directory
            </span>
          </Link>

          <nav className="hidden md:flex items-center gap-5 text-xs font-medium text-neutral-600 dark:text-neutral-400">
            {navLinks.map((link) => {
              const active = pathname.startsWith(link.href);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`hover:text-neutral-900 dark:hover:text-white transition-colors ${
                    active ? 'text-accent dark:text-sky-400 font-semibold' : ''
                  }`}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>
        </div>

        <div className="flex items-center gap-2.5">
          <button
            onClick={() => {
              window.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', metaKey: true }));
            }}
            className="hidden sm:flex items-center gap-2 px-2.5 py-1.5 text-xs text-neutral-500 rounded-md border border-neutral-300 dark:border-neutral-700 bg-neutral-50 dark:bg-neutral-900 hover:border-neutral-400 dark:hover:border-neutral-600 transition-all"
            title="Global search (Ctrl+K)"
          >
            <Search className="w-3.5 h-3.5" />
            <span>Search...</span>
            <kbd className="font-mono text-[10px] px-1 py-0.5 rounded bg-neutral-200 dark:bg-neutral-800 text-neutral-600 dark:text-neutral-400">
              ⌘K
            </kbd>
          </button>

          <ThemeToggle />
        </div>
      </div>
    </header>
  );
}
