# Source directory

Use official sources first and store the page used for each individual row in `source_url`.

| Source | Best use | Limits |
|---|---|---|
| [USAGov — elected officials](https://www.usa.gov/elected-officials) | Starting point for federal, state, territorial, mayoral, and local elected officials | A starting directory, not a complete contact export for every office |
| [SelectUSA — economic developers](https://www.trade.gov/selectusa-find-economic-developers) | State/territorial contacts for investment and business attraction | The named role differs by jurisdiction; it does not establish a matching role in every municipality |
| [National Governors Association — current Governors](https://www.nga.org/Governors/) | Current governor names across the 50 states and 5 territories | Names are a roster-level lead; office emails and LinkedIn profiles need individual confirmation |
| [Census Bureau — government organization data](https://data.census.gov/table/GOVSORGTIMESERIES.GS00ORG02) | Defining and counting local government units; building jurisdiction coverage | A government-unit list does not itself identify officeholders |
| Official state, territorial, city, and agency websites | Current officeholders, direct work contacts, and agency-specific reporting lines | Coverage and page structure vary; verify each row against the page |
| [State of Delaware — Incorporated Municipalities](https://delaware.gov/guides/municipalities/) | Defines the Delaware pilot's local-government scope: 57 incorporated municipalities | Names the municipalities, not their current officeholders |
| [Delaware Elections — Statewide Elected Officials](https://elections.delaware.gov/public/forms/pdfs/electedofficialslist.pdf) | Current statewide elected-office names and official office contacts | Does not cover municipal or economic-development roles |
| [Delaware Prosperity Partnership — Team](https://www.choosedelaware.com/state-economic-development-agency/the-team/) | Current economic-development team, titles, direct public email/phone and LinkedIn links | Does not identify every role in the project's list |
| [DNREC — Climate, Coastal and Energy Contacts](https://dnrec.delaware.gov/climate-coastal-energy/contacts/) | State Energy Office leadership and published contact information | A listed energy administrator is not automatically an investment lead; review role fit |
| [Town of Middletown — Mayor and Council](https://www.middletown.delaware.gov/mayor-council) and [contact directory](https://www.middletown.delaware.gov/contact-us) | Current mayor, vice-mayor and office phone numbers | The town does not publish a direct email for these officials on these pages |
| [City of Newark — Council Members](https://www.newarkde.gov/475/Council-Members) and [staff directory](https://newarkde.gov/m/directory) | Current city elected officials and published contact details | Personal email may be published where no government address is provided |
| [City of Wilmington — Mayor's Office](https://www.wilmingtonde.gov/government/office-of-the-mayor/meetingrequest) | Mayor's name and office phone | No direct email listed on this page |

For LinkedIn, use the person's public profile only after confirming identity through an official name/title/organization match. Record the profile URL as a separate public professional profile; do not infer URLs from a naming pattern.

`scripts/import_selectusa.py` imports named state/territory investment contact leads from the current SelectUSA directory. Imported records are marked `needs_review`: the source is official, but the listed title and current employment still need confirmation on the person's agency/employer page. The directory does not supply LinkedIn profile URLs.

The supplied `US_Government_and_Economic_Leadership.xlsx` is retained as source material, not treated as verified contacts. See `SOURCE_WORKBOOK_AUDIT.md` before using its rows.
