import { Person, Office, StateInfo } from '@/types';
import peopleData from '@/data/all_people.json';
import seedData from '@/data/seed.json';

const allPeople: Person[] = peopleData as Person[];
const seedOffices: Office[] = seedData.offices as Office[];

export const STATE_MAP: Record<string, { code: string; name: string; type: 'state' | 'territory' | 'federal_district' }> = {
  AL: { code: 'AL', name: 'Alabama', type: 'state' },
  AK: { code: 'AK', name: 'Alaska', type: 'state' },
  AZ: { code: 'AZ', name: 'Arizona', type: 'state' },
  AR: { code: 'AR', name: 'Arkansas', type: 'state' },
  CA: { code: 'CA', name: 'California', type: 'state' },
  CO: { code: 'CO', name: 'Colorado', type: 'state' },
  CT: { code: 'CT', name: 'Connecticut', type: 'state' },
  DE: { code: 'DE', name: 'Delaware', type: 'state' },
  FL: { code: 'FL', name: 'Florida', type: 'state' },
  GA: { code: 'GA', name: 'Georgia', type: 'state' },
  HI: { code: 'HI', name: 'Hawaii', type: 'state' },
  ID: { code: 'ID', name: 'Idaho', type: 'state' },
  IL: { code: 'IL', name: 'Illinois', type: 'state' },
  IN: { code: 'IN', name: 'Indiana', type: 'state' },
  IA: { code: 'IA', name: 'Iowa', type: 'state' },
  KS: { code: 'KS', name: 'Kansas', type: 'state' },
  KY: { code: 'KY', name: 'Kentucky', type: 'state' },
  LA: { code: 'LA', name: 'Louisiana', type: 'state' },
  ME: { code: 'ME', name: 'Maine', type: 'state' },
  MD: { code: 'MD', name: 'Maryland', type: 'state' },
  MA: { code: 'MA', name: 'Massachusetts', type: 'state' },
  MI: { code: 'MI', name: 'Michigan', type: 'state' },
  MN: { code: 'MN', name: 'Minnesota', type: 'state' },
  MS: { code: 'MS', name: 'Mississippi', type: 'state' },
  MO: { code: 'MO', name: 'Missouri', type: 'state' },
  MT: { code: 'MT', name: 'Montana', type: 'state' },
  NE: { code: 'NE', name: 'Nebraska', type: 'state' },
  NV: { code: 'NV', name: 'Nevada', type: 'state' },
  NH: { code: 'NH', name: 'New Hampshire', type: 'state' },
  NJ: { code: 'NJ', name: 'New Jersey', type: 'state' },
  NM: { code: 'NM', name: 'New Mexico', type: 'state' },
  NY: { code: 'NY', name: 'New York', type: 'state' },
  NC: { code: 'NC', name: 'North Carolina', type: 'state' },
  ND: { code: 'ND', name: 'North Dakota', type: 'state' },
  OH: { code: 'OH', name: 'Ohio', type: 'state' },
  OK: { code: 'OK', name: 'Oklahoma', type: 'state' },
  OR: { code: 'OR', name: 'Oregon', type: 'state' },
  PA: { code: 'PA', name: 'Pennsylvania', type: 'state' },
  RI: { code: 'RI', name: 'Rhode Island', type: 'state' },
  SC: { code: 'SC', name: 'South Carolina', type: 'state' },
  SD: { code: 'SD', name: 'South Dakota', type: 'state' },
  TN: { code: 'TN', name: 'Tennessee', type: 'state' },
  TX: { code: 'TX', name: 'Texas', type: 'state' },
  UT: { code: 'UT', name: 'Utah', type: 'state' },
  VT: { code: 'VT', name: 'Vermont', type: 'state' },
  VA: { code: 'VA', name: 'Virginia', type: 'state' },
  WA: { code: 'WA', name: 'Washington', type: 'state' },
  WV: { code: 'WV', name: 'West Virginia', type: 'state' },
  WI: { code: 'WI', name: 'Wisconsin', type: 'state' },
  WY: { code: 'WY', name: 'Wyoming', type: 'state' },
  DC: { code: 'DC', name: 'District of Columbia', type: 'federal_district' },
  PR: { code: 'PR', name: 'Puerto Rico', type: 'territory' },
  GU: { code: 'GU', name: 'Guam', type: 'territory' },
  VI: { code: 'VI', name: 'U.S. Virgin Islands', type: 'territory' },
  AS: { code: 'AS', name: 'American Samoa', type: 'territory' },
  MP: { code: 'MP', name: 'Northern Mariana Islands', type: 'territory' },
};

export async function getPeople(): Promise<Person[]> {
  return allPeople;
}

export async function getPersonBySlug(slug: string): Promise<Person | null> {
  const person = allPeople.find((p) => p.slug === slug);
  return person || null;
}

export async function getOffices(): Promise<Office[]> {
  // Aggregate offices from seed and people positions
  const officeMap = new Map<string, Office>();
  
  for (const o of seedOffices) {
    officeMap.set(o.id, o);
  }

  for (const p of allPeople) {
    if (!officeMap.has(p.officeId)) {
      officeMap.set(p.officeId, {
        id: p.officeId,
        slug: p.officeId.replace(/^office-/, ''),
        name: p.officeName,
        branch: p.jurisdictionLevel === 'federal' ? (p.officeName.includes('Senator') || p.officeName.includes('Representative') ? 'legislative' : 'executive') : 'executive',
        level: p.jurisdictionLevel,
        jurisdictionState: p.jurisdictionState,
        jurisdictionDistrict: p.jurisdictionDistrict,
        currentHolderId: p.id,
        currentHolderName: p.fullName,
        description: `Official public office for ${p.officeName}.`,
        holdersTimeline: [
          {
            personId: p.id,
            personName: p.fullName,
            personSlug: p.slug,
            startDate: p.timeline[0]?.startDate || '2024-01-01',
            party: p.party
          }
        ]
      });
    }
  }

  return Array.from(officeMap.values());
}

export async function getOfficeBySlug(slug: string): Promise<Office | null> {
  const offices = await getOffices();
  return offices.find((o) => o.slug === slug || o.id === `office-${slug}`) || null;
}

export async function getStates(): Promise<StateInfo[]> {
  const counts: Record<string, number> = {};

  for (const p of allPeople) {
    if (p.jurisdictionState) {
      counts[p.jurisdictionState] = (counts[p.jurisdictionState] || 0) + 1;
    }
  }

  return Object.values(STATE_MAP).map((s) => ({
    code: s.code,
    name: s.name,
    type: s.type,
    officialsCount: (counts[s.code] || 0) + (counts[s.name] || 0),
  }));
}

export async function getStateByCode(code: string): Promise<{ state: StateInfo; officials: Person[] } | null> {
  const upper = code.toUpperCase();
  const entry = STATE_MAP[upper] || Object.values(STATE_MAP).find((s) => s.name.toLowerCase() === code.toLowerCase());
  if (!entry) return null;

  const officials = allPeople.filter(
    (p) => p.jurisdictionState === entry.name || p.jurisdictionState === entry.code
  );

  return {
    state: {
      code: entry.code,
      name: entry.name,
      type: entry.type,
      officialsCount: officials.length,
    },
    officials,
  };
}

export async function getStats() {
  const total = allPeople.length;
  const verified = allPeople.filter((p) => p.verificationLevel === 'verified').length;
  const verifiedPct = total > 0 ? Math.round((verified / total) * 100) : 100;
  
  const federal = allPeople.filter((p) => p.jurisdictionLevel === 'federal').length;
  const state = allPeople.filter((p) => p.jurisdictionLevel === 'state').length;
  const local = allPeople.filter((p) => p.jurisdictionLevel === 'local').length;

  const stateLegislatures = allPeople.filter((p) => p.id.startsWith('leg-')).length;
  const congress = allPeople.filter(
    (p) => p.id.startsWith('congress-') || (p.jurisdictionLevel === 'federal' && (p.officeName.includes('Senator') || p.officeName.includes('Representative')))
  ).length;
  const governors = allPeople.filter((p) => p.officeName.includes('Governor')).length;
  const stateLeadership = allPeople.filter(
    (p) => p.jurisdictionLevel === 'state' && !p.id.startsWith('leg-') && !p.officeName.includes('Governor')
  ).length;
  const federalExecutive = allPeople.filter(
    (p) => p.jurisdictionLevel === 'federal' && !p.id.startsWith('congress-') && !p.officeName.includes('Senator') && !p.officeName.includes('Representative') && !p.officeName.includes('Justice')
  ).length;
  const judicial = allPeople.filter((p) => p.officeName.includes('Justice') || p.officeName.includes('Judge')).length;

  const energy = allPeople.filter(
    (p) => p.id.includes('energy') || p.officeName.toLowerCase().includes('energy') || p.officeName.toLowerCase().includes('power')
  ).length;
  const agri = allPeople.filter(
    (p) => p.id.includes('agri') || p.officeName.toLowerCase().includes('agriculture') || p.officeName.toLowerCase().includes('farming')
  ).length;
  const manufacturing = allPeople.filter(
    (p) => p.id.includes('manufacturing') || p.officeName.toLowerCase().includes('mep') || p.officeName.toLowerCase().includes('manufacturing')
  ).length;
  const ev = allPeople.filter(
    (p) => p.id.includes('ev-') || p.id.includes('sec-ev') || p.officeName.toLowerCase().includes('electric vehicle') || p.officeName.toLowerCase().includes('nevi') || p.officeName.toLowerCase().includes('mobility')
  ).length;
  const datacenter = allPeople.filter(
    (p) => p.id.includes('data-center') || p.officeName.toLowerCase().includes('information technology') || p.officeName.toLowerCase().includes('cio') || p.officeName.toLowerCase().includes('cto') || p.officeName.toLowerCase().includes('data center')
  ).length;

  return {
    total,
    verified,
    verifiedPct,
    federal,
    state,
    local,
    stateLegislatures,
    congress,
    governors,
    stateLeadership,
    federalExecutive,
    judicial,
    datacenter,
    energy,
    agri,
    manufacturing,
    ev,
    lastUpdated: '2026-10-15',
  };
}
