#!/usr/bin/env python3
"""Build a self-contained, offline HTML browser from the project CSV files."""

from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlparse
from xml.sax.saxutils import escape
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DIST = ROOT / "dist"


def read_csv(name: str) -> list[dict[str, str]]:
    path = DATA / name
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def require_url(value: str, where: str) -> None:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{where}: expected an http(s) source URL")


def validate(payload: dict[str, list[dict[str, str]]]) -> None:
    contacts = payload["contacts"]
    ids: set[str] = set()
    for line, row in enumerate(contacts, start=2):
        where = f"contacts.csv:{line}"
        for field in ("person_id", "name", "role_code", "role_title", "jurisdiction_level", "jurisdiction_name", "source_url", "checked_on", "status"):
            if not row.get(field, "").strip():
                raise ValueError(f"{where}: missing {field}")
        if row["person_id"] in ids:
            raise ValueError(f"{where}: duplicate person_id {row['person_id']}")
        ids.add(row["person_id"])
        require_url(row["source_url"], where)
        if row.get("linkedin_url", "").strip():
            require_url(row["linkedin_url"], f"{where} linkedin_url")
        email = row.get("email", "").strip()
        if email and ("@" not in email or any(ch.isspace() for ch in email)):
            raise ValueError(f"{where}: malformed email value")

    for line, row in enumerate(payload["relationships"], start=2):
        where = f"relationships.csv:{line}"
        for field in ("from_person_id", "to_person_id", "relationship_type", "source_url", "checked_on"):
            if not row.get(field, "").strip():
                raise ValueError(f"{where}: missing {field}")
        if row["from_person_id"] not in ids or row["to_person_id"] not in ids:
            raise ValueError(f"{where}: relationship endpoint is missing from contacts.csv")
        if row["relationship_type"] not in {"reports_to", "coordinates_with", "same_agency", "other"}:
            raise ValueError(f"{where}: unsupported relationship_type")
        require_url(row["source_url"], where)

    for line, row in enumerate(payload["coverage"], start=2):
        where = f"coverage.csv:{line}"
        for field in ("jurisdiction_level", "jurisdiction_name", "role_code", "role_title", "status"):
            if not row.get(field, "").strip():
                raise ValueError(f"{where}: missing {field}")
        if row.get("source_url", "").strip():
            require_url(row["source_url"], where)


def csv_headers(name: str) -> list[str]:
    with (DATA / name).open(encoding="utf-8-sig", newline="") as f:
        return next(csv.reader(f), [])


def column_name(number: int) -> str:
    name = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        name = chr(65 + remainder) + name
    return name


def xlsx_sheet(headers: list[str], rows: list[dict[str, str]]) -> str:
    all_rows = [headers] + [[row.get(key, "") for key in headers] for row in rows]
    xml_rows = []
    for row_number, values in enumerate(all_rows, start=1):
        cells = []
        for col_number, value in enumerate(values, start=1):
            ref = f"{column_name(col_number)}{row_number}"
            text = escape(str(value or ""))
            cells.append(f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{text}</t></is></c>')
        xml_rows.append(f'<row r="{row_number}">{"".join(cells)}</row>')
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>' + "".join(xml_rows) + "</sheetData></worksheet>"


def write_workbook(payload: dict[str, list[dict[str, str]]]) -> Path:
    tables = [
        ("Contacts", "contacts.csv", payload["contacts"]),
        ("Relationships", "relationships.csv", payload["relationships"]),
        ("Coverage", "coverage.csv", payload["coverage"]),
        ("Jurisdictions", "jurisdictions.csv", payload["jurisdictions"]),
    ]
    workbook_path = DATA / "contacts.xlsx"
    content_overrides = "".join(
        f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i in range(1, len(tables) + 1)
    )
    sheets = "".join(
        f'<sheet name="{name}" sheetId="{i}" r:id="rId{i}"/>'
        for i, (name, _, _) in enumerate(tables, start=1)
    )
    workbook_rels = "".join(
        f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>'
        for i in range(1, len(tables) + 1)
    )
    with ZipFile(workbook_path, "w", ZIP_DEFLATED) as book:
        book.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>' + content_overrides + "</Types>")
        book.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        book.writestr("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + sheets + "</sheets></workbook>")
        book.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + workbook_rels + "</Relationships>")
        for i, (_, filename, rows) in enumerate(tables, start=1):
            book.writestr(f"xl/worksheets/sheet{i}.xml", xlsx_sheet(csv_headers(filename), rows))
    return workbook_path


def main() -> None:
    payload = {
        "contacts": read_csv("contacts.csv"),
        "relationships": read_csv("relationships.csv"),
        "coverage": read_csv("coverage.csv"),
        "jurisdictions": read_csv("jurisdictions.csv"),
    }
    validate(payload)
    encoded = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    template = (ROOT / "app" / "index.template.html").read_text(encoding="utf-8")
    output = template.replace("__DATA_JSON__", encoded)
    DIST.mkdir(exist_ok=True)
    (DIST / "index.html").write_text(output, encoding="utf-8")
    workbook_path = write_workbook(payload)
    print(f"Built {DIST / 'index.html'} and {workbook_path} ({len(payload['contacts'])} contacts)")


if __name__ == "__main__":
    main()
