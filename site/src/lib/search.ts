import MiniSearch from 'minisearch';
import { Person } from '@/types';

export function createSearchIndex(people: Person[]) {
  const miniSearch = new MiniSearch({
    fields: ['fullName', 'officeName', 'jurisdictionState', 'party', 'bio'],
    storeFields: ['id', 'slug', 'fullName', 'officeName', 'jurisdictionLevel', 'jurisdictionState', 'party', 'verificationLevel'],
    searchOptions: {
      boost: { fullName: 3, officeName: 2, jurisdictionState: 1 },
      fuzzy: 0.2,
      prefix: true,
    },
  });

  miniSearch.addAll(people);
  return miniSearch;
}
