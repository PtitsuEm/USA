# Instructions for coding agents

- Read `PROJECT_SPEC.md` before changing the data model or UI.
- Keep the application static and offline: no hosted backend, analytics, external scripts, or network calls from the app.
- Treat `data/contacts.csv`, `data/relationships.csv`, and `data/coverage.csv` as the source of truth. Regenerate `dist/index.html` with `python3 scripts/build.py` after changing them.
- Never invent names, email addresses, LinkedIn matches, positions, or reporting relationships. Include a source URL and verification date for factual records.
- Do not draw a reporting line unless a source confirms it. Keep investor servicing distinct from foreign-investment attraction unless a source shows they are the same role.
- Preserve user-facing navigation by jurisdiction, role, and person. Keep empty datasets clearly labeled as empty, not complete.
