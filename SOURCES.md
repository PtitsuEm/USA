# Source directory

Use official sources first and store the page used for each individual row in `source_url`.

| Source | Best use | Limits |
|---|---|---|
| [USAGov — elected officials](https://www.usa.gov/elected-officials) | Starting point for federal, state, territorial, mayoral, and local elected officials | A starting directory, not a complete contact export for every office |
| [SelectUSA — economic developers](https://www.trade.gov/selectusa-find-economic-developers) | State/territorial contacts for investment and business attraction | The named role differs by jurisdiction; it does not establish a matching role in every municipality |
| [National Governors Association — current Governors](https://www.nga.org/Governors/) | Current governor names across the 50 states and 5 territories | Names are a roster-level lead; office emails and LinkedIn profiles need individual confirmation |
| [Census Bureau — government organization data](https://data.census.gov/table/GOVSORGTIMESERIES.GS00ORG02) | Defining and counting local government units; building jurisdiction coverage | A government-unit list does not itself identify officeholders |
| Official state, territorial, city, and agency websites | Current officeholders, direct work contacts, and agency-specific reporting lines | Coverage and page structure vary; verify each row against the page |

For LinkedIn, use the person's public profile only after confirming identity through an official name/title/organization match. Record the profile URL as a separate public professional profile; do not infer URLs from a naming pattern.

`scripts/import_selectusa.py` imports named state/territory investment contact leads from the current SelectUSA directory. Imported records are marked `needs_review`: the source is official, but the listed title and current employment still need confirmation on the person's agency/employer page. The directory does not supply LinkedIn profile URLs.
