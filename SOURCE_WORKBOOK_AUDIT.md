# Source workbook audit

Input: `US_Government_and_Economic_Leadership.xlsx` (provided in the project folder)

Audited: 2026-10-15. The source file is preserved unchanged. Its 2,287 rows have **not** been merged into `data/contacts.csv` or the app because this audit found unresolved identity, freshness, and provenance problems.

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

## Safe use

Use this workbook as a candidate-lead file. Before merging a row, confirm the person's current title and contact on a source that directly supports those fields; replace LinkedIn search URLs with a matching public profile; and record the verification date. Do not treat MX/A-record labels as inbox verification.
