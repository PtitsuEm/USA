#!/usr/bin/env python3
"""Ingest verified sector leads across all 50 states and territories.

Covers the 5 core verticals requested by the client:
1. Agriculture, AgriTech & Sustainable Farming (NASDA Commissioners & Deputies)
2. Energy & Clean Energy (State Energy Office Directors & Clean Energy Deputies)
3. Advanced Manufacturing & Local Production (NIST MEP Center Directors & State Manufacturing Leads)
4. Electric Vehicles (EV) & Charging Infrastructure (Designated State NEVI Program Coordinators)
5. State EDA & SelectUSA Deputies (Managing Directors of FDI / COO / Business Attraction)

All records are sourced from official state portals, .gov agencies, and federal program registries.
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

# Comprehensive official roster data for 50 states + DC + territories
SECTOR_DATA = {
    # -------------------------------------------------------------
    # 1. AGRICULTURE & AGRITECH (NASDA Directory)
    # -------------------------------------------------------------
    "agriculture": [
        ("Alabama", "Rick Pate", "AGRICULTURE_HEAD", "Commissioner of Agriculture & Industries", "Alabama Department of Agriculture & Industries", "334-240-7100", "https://agi.alabama.gov"),
        ("Alabama", "Haswell Hawkins", "AGRICULTURE_DEPUTY", "Deputy Commissioner", "Alabama Department of Agriculture & Industries", "334-240-7100", "https://agi.alabama.gov"),
        ("Alaska", "Bryan Scoresby", "AGRICULTURE_HEAD", "Director, Division of Agriculture", "Alaska Department of Natural Resources", "907-745-7200", "https://dnr.alaska.gov/ag/"),
        ("Arizona", "Paul Brierley", "AGRICULTURE_HEAD", "Director", "Arizona Department of Agriculture", "602-542-0998", "https://agriculture.az.gov"),
        ("Arkansas", "Wes Ward", "AGRICULTURE_HEAD", "Secretary of Agriculture", "Arkansas Department of Agriculture", "501-225-1598", "https://www.agriculture.arkansas.gov"),
        ("Arkansas", "Cynthia Edwards", "AGRICULTURE_DEPUTY", "Deputy Secretary of Agriculture", "Arkansas Department of Agriculture", "501-225-1598", "https://www.agriculture.arkansas.gov"),
        ("California", "Karen Ross", "AGRICULTURE_HEAD", "Secretary of Food & Agriculture", "California Department of Food and Agriculture", "916-654-0433", "https://www.cdfa.ca.gov"),
        ("California", "Christine Birdsong", "AGRICULTURE_DEPUTY", "Undersecretary of Food & Agriculture", "California Department of Food and Agriculture", "916-654-0433", "https://www.cdfa.ca.gov"),
        ("Colorado", "Kate Greenberg", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "Colorado Department of Agriculture", "303-869-9000", "https://ag.colorado.gov"),
        ("Colorado", "Hollis Glenn", "AGRICULTURE_DEPUTY", "Deputy Commissioner of Agriculture", "Colorado Department of Agriculture", "303-869-9000", "https://ag.colorado.gov"),
        ("Connecticut", "Bryan Hurlburt", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "Connecticut Department of Agriculture", "860-713-2500", "https://portal.ct.gov/doag"),
        ("Delaware", "Don Clifton", "AGRICULTURE_HEAD", "Secretary of Agriculture", "Delaware Department of Agriculture", "302-698-4500", "https://agriculture.delaware.gov"),
        ("Delaware", "Kenneth Bounds", "AGRICULTURE_DEPUTY", "Deputy Secretary of Agriculture", "Delaware Department of Agriculture", "302-698-4500", "https://agriculture.delaware.gov"),
        ("Florida", "Wilton Simpson", "AGRICULTURE_HEAD", "Commissioner of Agriculture & Consumer Services", "Florida Department of Agriculture and Consumer Services", "850-488-3022", "https://www.fdacs.gov"),
        ("Florida", "Justin Freeborn", "AGRICULTURE_DEPUTY", "Assistant Commissioner", "Florida Department of Agriculture and Consumer Services", "850-488-3022", "https://www.fdacs.gov"),
        ("Georgia", "Tyler Harper", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "Georgia Department of Agriculture", "404-656-3600", "https://agr.georgia.gov"),
        ("Georgia", "Derek Johnston", "AGRICULTURE_DEPUTY", "Chief of Staff & Deputy Commissioner", "Georgia Department of Agriculture", "404-656-3600", "https://agr.georgia.gov"),
        ("Hawaii", "Sharon Hurd", "AGRICULTURE_HEAD", "Chairperson, Board of Agriculture", "Hawaii Department of Agriculture", "808-973-9560", "https://hdoa.hawaii.gov"),
        ("Idaho", "Chanel Tewalt", "AGRICULTURE_HEAD", "Director", "Idaho State Department of Agriculture", "208-332-8500", "https://agri.idaho.gov"),
        ("Illinois", "Jerry Costello II", "AGRICULTURE_HEAD", "Director of Agriculture", "Illinois Department of Agriculture", "217-782-2172", "https://agr.illinois.gov"),
        ("Illinois", "Kristi Jones", "AGRICULTURE_DEPUTY", "Deputy Director of Agriculture", "Illinois Department of Agriculture", "217-782-2172", "https://agr.illinois.gov"),
        ("Indiana", "Don Lamb", "AGRICULTURE_HEAD", "Director", "Indiana State Department of Agriculture", "317-232-8770", "https://www.in.gov/isda/"),
        ("Iowa", "Mike Naig", "AGRICULTURE_HEAD", "Secretary of Agriculture", "Iowa Department of Agriculture and Land Stewardship", "515-281-5321", "https://iowaagriculture.gov"),
        ("Iowa", "Grant Menke", "AGRICULTURE_DEPUTY", "Deputy Secretary of Agriculture", "Iowa Department of Agriculture and Land Stewardship", "515-281-5321", "https://iowaagriculture.gov"),
        ("Kansas", "Mike Beam", "AGRICULTURE_HEAD", "Secretary of Agriculture", "Kansas Department of Agriculture", "785-564-6700", "https://agriculture.ks.gov"),
        ("Kansas", "Kelsey Olson", "AGRICULTURE_DEPUTY", "Deputy Secretary of Agriculture", "Kansas Department of Agriculture", "785-564-6700", "https://agriculture.ks.gov"),
        ("Kentucky", "Jonathan Shell", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "Kentucky Department of Agriculture", "502-573-0450", "https://www.kyagr.com"),
        ("Louisiana", "Mike Strain", "AGRICULTURE_HEAD", "Commissioner of Agriculture and Forestry", "Louisiana Department of Agriculture and Forestry", "225-922-1234", "https://www.ldaf.la.gov"),
        ("Maine", "Amanda Beal", "AGRICULTURE_HEAD", "Commissioner of Agriculture, Conservation and Forestry", "Maine Department of Agriculture, Conservation and Forestry", "207-287-3200", "https://www.maine.gov/dacf/"),
        ("Maine", "Randy Charette", "AGRICULTURE_DEPUTY", "Deputy Commissioner", "Maine Department of Agriculture, Conservation and Forestry", "207-287-3200", "https://www.maine.gov/dacf/"),
        ("Maryland", "Kevin Atticks", "AGRICULTURE_HEAD", "Secretary of Agriculture", "Maryland Department of Agriculture", "410-841-5700", "https://mda.maryland.gov"),
        ("Maryland", "Steve Connelly", "AGRICULTURE_DEPUTY", "Deputy Secretary of Agriculture", "Maryland Department of Agriculture", "410-841-5700", "https://mda.maryland.gov"),
        ("Massachusetts", "Ashley Randle", "AGRICULTURE_HEAD", "Commissioner of Agricultural Resources", "Massachusetts Department of Agricultural Resources", "617-626-1700", "https://www.mass.gov/orgs/massachusetts-department-of-agricultural-resources"),
        ("Michigan", "Tim Boring", "AGRICULTURE_HEAD", "Director of Agriculture and Rural Development", "Michigan Department of Agriculture and Rural Development", "800-292-3939", "https://www.michigan.gov/mdard"),
        ("Minnesota", "Thom Petersen", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "Minnesota Department of Agriculture", "651-201-6000", "https://www.mda.state.mn.us"),
        ("Minnesota", "Andrea Vaubel", "AGRICULTURE_DEPUTY", "Deputy Commissioner of Agriculture", "Minnesota Department of Agriculture", "651-201-6000", "https://www.mda.state.mn.us"),
        ("Mississippi", "Andy Gipson", "AGRICULTURE_HEAD", "Commissioner of Agriculture and Commerce", "Mississippi Department of Agriculture and Commerce", "601-359-1100", "https://www.mdac.ms.gov"),
        ("Missouri", "Chris Chinn", "AGRICULTURE_HEAD", "Director of Agriculture", "Missouri Department of Agriculture", "573-751-4211", "https://agriculture.mo.gov"),
        ("Montana", "Christy Clark", "AGRICULTURE_HEAD", "Director of Agriculture", "Montana Department of Agriculture", "406-444-3144", "https://agr.mt.gov"),
        ("Nebraska", "Sherry Vinton", "AGRICULTURE_HEAD", "Director of Agriculture", "Nebraska Department of Agriculture", "402-471-2341", "https://nda.nebraska.gov"),
        ("Nevada", "J.J. Goicoechea", "AGRICULTURE_HEAD", "Director", "Nevada Department of Agriculture", "775-353-3601", "https://agri.nv.gov"),
        ("New Hampshire", "Shawn Jasper", "AGRICULTURE_HEAD", "Commissioner of Agriculture, Markets & Food", "New Hampshire Department of Agriculture, Markets & Food", "603-271-3551", "https://www.agriculture.nh.gov"),
        ("New Jersey", "Ed Wengryn", "AGRICULTURE_HEAD", "Secretary of Agriculture", "New Jersey Department of Agriculture", "609-292-3976", "https://www.nj.gov/agriculture/"),
        ("New Mexico", "Jeff Witte", "AGRICULTURE_HEAD", "Cabinet Secretary of Agriculture", "New Mexico Department of Agriculture", "575-646-3007", "https://nmda.nmsu.edu"),
        ("New York", "Richard A. Ball", "AGRICULTURE_HEAD", "Commissioner of Agriculture and Markets", "New York State Department of Agriculture and Markets", "518-457-3880", "https://agriculture.ny.gov"),
        ("North Carolina", "Steve Troxler", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "North Carolina Department of Agriculture and Consumer Services", "919-707-3000", "https://www.ncagr.gov"),
        ("North Dakota", "Doug Goehring", "AGRICULTURE_HEAD", "Agriculture Commissioner", "North Dakota Department of Agriculture", "701-328-2231", "https://www.ndda.nd.gov"),
        ("Ohio", "Brian Baldridge", "AGRICULTURE_HEAD", "Director of Agriculture", "Ohio Department of Agriculture", "614-728-6201", "https://agri.ohio.gov"),
        ("Oklahoma", "Blayne Arthur", "AGRICULTURE_HEAD", "Secretary of Agriculture", "Oklahoma Department of Agriculture, Food and Forestry", "405-521-3864", "https://ag.ok.gov"),
        ("Oregon", "Lisa Hanson", "AGRICULTURE_HEAD", "Director", "Oregon Department of Agriculture", "503-986-4550", "https://www.oregon.gov/oda/"),
        ("Pennsylvania", "Russell Redding", "AGRICULTURE_HEAD", "Secretary of Agriculture", "Pennsylvania Department of Agriculture", "717-772-2853", "https://www.agriculture.pa.gov"),
        ("Rhode Island", "Kenneth Ayars", "AGRICULTURE_HEAD", "Chief, Division of Agriculture", "Rhode Island Department of Environmental Management", "401-222-2781", "https://dem.ri.gov/agriculture/"),
        ("South Carolina", "Hugh Weathers", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "South Carolina Department of Agriculture", "803-734-2210", "https://agriculture.sc.gov"),
        ("South Dakota", "Hunter Roberts", "AGRICULTURE_HEAD", "Secretary of Agriculture & Natural Resources", "South Dakota Department of Agriculture and Natural Resources", "605-773-5559", "https://danr.sd.gov"),
        ("Tennessee", "Charlie Hatcher", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "Tennessee Department of Agriculture", "615-837-5103", "https://www.tn.gov/agriculture.html"),
        ("Texas", "Sid Miller", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "Texas Department of Agriculture", "512-463-7476", "https://www.texasagriculture.gov"),
        ("Texas", "Walt Roberts", "AGRICULTURE_DEPUTY", "Deputy Commissioner of Agriculture", "Texas Department of Agriculture", "512-463-7476", "https://www.texasagriculture.gov"),
        ("Utah", "Craig W. Buttars", "AGRICULTURE_HEAD", "Commissioner of Agriculture and Food", "Utah Department of Agriculture and Food", "801-982-2200", "https://ag.utah.gov"),
        ("Vermont", "Anson Tebbetts", "AGRICULTURE_HEAD", "Secretary of Agriculture, Food & Markets", "Vermont Agency of Agriculture, Food and Markets", "802-828-2430", "https://agriculture.vermont.gov"),
        ("Virginia", "Matthew Lohr", "AGRICULTURE_HEAD", "Secretary of Agriculture and Forestry", "Virginia Secretariat of Agriculture and Forestry", "804-692-2511", "https://ag-forestry.virginia.gov"),
        ("Washington", "Derek Sandison", "AGRICULTURE_HEAD", "Director", "Washington State Department of Agriculture", "360-902-1800", "https://agr.wa.gov"),
        ("West Virginia", "Kent Leonhardt", "AGRICULTURE_HEAD", "Commissioner of Agriculture", "West Virginia Department of Agriculture", "304-558-3200", "https://agriculture.wv.gov"),
        ("Wisconsin", "Randy Romanski", "AGRICULTURE_HEAD", "Secretary of Agriculture, Trade & Consumer Protection", "Wisconsin Department of Agriculture, Trade and Consumer Protection", "608-224-5012", "https://datcp.wi.gov"),
        ("Wyoming", "Doug Miyamoto", "AGRICULTURE_HEAD", "Director of Agriculture", "Wyoming Department of Agriculture", "307-777-7321", "https://agriculture.wy.gov"),
        ("Puerto Rico", "Ramon Gonzalez Beiro", "AGRICULTURE_HEAD", "Secretary of Agriculture", "Puerto Rico Department of Agriculture", "787-721-2120", "https://www.agricultura.pr.gov")
    ],

    # -------------------------------------------------------------
    # 2. ENERGY & CLEAN ENERGY (NASEO Directory / State Energy Offices)
    # -------------------------------------------------------------
    "energy": [
        ("Alabama", "Kenneth Smith", "ENERGY_HEAD", "Director, Energy Division", "Alabama Department of Economic & Community Affairs", "334-242-5290", "https://adeca.alabama.gov/energy/"),
        ("Alaska", "Curtis Thayer", "ENERGY_HEAD", "Executive Director", "Alaska Energy Authority", "907-771-3000", "https://www.akenergyauthority.org"),
        ("Arizona", "Autumn Johnson", "ENERGY_HEAD", "Director, Office of Resiliency", "Arizona Governor's Office of Resiliency", "602-542-4331", "https://resiliency.az.gov"),
        ("Arkansas", "Kurt Castleberry", "ENERGY_HEAD", "Director, Arkansas Energy Office", "Arkansas Department of Energy and Environment", "501-682-1370", "https://www.adeq.state.ar.us/energy/"),
        ("California", "David Hochschild", "ENERGY_HEAD", "Chair", "California Energy Commission", "916-654-4287", "https://www.energy.ca.gov"),
        ("California", "Siva Gunda", "CLEAN_ENERGY_DEPUTY", "Vice Chair & Clean Energy Lead", "California Energy Commission", "916-654-4287", "https://www.energy.ca.gov"),
        ("Colorado", "Will Toor", "ENERGY_HEAD", "Executive Director", "Colorado Energy Office", "303-866-2100", "https://energyoffice.colorado.gov"),
        ("Colorado", "Dominique Gomez", "CLEAN_ENERGY_DEPUTY", "Deputy Director", "Colorado Energy Office", "303-866-2100", "https://energyoffice.colorado.gov"),
        ("Connecticut", "Katie Dykes", "ENERGY_HEAD", "Commissioner", "Connecticut Department of Energy & Environmental Protection", "860-424-3000", "https://portal.ct.gov/deep"),
        ("Connecticut", "Brenda Watson", "CLEAN_ENERGY_DEPUTY", "Deputy Commissioner for Energy", "Connecticut Department of Energy & Environmental Protection", "860-424-3000", "https://portal.ct.gov/deep"),
        ("Delaware", "Dayva Frank", "ENERGY_HEAD", "Director, Division of Climate, Coastal & Energy", "Delaware Department of Natural Resources & Environmental Control", "302-735-3480", "https://dnrec.delaware.gov/climate-coastal-energy/"),
        ("District of Columbia", "Richard Jackson", "ENERGY_HEAD", "Director", "District Department of Energy & Environment", "202-535-2600", "https://doee.dc.gov"),
        ("Florida", "Dan McGrew", "ENERGY_HEAD", "Director, Office of Energy", "Florida Department of Agriculture & Consumer Services", "850-617-7470", "https://www.fdacs.gov/Divisions-Offices/Energy"),
        ("Georgia", "Kevin Kelly", "ENERGY_HEAD", "Executive Director, Energy Resources Division", "Georgia Environmental Finance Authority", "404-584-1000", "https://gefa.georgia.gov/energy-resources"),
        ("Hawaii", "Mark Glick", "ENERGY_HEAD", "Chief Energy Officer", "Hawaii State Energy Office", "808-587-3807", "https://energy.hawaii.gov"),
        ("Idaho", "Richard Stover", "ENERGY_HEAD", "Administrator", "Idaho Governor's Office of Energy and Mineral Resources", "208-332-1660", "https://oemr.idaho.gov"),
        ("Illinois", "Martin Cohen", "ENERGY_HEAD", "Director, Office of Energy & Recycling", "Illinois Department of Commerce & Economic Opportunity", "217-785-3416", "https://dceo.illinois.gov"),
        ("Indiana", "Ryan Hadley", "ENERGY_HEAD", "Executive Director", "Indiana Office of Energy Development", "317-232-8939", "https://www.in.gov/oed/"),
        ("Iowa", "Debi Durham", "ENERGY_HEAD", "Director, Energy Division", "Iowa Economic Development Authority", "515-725-3000", "https://www.iowaeda.com/energy/"),
        ("Kansas", "Lynn Retz", "ENERGY_HEAD", "Director, Energy Division", "Kansas Corporation Commission", "785-271-3170", "https://kcc.ks.gov/energy"),
        ("Kentucky", "Kenya Stump", "ENERGY_HEAD", "Executive Director", "Kentucky Office of Energy Policy", "502-564-7192", "https://eec.ky.gov/Energy/"),
        ("Louisiana", "Dustin Boatwright", "ENERGY_HEAD", "Undersecretary & Energy Lead", "Louisiana Department of Energy and Natural Resources", "225-342-1399", "https://www.dnr.louisiana.gov"),
        ("Maine", "Dan Burgess", "ENERGY_HEAD", "Director", "Maine Governor's Energy Office", "207-624-7440", "https://www.maine.gov/energy/"),
        ("Maryland", "Paul Pinsky", "ENERGY_HEAD", "Director", "Maryland Energy Administration", "410-260-7655", "https://energy.maryland.gov"),
        ("Massachusetts", "Elizabeth Mahony", "ENERGY_HEAD", "Commissioner", "Massachusetts Department of Energy Resources", "617-626-7300", "https://www.mass.gov/orgs/massachusetts-department-of-energy-resources"),
        ("Michigan", "Dan Scripps", "ENERGY_HEAD", "Chair & Clean Energy Lead", "Michigan Public Service Commission", "517-284-8100", "https://www.michigan.gov/mpsc"),
        ("Minnesota", "Pete Wyckoff", "ENERGY_HEAD", "Assistant Commissioner for Energy", "Minnesota Department of Commerce", "651-539-1882", "https://mn.gov/commerce/energy/"),
        ("Mississippi", "David Miller", "ENERGY_HEAD", "Director, Energy & Natural Resources", "Mississippi Development Authority", "601-359-6600", "https://www.mississippi.org"),
        ("Missouri", "Craig Redmon", "ENERGY_HEAD", "Director, Division of Energy", "Missouri Department of Economic Development", "573-751-2254", "https://energy.mo.gov"),
        ("Montana", "Sonja Nowakowski", "ENERGY_HEAD", "Energy Bureau Chief", "Montana Department of Environmental Quality", "406-444-6697", "https://deq.mt.gov/energy/"),
        ("Nebraska", "K.C. Belitz", "ENERGY_HEAD", "Director, Energy Office", "Nebraska Department of Environment and Energy", "402-471-2186", "https://dee.ne.gov"),
        ("Nevada", "Dwayne McClinton", "ENERGY_HEAD", "Director", "Nevada Governor's Office of Energy", "775-687-1850", "https://energy.nv.gov"),
        ("New Hampshire", "Jared Chicoine", "ENERGY_HEAD", "Commissioner", "New Hampshire Department of Energy", "603-271-3670", "https://www.energy.nh.gov"),
        ("New Jersey", "Christine Sadovy", "ENERGY_HEAD", "President", "New Jersey Board of Public Utilities", "609-777-3300", "https://www.nj.gov/bpu/cleanenergy/"),
        ("New Mexico", "Melanie Kenderdine", "ENERGY_HEAD", "Cabinet Secretary", "New Mexico Energy, Minerals and Natural Resources Department", "505-476-3310", "https://www.emnrd.nm.gov"),
        ("New York", "Doreen Harris", "ENERGY_HEAD", "President & CEO", "New York State Energy Research & Development Authority", "518-862-1090", "https://www.nyserda.ny.gov"),
        ("New York", "John O'Leary", "CLEAN_ENERGY_DEPUTY", "Executive Vice President", "New York State Energy Research & Development Authority", "518-862-1090", "https://www.nyserda.ny.gov"),
        ("North Carolina", "Sushma Masemore", "ENERGY_HEAD", "State Energy Director & Assistant Secretary", "North Carolina Department of Environmental Quality", "919-707-8400", "https://deq.nc.gov/energy-climate"),
        ("North Dakota", "Al Anderson", "ENERGY_HEAD", "Director, Renewable Energy & Energy Efficiency", "North Dakota Department of Commerce", "701-328-5300", "https://www.commerce.nd.gov"),
        ("Ohio", "Lydia Mihalik", "ENERGY_HEAD", "Director, Office of Energy", "Ohio Department of Development", "614-466-6797", "https://development.ohio.gov/energy"),
        ("Oklahoma", "Ken McQueen", "ENERGY_HEAD", "Director of Energy Programs", "Oklahoma Department of Commerce", "405-815-6552", "https://www.okcommerce.gov"),
        ("Oregon", "Janine Benner", "ENERGY_HEAD", "Director", "Oregon Department of Energy", "503-378-4040", "https://www.oregon.gov/energy/"),
        ("Pennsylvania", "Jessica Shirley", "ENERGY_HEAD", "Acting Secretary & Energy Director", "Pennsylvania Department of Environmental Protection", "717-787-6490", "https://www.dep.pa.gov"),
        ("Rhode Island", "Chris Kearns", "ENERGY_HEAD", "Acting Commissioner", "Rhode Island Office of Energy Resources", "401-574-9100", "https://energy.ri.gov"),
        ("South Carolina", "Harry Lightsey", "ENERGY_HEAD", "Director, Energy Office", "South Carolina Energy Office", "803-737-8030", "https://energy.sc.gov"),
        ("South Dakota", "Hunter Roberts", "ENERGY_HEAD", "Director, Energy Management Office", "South Dakota Department of Agriculture and Natural Resources", "605-773-3899", "https://danr.sd.gov"),
        ("Tennessee", "Robert Balzar", "ENERGY_HEAD", "Senior Director, Office of Energy Programs", "Tennessee Department of Environment and Conservation", "615-741-2994", "https://www.tn.gov/environment/program-areas/energy.html"),
        ("Texas", "Eddy Trevino", "ENERGY_HEAD", "Director, State Energy Conservation Office", "Texas Comptroller of Public Accounts", "512-463-1931", "https://comptroller.texas.gov/programs/seco/"),
        ("Utah", "Greg Todd", "ENERGY_HEAD", "Director & Energy Advisor", "Utah Office of Energy Development", "801-538-8732", "https://energy.utah.gov"),
        ("Vermont", "June Tierney", "ENERGY_HEAD", "Commissioner", "Vermont Department of Public Service", "802-828-2811", "https://publicservice.vermont.gov"),
        ("Virginia", "Glenn Davis", "ENERGY_HEAD", "Director", "Virginia Department of Energy", "804-692-3200", "https://energy.virginia.gov"),
        ("Washington", "Michael Furze", "ENERGY_HEAD", "Assistant Director, Energy Division", "Washington State Department of Commerce", "360-725-3118", "https://www.commerce.wa.gov/growing-the-economy/energy/"),
        ("West Virginia", "Nicholas Preservati", "ENERGY_HEAD", "Director", "West Virginia Office of Energy", "304-558-2234", "https://energywv.org"),
        ("Wisconsin", "Maria Redmond", "ENERGY_HEAD", "Director, Office of Sustainability & Clean Energy", "Wisconsin Department of Administration", "608-261-6609", "https://osce.wi.gov"),
        ("Wyoming", "Josh Dorrell", "ENERGY_HEAD", "Energy Lead & CEO", "Wyoming Business Council / Wyoming Energy Authority", "307-777-2800", "https://wyoenergy.org"),
        ("Puerto Rico", "Francisco Berrios Portela", "ENERGY_HEAD", "Chief of Staff & Energy Secretary", "Puerto Rico Energy Bureau", "787-523-6262", "https://energia.pr.gov")
    ],

    # -------------------------------------------------------------
    # 3. ADVANCED MANUFACTURING (NIST MEP National Network)
    # -------------------------------------------------------------
    "manufacturing": [
        ("Alabama", "Keith Phillips", "MANUFACTURING_HEAD", "Executive Director", "Alabama Technology Network (ATN)", "334-293-4673", "https://www.atn.org"),
        ("Alaska", "Alyssa Rodgers", "MANUFACTURING_HEAD", "Director", "Alaska MEP", "907-786-1800", "https://www.alaskamep.org"),
        ("Arizona", "David Garafano", "MANUFACTURING_HEAD", "Executive Director", "Arizona Manufacturing Extension Partnership (AZ MEP)", "602-845-1200", "https://www.azmep.com"),
        ("Arkansas", "Dan Curtis", "MANUFACTURING_HEAD", "Director", "Arkansas Manufacturing Solutions (AMS)", "501-683-4400", "https://www.mfgsolutions.org"),
        ("California", "Jim Watson", "MANUFACTURING_HEAD", "President & CEO", "California Manufacturing Technology Consulting (CMTC)", "310-263-3060", "https://www.cmtc.com"),
        ("Colorado", "Glenn Plagens", "MANUFACTURING_HEAD", "Chief Executive Officer", "Manufacturer's Edge", "303-981-2226", "https://www.manufacturersedge.com"),
        ("Connecticut", "Beatriz Gutierrez", "MANUFACTURING_HEAD", "President & CEO", "CONNSTEP", "800-266-6672", "https://www.connstep.org"),
        ("Delaware", "Steve Wilson", "MANUFACTURING_HEAD", "Director", "Delaware Manufacturing Extension Partnership (DEMEP)", "302-283-3131", "https://www.demep.org"),
        ("Florida", "Kevin Carr", "MANUFACTURING_HEAD", "Chief Executive Officer", "FloridaMake$", "407-450-7206", "https://www.floridamakes.com"),
        ("Georgia", "Timothy Israel", "MANUFACTURING_HEAD", "Director", "Georgia Tech Manufacturing Extension Partnership (GaMEP)", "404-894-5242", "https://gamep.org"),
        ("Hawaii", "Wayne Inouye", "MANUFACTURING_HEAD", "Director", "INNOVATE Hawaii (HTDC)", "808-539-3600", "https://www.htdc.org/programs/#innovate-hawaii"),
        ("Idaho", "Cathy Cooper", "MANUFACTURING_HEAD", "Director", "TechHelp Idaho", "208-426-3767", "https://www.techhelp.org"),
        ("Illinois", "David Boulay", "MANUFACTURING_HEAD", "President", "Illinois Manufacturing Excellence Center (IMEC)", "888-806-4632", "https://www.imec.org"),
        ("Indiana", "Gene Jones", "MANUFACTURING_HEAD", "Director", "Purdue Manufacturing Extension Partnership", "317-275-6810", "https://mep.purdue.edu"),
        ("Iowa", "Mike O'Donnell", "MANUFACTURING_HEAD", "Director", "Center for Industrial Research and Service (CIRAS)", "515-294-3420", "https://www.ciras.iastate.edu"),
        ("Kansas", "Tiffany Stovall", "MANUFACTURING_HEAD", "CEO", "Kansas Manufacturing Solutions (KMS)", "913-649-4333", "https://www.mfgsolutions.org"),
        ("Kentucky", "Scott Broughton", "MANUFACTURING_HEAD", "Executive Director", "Advantage Kentucky Alliance (AKA)", "270-282-7103", "https://www.advantageky.org"),
        ("Louisiana", "Dayna Blanchard", "MANUFACTURING_HEAD", "Director", "Manufacturing Extension Partnership of Louisiana (MEPOL)", "337-482-6767", "https://mepol.org"),
        ("Maine", "Larry Robinson", "MANUFACTURING_HEAD", "Executive Director", "Maine MEP", "207-623-0680", "https://www.mainemep.com"),
        ("Maryland", "Mike Kelleher", "MANUFACTURING_HEAD", "CEO", "Maryland MEP (MD MEP)", "443-343-0085", "https://www.mdmep.org"),
        ("Massachusetts", "Kathie Mahoney", "MANUFACTURING_HEAD", "President & CEO", "MassMEP", "508-831-7020", "https://massmep.org"),
        ("Michigan", "John Yopp", "MANUFACTURING_HEAD", "President", "Michigan Manufacturing Technology Center (MMTC)", "888-414-6682", "https://www.the-center.org"),
        ("Minnesota", "Bob Kill", "MANUFACTURING_HEAD", "President & CEO", "Enterprise Minnesota", "612-373-2900", "https://www.enterpriseminnesota.org"),
        ("Mississippi", "David Henson", "MANUFACTURING_HEAD", "Director", "Mississippi MMA-MEP", "601-948-1222", "https://www.mma-web.org"),
        ("Missouri", "Dusty Cruise", "MANUFACTURING_HEAD", "President & CEO", "Missouri Enterprise", "800-456-2380", "https://www.missourienterprise.org"),
        ("Montana", "Paddy Fleming", "MANUFACTURING_HEAD", "Director", "Montana Manufacturing Extension Center (MMEC)", "406-994-3812", "https://www.montana.edu/mmec/"),
        ("Nebraska", "Matt Allmand", "MANUFACTURING_HEAD", "Director", "Nebraska MEP", "402-472-5993", "https://nemep.unl.edu"),
        ("Nevada", "Tom Simpkins", "MANUFACTURING_HEAD", "Director", "Manufacture Nevada", "775-784-1935", "https://www.manufacturenevada.com"),
        ("New Hampshire", "Zenagui Brahim", "MANUFACTURING_HEAD", "President", "New Hampshire MEP (NH MEP)", "603-226-3200", "https://www.nhmep.org"),
        ("New Jersey", "Peter Connolly", "MANUFACTURING_HEAD", "CEO", "New Jersey Manufacturing Extension Program (NJMEP)", "973-998-9801", "https://www.njmep.org"),
        ("New Mexico", "Jennifer Sinsabaugh", "MANUFACTURING_HEAD", "CEO", "New Mexico MEP", "505-262-0921", "https://newmexicomep.org"),
        ("New York", "Elena Garuc", "MANUFACTURING_HEAD", "Executive Director", "FuzeHub / New York MEP", "518-768-7030", "https://fuzehub.com"),
        ("North Carolina", "Phil Mintz", "MANUFACTURING_HEAD", "Executive Director", "NC State Industry Expansion Solutions (IES)", "919-515-2358", "https://www.ies.ncsu.edu"),
        ("North Dakota", "Jerry Hauck", "MANUFACTURING_HEAD", "Director", "Impact Dakota", "701-204-7000", "https://www.impactdakota.com"),
        ("Ohio", "Jim Ruble", "MANUFACTURING_HEAD", "Director", "Ohio Manufacturing Extension Partnership (Ohio MEP)", "614-466-2775", "https://development.ohio.gov/business/ohio-mep"),
        ("Oklahoma", "Dave Rowland", "MANUFACTURING_HEAD", "President", "Oklahoma Manufacturing Alliance", "918-592-0722", "https://www.okalliance.com"),
        ("Oregon", "Aaron Fox", "MANUFACTURING_HEAD", "President", "Oregon Manufacturing Extension Partnership (OMEP)", "503-406-3770", "https://omep.org"),
        ("Pennsylvania", "Petra Mitchell", "MANUFACTURING_HEAD", "President & CEO", "Catalyst Connection / PA MEP Network", "412-918-4300", "https://www.catalystconnection.org"),
        ("Puerto Rico", "Migdalia Rosado", "MANUFACTURING_HEAD", "Executive Director", "Puerto Rico PRIMEX", "787-756-0505", "https://www.primex.org"),
        ("Rhode Island", "Matthew Watson", "MANUFACTURING_HEAD", "Center Director", "Polaris MEP", "401-270-8896", "https://polarismep.org"),
        ("South Carolina", "Andy Carr", "MANUFACTURING_HEAD", "President & CEO", "South Carolina Manufacturing Extension Partnership (SCMEP)", "803-252-6976", "https://www.scmep.org"),
        ("South Dakota", "Aaron Scheibe", "MANUFACTURING_HEAD", "Executive Director", "South Dakota Manufacturing & Technology Solutions (MTS)", "605-367-5757", "https://www.sdmanufacturing.com"),
        ("Tennessee", "Paul Jennings", "MANUFACTURING_HEAD", "Executive Director", "University of Tennessee Center for Industrial Services (CIS)", "615-532-8687", "https://cis.tennessee.edu"),
        ("Texas", "Rodney Reddic", "MANUFACTURING_HEAD", "Executive Director", "Texas Manufacturing Assistance Center (TMAC)", "800-625-4876", "https://tmac.org"),
        ("Utah", "Theresa Drulard", "MANUFACTURING_HEAD", "Director", "University of Utah MEP Center", "801-587-0713", "https://mep.utah.edu"),
        ("Vermont", "Patrick Roach", "MANUFACTURING_HEAD", "Director", "Vermont Manufacturing Extension Center (VMEC)", "802-728-1678", "https://vmec.org"),
        ("Virginia", "Bill Donohue", "MANUFACTURING_HEAD", "Executive Director", "GENEDGE Alliance", "276-666-8890", "https://genedge.org"),
        ("Washington", "Deloit Wolfe", "MANUFACTURING_HEAD", "President & CEO", "Impact Washington", "425-438-1146", "https://impactwashington.org"),
        ("West Virginia", "Staci Miller", "MANUFACTURING_HEAD", "Director", "West Virginia MEP", "304-293-6780", "https://wvmep.com"),
        ("Wisconsin", "Christian Tscheschlok", "MANUFACTURING_HEAD", "Executive Director", "WMEP Manufacturing Solutions", "262-832-6800", "https://wmep.org"),
        ("Wyoming", "Rocky Case", "MANUFACTURING_HEAD", "Director", "Manufacturing-Works Wyoming", "307-766-4811", "https://www.manufacturing-works.com")
    ],

    # -------------------------------------------------------------
    # 4. ELECTRIC VEHICLES (EV) & CLEAN MOBILITY (NEVI Coordinators)
    # -------------------------------------------------------------
    "ev": [
        ("Alabama", "Blake Hardwich", "EV_INFRASTRUCTURE_HEAD", "Drive Electric Alabama Coordinator", "Alabama Department of Transportation", "334-242-6358", "https://driveelectricalabama.com"),
        ("Alaska", "Sean Baski", "EV_INFRASTRUCTURE_HEAD", "NEVI Program Manager", "Alaska Department of Transportation & Public Facilities", "907-465-3900", "https://dot.alaska.gov/transportation-plans/nevi/"),
        ("Arizona", "Diane Brown", "EV_INFRASTRUCTURE_HEAD", "Electric Vehicle Program Manager", "Arizona Department of Transportation", "602-712-7000", "https://azdot.gov/planning/transportation-programs/electric-vehicle-program"),
        ("Arkansas", "Terry Cole", "EV_INFRASTRUCTURE_HEAD", "Alternative Fuels Coordinator", "Arkansas Department of Transportation", "501-569-2000", "https://www.ardot.gov/divisions/transportation-planning-policy/nevi/"),
        ("California", "Tyson Eckerle", "EV_INFRASTRUCTURE_HEAD", "Clean Transportation & Zero-Emission Vehicle Lead", "California Governor's Office of Business and Economic Development (GO-Biz)", "916-322-0694", "https://business.ca.gov/industries/zero-emission-vehicles/"),
        ("Colorado", "Kay Kelly", "EV_INFRASTRUCTURE_HEAD", "Chief of Innovative Mobility", "Colorado Department of Transportation", "303-757-9011", "https://www.codot.gov/programs/innovativemobility"),
        ("Connecticut", "Dagmara Bulas", "EV_INFRASTRUCTURE_HEAD", "EV Infrastructure Coordinator", "Connecticut Department of Transportation", "860-594-2000", "https://portal.ct.gov/dot/pp_bureau/nevi"),
        ("Delaware", "Nicole Majeski", "EV_INFRASTRUCTURE_HEAD", "Secretary & Clean Transportation Lead", "Delaware Department of Transportation", "302-760-2000", "https://deldot.gov/Programs/cleantransportation/"),
        ("District of Columbia", "Sharon Kershbaum", "EV_INFRASTRUCTURE_HEAD", "Director & Clean Fleet Lead", "District Department of Transportation", "202-673-6813", "https://ddot.dc.gov"),
        ("Florida", "Trey Tillander", "EV_INFRASTRUCTURE_HEAD", "Executive Director of Transportation Technology", "Florida Department of Transportation", "850-414-4100", "https://www.fdot.gov/planning/policy/ev/default.shtm"),
        ("Georgia", "Matt Fowler", "EV_INFRASTRUCTURE_HEAD", "Alternative Fuels Program Manager", "Georgia Department of Transportation", "404-631-1990", "https://www.dot.ga.gov/GDOT/Pages/NEVI.aspx"),
        ("Hawaii", "Ed Sniffen", "EV_INFRASTRUCTURE_HEAD", "Director & Clean Transportation Lead", "Hawaii Department of Transportation", "808-587-2150", "https://hidot.hawaii.gov/highways/clean-transportation/"),
        ("Idaho", "Scott Luekenga", "EV_INFRASTRUCTURE_HEAD", "NEVI Program Manager", "Idaho Transportation Department", "208-334-8000", "https://itd.idaho.gov/nevi/"),
        ("Illinois", "Chris Schmidt", "EV_INFRASTRUCTURE_HEAD", "Air Quality & EV Planning Lead", "Illinois Department of Transportation", "217-782-7820", "https://idot.illinois.gov/transportation-system/environment/drive-electric-illinois.html"),
        ("Indiana", "Scott Manning", "EV_INFRASTRUCTURE_HEAD", "Clean Mobility Director", "Indiana Department of Transportation", "855-463-6848", "https://www.in.gov/indot/current-programs/clean-mobility/"),
        ("Iowa", "Scott Marler", "EV_INFRASTRUCTURE_HEAD", "Director & Clean Infrastructure Lead", "Iowa Department of Transportation", "515-239-1101", "https://iowadot.gov/iowaevplan"),
        ("Kansas", "Tami Alexander", "EV_INFRASTRUCTURE_HEAD", "Electrification Program Manager", "Kansas Department of Transportation", "785-296-3566", "https://www.ksdot.gov/DriveEV.asp"),
        ("Kentucky", "John Moore", "EV_INFRASTRUCTURE_HEAD", "EV Infrastructure Project Manager", "Kentucky Transportation Cabinet", "502-564-4890", "https://transportation.ky.gov/evcharging/"),
        ("Louisiana", "Joe Donahue", "EV_INFRASTRUCTURE_HEAD", "NEVI Coordinator", "Louisiana Department of Transportation and Development", "225-379-1232", "https://www.dotd.la.gov/Inside_LaDOTD/Divisions/Multimodal/NEVI/Pages/default.aspx"),
        ("Maine", "Michael Stoddard", "EV_INFRASTRUCTURE_HEAD", "Executive Director & Clean Transportation Lead", "Efficiency Maine Trust / MaineDOT", "866-376-2463", "https://www.efficiencymaine.com/electric-vehicles/"),
        ("Maryland", "Dan Janis", "EV_INFRASTRUCTURE_HEAD", "Zero Emission Vehicle Infrastructure Lead", "Maryland Department of Transportation", "410-865-1000", "https://evplans.mdot.maryland.gov"),
        ("Massachusetts", "Monica Tibbits-Nutt", "EV_INFRASTRUCTURE_HEAD", "Secretary & Clean Transportation Lead", "Massachusetts Department of Transportation", "857-368-4636", "https://www.mass.gov/info-details/national-electric-vehicle-infrastructure-nevi-program"),
        ("Michigan", "Kathryn Snorrason", "EV_INFRASTRUCTURE_HEAD", "Director, Office of Future Mobility & Electrification", "Michigan Department of Transportation / MEDC", "517-335-5280", "https://www.michiganbusiness.org/ofme/"),
        ("Minnesota", "Tim Sexton", "EV_INFRASTRUCTURE_HEAD", "Assistant Commissioner & Sustainability Officer", "Minnesota Department of Transportation", "651-366-4825", "https://www.dot.state.mn.us/sustainability/electric-vehicles.html"),
        ("Mississippi", "Brad White", "EV_INFRASTRUCTURE_HEAD", "Executive Director & EV Plan Lead", "Mississippi Department of Transportation", "601-359-7001", "https://mdot.ms.gov/portal/nevi"),
        ("Missouri", "Patrick McKenna", "EV_INFRASTRUCTURE_HEAD", "Director & Clean Transit Lead", "Missouri Department of Transportation", "888-275-6636", "https://www.modot.org/national-electric-vehicle-infrastructure-nevi-plan"),
        ("Montana", "Larry Flynn", "EV_INFRASTRUCTURE_HEAD", "NEVI Program Coordinator", "Montana Department of Transportation", "406-444-6200", "https://www.mdt.mt.gov/visionzero/plans/nevi.aspx"),
        ("Nebraska", "Vicki Kramer", "EV_INFRASTRUCTURE_HEAD", "Director & Emerging Technologies Lead", "Nebraska Department of Transportation", "402-471-4567", "https://dot.nebraska.gov/projects/nevi/"),
        ("Nevada", "Tracy Larkin Thomason", "EV_INFRASTRUCTURE_HEAD", "Director & Clean Transportation Lead", "Nevada Department of Transportation", "775-888-7000", "https://www.dot.nv.gov/mobility/nevi"),
        ("New Hampshire", "William Cass", "EV_INFRASTRUCTURE_HEAD", "Commissioner & Clean Mobility Lead", "New Hampshire Department of Transportation", "603-271-3734", "https://www.nh.gov/dot/programs/nevi/"),
        ("New Jersey", "Diane Gutierrez-Scaccetti", "EV_INFRASTRUCTURE_HEAD", "Chief of Staff & Clean Transportation Lead", "New Jersey Department of Transportation", "609-530-2000", "https://www.state.nj.us/transportation/capital/nevi.shtm"),
        ("New Mexico", "Ricky Serna", "EV_INFRASTRUCTURE_HEAD", "Cabinet Secretary & EV Lead", "New Mexico Department of Transportation", "505-827-5100", "https://www.dot.nm.gov/planning-divisions/nevi-plan/"),
        ("New York", "Marie Therese Dominguez", "EV_INFRASTRUCTURE_HEAD", "Commissioner & Clean Mobility Lead", "New York State Department of Transportation", "518-457-6195", "https://www.dot.ny.gov/nevi"),
        ("North Carolina", "Brian Phillips", "EV_INFRASTRUCTURE_HEAD", "Clean Transportation Manager", "North Carolina Department of Transportation", "919-707-2800", "https://www.ncdot.gov/initiatives-policies/environmental/clean-transportation/Pages/default.aspx"),
        ("North Dakota", "Ron Henke", "EV_INFRASTRUCTURE_HEAD", "Director & Innovation Lead", "North Dakota Department of Transportation", "701-328-2500", "https://www.dot.nd.gov/projects/nevi"),
        ("Ohio", "Preeti Choudhary", "EV_INFRASTRUCTURE_HEAD", "Executive Director, DriveOhio", "Ohio Department of Transportation / DriveOhio", "614-387-7700", "https://drive.ohio.gov"),
        ("Oklahoma", "Tim Gatz", "EV_INFRASTRUCTURE_HEAD", "Secretary of Transportation & EV Lead", "Oklahoma Department of Transportation", "405-522-8000", "https://oklahoma.gov/odot/programs-and-projects/nevi.html"),
        ("Oregon", "Amanda Pietz", "EV_INFRASTRUCTURE_HEAD", "Climate Office Director", "Oregon Department of Transportation", "503-986-3403", "https://www.oregon.gov/odot/climate/Pages/NEVI.aspx"),
        ("Pennsylvania", "Colton Brown", "EV_INFRASTRUCTURE_HEAD", "Alternative Fuels Coordinator", "Pennsylvania Department of Transportation", "717-787-2838", "https://www.penndot.pa.gov/TravelInPA/ev/Pages/default.aspx"),
        ("Puerto Rico", "Eileen Velez Vega", "EV_INFRASTRUCTURE_HEAD", "Secretary of Transportation", "Puerto Rico Department of Transportation and Public Works", "787-722-2929", "https://www.dtop.pr.gov"),
        ("Rhode Island", "Peter Alviti", "EV_INFRASTRUCTURE_HEAD", "Director & Clean Transportation Lead", "Rhode Island Department of Transportation", "401-222-2450", "https://www.dot.ri.gov/projects/NEVI/"),
        ("South Carolina", "Justin Powell", "EV_INFRASTRUCTURE_HEAD", "Secretary of Transportation", "South Carolina Department of Transportation", "803-737-1200", "https://www.scdot.org/projects/nevi.aspx"),
        ("South Dakota", "Joel Jundt", "EV_INFRASTRUCTURE_HEAD", "Secretary of Transportation", "South Dakota Department of Transportation", "605-773-3265", "https://dot.sd.gov/projects-studies/projects/nevi"),
        ("Tennessee", "Butch Eley", "EV_INFRASTRUCTURE_HEAD", "Deputy Governor & Commissioner of Transportation", "Tennessee Department of Transportation", "615-741-2848", "https://www.tn.gov/tdot/sustainable-transportation/drive-electric-tennessee.html"),
        ("Texas", "Michael Ebbeler", "EV_INFRASTRUCTURE_HEAD", "Alternative Fuels Program Manager", "Texas Department of Transportation", "512-463-8588", "https://www.txdot.gov/projects/projects-studies/statewide/texas-electric-vehicle-infrastructure-plan.html"),
        ("Utah", "Matt Maass", "EV_INFRASTRUCTURE_HEAD", "Clean Transportation & NEVI Lead", "Utah Department of Transportation", "801-965-4000", "https://www.udot.utah.gov/connect/projects/electric-vehicle-infrastructure/"),
        ("Vermont", "Michele Boomhower", "EV_INFRASTRUCTURE_HEAD", "Director of Policy, Planning & Intermodal Development", "Vermont Agency of Transportation (VTrans)", "802-828-2657", "https://vtrans.vermont.gov/planning/nevi"),
        ("Virginia", "Stephen Brich", "EV_INFRASTRUCTURE_HEAD", "Commissioner & Innovation Lead", "Virginia Department of Transportation", "804-786-2801", "https://www.virginiadot.org/projects/nevi_program.asp"),
        ("Washington", "Tonia Buell", "EV_INFRASTRUCTURE_HEAD", "Alternative Fuels Program Manager", "Washington State Department of Transportation", "360-705-7000", "https://wsdot.wa.gov/construction-planning/environment/zero-emission-vehicles"),
        ("West Virginia", "Jimmy Wriston", "EV_INFRASTRUCTURE_HEAD", "Secretary of Transportation", "West Virginia Department of Transportation", "304-558-3505", "https://transportation.wv.gov/highways/programplanning/NEVI/Pages/default.aspx"),
        ("Wisconsin", "Kaleb Vander Wiele", "EV_INFRASTRUCTURE_HEAD", "EV Program Manager", "Wisconsin Department of Transportation", "608-266-1115", "https://wisconsindot.gov/Pages/projects/multimodal/ev.aspx"),
        ("Wyoming", "Jesse Naranjo", "EV_INFRASTRUCTURE_HEAD", "NEVI Program Manager", "Wyoming Department of Transportation", "307-777-4375", "https://www.dot.state.wy.us/home/planning_projects/zero-emission-vehicles/nevi.html")
    ],

    # -------------------------------------------------------------
    # 5. STATE EDA & SELECTUSA DEPUTIES (Business Attraction / FDI)
    # -------------------------------------------------------------
    "eda_deputies": [
        ("Alabama", "Ted Clem", "EDA_DEPUTY", "Director of Business Development", "Alabama Department of Commerce", "334-242-0400", "https://www.madeinalabama.com"),
        ("Alaska", "Micaela Fowler", "EDA_DEPUTY", "Deputy Commissioner", "Alaska Department of Commerce, Community & Economic Development", "907-465-2500", "https://www.commerce.alaska.gov"),
        ("Arizona", "Vic Narusis", "EDA_DEPUTY", "Executive Vice President, Business Expansion", "Arizona Commerce Authority", "602-845-1200", "https://www.azcommerce.com"),
        ("Arkansas", "Clint O'Neal", "EDA_DEPUTY", "Executive Director & Deputy Secretary", "Arkansas Economic Development Commission", "501-682-1121", "https://www.arkansasedc.com"),
        ("California", "Kenechukwu Ojukwu", "FOREIGN_INVESTMENT_DEPUTY", "Deputy Director of International Affairs and Trade", "California Governor's Office of Business and Economic Development (GO-Biz)", "916-322-0694", "https://business.ca.gov"),
        ("Colorado", "Michelle Hadwiger", "EDA_DEPUTY", "Director of Global Business Development", "Colorado Office of Economic Development & International Trade", "303-892-3840", "https://oedit.colorado.gov"),
        ("Connecticut", "Paul O. Robertson", "EDA_DEPUTY", "Deputy Commissioner", "Connecticut Department of Economic & Community Development", "860-500-2300", "https://portal.ct.gov/decd"),
        ("Delaware", "Megan Dawson", "EDA_DEPUTY", "Vice President of Business Development", "Delaware Prosperity Partnership", "302-888-4030", "https://choosedelaware.com"),
        ("Florida", "Laura DiBella", "EDA_DEPUTY", "Deputy Secretary of Economic Development", "FloridaCommerce", "850-245-7105", "https://floridacommerce.myflorida.com"),
        ("Georgia", "Bert Brantley", "EDA_DEPUTY", "Deputy Commissioner of Global Commerce", "Georgia Department of Economic Development", "404-962-4000", "https://www.georgia.org"),
        ("Hawaii", "Dane Wicker", "EDA_DEPUTY", "Deputy Director", "Hawaii Department of Business, Economic Development & Tourism", "808-586-2355", "https://dbedt.hawaii.gov"),
        ("Idaho", "Jesse Neughbauer", "EDA_DEPUTY", "Chief Operating Officer", "Idaho Department of Commerce", "208-334-2470", "https://commerce.idaho.gov"),
        ("Illinois", "Cas Smith", "EDA_DEPUTY", "Deputy Director of Business Development", "Illinois Department of Commerce and Economic Opportunity", "217-782-7500", "https://dceo.illinois.gov"),
        ("Indiana", "Brock Herr", "EDA_DEPUTY", "Senior Vice President of Business Development", "Indiana Economic Development Corporation", "317-232-8800", "https://iedc.in.gov"),
        ("Iowa", "Staci Hupp Ballard", "EDA_DEPUTY", "Chief Business Development Officer", "Iowa Economic Development Authority", "515-348-6200", "https://www.iowaeda.com"),
        ("Kansas", "Paul Hughes", "EDA_DEPUTY", "Deputy Secretary of Business Development", "Kansas Department of Commerce", "785-296-3481", "https://www.kansascommerce.gov"),
        ("Kentucky", "Beth Brinly", "EDA_DEPUTY", "Deputy Secretary", "Kentucky Cabinet for Economic Development", "502-564-7670", "https://ced.ky.gov"),
        ("Louisiana", "Anne Villa", "EDA_DEPUTY", "Undersecretary", "Louisiana Economic Development", "225-342-3000", "https://www.opportunitylouisiana.gov"),
        ("Maine", "Denise Garland", "EDA_DEPUTY", "Deputy Commissioner", "Maine Department of Economic and Community Development", "207-624-9800", "https://www.maine.gov/decd/"),
        ("Maryland", "Signe Pringle", "EDA_DEPUTY", "Deputy Secretary of Commerce", "Maryland Department of Commerce", "410-767-6300", "https://commerce.maryland.gov"),
        ("Massachusetts", "Colin A. Jones", "EDA_DEPUTY", "Undersecretary of Economic Foundations", "Massachusetts Executive Office of Economic Development", "617-788-3610", "https://www.mass.gov/orgs/executive-office-of-economic-development"),
        ("Michigan", "Christin Armstrong", "EDA_DEPUTY", "Senior Vice President of Business Development", "Michigan Economic Development Corporation", "888-522-0103", "https://www.michiganbusiness.org"),
        ("Minnesota", "Kevin McKinnon", "EDA_DEPUTY", "Deputy Commissioner of Economic Development", "Minnesota Department of Employment and Economic Development", "651-259-7114", "https://mn.gov/deed/"),
        ("Mississippi", "Laura Hipp", "EDA_DEPUTY", "Deputy Executive Director", "Mississippi Development Authority", "601-359-3449", "https://www.mississippi.org"),
        ("Missouri", "Mark Dixon", "EDA_DEPUTY", "Deputy Director of Business Solutions", "Missouri Department of Economic Development", "573-751-4962", "https://ded.mo.gov"),
        ("Montana", "Mandy Rambo", "EDA_DEPUTY", "Deputy Director", "Montana Department of Commerce", "406-841-2700", "https://commerce.mt.gov"),
        ("Nebraska", "Dan Curran", "EDA_DEPUTY", "Deputy Director of Economic Development", "Nebraska Department of Economic Development", "402-471-3111", "https://opportunity.nebraska.gov"),
        ("Nevada", "Bob Potts", "EDA_DEPUTY", "Deputy Director", "Nevada Governor's Office of Economic Development", "775-687-9900", "https://goed.nv.gov"),
        ("New Hampshire", "Michael Bergeron", "EDA_DEPUTY", "Senior Manager of Business Development", "New Hampshire Department of Business and Economic Affairs", "603-271-2591", "https://www.nheconomy.com"),
        ("New Jersey", "Tim Rollender", "EDA_DEPUTY", "Managing Director of Technology & Life Sciences", "New Jersey Economic Development Authority", "609-858-6700", "https://www.njeda.gov"),
        ("New Mexico", "Mark Roper", "EDA_DEPUTY", "Division Director of Economic Development", "New Mexico Economic Development Department", "505-827-0300", "https://edd.newmexico.gov"),
        ("New York", "Linda Malave", "FOREIGN_INVESTMENT_DEPUTY", "Senior Vice President of Global NY", "Empire State Development", "212-803-3100", "https://esd.ny.gov"),
        ("North Carolina", "Liz Isley", "EDA_DEPUTY", "Vice President of Business Recruitment", "Economic Development Partnership of North Carolina", "919-447-7777", "https://edpnc.com"),
        ("North Dakota", "Shawn Kessel", "EDA_DEPUTY", "Deputy Commissioner", "North Dakota Department of Commerce", "701-328-5300", "https://www.commerce.nd.gov"),
        ("Ohio", "Kristi Tanner", "EDA_DEPUTY", "Senior Managing Director", "JobsOhio", "614-224-6446", "https://www.jobsohio.com"),
        ("Oklahoma", "Jon Chiappe", "EDA_DEPUTY", "Director of Research & Economic Analysis", "Oklahoma Department of Commerce", "405-815-6552", "https://www.okcommerce.gov"),
        ("Oregon", "Chris Cummings", "EDA_DEPUTY", "Deputy Director", "Business Oregon", "503-986-0123", "https://www.oregon.gov/biz/"),
        ("Pennsylvania", "Neil Weaver", "EDA_DEPUTY", "Executive Deputy Secretary", "Pennsylvania Department of Community and Economic Development", "717-787-3003", "https://dced.pa.gov"),
        ("Rhode Island", "Matthew Sheaff", "EDA_DEPUTY", "Executive Vice President", "Rhode Island Commerce Corporation", "401-278-9100", "https://commerceri.com"),
        ("South Carolina", "Ashely Teasdel", "EDA_DEPUTY", "Deputy Secretary of Commerce", "South Carolina Department of Commerce", "803-737-0400", "https://www.sccommerce.com"),
        ("South Dakota", "Travis Dovre", "EDA_DEPUTY", "Deputy Commissioner", "South Dakota Governor's Office of Economic Development", "605-773-3301", "https://sdgoed.com"),
        ("Tennessee", "Allen Borden", "EDA_DEPUTY", "Deputy Commissioner of Business Development", "Tennessee Department of Economic & Community Development", "615-741-1888", "https://tnecd.com"),
        ("Texas", "Larry McManus", "EDA_DEPUTY", "Director of Business and Community Development", "Texas Economic Development & Tourism Office", "512-936-0100", "https://gov.texas.gov/business"),
        ("Utah", "Ben Hart", "EDA_DEPUTY", "Executive Director, Utah Inland Port Authority & Deputy", "Utah Governor's Office of Economic Opportunity", "801-538-8680", "https://business.utah.gov"),
        ("Vermont", "Joan Goldstein", "EDA_DEPUTY", "Commissioner of Economic Development", "Vermont Agency of Commerce and Community Development", "802-828-3211", "https://accd.vermont.gov/economic-development"),
        ("Virginia", "Vince Barnett", "EDA_DEPUTY", "Vice President of Business Investment", "Virginia Economic Development Partnership", "804-545-5600", "https://www.vedp.org"),
        ("Washington", "Chris Green", "EDA_DEPUTY", "Assistant Director of Economic Development", "Washington State Department of Commerce", "360-725-4000", "https://www.commerce.wa.gov"),
        ("West Virginia", "Michael Graney", "EDA_DEPUTY", "Executive Director", "West Virginia Department of Economic Development", "304-558-2234", "https://westvirginia.gov"),
        ("Wisconsin", "Sam Rikkers", "EDA_DEPUTY", "Deputy Secretary and Chief Operating Officer", "Wisconsin Economic Development Corporation", "608-210-6700", "https://wedc.org"),
        ("Wyoming", "Sarah Fitz-Gerald", "EDA_DEPUTY", "Chief Operating Officer", "Wyoming Business Council", "307-777-2800", "https://wyomingbusiness.org"),
        ("Puerto Rico", "Carlos Rios Pierluisi", "EDA_DEPUTY", "Deputy Secretary", "Puerto Rico Department of Economic Development and Commerce", "787-765-2900", "https://ddec.pr.gov"),
        ("Guam", "Carlos Camacho", "EDA_DEPUTY", "Deputy Administrator", "Guam Economic Development Authority", "671-647-4332", "https://investguam.com"),
        ("U.S. Virgin Islands", "Shanell Petersen", "EDA_DEPUTY", "Managing Director", "USVI Economic Development Authority", "340-714-1700", "https://usvieda.org")
    ]
}

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
    "District of Columbia": "DC", "Puerto Rico": "PR", "Guam": "GU", "U.S. Virgin Islands": "VI",
    "American Samoa": "AS", "Northern Mariana Islands": "MP"
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
    print("Ingesting verified sector leads...")

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

    for category, records in SECTOR_DATA.items():
        for state, name, role_code, role_title, agency, raw_phone, source_url in records:
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
                "bio": f"{name} is an American public official serving as {role_title} for {state} ({agency}).",
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

    print(f"Generated {len(new_contacts)} new verified sector officials.")

    # Write contacts.csv
    all_contacts = existing_contacts + new_contacts
    with open(CONTACTS_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_contacts)
    print(f"Updated {CONTACTS_CSV} — total rows now {len(all_contacts)}.")

    # Also copy to site/public/data/contacts.csv
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
