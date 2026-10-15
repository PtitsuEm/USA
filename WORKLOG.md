# Work log

## 2026-10-15

- Created the local Git repository on branch `main`; no GitHub remote has been configured and nothing has been pushed.
- Added a project spec, source directory, CSV schemas, a zero-dependency builder, and a self-contained offline browser UI.
- The UI supports navigation by jurisdiction and role, text search, status/coverage view, and a person-centered graph driven only by sourced relationship rows.
- Imported 56 state-designated economic/investment contact leads from the official SelectUSA directory: 50 states, 5 territories, and DC. Their records are `needs_review`; names/titles and employment still need confirmation on agency pages. Published emails are included. The source directory provides no LinkedIn URLs, so those cells are blank.
- Added `scripts/import_selectusa.py --refresh-selectusa` for a source refresh. It leaves imported leads at `needs_review`; it does not validate current employment or infer LinkedIn URLs.
- Fixed the SelectUSA refresh parser: it now keeps the published person's name, title, agency, and email in their respective CSV columns instead of joining the directory text into the name field. Refreshed all 56 rows and rebuilt the app/workbook.
- Added `data/contacts.xlsx`, generated with sheets for contacts, relationships, coverage, and jurisdictions.
- Antigravity CLI is installed, but its non-interactive review was denied because it requires a command permission that headless mode cannot prompt for. To involve Antigravity, open this same folder in the Antigravity IDE and ask it to read `AGENTS.md`, `PROJECT_SPEC.md`, and this log. Do not enable permission bypasses.

## Remaining work

- Independently verify imported contacts against current employer/agency pages and find matching LinkedIn profiles where public and unambiguous.
- Build source-backed batches for governors, deputy governors/successors, mayors, and the economic/energy roles.
- Obtain and define a complete municipality list for each state and territory; keep the Census unit definition explicit and account for territorial differences.
- Populate `relationships.csv` only for sourced reporting or coordination links.
- Refresh the generated `dist/index.html` and `data/contacts.xlsx` after every data change with `python3 scripts/build.py`.
