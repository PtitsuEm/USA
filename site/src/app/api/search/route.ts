import { NextResponse } from 'next/server';
import { getPeople } from '@/lib/data';
import { createSearchIndex } from '@/lib/search';

let cachedIndex: any = null;
let allPeopleCache: any = null;

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const q = searchParams.get('q') || '';

  if (!q.trim()) {
    return NextResponse.json([]);
  }

  if (!allPeopleCache) {
    allPeopleCache = await getPeople();
    cachedIndex = createSearchIndex(allPeopleCache);
  }

  const results = cachedIndex.search(q, { prefix: true, fuzzy: 0.2 });
  const ids = new Set(results.slice(0, 15).map((r: any) => r.id));
  const matched = allPeopleCache.filter((p: any) => ids.has(p.id));

  return NextResponse.json(matched);
}
