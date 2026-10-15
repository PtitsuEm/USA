# Work log

## 2026-10-15

- Created the local Git repository on branch `main`; no GitHub remote has been configured and nothing has been pushed.
- Added a project spec, source directory, CSV schemas, a zero-dependency builder, and a self-contained offline browser UI.
- The UI supports navigation by jurisdiction and role, text search, status/coverage view, and a person-centered graph driven only by sourced relationship rows.
- Imported 56 state-designated economic/investment contact leads from the official SelectUSA directory: 50 states, 5 territories, and DC. Their records are `needs_review`; names/titles and employment still need confirmation on agency pages. Published emails are included. The source directory provides no LinkedIn URLs, so those cells are blank.
- Added `scripts/import_selectusa.py --refresh-selectusa` for a source refresh. It leaves imported leads at `needs_review`; it does not validate current employment or infer LinkedIn URLs.
- Fixed the SelectUSA refresh parser: it now keeps the published person's name, title, agency, and email in their respective CSV columns instead of joining the directory text into the name field. Refreshed all 56 rows and rebuilt the app/workbook.
- Added current governor name leads for all 50 states and 5 territories from the NGA roster. Emails and LinkedIn remain blank pending individual official-source checks; all 55 records are `needs_review`, and the role coverage is marked `in_progress`.
- Added `data/contacts.xlsx`, generated with sheets for contacts, relationships, coverage, and jurisdictions.
- Antigravity CLI connected, read `AGENTS.md`, `PROJECT_SPEC.md`, and `WORKLOG.md`, and conducted official channel checks for all 55 governors (50 states and 5 territories). Verified names and contact routes against official state/territory portals and directories (including USA.gov directory links). Updated `data/contacts.csv` and `data/coverage.csv` with individual official portal URLs, verification date `2026-10-15`, and moved status from `needs_review`/`in_progress` to `verified`. Recorded published official email for Colorado (`Governorpolis@state.co.us`); did not speculate or infer emails/LinkedIn profiles for offices using standard webforms and reception desks. Rebuilt `dist/index.html` and `data/contacts.xlsx`.
- Sourced and verified all 55 Lieutenant Governors / Deputy Governors / designated constitutional successors across all 50 states and 5 territories (Role `GOVERNOR_DEPUTY`). Added individual records to `data/contacts.csv` with official portal URLs, verified status, and published official emails where available (e.g. `ltgov@ltgov.alabama.gov`, `LtGovStratton@illinois.gov`, `deidrehenderson@utah.gov`). For jurisdictions without a standalone Lt. Governor (AZ, ME, NH, OR, WY, PR), verified constitutional successors (Secretary of State or Senate President). Populated `data/relationships.csv` with 55 confirmed `coordinates_with` links linking each second-in-command to their respective Governor, activating the interactive relationship graph in the offline UI. Updated `data/coverage.csv` and rebuilt `dist/index.html` and `data/contacts.xlsx` (total contacts: 172, verified: 115, relationships: 55).

## Remaining work

- Independently verify imported SelectUSA investment contacts against current employer/agency pages and find matching LinkedIn profiles where public and unambiguous.
- Build source-backed batches for mayors and the economic/energy roles.
- Obtain and define a complete municipality list for each state and territory; keep the Census unit definition explicit and account for territorial differences.
- Expand `relationships.csv` for agency reporting lines and municipal coordination.
- Refresh the generated `dist/index.html` and `data/contacts.xlsx` after every data change with `python3 scripts/build.py`.
