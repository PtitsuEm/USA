import { VerificationLevel } from '@/types';
import { CheckCircle2, ShieldCheck, AlertCircle, AlertTriangle } from 'lucide-react';

interface Props {
  level: VerificationLevel;
  className?: string;
  showText?: boolean;
}

export default function VerificationBadge({ level, className = '', showText = true }: Props) {
  switch (level) {
    case 'verified':
      return (
        <span
          title="Verified: Confirmed by an official primary .gov portal or official legislative/court record."
          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-800/60 ${className}`}
        >
          <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
          {showText && <span>Verified</span>}
        </span>
      );
    case 'corroborated':
      return (
        <span
          title="Corroborated: Confirmed by 2+ reliable independent secondary sources."
          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-sky-50 dark:bg-sky-950/40 text-sky-700 dark:text-sky-400 border border-sky-200 dark:border-sky-800/60 ${className}`}
        >
          <ShieldCheck className="w-3.5 h-3.5 shrink-0" />
          {showText && <span>Corroborated</span>}
        </span>
      );
    case 'unverified':
      return (
        <span
          title="Unverified: Preliminary or single-source reference pending direct official audit."
          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-amber-50 dark:bg-amber-950/40 text-amber-700 dark:text-amber-400 border border-amber-200 dark:border-amber-800/60 ${className}`}
        >
          <AlertCircle className="w-3.5 h-3.5 shrink-0" />
          {showText && <span>Unverified</span>}
        </span>
      );
    case 'disputed':
      return (
        <span
          title="Disputed: Conflicting reports or officeholder transitions in progress."
          className={`inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium bg-rose-50 dark:bg-rose-950/40 text-rose-700 dark:text-rose-400 border border-rose-200 dark:border-rose-800/60 ${className}`}
        >
          <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
          {showText && <span>Disputed</span>}
        </span>
      );
  }
}
