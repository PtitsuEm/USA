#!/usr/bin/env python3
"""Tests for scripts/validate_contacts.py. Run: python3 -m unittest tests.test_validation"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import validate_contacts as v  # noqa: E402

CONTACT_HEADER = ["person_id", "name", "role_code", "role_title", "jurisdiction_level", "jurisdiction_name", "parent_jurisdiction", "municipality_type", "agency", "email", "phone", "linkedin_url", "source_url", "checked_on", "status"]


def contact_row(**overrides):
    row = dict.fromkeys(CONTACT_HEADER, "")
    row.update({
        "person_id": "id-1",
        "name": "Test Person",
        "role_code": "GOVERNOR",
        "role_title": "Governor",
        "jurisdiction_level": "state_territory",
        "jurisdiction_name": "Test State",
        "source_url": "https://example.gov/page",
        "checked_on": "2026-10-15",
        "status": "needs_review",
    })
    row.update(overrides)
    return row


def coverage_row(**overrides):
    row = dict.fromkeys(["jurisdiction_level", "jurisdiction_name", "parent_jurisdiction", "municipality_type", "role_code", "role_title", "status", "source_url", "checked_on", "notes"], "")
    row.update({
        "jurisdiction_level": "state_territory",
        "jurisdiction_name": "Test State",
        "role_code": "EDA_HEAD",
        "role_title": "EDA head",
        "status": "in_progress",
        "source_url": "https://example.gov/eda",
        "checked_on": "2026-10-15",
    })
    row.update(overrides)
    return row


def jurisdiction_rows():
    return [
        {"jurisdiction_level": "federal", "jurisdiction_name": "United States", "jurisdiction_type": "federal", "parent_jurisdiction": ""},
        {"jurisdiction_level": "state_territory", "jurisdiction_name": "Test State", "jurisdiction_type": "state", "parent_jurisdiction": ""},
        {"jurisdiction_level": "municipality", "jurisdiction_name": "Test City", "jurisdiction_type": "municipality", "parent_jurisdiction": "Test State"},
    ]


def by_check(findings):
    return {f.check for f in findings}


class EmailTests(unittest.TestCase):
    def test_valid_email_passes(self):
        for good in ("a.b@c.gov", "Capital.Words@Example.COM", "x+y-tag_1@d.co.us", "governorpolis@state.co.us"):
            self.assertTrue(v.email_syntax_ok(good)[0], good)

    def test_invalid_email_fails(self):
        for bad in ("no-at-sign", "double@@example.gov", "bad user@example.gov", "@example.gov", "a@host", "a..b@example.gov", ".a@example.gov", "a@-bad-.gov"):
            ok, why = v.email_syntax_ok(bad)
            self.assertFalse(ok, f"{bad} should fail: {why}")


class PhoneTests(unittest.TestCase):
    def test_valid_nanp(self):
        for good in ("(334) 590-5982", "334-590-5982", "+1 302 366 7000", "302.378.5670", "(302) 366-7000 x12"):
            self.assertTrue(v.us_phone_syntax_ok(good)[0], good)

    def test_invalid_nanp(self):
        for bad in ("555-1234", "1234567890", "(255) 123-4567", "555-013-4567", "abc-def-ghij", ""):
            self.assertFalse(v.us_phone_syntax_ok(bad)[0], bad)


class DateTests(unittest.TestCase):
    def test_valid_and_invalid(self):
        self.assertTrue(v.checked_on_ok("2026-02-29" if False else "2016-02-29")[0])  # leap day
        self.assertFalse(v.checked_on_ok("2026/10/15")[0])
        self.assertFalse(v.checked_on_ok("2026-13-01")[0])
        self.assertFalse(v.checked_on_ok("" )[0])


class ContactChecksTests(unittest.TestCase):
    def test_clean_row_has_no_errors(self):
        findings = v.check_contacts([contact_row()], ["phone"])
        self.assertEqual([], [f for f in findings if f.severity == v.ERRORS])

    def test_blank_email_is_warning_only(self):
        findings = v.check_contacts([contact_row(email="")], [])
        self.assertEqual({"email_syntax"}, {f.check for f in findings})
        self.assertEqual(v.WARNINGS, findings[0].severity)

    def test_bad_email_is_error(self):
        findings = v.check_contacts([contact_row(email="bad user@gov")], [])
        error_findings = [f for f in findings if f.severity == v.ERRORS]
        self.assertEqual(["email_syntax"], [f.check for f in error_findings])

    def test_missing_source_url(self):
        findings = v.check_contacts([contact_row(source_url="")], [])
        self.assertIn("source_url", by_check(f for f in findings if f.severity == v.ERRORS))

    def test_bad_source_url(self):
        findings = v.check_contacts([contact_row(source_url="not-a-url")], [])
        self.assertIn("source_url", by_check(f for f in findings if f.severity == v.ERRORS))

    def test_bad_date(self):
        findings = v.check_contacts([contact_row(checked_on="10/15/2026")], [])
        self.assertIn("checked_on_format", by_check(f for f in findings if f.severity == v.ERRORS))

    def test_duplicate_id(self):
        findings = v.check_contacts([contact_row(), contact_row(person_id="id-1")], [])
        dup = [f for f in findings if f.check == "duplicate_person_id"]
        self.assertEqual(1, len(dup))
        self.assertEqual(v.ERRORS, dup[0].severity)
        self.assertIn("first seen on line 2", dup[0].message)

    def test_bad_phone_reported(self):
        findings = v.check_contacts([contact_row(phone="555-1234"), contact_row(person_id="id-2", phone="(255) 123-4567")], ["phone"])
        self.assertEqual({"us_phone_format"}, by_check(f for f in findings if f.severity == v.ERRORS))
        self.assertEqual(2, len([f for f in findings if f.severity == v.ERRORS]))

    def test_empty_phone_cell_ok(self):
        findings = v.check_contacts([contact_row(phone="")], ["phone"])
        self.assertFalse([f for f in findings if f.severity == v.ERRORS])

    def test_unknown_status_warns(self):
        findings = v.check_contacts([contact_row(status="done", email="a@g.gov")], [])
        self.assertEqual({"status_vocabulary"}, by_check(findings))


class RelationshipChecksTests(unittest.TestCase):
    def rel(self, **overrides):
        row = {"from_person_id": "id-1", "to_person_id": "id-2", "relationship_type": "reports_to", "label": "works", "source_url": "https://example.gov/rel", "checked_on": "2026-10-15"}
        row.update(overrides)
        return row

    def test_clean_relationship(self):
        ids = {"id-1", "id-2"}
        self.assertEqual([], [f for f in v.check_relationships([self.rel()], ids) if f.severity == v.ERRORS])

    def test_unknown_endpoint(self):
        findings = [f for f in v.check_relationships([self.rel(to_person_id="ghost")], {"id-1"}) if f.severity == v.ERRORS]
        self.assertEqual(["unknown_person"], [f.check for f in findings])

    def test_bad_type(self):
        findings = [f for f in v.check_relationships([self.rel(relationship_type="friend")], {"id-1", "id-2"}) if f.severity == v.ERRORS]
        self.assertEqual(["relationship_type"], [f.check for f in findings])

    def test_duplicate(self):
        rows = [self.rel(), self.rel()]
        findings = [f for f in v.check_relationships(rows, {"id-1", "id-2"}) if f.severity == v.ERRORS]
        self.assertIn("duplicate_relationship", by_check(findings))


class CoverageChecksTests(unittest.TestCase):
    def test_in_progress_requires_url(self):
        findings = [f for f in v.check_coverage([coverage_row(source_url="")], set()) if f.severity == v.ERRORS]
        self.assertEqual(["source_url"], [f.check for f in findings])

    def test_not_started_url_not_required(self):
        row = coverage_row(status="not_started", source_url="", checked_on="")
        findings = v.check_coverage([row], {("state_territory", "Test State")})
        self.assertEqual([], [f for f in findings if f.severity == v.ERRORS])

    def test_bad_status_is_error(self):
        findings = [f for f in v.check_coverage([coverage_row(status="whatever")], set()) if f.severity == v.ERRORS]
        self.assertEqual(["status_vocabulary"], [f.check for f in findings])

    def test_duplicate_role_row(self):
        findings = [f for f in v.check_coverage([coverage_row(), coverage_row()], set()) if f.severity == v.ERRORS]
        self.assertEqual(["duplicate_role_row"], [f.check for f in findings])

    def test_unknown_jurisdiction_warns(self):
        findings = v.check_coverage([coverage_row()], set())
        self.assertEqual({"unknown_jurisdiction"}, by_check(findings))


class JurisdictionChecksTests(unittest.TestCase):
    def test_clean_list(self):
        findings, known = v.check_jurisdictions(jurisdiction_rows())
        self.assertEqual([], [f for f in findings if f.severity == v.ERRORS])
        self.assertIn(("state_territory", "Test State"), known)

    def test_orphan_municipality(self):
        rows = jurisdiction_rows()
        rows[2]["parent_jurisdiction"] = ""
        findings = [f for f in v.check_jurisdictions(rows)[0] if f.severity == v.ERRORS]
        self.assertEqual(["missing_parent"], [f.check for f in findings])

    def test_duplicate(self):
        rows = jurisdiction_rows() + jurisdiction_rows()[-1:]
        findings = [f for f in v.check_jurisdictions(rows)[0] if f.severity == v.ERRORS]
        self.assertEqual(["duplicate_jurisdiction"], [f.check for f in findings])


class FullValidationTests(unittest.TestCase):
    def test_payload_end_to_end(self):
        state = ("state_territory", "Test State")
        jurisdiction = {"jurisdiction_level": state[0], "jurisdiction_name": state[1], "jurisdiction_type": "state", "parent_jurisdiction": ""}
        payload = {
            "contacts.csv": (list(CONTACT_HEADER), [contact_row()]),
            "relationships.csv": (["from_person_id", "to_person_id", "relationship_type", "label", "source_url", "checked_on"], []),
            "coverage.csv": (list(coverage_row().keys()), [coverage_row(source_url="", status="not_started", checked_on="")]),
            "jurisdictions.csv": (list(jurisdiction.keys()), [jurisdiction]),
        }
        findings = v.validate(payload)
        errors = [f for f in findings if f.severity == v.ERRORS]
        warnings = [f for f in findings if f.severity == v.WARNINGS and f.check != "email_syntax"]
        self.assertEqual([], errors, [f.message for f in errors])
        self.assertEqual([], warnings, [f.message for f in warnings])

    def test_empty_relationships_is_ok(self):
        state = ("state_territory", "Test State")
        jurisdiction = {"jurisdiction_level": state[0], "jurisdiction_name": state[1], "jurisdiction_type": "state", "parent_jurisdiction": ""}
        payload = {
            "contacts.csv": (list(CONTACT_HEADER), [contact_row()]),
            "relationships.csv": (["from_person_id", "to_person_id"], []),
            "coverage.csv": (list(coverage_row().keys()), []),
            "jurisdictions.csv": (list(jurisdiction.keys()), [jurisdiction]),
        }
        findings = v.validate(payload)
        self.assertFalse([f for f in findings if f.severity == v.ERRORS and f.dataset == "relationships.csv"])


class ReportTests(unittest.TestCase):
    def test_report_contains_limitation_section(self):
        state = ("state_territory", "Test State")
        jurisdiction = {"jurisdiction_level": state[0], "jurisdiction_name": state[1], "jurisdiction_type": "state", "parent_jurisdiction": ""}
        payload = {
            "contacts.csv": (list(CONTACT_HEADER), [contact_row()]),
            "relationships.csv": (["from_person_id", "to_person_id"], []),
            "coverage.csv": (list(coverage_row().keys()), []),
            "jurisdictions.csv": (list(jurisdiction.keys()), [jurisdiction]),
        }
        text = v.build_report(payload, v.validate(payload))
        self.assertIn("syntax only", text)
        self.assertIn("does not mean the number is active", text)
        self.assertIn("No network access", text)
        self.assertIn("coverage.csv statuses", text)


if __name__ == "__main__":
    unittest.main()
