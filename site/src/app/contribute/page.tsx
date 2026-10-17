'use client';

import { useState } from 'react';
import Breadcrumbs from '@/components/Breadcrumbs';
import { Send, CheckCircle2 } from 'lucide-react';

export default function ContributePage() {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    personName: '',
    office: '',
    correctionType: 'outdated_person',
    sourceUrl: '',
    details: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div className="max-w-xl space-y-6">
      <Breadcrumbs items={[{ label: 'Suggest a Correction' }]} />

      <div className="border-b border-neutral-200 dark:border-neutral-800 pb-4">
        <h1 className="font-serif text-2xl font-bold text-neutral-900 dark:text-white">
          Suggest a Correction
        </h1>
        <p className="text-xs text-neutral-500 mt-1">
          Public leadership changes frequently. Help maintain data accuracy by providing a primary government source URL.
        </p>
      </div>

      {submitted ? (
        <div className="p-6 rounded-lg border border-emerald-200 dark:border-emerald-800 bg-emerald-50 dark:bg-emerald-950/20 text-center space-y-2">
          <CheckCircle2 className="w-8 h-8 text-emerald-600 dark:text-emerald-400 mx-auto" />
          <h3 className="font-serif font-semibold text-emerald-900 dark:text-emerald-200">
            Correction Submitted for Review
          </h3>
          <p className="text-xs text-emerald-800 dark:text-emerald-300">
            Thank you. An automated auditor will verify the provided source URL against the primary domain before updating the public dataset.
          </p>
          <button
            onClick={() => setSubmitted(false)}
            className="mt-3 px-3 py-1 text-xs rounded border border-emerald-300 dark:border-emerald-700 hover:bg-emerald-100"
          >
            Submit another correction
          </button>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Official Name
            </label>
            <input
              type="text"
              required
              value={formData.personName}
              onChange={(e) => setFormData({ ...formData, personName: e.target.value })}
              placeholder="e.g. John Smith"
              className="w-full p-2.5 rounded border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white focus:outline-none focus:border-accent"
            />
          </div>

          <div>
            <label className="block font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Office / Jurisdiction
            </label>
            <input
              type="text"
              value={formData.office}
              onChange={(e) => setFormData({ ...formData, office: e.target.value })}
              placeholder="e.g. Mayor of Glendale, AZ"
              className="w-full p-2.5 rounded border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white focus:outline-none focus:border-accent"
            />
          </div>

          <div>
            <label className="block font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Type of Correction
            </label>
            <select
              value={formData.correctionType}
              onChange={(e) => setFormData({ ...formData, correctionType: e.target.value })}
              className="w-full p-2.5 rounded border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white focus:outline-none"
            >
              <option value="outdated_person">Former official / replaced by newly elected</option>
              <option value="title_correction">Title or agency name correction</option>
              <option value="contact_update">Published phone / email update</option>
              <option value="spelling">Name spelling correction</option>
            </select>
          </div>

          <div>
            <label className="block font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Primary Source URL <span className="text-rose-500">* (Required)</span>
            </label>
            <input
              type="url"
              required
              value={formData.sourceUrl}
              onChange={(e) => setFormData({ ...formData, sourceUrl: e.target.value })}
              placeholder="https://www.cityname.gov/mayor or official announcement"
              className="w-full p-2.5 rounded border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white focus:outline-none focus:border-accent"
            />
            <span className="text-[11px] text-neutral-500 mt-1 block">
              Must be an official government portal (.gov), official city website, or certified election return.
            </span>
          </div>

          <div>
            <label className="block font-medium text-neutral-700 dark:text-neutral-300 mb-1">
              Explanation & Context
            </label>
            <textarea
              rows={3}
              value={formData.details}
              onChange={(e) => setFormData({ ...formData, details: e.target.value })}
              placeholder="Describe the discrepancy and when the transition occurred..."
              className="w-full p-2.5 rounded border border-neutral-300 dark:border-neutral-700 bg-white dark:bg-neutral-900 text-neutral-900 dark:text-white focus:outline-none focus:border-accent"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2.5 px-4 rounded bg-accent dark:bg-sky-600 text-white font-medium hover:bg-accent-light dark:hover:bg-sky-500 flex items-center justify-center gap-2 transition-colors"
          >
            <Send className="w-3.5 h-3.5" />
            <span>Submit for Verification</span>
          </button>
        </form>
      )}
    </div>
  );
}
