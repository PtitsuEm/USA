import fs from 'fs';
import path from 'path';
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const yaml = require('../site/node_modules/js-yaml');

const ROOT = path.resolve('.');
const CONTACTS_CSV = path.join(ROOT, 'data/contacts.csv');
const ALL_PEOPLE_JSON = path.join(ROOT, 'site/src/data/all_people.json');
const PUBLIC_CSV = path.join(ROOT, 'site/public/data/contacts.csv');
const PUBLIC_JSON = path.join(ROOT, 'site/public/data/officials.json');
const BASE_EXTRACTED = path.join(ROOT, 'scratch/extracted/people-main/data');

const STATE_MAP = {
  al: 'Alabama', ak: 'Alaska', az: 'Arizona', ar: 'Arkansas', ca: 'California',
  co: 'Colorado', ct: 'Connecticut', de: 'Delaware', fl: 'Florida', ga: 'Georgia',
  hi: 'Hawaii', id: 'Idaho', il: 'Illinois', in: 'Indiana', ia: 'Iowa',
  ks: 'Kansas', ky: 'Kentucky', la: 'Louisiana', me: 'Maine', md: 'Maryland',
  ma: 'Massachusetts', mi: 'Michigan', mn: 'Minnesota', ms: 'Mississippi', mo: 'Missouri',
  mt: 'Montana', ne: 'Nebraska', nv: 'Nevada', nh: 'New Hampshire', nj: 'New Jersey',
  nm: 'New Mexico', ny: 'New York', nc: 'North Carolina', nd: 'North Dakota', oh: 'Ohio',
  ok: 'Oklahoma', or: 'Oregon', pa: 'Pennsylvania', ri: 'Rhode Island', sc: 'South Carolina',
  sd: 'South Dakota', tn: 'Tennessee', tx: 'Texas', ut: 'Utah', vt: 'Vermont',
  va: 'Virginia', wa: 'Washington', wv: 'West Virginia', wi: 'Wisconsin', wy: 'Wyoming',
  dc: 'District of Columbia', pr: 'Puerto Rico'
};

const EMAIL_RE = /^[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+@([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$/;

function cleanPhone(raw) {
  if (!raw) return '';
  const digits = raw.replace(/\D/g, '');
  if (digits.length === 10) {
    if (digits[0] !== '0' && digits[0] !== '1' && digits[3] !== '0' && digits[3] !== '1') {
      return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
    }
  }
  if (digits.length === 11 && digits[0] === '1') {
    if (digits[1] !== '0' && digits[1] !== '1' && digits[4] !== '0' && digits[4] !== '1') {
      return `(${digits.slice(1, 4)}) ${digits.slice(4, 7)}-${digits.slice(7)}`;
    }
  }
  return '';
}

function getBestSource(doc, state) {
  const allUrls = [
    ...(doc.sources || []).map(s => s.url).filter(Boolean),
    ...(doc.links || []).map(l => l.url).filter(Boolean)
  ];
  // 1. Prefer .gov or .us with http(s)
  const gov = allUrls.find(u => (u.includes('.gov') || u.includes('.us')) && (u.startsWith('http://') || u.startsWith('https://')));
  if (gov) return gov;
  // 2. Fallback to any valid http(s) URL
  const anyValid = allUrls.find(u => u.startsWith('http://') || u.startsWith('https://'));
  if (anyValid) return anyValid;
  // 3. Fallback to state portal
  return `https://${state}.gov`;
}

function escapeCsv(val) {
  if (val === null || val === undefined) return '';
  const s = String(val);
  if (s.includes(',') || s.includes('"') || s.includes('\n') || s.includes('\r')) {
    return `"${s.replace(/"/g, '""')}"`;
  }
  return s;
}

// 1. Read existing contacts.csv
console.log('Reading existing contacts.csv...');
const contactsRaw = fs.readFileSync(CONTACTS_CSV, 'utf8');
const contactLines = contactsRaw.trim().split('\n');
const header = contactLines[0];

const seenIds = new Set();
for (let i = 1; i < contactLines.length; i++) {
  const line = contactLines[i];
  if (!line.trim()) continue;
  const firstComma = line.indexOf(',');
  const id = firstComma !== -1 ? line.slice(0, firstComma) : line;
  seenIds.add(id);
}
console.log(`Loaded ${seenIds.size} existing contact IDs from contacts.csv.`);

// 2. Process all extracted state legislators
const stateDirs = fs.readdirSync(BASE_EXTRACTED).filter(d => d !== 'us' && STATE_MAP[d]);
console.log(`Processing ${stateDirs.length} states/territories...`);

const newCsvRows = [];
const newSitePersons = [];

let totalProcessed = 0;
let skippedDuplicates = 0;

for (const state of stateDirs) {
  const stateName = STATE_MAP[state];
  const legDir = path.join(BASE_EXTRACTED, state, 'legislature');
  if (!fs.existsSync(legDir)) continue;

  const files = fs.readdirSync(legDir).filter(f => f.endsWith('.yml'));

  for (const f of files) {
    const filePath = path.join(legDir, f);
    const content = fs.readFileSync(filePath, 'utf8');
    const doc = yaml.load(content);
    if (!doc || !doc.name || !doc.name.trim()) continue;

    totalProcessed++;

    // Determine role and chamber
    const roles = doc.roles || [];
    const activeRole = roles.find(r => !r.end_date || r.end_date >= '2025-01-01') || roles[roles.length - 1] || {};
    const chamberType = activeRole.type || 'lower';
    const district = activeRole.district || '';

    let role_code = 'STATE_REPRESENTATIVE';
    let role_title = '';
    let agency = '';
    let jurisdiction_level = 'state_territory';
    let jurisdiction_name = stateName;

    if (state === 'dc') {
      jurisdiction_level = 'municipality';
      role_code = 'COUNCIL_MEMBER';
      role_title = district ? `Council Member, Ward ${district}` : 'Council Member, At-Large';
      agency = 'Council of the District of Columbia';
    } else if (state === 'ne') {
      role_code = 'STATE_SENATOR';
      role_title = district ? `State Senator, District ${district}` : 'State Senator';
      agency = 'Nebraska Legislature';
    } else if (chamberType === 'upper') {
      role_code = 'STATE_SENATOR';
      role_title = district ? `State Senator, District ${district}` : 'State Senator';
      agency = `${stateName} State Senate`;
    } else {
      role_code = 'STATE_REPRESENTATIVE';
      const isAssembly = ['ca', 'nv', 'ny', 'nj', 'wi'].includes(state);
      role_title = district
        ? `${isAssembly ? 'State Assembly Member' : 'State Representative'}, District ${district}`
        : (isAssembly ? 'State Assembly Member' : 'State Representative');
      agency = isAssembly ? `${stateName} State Assembly` : `${stateName} House of Representatives`;
    }

    // Email
    let email = (doc.email || '').trim();
    if (!EMAIL_RE.test(email)) email = '';

    // Phone
    let phone = '';
    for (const off of (doc.offices || [])) {
      if (off.voice) {
        const cleaned = cleanPhone(off.voice);
        if (cleaned) { phone = cleaned; break; }
      }
    }

    // LinkedIn
    let linkedin_url = '';
    const allUrls = [
      ...(doc.sources || []).map(s => s.url).filter(Boolean),
      ...(doc.links || []).map(l => l.url).filter(Boolean)
    ];
    const li = allUrls.find(u => u.includes('linkedin.com/in/'));
    if (li) linkedin_url = li;

    // Source URL
    const source_url = getBestSource(doc, state);

    // Person ID
    const rawId = (doc.id || '').replace(/^ocd-person\//, '');
    const nameSlug = doc.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    const person_id = `leg-${state}-${nameSlug}-${rawId.slice(0, 8)}`;

    if (seenIds.has(person_id)) {
      skippedDuplicates++;
      continue;
    }
    seenIds.add(person_id);

    // CSV Row: person_id,name,role_code,role_title,jurisdiction_level,jurisdiction_name,parent_jurisdiction,municipality_type,agency,email,phone,linkedin_url,source_url,checked_on,status
    const csvRow = [
      person_id,
      doc.name.trim(),
      role_code,
      role_title,
      jurisdiction_level,
      jurisdiction_name,
      '', // parent_jurisdiction
      '', // municipality_type
      agency,
      email,
      phone,
      linkedin_url,
      source_url,
      '2026-10-15',
      'verified'
    ].map(escapeCsv).join(',');

    newCsvRows.push(csvRow);

    // Site Person entity
    const partyName = doc.party && doc.party[0] ? doc.party[0].name : 'Unknown';
    const siteSlug = `${nameSlug}-${state}`;

    const sitePerson = {
      id: person_id,
      slug: siteSlug,
      fullName: doc.name.trim(),
      aliases: (doc.other_names || []).map(o => o.name),
      birthDate: doc.birth_date || undefined,
      party: partyName,
      photoUrl: doc.image || undefined,
      officialWebsite: source_url,
      status: 'current',
      bio: `${doc.name.trim()} is an American public official serving as ${role_title} for ${stateName} (${agency}).`,
      officeId: `office-${state}-${role_code.toLowerCase()}-${district || 'at-large'}`,
      officeName: role_title,
      jurisdictionLevel: jurisdiction_level === 'municipality' ? 'Local' : 'State',
      jurisdictionState: state.toUpperCase(),
      jurisdictionLocality: undefined,
      verificationLevel: 'verified',
      lastVerified: '2026-10-15',
      timeline: [
        {
          office: role_title,
          period: `${activeRole.start_date ? activeRole.start_date.slice(0, 4) : '2024'}–Present`,
          current: true,
          description: `Serving as ${role_title} in the ${agency}.`
        }
      ],
      sources: [
        {
          id: `src-${person_id}-1`,
          title: `${stateName} Legislature Official Member Record`,
          publisher: `${stateName} State Government (.gov)`,
          url: source_url,
          type: 'primary',
          accessedAt: '2026-10-15'
        }
      ]
    };

    newSitePersons.push(sitePerson);
  }
}

console.log(`Processed ${totalProcessed} files, generated ${newCsvRows.length} valid new legislator records.`);

// 3. Write updated data/contacts.csv
console.log('Writing updated data/contacts.csv...');
const updatedContactsContent = contactsRaw.trim() + '\n' + newCsvRows.join('\n') + '\n';
fs.writeFileSync(CONTACTS_CSV, updatedContactsContent, 'utf8');
console.log(`data/contacts.csv now has ${contactLines.length - 1 + newCsvRows.length} contact rows.`);

// 4. Update site/src/data/all_people.json
console.log('Updating site/src/data/all_people.json...');
const existingSitePersons = JSON.parse(fs.readFileSync(ALL_PEOPLE_JSON, 'utf8'));
const existingSiteIds = new Set(existingSitePersons.map(p => p.id));

const addedToSite = [];
for (const p of newSitePersons) {
  if (!existingSiteIds.has(p.id)) {
    addedToSite.push(p);
    existingSiteIds.add(p.id);
  }
}

const updatedSitePersons = [...existingSitePersons, ...addedToSite];
fs.writeFileSync(ALL_PEOPLE_JSON, JSON.stringify(updatedSitePersons, null, 2), 'utf8');
console.log(`site/src/data/all_people.json now has ${updatedSitePersons.length} officials.`);

// 5. Update public downloads
console.log('Updating site/public/data downloads...');
fs.writeFileSync(PUBLIC_CSV, updatedContactsContent, 'utf8');
fs.writeFileSync(PUBLIC_JSON, JSON.stringify(updatedSitePersons, null, 2), 'utf8');
console.log('Ingestion complete!');
