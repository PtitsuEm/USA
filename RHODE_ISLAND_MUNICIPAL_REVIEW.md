# Rhode Island municipal mayor verification — 2026-10-15

Reviewed the five imported mayor candidates for Warwick, Pawtucket, East Providence, Woonsocket, and Cranston against official city sources. Current mayor identity and role were confirmed for all five. Four workbook names were incorrect or malformed; the Cranston name was abbreviated. Record IDs were retained and records corrected in `data/contacts.csv`; matching coverage rows were updated in `data/coverage.csv`.

| Municipality | Current mayor | Published contact data added | Official source | Finding about imported value |
|---|---|---|---|---|
| Warwick | Frank J. Picozzi | Mayor’s Office phone: (401) 738-2000; no personal email or LinkedIn added | [City staff directory](https://www.warwickri.gov/m/directory); [government contact](https://www.warwickri.gov/164/Government); [City Council](https://www.warwickri.gov/213/City-Council---Legislative-Department) | William Foley is listed as Councilman Pro Temp, not mayor. |
| Pawtucket | Donald R. Grebien | Mayor’s Office: (401) 728-0500 ext. 281; no personal email or LinkedIn added | [Mayor’s Office](https://pawtucketri.gov/mayors-office-2/) | Michael A. Araujo is listed as Councilor At Large, not mayor. |
| East Providence | Roberto L. DaSilva | Mayor’s Office: (401) 435-7521; no personal email or LinkedIn added | [Mayor’s Office](https://eastprovidenceri.gov/departments/mayors-office); [2026 city meeting record](https://eastprovidenceri.gov/files-docs/26-10-02/city-council-regular-meeting-1062026) | “Robert Rodericks: At” was malformed; Robert Rodericks is City Council President. |
| Woonsocket | Christopher Beauchamp | Public mayor mailbox `mayor@woonsocketri.org`; phone: (401) 767-9205; no LinkedIn added | [Mayor’s page](https://www.woonsocketri.gov/319/Mayor-Christopher-Beauchamp) | Name/title confirmed; existing candidate was correct. |
| Cranston | Kenneth J. Hopkins | Mayor’s Office main line: (401) 461-1000; directory lists Hopkins at 780-3104; no personal email or LinkedIn added | [Mayor’s Office directory](https://www.cranstonri.gov/about/mayors-office-directory/); [Mayor page](https://www.cranstonri.gov/about/mayor-of-cranston/) | Workbook used abbreviated “Ken Hopkins”; normalized to the full official name. |

`verified` here means the official source supports the current person and role, plus any listed office contact. It does not mean an email mailbox or phone line was independently tested. Email syntax/publication is not proof of deliverability. No LinkedIn profile was added because no matching official-source-backed profile was verified.

This was one five-record pilot batch. It does not verify the remaining imported municipal candidates; those stay `needs_review`.
