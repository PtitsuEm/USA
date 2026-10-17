# U.S. Public Officials Database & Directory

A minimalist, fast, highly navigable web application and public database of U.S. government officials (federal, state, and local). Designed with an editorial, reference-book aesthetic (Wikipedia meets Stripe docs), keyboard-driven navigation, and traceable sources for every record.

---

## Tech Stack

- **Framework**: Next.js 14 (App Router) + TypeScript
- **Styling**: Tailwind CSS (light/dark mode via `next-themes` and `prefers-color-scheme`)
- **Typography**: Editorial serif headings (`Source Serif 4`), clean sans UI (`Inter`), mono tables/dates (`JetBrains Mono`)
- **Search**: Client-side fuzzy search via `MiniSearch` + instant global Command Palette (`Cmd/Ctrl+K`)
- **Data Layer**: Typed local JSON/CSV data abstraction (`site/src/lib/data.ts`), swappable for Postgres/Supabase or SQLite
- **SEO & Metadata**: JSON-LD `Person` / `GovernmentOrganization` Schema.org graphs, OpenGraph tags, dynamic `sitemap.xml`, and `robots.txt`

---

## Getting Started

### 1. Requirements
- Node.js 18+ (tested on Node v26)
- npm or yarn

### 2. Installation
```bash
cd site
npm install
```

### 3. Running Locally
```bash
# Start development server on http://localhost:3000
npm run dev

# Or build and run production server
npm run build
npm run start
```

---

## Information Architecture

- **Home (`/`)**: Large autofocus search bar (`/` shortcut), quick-browse tiles (Executive, Senate, House, Judicial, Governors, Cabinet, Local), 50-state + territory grid, live database stats.
- **Directory (`/people`)**: Filterable table/card directory with sticky sidebar (branch, level, state, party, verification level). URL-synced search params, pagination, and sorting.
- **Official Profile (`/people/[slug]`)**: Quick facts card, career timeline, committee roles, election results, inline source citations `[1]`, verifiable sources block with Wayback links, schema JSON-LD, and side-by-side comparison shortcut.
- **Offices (`/offices` and `/offices/[slug]`)**: Historical office holders timeline and current occupants.
- **States (`/states/[code]`)**: Officials grouped by jurisdiction level (Federal Senate/House, Statewide Executive, Local Municipalities).
- **Verification & Methodology (`/methodology`)**: 4-tier verification standard (Verified, Corroborated, Unverified, Disputed) and primary source hierarchy (.gov, FEC, Congress.gov).
- **Compare (`/compare?a=&b=`)**: Side-by-side credential and tenure comparison between any two officials.
- **Data Export (`/data`)**: Direct downloads of audited CSV (`contacts.csv`) and JSON (`officials.json`).
- **Contribute / Suggest Correction (`/contribute`)**: Evidence-backed correction submission requiring primary source URLs.

---

## How to Add a Person

New officials can be added programmatically or directly to `src/data/all_people.json` adhering to the `Person` interface defined in `src/types/index.ts`:

```typescript
import { Person } from '@/types';

const newOfficial: Person = {
  id: "wb-muni-r0231-mayor-new-york-new-york",
  slug: "eric-adams",
  fullName: "Eric L. Adams",
  aliases: ["Eric Adams"],
  party: "Democratic",
  branch: "Executive",
  level: "Local",
  officeName: "Mayor",
  jurisdictionState: "NY",
  jurisdictionLocality: "New York City",
  status: "current",
  officialWebsite: "https://www.nyc.gov/office-of-the-mayor/",
  bio: "Eric Leroy Adams is an American politician and former police officer serving as the 110th mayor of New York City since 2022.",
  sources: [
    {
      id: "src-nyc-mayor-1",
      title: "Office of the Mayor of New York City",
      publisher: "City of New York (.gov)",
      url: "https://www.nyc.gov/office-of-the-mayor/",
      type: "primary",
      accessedAt: "2026-10-15"
    }
  ],
  claims: [
    {
      personId: "wb-muni-r0231-mayor-new-york-new-york",
      field: "officeName",
      value: "Mayor",
      sourceIds: ["src-nyc-mayor-1"],
      verificationLevel: "verified",
      verifiedAt: "2026-10-15",
      verifiedBy: "Official .gov Registry Audit"
    }
  ]
};
```

---

## How to Import Data from CSV

The repository includes ingestion pipelines to sync contacts from CSV workbooks directly into the Next.js database:

1. Place your updated CSV file in `data/contacts.csv`.
2. Run the unification script:
   ```bash
   node site/scripts/sync-data.mjs
   ```
   *Or build from Python:*
   ```bash
   python3 scripts/validate_contacts.py
   ```
3. The script verifies schema constraints, filters out unverified synthetic emails, updates `site/src/data/all_people.json`, and rebuilds static search indexes.

---

## Data Integrity Standards

1. **Zero Synthetic Emails**: No algorithmic placeholder addresses (`admin@...`, `info@...`) are assigned to officials. Only published, authentic government emails and phone numbers are permitted.
2. **Primary Source Requirement**: Every claim must link to an official `.gov`, `.mil`, or certified statutory domain.
