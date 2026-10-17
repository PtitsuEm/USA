#!/usr/bin/env python3
"""Import role-matched municipal candidate leads from the supplied workbook.

Only names, listed titles, jurisdiction, and the workbook's official-site URL are
imported. Contact endpoints and LinkedIn values are deliberately omitted because
the workbook audit found them stale or unsupported. Every imported row remains
needs_review until an agent checks a direct current source.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = ROOT / "US_Government_and_Economic_Leadership.xlsx"
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
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def column_index(cell_ref: str) -> int:
    letters = "".join(c for c in cell_ref if c.isalpha())
    result = 0
    for char in letters:
        result = result * 26 + ord(char.upper()) - 64
    return result - 1


def read_workbook_rows(path: Path) -> list[dict[str, str]]:
    """Read a basic xlsx worksheet with stdlib XML (shared and inline strings)."""
    with ZipFile(path) as archive:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared = [
                "".join(node.text or "" for node in item.findall(".//m:t", NS))
                for item in shared_root.findall("m:si", NS)
            ]
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        sheet = workbook.find(".//m:sheets/m:sheet", NS)
        if sheet is None:
            raise ValueError("Workbook has no worksheet")
        rel_id = sheet.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        rel = next((x for x in rels if x.attrib.get("Id") == rel_id), None)
        if rel is None:
            raise ValueError("Cannot resolve first worksheet")
        target = rel.attrib["Target"].lstrip("/")
        if not target.startswith("xl/"):
            target = f"xl/{target}"
        sheet_root = ET.fromstring(archive.read(target))
        sheet_rows = sheet_root.findall(".//m:sheetData/m:row", NS)

    decoded: list[list[str]] = []
    for row in sheet_rows:
        cells: list[str] = []
        for cell in row.findall("m:c", NS):
            index = column_index(cell.attrib["r"])
            while len(cells) <= index:
                cells.append("")
            if cell.attrib.get("t") == "inlineStr":
                value = "".join(node.text or "" for node in cell.findall(".//m:t", NS))
            else:
                value_node = cell.find("m:v", NS)
                value = "" if value_node is None else value_node.text or ""
                if cell.attrib.get("t") == "s" and value:
                    value = shared[int(value)]
            cells[index] = value.strip()
        decoded.append(cells)

    if not decoded:
        return []
    headers = decoded[0]
    result = []
    for source_row, values in enumerate(decoded[1:], start=2):
        row = {headers[i]: values[i] if i < len(values) else "" for i in range(len(headers))}
        row["_source_row"] = str(source_row)
        result.append(row)
    return result


def canonical_city(value: str) -> str:
    city = re.sub(r"\s+", " ", value.strip())
    aliases = {"new york city": "New York", "nyc": "New York"}
    return aliases.get(city.casefold(), city)


def role_for(row: dict[str, str]) -> str | None:
    title = re.sub(r"\s+", " ", row.get("Role_Title", "").strip()).casefold()
    branch = row.get("Branch", "").strip().casefold()

    if branch == "administrative":
        if re.fullmatch(r"(?:acting )?(?:(?:city|town|village) )?mayor", title):
            return "MAYOR"
        # The workbook uses the ambiguous composite title "City Manager / Deputy Mayor"
        # for a large batch. A city manager is not automatically a deputy mayor, so
        # leave those rows for source review rather than assigning them to MAYOR_DEPUTY.
        if "city manager" not in title and "mayor" in title and any(
            term in title for term in ("deputy", "vice", "pro tem")
        ):
            return "MAYOR_DEPUTY"

    if branch == "economic development":
        if "economic development" in title and any(
            term in title for term in ("director", "chief", "executive", "president", "commissioner", "ceo")
        ):
            return "EDA_HEAD"

    if branch == "foreign investment" and any(
        term in title for term in ("fdi", "foreign investment", "international investment", "global business")
    ):
        return "FOREIGN_INVESTMENT_DEPUTY" if "deputy" in title else "FOREIGN_INVESTMENT_HEAD"
    return None


def clean_candidate_name(raw: str) -> str | None:
    name = re.sub(r"\s+", " ", raw.strip())
    # Drop trailing annotations while preserving the actual candidate name.
    name = re.sub(r"\s*\([^)]*\)\s*$", "", name).strip()
    lowered = name.casefold()
    noise = (
        "reflects on", "pro tem", "leadership team", "in bay state", "resigns",
        "city council", "democrat ", "republican ", "district attorney",
        "our mayor", "handling project", "asks governor", "stands behind",
        "municipal", "not available", "vacant",
    )
    if not name or any(marker in lowered for marker in noise):
        return None
    if any(mark in name for mark in ("[[", "]]", "<", ">", "<!--", "ref>")):
        return None
    tokens = name.split()
    if len(tokens) < 2 or len(tokens) > 6:
        return None
    if tokens[-1].casefold() in {"mc", "mc.", "pro", "tem", "the"}:
        return None
    if sum(char.isalpha() for char in name) < 4:
        return None
    return name


def valid_url(value: str) -> bool:
    parsed = urlparse(value.strip())
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def norm(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.casefold())
    return "".join(c for c in decomposed if c.isalnum())


def person_key(row: dict[str, str]) -> tuple[str, str, str, str]:
    return (
        norm(row.get("name", "")), row.get("role_code", ""),
        norm(row.get("jurisdiction_name", "")), norm(row.get("parent_jurisdiction", "")),
    )


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with temp_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(rows)
    temp_path.replace(path)


def slug(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", ascii_value).strip("-") or "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="append candidate rows to the local datasets")
    parser.add_argument("--dry-run", action="store_true", help="preview import counts without writing (default)")
    args = parser.parse_args()

    source_rows = read_workbook_rows(WORKBOOK)
    contact_path, coverage_path, jurisdiction_path = (
        DATA / "contacts.csv", DATA / "coverage.csv", DATA / "jurisdictions.csv"
    )
    contact_fields, contacts = read_csv(contact_path)
    coverage_fields, coverage = read_csv(coverage_path)
    jurisdiction_fields, jurisdictions = read_csv(jurisdiction_path)
    today = date.today().isoformat()

    existing_people = {person_key(row) for row in contacts}
    existing_ids = {row["person_id"] for row in contacts}
    existing_jurisdictions = {
        (row["jurisdiction_level"], norm(row["jurisdiction_name"]), norm(row.get("parent_jurisdiction", "")))
        for row in jurisdictions
    }
    coverage_index = {
        (row["jurisdiction_level"], norm(row["jurisdiction_name"]), norm(row.get("parent_jurisdiction", "")),
         norm(row.get("municipality_type", "")), row["role_code"]): i
        for i, row in enumerate(coverage)
    }

    candidates: list[dict[str, str]] = []
    additions_coverage: dict[tuple[str, str, str, str, str], dict[str, str]] = {}
    additions_jurisdictions: dict[tuple[str, str, str], dict[str, str]] = {}
    tallies = Counter()
    seen_batch: set[tuple[str, str, str, str]] = set()

    for source in source_rows:
        if source.get("Jurisdiction_Level", "").casefold() != "municipal":
            continue
        role = role_for(source)
        if not role:
            tallies["outside_target_roles"] += 1
            continue
        name = clean_candidate_name(source.get("Full_Name", ""))
        city = canonical_city(source.get("Municipality_City", ""))
        state = source.get("State_Territory", "").strip()
        source_url = source.get("Official_Website", "").strip()
        if not name or not city or not state or not valid_url(source_url):
            tallies["incomplete_or_malformed"] += 1
            continue
        candidate = {
            "name": name,
            "role_code": role,
            "jurisdiction_name": city,
            "parent_jurisdiction": state,
        }
        key = person_key(candidate)
        if key in existing_people or key in seen_batch:
            tallies["duplicate_or_existing"] += 1
            continue
        seen_batch.add(key)
        source_line = int(source["_source_row"])
        pid = f"wb-muni-r{source_line:04d}-{slug(role)}-{slug(city)}-{slug(state)}"
        if pid in existing_ids:
            tallies["duplicate_or_existing"] += 1
            continue

        role_title = re.sub(r"\s+", " ", source.get("Role_Title", "").strip())
        contact = {
            "person_id": pid,
            "name": name,
            "role_code": role,
            "role_title": role_title,
            "jurisdiction_level": "municipality",
            "jurisdiction_name": city,
            "parent_jurisdiction": state,
            "municipality_type": "municipality",
            "agency": "",
            "email": "",
            "phone": "",
            "linkedin_url": "",
            "source_url": source_url,
            "checked_on": today,
            "status": "needs_review",
        }
        candidates.append(contact)
        tallies[role] += 1

        municipality_key = ("municipality", norm(city), norm(state))
        if municipality_key not in existing_jurisdictions:
            additions_jurisdictions[municipality_key] = {
                "jurisdiction_level": "municipality",
                "jurisdiction_name": city,
                "jurisdiction_type": "municipality",
                "parent_jurisdiction": state,
            }
            existing_jurisdictions.add(municipality_key)

        ckey = ("municipality", norm(city), norm(state), norm("municipality"), role)
        notes = f"Unverified candidate imported from workbook row {source_line}; contact fields withheld pending direct source review."
        if ckey not in coverage_index:
            additions_coverage[ckey] = {
                "jurisdiction_level": "municipality",
                "jurisdiction_name": city,
                "parent_jurisdiction": state,
                "municipality_type": "municipality",
                "role_code": role,
                "role_title": role_title,
                "status": "needs_review",
                "source_url": source_url,
                "checked_on": today,
                "notes": notes,
            }
            coverage_index[ckey] = len(coverage) + len(additions_coverage) - 1
        else:
            idx = coverage_index[ckey]
            if idx < len(coverage) and coverage[idx]["status"] == "not_started":
                coverage[idx].update({"status": "needs_review", "source_url": source_url, "checked_on": today, "notes": notes})

    print(f"Workbook municipal candidate rows considered: {sum(1 for x in source_rows if x.get('Jurisdiction_Level','').casefold()=='municipal')}")
    print(f"Lead candidates to append: {len(candidates)}")
    for key, count in sorted(tallies.items()):
        print(f"  {key}: {count}")
    print(f"New municipality jurisdiction rows: {len(additions_jurisdictions)}")
    print(f"New or promoted coverage rows: {len(additions_coverage)} new, plus existing not_started rows promoted where a candidate was found")
    print("Imported contact data policy: name/title/location/source only; email, phone, and LinkedIn left blank; status=needs_review.")

    if not args.apply:
        print("Dry run only; pass --apply to append candidates.")
        return 0

    contacts.extend(candidates)
    coverage.extend(additions_coverage.values())
    jurisdictions.extend(additions_jurisdictions.values())
    write_csv(contact_path, contact_fields or CONTACT_FIELDS, contacts)
    write_csv(coverage_path, coverage_fields or COVERAGE_FIELDS, coverage)
    write_csv(jurisdiction_path, jurisdiction_fields or JURISDICTION_FIELDS, jurisdictions)
    print(f"Applied. New totals: contacts={len(contacts)}, coverage={len(coverage)}, jurisdictions={len(jurisdictions)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
