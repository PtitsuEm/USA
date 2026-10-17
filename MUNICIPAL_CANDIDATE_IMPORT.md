# Municipal candidate import

Date: 2026-10-15  
Input: `US_Government_and_Economic_Leadership.xlsx` (preserved unchanged)  
Importer: `scripts/import_municipal_leads.py`

## Imported batch

| Role | Added candidates |
|---|---:|
| `MAYOR` | 800 |
| `MAYOR_DEPUTY` | 71 |
| `EDA_HEAD` | 119 |
| `FOREIGN_INVESTMENT_HEAD` | 6 |
| **Total** | **996** |

The importer matched municipal rows by workbook branch/title, then required a nonempty name, municipality, state/territory, and HTTP(S) official-site URL. It skipped 42 duplicate/existing candidates, 28 incomplete or malformed candidates, and rows outside the targeted roles. It excluded the 116 ambiguous `City Manager / Deputy Mayor` composite titles rather than treating city managers as deputy mayors.

Each added row is `needs_review`. Imported fields are name, title, municipality, state, and workbook URL. Email, phone, LinkedIn, and agency are blank. No relationships were inferred. `checked_on` records the import date only; it does not mean the person, title, or URL was independently verified during import.

## Limits

The workbook is known to contain stale names and questionable identity/contact mappings. The `source_url` is the URL supplied in the workbook; its relevance to the individual and title has not been checked row by row. Do not treat these 996 rows as verified current officeholders or usable personal contacts. Confirm every row against a current official page before promoting its status or filling contact fields.

## Build

After import, `python3 scripts/build.py` regenerated:

- `data/contacts.xlsx`
- `dist/index.html`

Current totals immediately after this import: 1,276 contacts (223 `verified`, 1,053 `needs_review`), 1,818 coverage rows, and 1,012 jurisdiction rows. The relationship table was unchanged at 111 sourced links.
