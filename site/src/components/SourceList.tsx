import { Source } from '@/types';
import { ExternalLink, Archive } from 'lucide-react';

export default function SourceList({ sources }: { sources: Source[] }) {
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-8 pt-6 border-t border-neutral-200 dark:border-neutral-800">
      <h3 className="font-serif text-lg font-semibold text-neutral-900 dark:text-neutral-100 mb-3">
        Sources & Traceability
      </h3>
      <ol className="list-decimal list-outside ml-5 space-y-2 text-xs text-neutral-600 dark:text-neutral-400">
        {sources.map((src, idx) => (
          <li key={src.id || idx} id={`src-${idx + 1}`} className="pl-1 leading-relaxed">
            <span className="font-medium text-neutral-900 dark:text-neutral-200">
              {src.title}
            </span>
            {src.publisher && <span className="text-neutral-500"> — {src.publisher}</span>}
            <div className="inline-flex items-center gap-2 ml-2">
              <a
                href={src.url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-0.5 text-accent dark:text-sky-400 hover:underline"
              >
                <span>Direct portal</span>
                <ExternalLink className="w-3 h-3" />
              </a>
              {src.archiveUrl && (
                <a
                  href={src.archiveUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-0.5 text-neutral-500 hover:text-neutral-700 dark:hover:text-neutral-300"
                  title="Wayback Machine snapshot"
                >
                  <Archive className="w-3 h-3" />
                  <span>Archive</span>
                </a>
              )}
              {src.accessedAt && (
                <span className="text-neutral-400">· Accessed {src.accessedAt}</span>
              )}
            </div>
          </li>
        ))}
      </ol>
    </div>
  );
}
