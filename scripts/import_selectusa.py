#!/usr/bin/env python3
"""Import SelectUSA's public state/territory investment-contact leads.

Imported rows stay needs_review until confirmed on the contact's agency page.
Existing rows are never overwritten by this importer.
"""

from __future__ import annotations

import csv
import html
import re
import argparse
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
SOURCE = "https://www.trade.gov/selectusa-find-economic-developers"
FIELDS = [
    "person_id", "name", "role_code", "role_title", "jurisdiction_level",
    "jurisdiction_name", "parent_jurisdiction", "municipality_type", "agency",
    "email", "phone", "linkedin_url", "source_url", "checked_on", "status",
]


class TextLines(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.lines: list[str] = []
        self.current: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "br":
            self._flush()

    def handle_endtag(self, tag: str) -> None:
        if tag in {"p", "div", "li"}:
            self._flush()

    def handle_data(self, data: str) -> None:
        self.current.append(data)

    def _flush(self) -> None:
        text = " ".join(" ".join(self.current).split())
        if text:
            self.lines.append(text)
        self.current = []

    def finish(self) -> list[str]:
        self._flush()
        return self.lines


def slug(value: str) -> str:
    value = value.lower().replace("&", "and")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh-selectusa", action="store_true", help="refresh existing rows imported from SelectUSA")
    args = parser.parse_args()
    request = Request(SOURCE, headers={"User-Agent": "Mozilla/5.0 contact-catalog-research"})
    page = urlopen(request, timeout=30).read().decode("utf-8", "replace")
    table_match = re.search(r'<table class="table text-left base-table.*?</table>', page, re.S | re.I)
    if not table_match:
        raise RuntimeError("Could not find the SelectUSA contacts table; no files were changed.")
    table = table_match.group(0)

    jurisdictions_path = ROOT / "data" / "jurisdictions.csv"
    with jurisdictions_path.open(encoding="utf-8-sig", newline="") as f:
        jurisdictions = {row["jurisdiction_name"]: row for row in csv.DictReader(f)}

    parsed: list[dict[str, str]] = []
    cells = re.findall(r"<td\b[^>]*>(.*?)</td>", table, re.S | re.I)
    for cell in cells:
        heading = re.search(r"<h2\b[^>]*>(.*?)</h2>", cell, re.S | re.I)
        if not heading:
            continue
        source_jurisdiction = html.unescape(re.sub(r"<[^>]+>", "", heading.group(1))).strip()
        jurisdiction_name = "District of Columbia" if source_jurisdiction == "Washington, D.C." else source_jurisdiction
        jurisdiction = jurisdictions.get(jurisdiction_name)
        if not jurisdiction:
            raise RuntimeError(f"SelectUSA lists {source_jurisdiction!r}, which is missing from jurisdictions.csv.")

        mail = re.search(r'href=["\']mailto:([^"\']+)', cell, re.I)
        paragraph = re.search(r"<p\b[^>]*>(.*?)</p>", cell, re.S | re.I)
        if not paragraph:
            continue
        # Keep <br> tags intact: TextLines uses them to split the directory's
        # name, title, organization, and address into separate lines.
        body = paragraph.group(1)
        text = TextLines()
        text.feed(body)
        lines = text.finish()
        if not lines:
            continue

        name = lines[0].strip()
        email = html.unescape(mail.group(1)).strip() if mail else ""
        phone = next((line[2:].strip() for line in lines[1:] if line.startswith("T:") and line[2:].strip()), "")
        if not phone:
            phone = next((line[2:].strip() for line in lines[1:] if line.startswith("C:") and line[2:].strip()), "")
        info = [line for line in lines[1:] if not line.startswith(("T:", "C:"))]
        title = info[0] if info else "Title not stated in SelectUSA directory"
        agency = info[1] if len(info) > 1 else ""

        parsed.append({
            "person_id": f"selectusa-{slug(jurisdiction_name)}",
            "name": name,
            "role_code": "INVESTOR_RELATIONS_CONTACT",
            "role_title": title,
            "jurisdiction_level": jurisdiction["jurisdiction_level"],
            "jurisdiction_name": jurisdiction_name,
            "parent_jurisdiction": "",
            "municipality_type": "",
            "agency": agency,
            "email": email,
            "phone": phone,
            "linkedin_url": "",
            "source_url": SOURCE,
            "checked_on": date.today().isoformat(),
            "status": "needs_review",
        })

    contacts_path = ROOT / "data" / "contacts.csv"
    with contacts_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        existing = list(reader)
        if reader.fieldnames != FIELDS:
            raise RuntimeError("contacts.csv schema differs from the expected fields; no files were changed.")
    existing_by_id = {row["person_id"]: row for row in existing}
    additions = [row for row in parsed if row["person_id"] not in existing_by_id]
    refreshed = 0
    if args.refresh_selectusa:
        refreshed_by_id = {}
        for row in parsed:
            old = existing_by_id.get(row["person_id"])
            if old:
                if old["name"] == row["name"]:
                    row["linkedin_url"] = old["linkedin_url"]
                    row["phone"] = old.get("phone", "") or row["phone"]
                refreshed_by_id[row["person_id"]] = row
                refreshed += 1
        existing = [refreshed_by_id.get(row["person_id"], row) for row in existing]
    if not additions and not refreshed:
        print(f"No new rows; {len(parsed)} SelectUSA contacts are already present. Use --refresh-selectusa to refresh them.")
        return
    with contacts_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(existing)
        writer.writerows(additions)
    print(f"Added {len(additions)} and refreshed {refreshed} SelectUSA contact leads as needs_review.")


if __name__ == "__main__":
    main()
