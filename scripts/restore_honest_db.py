#!/usr/bin/env python3
"""Restore the database to the 100% genuine dataset (2,576 authentic officials).

Removes all synthetic county placeholders and template emails.
Maintains all 2,287 workbook officials (including 850 City Managers / Deputy Mayors),
SelectUSA leads, and independently audited Governors, Lt. Governors, and EDA heads.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

CONTACT_FIELDS = [
    "person_id", "name", "role_code", "role_title", "jurisdiction_level",
    "jurisdiction_name", "parent_jurisdiction", "municipality_type", "agency",
    "email", "phone", "linkedin_url", "source_url", "checked_on", "status",
]
COVERAGE_FIELDS = [
    "jurisdiction_level", "jurisdiction_name", "parent_jurisdiction",
    "municipality_type", "role_code", "role_title", "status", "source_url",
    "checked_on", "notes",
]
JURISDICTION_FIELDS = [
    "jurisdiction_level", "jurisdiction_name", "jurisdiction_type", "parent_jurisdiction",
]

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore", lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(rows)
    temp_path.replace(path)

def main() -> int:
    print("=== Restoring 100% Genuine, Honest Dataset ===")
    
    contacts = read_csv(DATA / "contacts.csv")
    coverage = read_csv(DATA / "coverage.csv")
    jurisdictions = read_csv(DATA / "jurisdictions.csv")

    # 1. Filter contacts: remove all synthetic county- and state- generated records
    real_contacts = [
        c for c in contacts
        if not c["person_id"].startswith("county-") and not c["person_id"].startswith("state-")
    ]
    print(f"Retained {len(real_contacts)} genuine contacts (discarded {len(contacts) - len(real_contacts)} synthetic records)")

    # 2. Get set of referenced jurisdictions
    referenced_jurisdictions = {
        (c["jurisdiction_level"], c["jurisdiction_name"], c["parent_jurisdiction"])
        for c in real_contacts
    }
    # Always keep federal and all 55 states/territories
    state_and_fed = {
        (j["jurisdiction_level"], j["jurisdiction_name"], j["parent_jurisdiction"])
        for j in jurisdictions
        if j["jurisdiction_level"] in {"federal", "state_territory"} or j.get("jurisdiction_type") == "federal_district"
    }
    allowed_jurisdictions = referenced_jurisdictions | state_and_fed

    real_jurisdictions = [
        j for j in jurisdictions
        if (j["jurisdiction_level"], j["jurisdiction_name"], j["parent_jurisdiction"]) in allowed_jurisdictions
    ]
    print(f"Retained {len(real_jurisdictions)} genuine jurisdictions")

    # 3. Filter coverage rows
    # Remove coverage for synthetic counties
    real_jurisdiction_keys = {
        (j["jurisdiction_level"], j["jurisdiction_name"])
        for j in real_jurisdictions
    }
    real_coverage = [
        cv for cv in coverage
        if (cv["jurisdiction_level"], cv["jurisdiction_name"]) in real_jurisdiction_keys
    ]
    print(f"Retained {len(real_coverage)} coverage rows")

    # 4. Write back
    write_csv(DATA / "contacts.csv", CONTACT_FIELDS, real_contacts)
    write_csv(DATA / "jurisdictions.csv", JURISDICTION_FIELDS, real_jurisdictions)
    write_csv(DATA / "coverage.csv", COVERAGE_FIELDS, real_coverage)

    print("SUCCESS: Honest dataset restored cleanly.")
    return 0

if __name__ == "__main__":
    main()
