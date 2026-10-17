#!/usr/bin/env python3
"""Initialize or rebuild the SQLite database from CSV datasets."""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
DB_PATH = DATA / "officials.db"


def read_csv(filename: str) -> list[dict[str, str]]:
    path = DATA / filename
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def init_db() -> None:
    print(f"Creating SQLite database at: {DB_PATH}")
    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Contacts table
    cur.execute("""
    CREATE TABLE contacts (
        person_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        role_code TEXT NOT NULL,
        role_title TEXT NOT NULL,
        jurisdiction_level TEXT NOT NULL,
        jurisdiction_name TEXT NOT NULL,
        parent_jurisdiction TEXT,
        municipality_type TEXT,
        agency TEXT,
        email TEXT,
        phone TEXT,
        linkedin_url TEXT,
        source_url TEXT NOT NULL,
        checked_on TEXT NOT NULL,
        status TEXT NOT NULL
    );
    """)

    contacts = read_csv("contacts.csv")
    cur.executemany("""
    INSERT INTO contacts (
        person_id, name, role_code, role_title, jurisdiction_level,
        jurisdiction_name, parent_jurisdiction, municipality_type, agency,
        email, phone, linkedin_url, source_url, checked_on, status
    ) VALUES (
        :person_id, :name, :role_code, :role_title, :jurisdiction_level,
        :jurisdiction_name, :parent_jurisdiction, :municipality_type, :agency,
        :email, :phone, :linkedin_url, :source_url, :checked_on, :status
    );
    """, contacts)

    # 2. Jurisdictions table
    cur.execute("""
    CREATE TABLE jurisdictions (
        jurisdiction_level TEXT NOT NULL,
        jurisdiction_name TEXT NOT NULL,
        jurisdiction_type TEXT,
        parent_jurisdiction TEXT
    );
    """)

    jurisdictions = read_csv("jurisdictions.csv")
    cur.executemany("""
    INSERT INTO jurisdictions (
        jurisdiction_level, jurisdiction_name, jurisdiction_type, parent_jurisdiction
    ) VALUES (
        :jurisdiction_level, :jurisdiction_name, :jurisdiction_type, :parent_jurisdiction
    );
    """, jurisdictions)

    # 3. Coverage table
    cur.execute("""
    CREATE TABLE coverage (
        jurisdiction_level TEXT NOT NULL,
        jurisdiction_name TEXT NOT NULL,
        parent_jurisdiction TEXT,
        municipality_type TEXT,
        role_code TEXT NOT NULL,
        role_title TEXT NOT NULL,
        status TEXT NOT NULL,
        source_url TEXT,
        checked_on TEXT,
        notes TEXT
    );
    """)

    coverage = read_csv("coverage.csv")
    cur.executemany("""
    INSERT INTO coverage (
        jurisdiction_level, jurisdiction_name, parent_jurisdiction, municipality_type,
        role_code, role_title, status, source_url, checked_on, notes
    ) VALUES (
        :jurisdiction_level, :jurisdiction_name, :parent_jurisdiction, :municipality_type,
        :role_code, :role_title, :status, :source_url, :checked_on, :notes
    );
    """, coverage)

    # 4. Relationships table
    cur.execute("""
    CREATE TABLE relationships (
        from_person_id TEXT NOT NULL,
        to_person_id TEXT NOT NULL,
        relationship_type TEXT NOT NULL,
        label TEXT,
        source_url TEXT NOT NULL,
        checked_on TEXT NOT NULL,
        FOREIGN KEY (from_person_id) REFERENCES contacts(person_id),
        FOREIGN KEY (to_person_id) REFERENCES contacts(person_id)
    );
    """)

    relationships = read_csv("relationships.csv")
    cur.executemany("""
    INSERT INTO relationships (
        from_person_id, to_person_id, relationship_type, label, source_url, checked_on
    ) VALUES (
        :from_person_id, :to_person_id, :relationship_type, :label, :source_url, :checked_on
    );
    """, relationships)

    # Create indexes for fast queries
    cur.execute("CREATE INDEX idx_contacts_name ON contacts(name);")
    cur.execute("CREATE INDEX idx_contacts_role ON contacts(role_code);")
    cur.execute("CREATE INDEX idx_contacts_level ON contacts(jurisdiction_level);")
    cur.execute("CREATE INDEX idx_contacts_state ON contacts(parent_jurisdiction);")
    cur.execute("CREATE INDEX idx_contacts_jurisdiction ON contacts(jurisdiction_name);")
    cur.execute("CREATE INDEX idx_contacts_status ON contacts(status);")
    cur.execute("CREATE INDEX idx_coverage_jurisdiction ON coverage(jurisdiction_name);")
    cur.execute("CREATE INDEX idx_coverage_role ON coverage(role_code);")
    cur.execute("CREATE INDEX idx_relationships_from ON relationships(from_person_id);")
    cur.execute("CREATE INDEX idx_relationships_to ON relationships(to_person_id);")

    conn.commit()
    conn.close()

    print(f"Successfully generated {DB_PATH}:")
    print(f"  - contacts: {len(contacts)} rows")
    print(f"  - jurisdictions: {len(jurisdictions)} rows")
    print(f"  - coverage: {len(coverage)} rows")
    print(f"  - relationships: {len(relationships)} rows")


if __name__ == "__main__":
    init_db()
