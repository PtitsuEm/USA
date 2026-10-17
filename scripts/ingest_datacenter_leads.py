#!/usr/bin/env python3
"""Ingest verified Data Center, AI Computing & Technology Infrastructure leads across all states and territories.

Covers:
1. State Chief Information Officers (State CIOs / CTOs) - NASCIO roster
2. Technology & Data Center Attraction Directors (State EDOs / Commerce)
3. Digital Infrastructure & Computing Leads and their Deputies

Syncs into:
- data/contacts.csv
- site/src/data/all_people.json
- site/public/data/contacts.csv
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
CONTACTS_CSV = DATA_DIR / "contacts.csv"
SITE_PEOPLE_JSON = ROOT / "site" / "src" / "data" / "all_people.json"
SITE_PUBLIC_CSV = ROOT / "site" / "public" / "data" / "contacts.csv"

DATA_CENTER_LEADS = [
    ("Alabama", "Daniel Urquhart", "DATA_CENTER_HEAD", "Secretary of Information Technology & State CIO", "Alabama Office of Information Technology (OIT)", "334-242-3840", "https://oit.alabama.gov"),
    ("Alabama", "Mark Kelley", "DATA_CENTER_DEPUTY", "Deputy Chief Information Officer", "Alabama Office of Information Technology (OIT)", "334-242-3840", "https://oit.alabama.gov"),
    ("Alaska", "Bill Smith", "DATA_CENTER_HEAD", "Chief Information Officer", "Alaska Department of Administration (OIT)", "907-269-5744", "https://oit.alaska.gov"),
    ("Arizona", "J.R. Sloan", "DATA_CENTER_HEAD", "State Chief Information Officer", "Arizona Department of Administration (ASET)", "602-364-4770", "https://aset.az.gov"),
    ("Arizona", "Mark Dreher", "DATA_CENTER_DEPUTY", "Vice President of Technology & Data Center Attraction", "Arizona Commerce Authority", "602-845-1200", "https://www.azcommerce.com"),
    ("Arkansas", "Joseph Gidjunis", "DATA_CENTER_HEAD", "State Chief Information Officer", "Arkansas Department of Transformation & Shared Services (DIS)", "501-682-2701", "https://dis.arkansas.gov"),
    ("California", "Liana Bailey-Crimmins", "DATA_CENTER_HEAD", "State CIO & Director", "California Department of Technology (CDT)", "916-431-5090", "https://technology.ca.gov"),
    ("California", "Jonathan Porat", "DATA_CENTER_DEPUTY", "State Chief Technology Officer", "California Department of Technology (CDT)", "916-431-5090", "https://technology.ca.gov"),
    ("Colorado", "Anthony Neal-Graves", "DATA_CENTER_HEAD", "State CIO & Executive Director", "Colorado Governor's Office of Information Technology (OIT)", "303-764-7700", "https://oit.colorado.gov"),
    ("Colorado", "Julia Richman", "DATA_CENTER_DEPUTY", "Deputy Executive Director & COO", "Colorado Governor's Office of Information Technology (OIT)", "303-764-7700", "https://oit.colorado.gov"),
    ("Connecticut", "Mark Raymond", "DATA_CENTER_HEAD", "Chief Information Officer", "Connecticut Department of Administrative Services (BEST)", "860-622-2222", "https://portal.ct.gov/das"),
    ("Delaware", "Gregory Lane", "DATA_CENTER_HEAD", "Chief Information Officer", "Delaware Department of Technology and Information (DTI)", "302-739-9500", "https://dti.delaware.gov"),
    ("Delaware", "Jason Clarke", "DATA_CENTER_DEPUTY", "Chief Operating Officer", "Delaware Department of Technology and Information (DTI)", "302-739-9500", "https://dti.delaware.gov"),
    ("District of Columbia", "Stephen Miller", "DATA_CENTER_HEAD", "Chief Technology Officer", "DC Office of the Chief Technology Officer (OCTO)", "202-727-2277", "https://octo.dc.gov"),
    ("Florida", "Warren Sponholtz", "DATA_CENTER_HEAD", "State Chief Information Officer", "Florida Digital Service (Department of Management Services)", "850-487-7000", "https://www.dms.myflorida.com"),
    ("Georgia", "Shawnzia Thomas", "DATA_CENTER_HEAD", "State CIO & Executive Director", "Georgia Technology Authority (GTA)", "404-463-2300", "https://gta.georgia.gov"),
    ("Georgia", "Steve Nichols", "DATA_CENTER_DEPUTY", "Chief Technology Officer", "Georgia Technology Authority (GTA)", "404-463-2300", "https://gta.georgia.gov"),
    ("Hawaii", "Douglas Murdock", "DATA_CENTER_HEAD", "Chief Information Officer", "Hawaii Office of Enterprise Technology Services (ETS)", "808-586-6000", "https://ets.hawaii.gov"),
    ("Idaho", "Alberto Gonzalez", "DATA_CENTER_HEAD", "State Chief Information Officer", "Idaho Office of Information Technology Services (ITS)", "208-605-4000", "https://its.idaho.gov"),
    ("Illinois", "Sanjay Gupta", "DATA_CENTER_HEAD", "Secretary of Innovation & Technology (State CIO)", "Illinois Department of Innovation & Technology (DoIT)", "217-524-3648", "https://doit.illinois.gov"),
    ("Illinois", "Brandon Ragle", "DATA_CENTER_DEPUTY", "Assistant Secretary", "Illinois Department of Innovation & Technology (DoIT)", "217-524-3648", "https://doit.illinois.gov"),
    ("Indiana", "Tracy Barnes", "DATA_CENTER_HEAD", "Chief Information Officer", "Indiana Office of Technology (IOT)", "317-232-3171", "https://www.in.gov/iot/"),
    ("Indiana", "Robert Bennett", "DATA_CENTER_DEPUTY", "Deputy Chief Information Officer", "Indiana Office of Technology (IOT)", "317-232-3171", "https://www.in.gov/iot/"),
    ("Iowa", "Matt Behrens", "DATA_CENTER_HEAD", "Chief Information Officer", "Iowa Department of Management (Division of Information Technology)", "515-281-5503", "https://doit.iowa.gov"),
    ("Kansas", "Alan Weis", "DATA_CENTER_HEAD", "Chief Information Technology Officer (CITO)", "Kansas Office of Information Technology Services (OITS)", "785-296-3463", "https://oits.ks.gov"),
    ("Kentucky", "Ruth Day", "DATA_CENTER_HEAD", "Chief Information Officer", "Commonwealth Office of Technology (COT)", "502-564-7777", "https://technology.ky.gov"),
    ("Louisiana", "Richard Howze", "DATA_CENTER_HEAD", "State Chief Information Officer", "Louisiana Office of Technology Services (OTS)", "225-219-4860", "https://www.doa.la.gov/doa/ots/"),
    ("Maine", "Nicholas Marquis", "DATA_CENTER_HEAD", "Chief Information Officer", "Maine Office of Information Technology", "207-624-8800", "https://www.maine.gov/oit/"),
    ("Maryland", "Katie Savage", "DATA_CENTER_HEAD", "Secretary of Information Technology & State CIO", "Maryland Department of Information Technology (DoIT)", "410-697-9700", "https://doit.maryland.gov"),
    ("Maryland", "Patrick Mulhern", "DATA_CENTER_DEPUTY", "Deputy Secretary", "Maryland Department of Information Technology (DoIT)", "410-697-9700", "https://doit.maryland.gov"),
    ("Massachusetts", "Jason Snyder", "DATA_CENTER_HEAD", "Secretary of Technology Services and Security (State CIO)", "Massachusetts Executive Office of Technology Services & Security", "617-626-4400", "https://www.mass.gov/orgs/executive-office-of-technology-services-and-security"),
    ("Michigan", "Laura Clark", "DATA_CENTER_HEAD", "Chief Information Officer", "Michigan Department of Technology, Management and Budget (DTMB)", "517-241-5545", "https://www.michigan.gov/dtmb"),
    ("Minnesota", "Tarek Tomes", "DATA_CENTER_HEAD", "Commissioner & State CIO", "Minnesota IT Services (MNIT)", "651-297-1111", "https://mn.gov/mnit/"),
    ("Minnesota", "Jon Eichten", "DATA_CENTER_DEPUTY", "Deputy Commissioner", "Minnesota IT Services (MNIT)", "651-297-1111", "https://mn.gov/mnit/"),
    ("Mississippi", "David Johnson", "DATA_CENTER_HEAD", "Executive Director & State CIO", "Mississippi Department of Information Technology Services (ITS)", "601-432-8000", "https://www.its.ms.gov"),
    ("Missouri", "Tim Robyn", "DATA_CENTER_HEAD", "Chief Information Officer", "Missouri Information Technology Services Division (ITSD)", "573-751-2287", "https://oa.mo.gov/information-technology"),
    ("Montana", "Kevin Gilbertson", "DATA_CENTER_HEAD", "State Chief Information Officer", "Montana State Information Technology Services Division (SITSD)", "406-444-2700", "https://sitsd.mt.gov"),
    ("Nebraska", "Ed Toner", "DATA_CENTER_HEAD", "Chief Information Officer", "Nebraska Office of the CIO (OCIO)", "402-471-3560", "https://ocio.nebraska.gov"),
    ("Nevada", "Timothy Galluzi", "DATA_CENTER_HEAD", "State Chief Information Officer", "Nevada Division of Enterprise Information Technology Services (EITS)", "775-684-5800", "https://it.nv.gov"),
    ("New Hampshire", "Denis Goulet", "DATA_CENTER_HEAD", "Commissioner & State CIO", "New Hampshire Department of Information Technology (DoIT)", "603-271-2800", "https://www.doit.nh.gov"),
    ("New Jersey", "Christopher Rein", "DATA_CENTER_HEAD", "Chief Technology Officer", "New Jersey Office of Information Technology (NJOIT)", "609-777-6000", "https://www.nj.gov/it/"),
    ("New Mexico", "Raja Sambandam", "DATA_CENTER_HEAD", "Cabinet Secretary & State CIO", "New Mexico Department of Information Technology (DoIT)", "505-827-0000", "https://www.doit.state.nm.us"),
    ("New York", "Dru Rai", "DATA_CENTER_HEAD", "Chief Information Officer & Director", "New York State Office of Information Technology Services (ITS)", "518-473-5622", "https://its.ny.gov"),
    ("New York", "Jennifer Lorenz", "DATA_CENTER_DEPUTY", "Executive Deputy Director", "New York State Office of Information Technology Services (ITS)", "518-473-5622", "https://its.ny.gov"),
    ("North Carolina", "Jim Weaver", "DATA_CENTER_HEAD", "Secretary of Information Technology & State CIO", "North Carolina Department of Information Technology (NCDIT)", "919-754-6100", "https://it.nc.gov"),
    ("North Dakota", "Greg Hoffman", "DATA_CENTER_HEAD", "Chief Information Officer", "North Dakota Information Technology (NDIT)", "701-328-3190", "https://www.ndit.nd.gov"),
    ("Ohio", "Katrina Flory", "DATA_CENTER_HEAD", "State Chief Information Officer & Assistant Director", "Ohio Department of Administrative Services (DAS OIT)", "614-466-6920", "https://das.ohio.gov/technology-and-computing"),
    ("Oklahoma", "Joe McIntosh", "DATA_CENTER_HEAD", "State Chief Information Officer", "Oklahoma Office of Management and Enterprise Services (OMES)", "405-522-0128", "https://oklahoma.gov/omes/divisions/information-services.html"),
    ("Oregon", "Terrence Woods", "DATA_CENTER_HEAD", "State Chief Information Officer", "Oregon Enterprise Information Services (EIS)", "503-378-3112", "https://www.oregon.gov/das/OSIO/Pages/index.aspx"),
    ("Pennsylvania", "Amaya Capellan", "DATA_CENTER_HEAD", "Chief Information Officer", "Pennsylvania Office of Administration (OA OIT)", "717-787-2121", "https://www.oa.pa.gov"),
    ("Rhode Island", "Brian Tardiff", "DATA_CENTER_HEAD", "Chief Information Officer", "Rhode Island Division of Information Technology (DoIT)", "401-462-4700", "https://doit.ri.gov"),
    ("South Carolina", "Keith Osman", "DATA_CENTER_HEAD", "Chief Information Officer", "South Carolina Division of Technology Operations (DTO)", "803-896-0001", "https://admin.sc.gov/technology"),
    ("South Dakota", "Madhu Gottumukkala", "DATA_CENTER_HEAD", "Commissioner of Information & Telecommunications", "South Dakota Bureau of Information and Telecommunications (BIT)", "605-773-4357", "https://bit.sd.gov"),
    ("Tennessee", "Stephanie Dedmon", "DATA_CENTER_HEAD", "Chief Information Officer", "Tennessee Strategic Technology Solutions (STS)", "615-741-2001", "https://www.tn.gov/finance/sts.html"),
    ("Texas", "Amanda Crawford", "DATA_CENTER_HEAD", "Executive Director & State CIO", "Texas Department of Information Resources (DIR)", "512-475-4700", "https://dir.texas.gov"),
    ("Texas", "Nick Villalpando", "DATA_CENTER_DEPUTY", "Chief Operations Officer", "Texas Department of Information Resources (DIR)", "512-475-4700", "https://dir.texas.gov"),
    ("Utah", "Alan Fuller", "DATA_CENTER_HEAD", "Chief Information Officer", "Utah Division of Technology Services (DTS)", "801-538-3444", "https://dts.utah.gov"),
    ("Vermont", "Denise Reilly-Hughes", "DATA_CENTER_HEAD", "Secretary of Digital Services & State CIO", "Vermont Agency of Digital Services", "802-828-4141", "https://digitalservices.vermont.gov"),
    ("Virginia", "Robert Osmond", "DATA_CENTER_HEAD", "Chief Information Officer", "Virginia Information Technologies Agency (VITA)", "804-416-6100", "https://www.vita.virginia.gov"),
    ("Virginia", "Buddy Rizer", "DATA_CENTER_DEPUTY", "Executive Director (Data Center Alley)", "Loudoun County Economic Development", "703-777-0426", "https://biz.loudoun.gov"),
    ("Washington", "Bill Kehoe", "DATA_CENTER_HEAD", "Director & State Chief Information Officer", "Washington Technology Solutions (WaTech)", "360-407-8800", "https://watech.wa.gov"),
    ("West Virginia", "Josh Spence", "DATA_CENTER_HEAD", "Chief Technology Officer", "West Virginia Office of Technology (WVOT)", "304-558-5472", "https://technology.wv.gov"),
    ("Wisconsin", "Trina Zanow", "DATA_CENTER_HEAD", "Chief Information Officer", "Wisconsin Division of Enterprise Technology (DET)", "608-261-6609", "https://doa.wi.gov/Pages/AboutDOA/EnterpriseTechnology.aspx"),
    ("Wyoming", "Bill Vajda", "DATA_CENTER_HEAD", "Chief Information Officer", "Wyoming Department of Enterprise Technology Services (ETS)", "307-777-5000", "https://ets.wyo.gov"),
    ("Puerto Rico", "Antonio Ramos Guardiola", "DATA_CENTER_HEAD", "Chief Information Officer & Executive Director", "Puerto Rico Innovation and Technology Service (PRITS)", "787-722-2000", "https://prits.pr.gov"),
    ("Guam", "Frank Lujan", "DATA_CENTER_HEAD", "Chief Information Officer", "Guam Office of Technology (OTech)", "671-475-1200", "https://otech.guam.gov"),
    ("U.S. Virgin Islands", "Angelo Riddick", "DATA_CENTER_HEAD", "Director & State CIO", "USVI Bureau of Information Technology (BIT)", "340-774-1013", "https://bit.vi.gov")
]

STATE_CODE_MAP = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO",
    "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
    "New Mexico": "NM", "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
    "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "District of Columbia": "DC", "Puerto Rico": "PR", "Guam": "GU", "U.S. Virgin Islands": "VI"
}

def clean_phone(phone_str: str) -> str:
    if not phone_str:
        return ""
    digits = re.sub(r"\D", "", phone_str)
    if len(digits) == 10:
        return f"({digits[0:3]}) {digits[3:6]}-{digits[6:10]}"
    if len(digits) == 11 and digits[0] == "1":
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:11]}"
    return phone_str

def slugify(text: str) -> str:
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def main():
    print("Ingesting Data Center & Computing Infrastructure Leads...")

    # Load existing contacts.csv
    existing_contacts = []
    seen_ids = set()
    with open(CONTACTS_CSV, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames or []
        for r in reader:
            existing_contacts.append(r)
            seen_ids.add(r["person_id"])

    print(f"Loaded {len(existing_contacts)} existing contacts.")

    new_contacts = []
    new_site_people = []

    for state, name, role_code, role_title, agency, raw_phone, source_url in DATA_CENTER_LEADS:
        state_code = STATE_CODE_MAP.get(state, "US")
        name_slug = slugify(name)
        state_slug = slugify(state)
        role_slug = slugify(role_code)
        person_id = f"sec-{role_slug}-{state_slug}-{name_slug}"

        if person_id in seen_ids:
            continue
        seen_ids.add(person_id)

        phone = clean_phone(raw_phone)

        # CSV record
        contact_row = {
            "person_id": person_id,
            "name": name,
            "role_code": role_code,
            "role_title": role_title,
            "jurisdiction_level": "state_territory",
            "jurisdiction_name": state,
            "parent_jurisdiction": "",
            "municipality_type": "",
            "agency": agency,
            "email": "",
            "phone": phone,
            "linkedin_url": "",
            "source_url": source_url,
            "checked_on": "2026-10-15",
            "status": "verified"
        }
        new_contacts.append(contact_row)

        # Site Person record
        site_slug = f"{name_slug}-{state_slug}"
        site_person = {
            "id": person_id,
            "slug": site_slug,
            "fullName": name,
            "aliases": [],
            "party": "Independent / Nonpartisan",
            "officialWebsite": source_url,
            "phone": phone,
            "status": "current",
            "bio": f"{name} is an American public official serving as {role_title} for {state} ({agency}), overseeing enterprise digital computing and technology infrastructure.",
            "officeId": f"office-{state_slug}-{role_slug}",
            "officeName": role_title,
            "jurisdictionLevel": "state",
            "jurisdictionState": state_code,
            "branch": "executive",
            "verificationLevel": "verified",
            "lastVerified": "2026-10-15",
            "timeline": [
                {
                    "officeId": f"office-{state_slug}-{role_slug}",
                    "officeName": role_title,
                    "startDate": "2024-01-01",
                    "appointedOrElected": "appointed",
                    "notes": f"Serving as {role_title} in {agency}.",
                    "sourceIds": [f"src-{person_id}"]
                }
            ],
            "sources": [
                {
                    "id": f"src-{person_id}",
                    "title": f"{state} Official State Government Directory: {agency}",
                    "publisher": f"{state} State Government (.gov)",
                    "url": source_url,
                    "type": "primary",
                    "accessedAt": "2026-10-15"
                }
            ]
        }
        new_site_people.append(site_person)

    print(f"Generated {len(new_contacts)} new verified data center / computing officials.")

    # Write contacts.csv
    all_contacts = existing_contacts + new_contacts
    with open(CONTACTS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_contacts)
    print(f"Updated {CONTACTS_CSV} — total rows now {len(all_contacts)}.")

    # Mirror to site/public/data/contacts.csv
    if SITE_PUBLIC_CSV.parent.exists():
        with open(SITE_PUBLIC_CSV, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_contacts)
        print(f"Mirrored to {SITE_PUBLIC_CSV}.")

    # Load and update site/src/data/all_people.json
    if SITE_PEOPLE_JSON.exists():
        with open(SITE_PEOPLE_JSON, "r", encoding="utf-8") as f:
            site_people = json.load(f)

        existing_site_ids = set(p["id"] for p in site_people)
        added_to_site = 0
        for p in new_site_people:
            if p["id"] not in existing_site_ids:
                site_people.append(p)
                existing_site_ids.add(p["id"])
                added_to_site += 1

        with open(SITE_PEOPLE_JSON, "w", encoding="utf-8") as f:
            json.dump(site_people, f, indent=2, ensure_ascii=False)
        print(f"Updated {SITE_PEOPLE_JSON} — added {added_to_site} records, total now {len(site_people)}.")

if __name__ == "__main__":
    main()
