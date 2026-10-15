#!/usr/bin/env python3
"""Read-only, offline format validator for the project CSV datasets.

Checks (format only, by design):
- contacts.csv: required fields, email syntax, optional U.S./NANP phone
  format when a phone column exists, required http(s) source_url,
  checked_on date format, duplicate person_id.
- relationships.csv: known relationship types, endpoints present in
  contacts.csv, required source_url and date when rows exist.
- coverage.csv: required role fields, source_url required unless the row
  is explicitly `not_started`, date format, duplicate role+jurisdiction
  rows, status vocabulary.
- jurisdictions.csv: duplicate jurisdictions, level/type vocabulary,
  municipality rows must name an existing parent jurisdiction.
- Cross-dataset: jurisdictions referenced by contacts/coverage should
  exist in jurisdictions.csv (warning only).

What it does NOT do: no network access, no sending of email, no dialing,
no MX lookups, no verification that an inbox or phone number is active.
A pass here means "the string is well-formed", nothing more. Whether an
address or number is real must be confirmed against the published source
per PROJECT_SPEC.md.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DEFAULT_REPORT = ROOT / "VALIDATION.md"

DATASETS = ("contacts.csv", "relationships.csv", "coverage.csv", "jurisdictions.csv")

CONTACT_REQUIRED = ("person_id", "name", "role_code", "role_title", "jurisdiction_level", "jurisdiction_name", "source_url", "checked_on", "status")
CONTACT_STATUSES = {"verified", "needs_review", "in_progress"}

RELATIONSHIP_REQUIRED = ("from_person_id", "to_person_id", "relationship_type", "source_url", "checked_on")
RELATIONSHIP_TYPES = {"reports_to", "coordinates_with", "same_agency", "other"}

COVERAGE_REQUIRED = ("jurisdiction_level", "jurisdiction_name", "role_code", "role_title", "status")
COVERAGE_STATUSES = {"verified", "needs_review", "in_progress", "not_started"}
# Rows still waiting on the first source may omit the URL.
COVERAGE_STATUS_ALLOWING_BLANK_URL = {"not_started"}

JURISDICTION_LEVELS = {"federal", "state_territory", "municipality"}
JURISDICTION_TYPES = {"federal", "state", "territory", "federal_district", "municipality"}

# Headers we would treat as a U.S. phone column, normalized (lowercase).
PHONE_HEADER_HINTS = {"phone", "phone_number", "phone_no", "telephone", "phone_us", "us_phone", "contact_phone"}

EMAIL_RE = re.compile(r"^[A-Za-z0-9!#$%&'*+/=?^_`{|}~.-]+@([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z]{2,63}$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
US_PHONE_RE = re.compile(
    r"^(?:\+?1[\s.-]?)?(?:\(\s*(\d{3})\s*\)|(\d{3}))[\s.-]?(\d{3})[\s.-]?(\d{4})(?:\s*(?:x|ext\.?|extension)\s*\d{1,6})?$",
    re.IGNORECASE,
)

ERRORS = "errors"
WARNINGS = "warnings"


class Finding:
    def __init__(self, dataset: str, severity: str, check: str, line: int, key: str, message: str):
        self.dataset = dataset
        self.severity = severity
        self.check = check
        self.line = line
        self.key = key  # row identifier, e.g. person_id
        self.message = message

    @property
    def where(self) -> str:
        base = f"{self.dataset}:{self.line}"
        return f"{base} `{self.key}`" if self.key else base


def error(dataset: str, check: str, line: int, key: str, message: str) -> Finding:
    return Finding(dataset, ERRORS, check, line, key, message)


def warn(dataset: str, check: str, line: int, key: str, message: str) -> Finding:
    return Finding(dataset, WARNINGS, check, line, key, message)


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def email_syntax_ok(address: str) -> tuple[bool, str]:
    """Format check only. Never implies the mailbox exists or is reachable."""
    if address.count("@") != 1:
        return False, "email must contain exactly one '@'"
    if not EMAIL_RE.match(address):
        return False, "email does not match expected syntax local@domain.tld"
    local = address.split("@", 1)[0]
    if ".." in local or local.startswith(".") or local.endswith("."):
        return False, "email local part has misplaced dots"
    if len(local) > 64:
        return False, "email local part exceeds 64 characters"
    if len(address) > 254:
        return False, "email exceeds 254 characters"
    return True, ""


def url_ok(value: str, required: bool) -> tuple[bool, str]:
    if not value.strip():
        return (False, "missing required http(s) URL") if required else (True, "")
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return False, "must be an http(s) URL with a host"
    return True, ""


def checked_on_ok(value: str) -> tuple[bool, str]:
    if not DATE_RE.match(value):
        return False, "date must be YYYY-MM-DD"
    try:
        date.fromisoformat(value)
    except ValueError:
        return False, "not a valid calendar date"
    return True, ""


def us_phone_syntax_ok(raw: str) -> tuple[bool, str]:
    """10-digit NANP shape only. Does NOT confirm the number is in service."""
    match = US_PHONE_RE.match(raw.strip())
    if not match:
        return False, "not a recognizable U.S. phone format (e.g. (555) 123-4567)"
    area = match.group(1) or match.group(2)
    if area[0] in "01":
        return False, "NANP area code must not start with 0 or 1"
    if match.group(3)[0] in "01":
        return False, "NANP exchange must not start with 0 or 1"
    return True, ""


def check_contacts(rows: list[dict[str, str]], phone_columns: list[str]) -> list[Finding]:
    name = "contacts.csv"
    findings: list[Finding] = []
    seen_ids: dict[str, int] = {}
    for line, row in enumerate(rows, start=2):
        pid = (row.get("person_id") or "").strip()
        for field in CONTACT_REQUIRED:
            if not (row.get(field) or "").strip():
                findings.append(error(name, "required_fields", line, pid, f"missing required field {field}"))
        if pid:
            if pid in seen_ids:
                findings.append(error(name, "duplicate_person_id", line, pid, f"duplicate person_id; first seen on line {seen_ids[pid]}"))
            else:
                seen_ids[pid] = line
        email = (row.get("email") or "").strip()
        if email:
            ok, why = email_syntax_ok(email)
            if not ok:
                findings.append(error(name, "email_syntax", line, pid, why))
        else:
            findings.append(warn(name, "email_syntax", line, pid, "no email value in row (blank cell); format check not applicable"))
        ok, why = url_ok(row.get("source_url") or "", required=True)
        if not ok:
            findings.append(error(name, "source_url", line, pid, why))
        if row.get("linkedin_url", "").strip():
            ok, why = url_ok(row["linkedin_url"] or "", required=True)
            if not ok:
                findings.append(error(name, "linkedin_url", line, pid, why))
        ok, why = checked_on_ok((row.get("checked_on") or "").strip())
        if not ok:
            findings.append(error(name, "checked_on_format", line, pid, why))
        status = (row.get("status") or "").strip()
        if status and status not in CONTACT_STATUSES:
            findings.append(warn(name, "status_vocabulary", line, pid, f"unknown status {status!r}"))
        for col in phone_columns:
            value = (row.get(col) or "").strip()
            if not value:
                continue
            ok, why = us_phone_syntax_ok(value)
            if not ok:
                findings.append(error(name, "us_phone_format", line, pid, f"{col}: {why}"))
    return findings


def check_relationships(rows: list[dict[str, str]], contact_ids: set[str]) -> list[Finding]:
    name = "relationships.csv"
    findings: list[Finding] = []
    seen_pairs: Counter[tuple[str, str, str]] = Counter()
    for line, row in enumerate(rows, start=2):
        label = (row.get("from_person_id") or "") + "->" + (row.get("to_person_id") or "")
        for field in RELATIONSHIP_REQUIRED:
            if not (row.get(field) or "").strip():
                findings.append(error(name, "required_fields", line, label, f"missing required field {field}"))
        for endpoint in ("from_person_id", "to_person_id"):
            if (row.get(endpoint) or "").strip() and row[endpoint].strip() not in contact_ids:
                findings.append(error(name, "unknown_person", line, label, f"{endpoint} not present in contacts.csv"))
        rel_type = (row.get("relationship_type") or "").strip()
        if rel_type and rel_type not in RELATIONSHIP_TYPES:
            findings.append(error(name, "relationship_type", line, label, f"unsupported relationship_type {rel_type!r}"))
        ok, why = url_ok(row.get("source_url") or "", required=True)
        if not ok:
            findings.append(error(name, "source_url", line, label, why))
        ok, why = checked_on_ok((row.get("checked_on") or "").strip())
        if not ok:
            findings.append(error(name, "checked_on_format", line, label, why))
        key = (row.get("from_person_id", ""), row.get("to_person_id", ""), rel_type)
        seen_pairs[key] += 1
        if seen_pairs[key] > 1:
            findings.append(error(name, "duplicate_relationship", line, label, "duplicate from/to/type row"))
    return findings


def check_coverage(rows: list[dict[str, str]], jurisdictions: set[tuple[str, str]]) -> list[Finding]:
    name = "coverage.csv"
    findings: list[Finding] = []
    seen_keys: dict[tuple[str, str, str], int] = {}
    for line, row in enumerate(rows, start=2):
        key = role_key(row)
        for field in COVERAGE_REQUIRED:
            if not (row.get(field) or "").strip():
                findings.append(error(name, "required_fields", line, key, f"missing required field {field}"))
        status = (row.get("status") or "").strip()
        if status and status not in COVERAGE_STATUSES:
            findings.append(error(name, "status_vocabulary", line, key, f"unknown status {status!r}"))
        url_required = status not in COVERAGE_STATUS_ALLOWING_BLANK_URL
        ok, why = url_ok(row.get("source_url") or "", required=url_required)
        if not ok:
            findings.append(error(name, "source_url", line, key, "source_url is required unless status is not_started" if why == "missing required http(s) URL" else why))
        if (row.get("checked_on") or "").strip():
            ok, why = checked_on_ok(row["checked_on"])
            if not ok:
                findings.append(error(name, "checked_on_format", line, key, why))
        dup_line = seen_keys.get((row.get("jurisdiction_level", ""), row.get("jurisdiction_name", ""), row.get("role_code", "")))
        if dup_line:
            findings.append(error(name, "duplicate_role_row", line, key, f"duplicate role row; first seen on line {dup_line}"))
        seen_keys[(row.get("jurisdiction_level", ""), row.get("jurisdiction_name", ""), row.get("role_code", ""))] = line
        jk = (row.get("jurisdiction_level", ""), row.get("jurisdiction_name", ""))
        if jk[0] and jk[1] and jk not in jurisdictions:
            findings.append(warn(name, "unknown_jurisdiction", line, key, "jurisdiction not present in jurisdictions.csv"))
    return findings


def role_key(row: dict[str, str]) -> str:
    return "/".join(part for part in (row.get("jurisdiction_level", ""), row.get("jurisdiction_name", ""), row.get("role_code", "")) if part)


def check_jurisdictions(rows: list[dict[str, str]]) -> tuple[list[Finding], set[tuple[str, str]]]:
    name = "jurisdictions.csv"
    findings: list[Finding] = []
    seen: dict[tuple[str, str], int] = {}
    known: set[tuple[str, str]] = set()
    for line, row in enumerate(rows, start=2):
        level = (row.get("jurisdiction_level") or "").strip()
        jname = (row.get("jurisdiction_name") or "").strip()
        jkey = f"{level}/{jname}"
        if level and level not in JURISDICTION_LEVELS:
            findings.append(error(name, "level_vocabulary", line, jkey, f"unknown jurisdiction_level {level!r}"))
        jtype = (row.get("jurisdiction_type") or "").strip()
        if jtype and jtype not in JURISDICTION_TYPES:
            findings.append(error(name, "type_vocabulary", line, jkey, f"unknown jurisdiction_type {jtype!r}"))
        if (level, jname) in seen:
            findings.append(error(name, "duplicate_jurisdiction", line, jkey, f"duplicate jurisdiction; first seen on line {seen[(level, jname)]}"))
        seen[(level, jname)] = line
        known.add((level, jname))
        parent = (row.get("parent_jurisdiction") or "").strip()
        if level == "municipality" and jtype == "municipality" and not parent:
            findings.append(error(name, "missing_parent", line, jkey, "municipality rows must name a parent state/territory"))
        if parent and ("state_territory", parent) not in known and not any(k[1] == parent and k[0] == "state_territory" for k in seen if k[0] == "state_territory"):
            findings.append(warn(name, "unknown_parent", line, jkey, f"parent {parent!r} not (yet) defined as state_territory"))
    return findings, known


def load_payload(data_dir: Path, contacts_path: Path | None = None) -> dict[str, tuple[list[str], list[dict[str, str]]]]:
    payload: dict[str, tuple[list[str], list[dict[str, str]]]] = {}
    for dataset in DATASETS:
        path = contacts_path if (dataset == "contacts.csv" and contacts_path) else data_dir / dataset
        payload[dataset] = read_csv(path)
    return payload


def validate(payload: dict[str, tuple[list[str], list[dict[str, str]]]]) -> list[Finding]:
    findings: list[Finding] = []
    contacts_rows = payload["contacts.csv"][1]
    jurisdictions_rows = payload["jurisdictions.csv"][1]

    # Structural notes for empty datasets and missing columns are surfaced as findings.
    for dataset, (headers, rows) in payload.items():
        if not headers:
            findings.append(error(dataset, "structure", 1, "", "no header row found"))
            continue
        required = {
            "contacts.csv": CONTACT_REQUIRED,
            "relationships.csv": (),
            "coverage.csv": COVERAGE_REQUIRED,
            "jurisdictions.csv": (),
        }[dataset]
        missing = [f for f in required if f not in headers]
        if missing:
            findings.append(error(dataset, "structure", 1, "", "missing expected columns: " + ", ".join(missing)))
        if "relationships.csv" == dataset and not rows:
            # An empty relationships file is valid but must stay visibly empty.
            pass

    phone_columns = [h for h in payload["contacts.csv"][0] if h.strip().lower() in PHONE_HEADER_HINTS]
    if not phone_columns:
        findings.insert(0, Finding("contacts.csv", WARNINGS, "phone_column", 1, "", "No phone column in the current schema; the U.S. phone-number format check was skipped. Schema left unchanged by design."))

    contact_ids = {(r.get("person_id") or "").strip() for r in contacts_rows} - {""}
    _findings, known_jurisdictions = check_jurisdictions(jurisdictions_rows)
    findings.extend(_findings)
    findings.extend(check_contacts(contacts_rows, phone_columns))
    findings.extend(check_relationships(payload["relationships.csv"][1], contact_ids))
    findings.extend(check_coverage(payload["coverage.csv"][1], known_jurisdictions))
    return findings


def describe_rows(payload) -> str:
    parts = []
    for dataset in DATASETS:
        n = len(payload[dataset][1])
        parts.append(f"{dataset}: {n} rows")
    return ", ".join(parts)


def build_report(payload, findings: list[Finding]) -> str:
    generated = date.today().isoformat()
    n_err = sum(1 for f in findings if f.severity == ERRORS)
    n_warn = sum(1 for f in findings if f.severity == WARNINGS)
    lines: list[str] = []
    lines.append("# VALIDATION.md")
    lines.append("")
    lines.append(f"Generated: {generated}, by `scripts/validate_contacts.py`, offline and read-only.")
    lines.append("")
    lines.append(describe_rows(payload))
    lines.append("")
    lines.append(f"Result: **{n_err} errors, {n_warn} warnings** (errors must be fixed before data changes ship; warnings are informational gaps)")
    lines.append("")
    lines.append("## What these checks prove — and do not prove")
    lines.append("")
    lines.append("- **Email check = syntax only.** It does **not** confirm an inbox or mail server exists. Per PROJECT_SPEC.md, an address counts as verified when it is published by an official source, not when a validator accepts its format.")
    lines.append("- **Phone check = U.S./NANP format only.** No phone calls, no carrier lookups, no network requests; a passing format does not mean the number is active or reachable.")
    lines.append("- **No network access.** The script opens local CSV files and writes this report; it performs no HTTP, SMTP, socket, or phone activity.")
    lines.append("- **Blank emails** are flagged as warnings, not errors: each blank entry is an explicit gap a human must fill from an official source.")
    lines.append("- **Cross-dataset warnings** (unknown jurisdiction, missing phone column) are advisory; they do not block a build.")
    lines.append("")
    lines.append("## Findings")
    lines.append("")
    if not findings:
        lines.append("_None._")
    else:
        for sev, title in ((ERRORS, "Errors"), (WARNINGS, "Warnings")):
            group = [f for f in findings if f.severity == sev]
            if not group:
                continue
            lines.append(f"### {title} ({len(group)})")
            lines.append("")
            for f in group:
                lines.append(f"- {f.where} — `{f.check}`: {f.message}")
            lines.append("")
    lines.append("## Coverage summary")
    lines.append("")
    contacts_rows = payload["contacts.csv"][1]
    blanks = sum(1 for r in contacts_rows if not (r.get("email") or "").strip())
    by_status = Counter((r.get("status") or "").strip() for r in contacts_rows)
    lines.append(f"- contacts.csv: {len(contacts_rows)} rows, {blanks} without a published email yet; statuses: " + ", ".join(f"{k}={v}" for k, v in sorted(by_status.items())))
    cov_by_status = Counter((r.get("status") or "").strip() for r in payload["coverage.csv"][1])
    lines.append(f"- coverage.csv statuses: " + ", ".join(f"{k}={v}" for k, v in sorted(cov_by_status.items())))
    lines.append("")
    lines.append("Remember: a format pass is not a verification pass. Every contact still needs ground-truth confirmation on the linked official source before its status moves beyond `needs_review` or reaches `verified` through a published official page.")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.strip().splitlines()[0])
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--contacts", default=None, help="override path of contacts.csv (for tests)")
    args = parser.parse_args()

    payload = load_payload(DATA, Path(args.contacts) if args.contacts else None)
    findings = validate(payload)
    report = build_report(payload, findings)
    Path(args.report).write_text(report, encoding="utf-8")

    n_err = sum(1 for f in findings if f.severity == ERRORS)
    n_warn = sum(1 for f in findings if f.severity == WARNINGS)
    n_phone = len([h for h in payload["contacts.csv"][0] if h.strip().lower() in PHONE_HEADER_HINTS])
    print(describe_rows(payload))
    print(f"Phone columns detected: {[h for h in payload['contacts.csv'][0] if h.strip().lower() in PHONE_HEADER_HINTS] or 'none'}")
    print(f"{n_err} errors, {n_warn} warnings")
    print(f"Report written to {args.report}")
    return 2 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
