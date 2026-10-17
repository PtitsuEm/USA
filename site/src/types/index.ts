export type VerificationLevel = 'verified' | 'corroborated' | 'unverified' | 'disputed';
export type GovernmentBranch = 'executive' | 'legislative' | 'judicial';
export type GovernmentLevel = 'federal' | 'state' | 'local';
export type OfficialStatus = 'current' | 'former';

export interface Person {
  id: string;
  slug: string;
  fullName: string;
  aliases?: string[];
  birthDate?: string;
  birthPlace?: string;
  party?: string;
  education?: string[];
  photoUrl?: string;
  photoCredit?: string;
  officialWebsite?: string;
  email?: string;
  phone?: string;
  socials?: { platform: string; url: string; handle: string }[];
  status: OfficialStatus;
  bio?: string;
  officeId: string;
  officeName: string;
  branch?: GovernmentBranch;
  jurisdictionLevel: GovernmentLevel;
  jurisdictionState?: string;
  jurisdictionDistrict?: string;
  verificationLevel: VerificationLevel;
  lastVerified: string;
  claims?: Claim[];
  sources: Source[];
  timeline: PositionTimeline[];
  elections?: Election[];
  committees?: string[];
}

export interface PositionTimeline {
  officeId: string;
  officeName: string;
  startDate: string;
  endDate?: string;
  appointedOrElected: 'elected' | 'appointed';
  notes?: string;
  sourceIds: string[];
}

export interface Office {
  id: string;
  slug: string;
  name: string;
  branch: GovernmentBranch;
  level: GovernmentLevel;
  jurisdictionState?: string;
  jurisdictionDistrict?: string;
  currentHolderId?: string;
  currentHolderName?: string;
  predecessor?: string;
  successor?: string;
  description?: string;
  holdersTimeline: {
    personId: string;
    personName: string;
    personSlug: string;
    startDate: string;
    endDate?: string;
    party?: string;
  }[];
}

export interface Election {
  personId: string;
  year: number;
  officeName: string;
  result: 'won' | 'lost';
  votePct?: number;
  opponent?: string;
  sourceId: string;
}

export interface Source {
  id: string;
  title: string;
  publisher: string;
  url: string;
  archiveUrl?: string;
  type: 'primary' | 'secondary' | 'tertiary';
  accessedAt: string;
}

export interface Claim {
  personId: string;
  field: string;
  value: string;
  sourceIds: string[];
  verificationLevel: VerificationLevel;
  verifiedAt: string;
  verifiedBy: string;
}

export interface Revision {
  entityId: string;
  field: string;
  oldValue: string;
  newValue: string;
  date: string;
  reason: string;
}

export interface StateInfo {
  code: string;
  name: string;
  type: 'state' | 'territory' | 'federal_district';
  capital?: string;
  officialsCount: number;
}
