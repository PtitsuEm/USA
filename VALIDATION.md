# VALIDATION.md

Generated: 2026-10-15, by `scripts/validate_contacts.py`, offline and read-only.

contacts.csv: 172 rows, relationships.csv: 55 rows, coverage.csv: 774 rows, jurisdictions.csv: 114 rows

Result: **0 errors, 109 warnings** (errors must be fixed before data changes ship; warnings are informational gaps)

## What these checks prove — and do not prove

- **Email check = syntax only.** It does **not** confirm an inbox or mail server exists. Per PROJECT_SPEC.md, an address counts as verified when it is published by an official source, not when a validator accepts its format.
- **Phone check = U.S./NANP format only.** No phone calls, no carrier lookups, no network requests; a passing format does not mean the number is active or reachable.
- **No network access.** The script opens local CSV files and writes this report; it performs no HTTP, SMTP, socket, or phone activity.
- **Blank emails** are flagged as warnings, not errors: each blank entry is an explicit gap a human must fill from an official source.
- **Cross-dataset warnings** (unknown jurisdiction, missing phone column) are advisory; they do not block a build.

## Findings

### Warnings (109)

- contacts.csv:58 `governor-alabama` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:59 `governor-alaska` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:60 `governor-american-samoa` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:61 `governor-arizona` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:62 `governor-arkansas` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:63 `governor-california` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:65 `governor-connecticut` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:66 `governor-delaware` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:67 `governor-florida` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:68 `governor-georgia` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:69 `governor-guam` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:70 `governor-hawaii` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:71 `governor-idaho` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:72 `governor-illinois` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:73 `governor-indiana` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:74 `governor-iowa` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:75 `governor-kansas` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:76 `governor-kentucky` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:77 `governor-louisiana` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:78 `governor-maine` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:79 `governor-maryland` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:80 `governor-massachusetts` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:81 `governor-michigan` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:82 `governor-minnesota` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:83 `governor-mississippi` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:84 `governor-missouri` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:85 `governor-montana` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:86 `governor-nebraska` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:87 `governor-nevada` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:88 `governor-new-hampshire` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:89 `governor-new-jersey` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:90 `governor-new-mexico` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:91 `governor-new-york` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:92 `governor-north-carolina` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:93 `governor-north-dakota` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:94 `governor-northern-mariana-islands` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:95 `governor-ohio` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:96 `governor-oklahoma` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:97 `governor-oregon` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:98 `governor-pennsylvania` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:99 `governor-puerto-rico` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:100 `governor-rhode-island` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:101 `governor-south-carolina` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:102 `governor-south-dakota` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:103 `governor-tennessee` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:104 `governor-texas` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:105 `governor-utah` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:106 `governor-vermont` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:107 `governor-u-s--virgin-islands` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:108 `governor-virginia` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:109 `governor-washington` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:110 `governor-west-virginia` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:111 `governor-wisconsin` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:112 `governor-wyoming` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:113 `ltgov-delaware` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:116 `mayor-wilmington-de` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:118 `mayor-middletown-de` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:119 `vice-mayor-middletown-de` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:121 `ltgov-alaska` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:122 `ltgov-american-samoa` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:123 `ltgov-arizona` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:124 `ltgov-arkansas` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:125 `ltgov-california` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:126 `ltgov-colorado` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:127 `ltgov-connecticut` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:128 `ltgov-florida` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:129 `ltgov-georgia` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:130 `ltgov-guam` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:131 `ltgov-hawaii` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:132 `ltgov-idaho` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:134 `ltgov-indiana` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:135 `ltgov-iowa` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:136 `ltgov-kansas` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:137 `ltgov-kentucky` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:138 `ltgov-louisiana` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:139 `ltgov-maine` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:140 `ltgov-maryland` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:141 `ltgov-massachusetts` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:142 `ltgov-michigan` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:143 `ltgov-minnesota` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:144 `ltgov-mississippi` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:145 `ltgov-missouri` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:146 `ltgov-montana` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:147 `ltgov-nebraska` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:148 `ltgov-nevada` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:149 `ltgov-new-hampshire` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:150 `ltgov-new-jersey` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:151 `ltgov-new-mexico` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:152 `ltgov-new-york` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:153 `ltgov-north-carolina` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:154 `ltgov-north-dakota` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:155 `ltgov-northern-mariana-islands` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:156 `ltgov-ohio` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:157 `ltgov-oklahoma` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:158 `ltgov-oregon` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:159 `ltgov-pennsylvania` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:160 `ltgov-puerto-rico` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:161 `ltgov-rhode-island` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:162 `ltgov-south-carolina` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:163 `ltgov-south-dakota` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:164 `ltgov-tennessee` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:165 `ltgov-texas` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:167 `ltgov-vermont` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:168 `ltgov-u-s--virgin-islands` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:169 `ltgov-virginia` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:170 `ltgov-washington` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:171 `ltgov-west-virginia` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:172 `ltgov-wisconsin` — `email_syntax`: no email value in row (blank cell); format check not applicable
- contacts.csv:173 `ltgov-wyoming` — `email_syntax`: no email value in row (blank cell); format check not applicable

## Coverage summary

- contacts.csv: 172 rows, 109 without a published email yet; statuses: needs_review=57, verified=115
- coverage.csv statuses: in_progress=110, needs_review=2, not_started=546, verified=116

Remember: a format pass is not a verification pass. Every contact still needs ground-truth confirmation on the linked official source before its status moves beyond `needs_review` or reaches `verified` through a published official page.
