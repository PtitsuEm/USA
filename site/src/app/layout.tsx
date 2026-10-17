import type { Metadata } from 'next';
import './globals.css';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import CommandPalette from '@/components/CommandPalette';

export const metadata: Metadata = {
  title: 'U.S. Public Officials Reference Database',
  description: 'A minimalist, fast, traceable directory of federal, state, and local U.S. government officials. Sourced from primary official government records.',
  metadataBase: new URL('https://usofficials.directory'),
  openGraph: {
    title: 'U.S. Public Officials Reference Database',
    description: 'Minimalist, fast, traceable directory of federal, state, and local U.S. officials.',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="min-h-screen flex flex-col bg-background text-foreground">
        <Header />
        <CommandPalette />
        <main className="flex-1 max-w-content w-full mx-auto px-4 sm:px-6 py-8">
          {children}
        </main>
        <Footer />
      </body>
    </html>
  );
}
