import { MetadataRoute } from 'next';
import { getPeople, getStates, getOffices } from '@/lib/data';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://usofficials.directory';
  const people = await getPeople();
  const states = await getStates();
  const offices = await getOffices();

  const staticRoutes = ['', '/people', '/offices', '/methodology', '/contribute', '/about', '/changelog', '/data', '/compare'].map((route) => ({
    url: `${baseUrl}${route}`,
    lastModified: new Date('2026-10-15'),
  }));

  const peopleRoutes = people.slice(0, 100).map((p) => ({
    url: `${baseUrl}/people/${p.slug}`,
    lastModified: new Date(p.lastVerified || '2026-10-15'),
  }));

  const stateRoutes = states.map((s) => ({
    url: `${baseUrl}/states/${s.code.toLowerCase()}`,
    lastModified: new Date('2026-10-15'),
  }));

  const officeRoutes = offices.slice(0, 50).map((o) => ({
    url: `${baseUrl}/offices/${o.slug}`,
    lastModified: new Date('2026-10-15'),
  }));

  return [...staticRoutes, ...peopleRoutes, ...stateRoutes, ...officeRoutes];
}
