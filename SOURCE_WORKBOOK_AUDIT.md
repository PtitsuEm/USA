# Source workbook audit

Input: `US_Government_and_Economic_Leadership.xlsx` (provided in the project folder)

Initial audit: 2026-10-15. The source file is preserved unchanged. One row from it was independently checked against a current official source and added to `data/contacts.csv`. A later, clearly marked municipal candidate batch was imported without claiming current employment; see the addendum below. The workbook still has unresolved identity, freshness, and provenance problems.

## Structure

- 2,287 data rows, 62 distinct values in `State_Territory` (the column also includes federal and city names, so it is not a clean state list).
- 1,916 rows are labelled Municipal; 306 State/Territory; 12 Federal; and 53 Specialized Cluster.
- 2,149 LinkedIn cells (94%) are LinkedIn search-result URLs, not a person's profile. Only 137 rows contain a `/in/` profile URL.
- 1,553 rows have no phone number.
- The workbook labels 1,422 emails “Verified MX” and 53 “Verified (A-Record)”. Those labels establish, at most, domain mail/DNS configuration; they do not confirm a person's mailbox or identity.
- There are 230 repeated email values and 61 repeated names. Repetition may sometimes be shared office contacts, but needs deduplication before merging.

## Delaware spot check

The file lists Kurt Foreman as Delaware Prosperity Partnership President & CEO, but the DPP announced Monique Claiborne as the incoming President & CEO effective September 14, 2026, and its current team page lists her contact details. The workbook also labels a Noah Olson row as an `fdi@delaware.gov` contact, while DPP's team page publishes his current title and `@choosedelaware.com` address. These discrepancies show that MX status cannot be used as proof that the person's details are current or correct.

The app therefore uses records from the workbook only after a separate official-source check. Where this pilot has not confirmed a detail, the field remains blank or the record remains `needs_review`.

## Verified transfer

- The workbook listed Kelly Cummins as Principal Deputy Director / Acting Director, OCED. A later current DOE leadership check superseded that old transfer: DOE now lists **Scott Milliren — Director, OCED** and **Melissa Klembara — Deputy Director, OCED**. The database has been corrected to those current officeholders using their official DOE biographies. No personal email, phone, or LinkedIn was found on those biographies, so these fields remain blank.
- The workbook has 105 exact name/jurisdiction overlaps with records already in the main database. Those rows were not recopied: several supplied emails conflict with official records (for example, generic Secretary of State addresses placed on lieutenant-governor rows), and most LinkedIn URLs are search pages.

DOE sources: [Scott Milliren official biography](https://www.energy.gov/cmei/oced/person/scott-milliren), [Melissa Klembara official biography](https://www.energy.gov/cmei/oced/person/melissa-klembara), and [current OCED leadership](https://www.energy.gov/cmei/oced/office-clean-energy-demonstrations).

## Municipal candidate import addendum — 2026-10-15

To expand the review queue, 996 municipal candidates were imported from workbook rows whose branch/title matched the project's target roles and whose row contained a name, municipality, state, and an HTTP(S) official-site URL. All are `needs_review`. The import copied only the workbook name, listed title, jurisdiction, and URL. Email, phone, LinkedIn, and agency were left blank. The `checked_on` value is the import date, not proof that the person or role was checked against the linked site.

Counts: 800 `MAYOR`, 71 `MAYOR_DEPUTY`, 119 `EDA_HEAD`, and 6 `FOREIGN_INVESTMENT_HEAD`. The workbook's 116 composite `City Manager / Deputy Mayor` entries were excluded because that title does not establish that a city manager is also deputy mayor. The importer also skipped 42 duplicates/existing records and 28 incomplete or malformed candidates. No reporting relationships were inferred.

These are candidate leads, not verified people-in-office. The official-site URLs came from the workbook and have not yet been individually checked or shown to support the named person/title. Known workbook freshness and identity problems still apply. The records must remain `needs_review` until direct, current sources confirm them. Rebuild the offline app and workbook with `python3 scripts/build.py` after later source-backed corrections.

## Safe use

Use this workbook as a candidate-lead file. Before merging a row, confirm the person's current title and contact on a source that directly supports those fields; replace LinkedIn search URLs with a matching public profile; and record the verification date. Do not treat MX/A-record labels as inbox verification.
