'use client';

import { useState } from 'react';
import Breadcrumbs from '@/components/Breadcrumbs';
import { Person } from '@/types';
import peopleData from '@/data/all_people.json';
import VerificationBadge from '@/components/VerificationBadge';
import { ArrowRightLeft } from 'lucide-react';

const allPeople: Person[] = peopleData as Person[];

export default function ComparePage() {
  const [personAId, setPersonAId] = useState(allPeople[0]?.id || '');
  const [personBId, setPersonBId] = useState(allPeople[1]?.id || '');

  const personA = allPeople.find((p) => p.id === personAId);
  const personB = allPeople.find((p) => p.id === personBId);

  return (
    <div className="space-y-6">
      <Breadcrumbs items={[{ label: 'Compare Officials' }]} />

      <div>
        <h1 className="font-serif text-3xl font-bold text-neutral-900 dark:text-white">
          Compare Public Officials
        </h1>
        <p className="text-xs text-neutral-500 mt-1">
          Side-by-side comparison of public offices, tenure, verification level, and official credentials.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-neutral-50 dark:bg-neutral-900/50">
        <div>
          <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1">
            Official A
          </label>
          <select
            value={personAId}
            onChange={(e) => setPersonAId(e.target.value)}
            className="w-full p-2 text-xs rounded border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white focus:outline-none"
          >
            {allPeople.slice(0, 50).map((p) => (
              <option key={p.id} value={p.id}>
                {p.fullName} — {p.officeName} ({p.jurisdictionState || 'Federal'})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-xs font-medium text-neutral-700 dark:text-neutral-300 mb-1">
            Official B
          </label>
          <select
            value={personBId}
            onChange={(e) => setPersonBId(e.target.value)}
            className="w-full p-2 text-xs rounded border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white focus:outline-none"
          >
            {allPeople.slice(0, 50).map((p) => (
              <option key={p.id} value={p.id}>
                {p.fullName} — {p.officeName} ({p.jurisdictionState || 'Federal'})
              </option>
            ))}
          </select>
        </div>
      </div>

      {personA && personB && (
        <div className="grid grid-cols-2 gap-4 text-xs">
          {/* Card A */}
          <div className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40 space-y-3">
            <div>
              <VerificationBadge level={personA.verificationLevel} />
              <h2 className="font-serif text-lg font-bold text-neutral-900 dark:text-white mt-1">
                {personA.fullName}
              </h2>
              <div className="text-neutral-500">{personA.officeName}</div>
            </div>
            <div className="space-y-1.5 pt-2 border-t border-neutral-100 dark:border-neutral-800">
              <div><strong>Party:</strong> {personA.party || 'Nonpartisan'}</div>
              <div><strong>Level:</strong> {personA.jurisdictionLevel}</div>
              <div><strong>State:</strong> {personA.jurisdictionState || 'Federal'}</div>
              <div><strong>Born:</strong> {personA.birthDate || 'Not listed'}</div>
              <div><strong>Verified:</strong> {personA.lastVerified}</div>
            </div>
          </div>

          {/* Card B */}
          <div className="p-4 rounded-lg border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900/40 space-y-3">
            <div>
              <VerificationBadge level={personB.verificationLevel} />
              <h2 className="font-serif text-lg font-bold text-neutral-900 dark:text-white mt-1">
                {personB.fullName}
              </h2>
              <div className="text-neutral-500">{personB.officeName}</div>
            </div>
            <div className="space-y-1.5 pt-2 border-t border-neutral-100 dark:border-neutral-800">
              <div><strong>Party:</strong> {personB.party || 'Nonpartisan'}</div>
              <div><strong>Level:</strong> {personB.jurisdictionLevel}</div>
              <div><strong>State:</strong> {personB.jurisdictionState || 'Federal'}</div>
              <div><strong>Born:</strong> {personB.birthDate || 'Not listed'}</div>
              <div><strong>Verified:</strong> {personB.lastVerified}</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
