# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bröckel is a municipality in the Samtgemeinde Flotwedel, Landkreis Celle, Lower Saxony (Niedersachsen). The Ortsfeuerwehr Bröckel is a base fire station (Stützpunktfeuerwehr) of the volunteer fire department Freiwillige Feuerwehr Flotwedel.

The fire department is migrating from the management software Fox112 (https://celle.fox112.de/) to FeuerON (https://www.feueron.de/), a web application provided centrally by the state of Lower Saxony for all fire departments.

This repository serves three purposes:
1. **Documentation**: German-language user guide for FeuerON, built with [Zensical](https://github.com/zensical/zensical) (a static site generator based on Material for MkDocs).
2. **Content generation**: Automated screenshot capture and annotation tools for the documentation (Playwright, Pillow).
3. **Data migration**: Tools to migrate and transform data from Fox112 to FeuerON (FeuerON supports CSV import).

## Commands

```bash
# Install dependencies
uv sync

# Install Playwright browser (one-time setup)
uv run playwright install chromium

# Serve docs locally at http://localhost:8000
uv run zensical serve

# Build static site to site/ directory
uv run zensical build
uv run zensical build --clean

# Lint and format Python code
uv run ruff check .
uv run ruff format .

# CLI (Typer) — all project-specific commands
uv run info --help

# Generate FeuerON screenshots (requires FEUERON_USERNAME, FEUERON_PASSWORD env vars)
uv run info screenshots generate    # full pipeline (capture → annotate → frame)
uv run info screenshots capture     # only take screenshots
uv run info screenshots annotate    # only apply annotations
uv run info screenshots frame       # only apply browser frames

# Data migration (Fox112 → FeuerON)
uv run info migration bank-check FOX112.xlsx BANKVERBINDUNGEN.csv -o output.csv
uv run info migration contact-check FOX112.xlsx ERREICHBARKEITEN.xlsx -o output.csv
uv run info migration passive-import FOX112.xlsx ERREICHBARKEITEN.xlsx PERSONALDATEN.xml -o output.csv
```

## Architecture

**Screenshot pipeline** (three-stage process orchestrated by `scripts/feueron/generate.py`):

1. **Capture** (`scripts/feueron/screenshots.py`): Playwright automates Chromium to log into FeuerON.de and capture pages at 1920x1080. Raw PNGs saved to `docs/assets/feueron/screenshots/raw/`.

2. **Annotate** (`scripts/feueron/annotations.py` + `tools/annotation.py`): Marker definitions (rectangles/circles with labels, colors, opacity) are applied to raw screenshots using Pillow. Output goes to `docs/assets/feueron/screenshots/annotated/`.

3. **Frame** (`tools/browserframe.py`): Screenshots are composited into browser window chrome using 9-slice scaling with template images from `tools/assets/`. Output goes to `docs/assets/feueron/screenshots/framed/`.

**Data migration** (`scripts/feueron/migration/`):

- `report_parser.py` — Generic parser for paginated FeuerON CSV reports (shared across report types).
- `bank_check.py` — Compares Fox112 bank details with FeuerON Bankverbindungen report; outputs FeuerON CSV import.
- `erreichbarkeiten_parser.py` — Parser for the FeuerON Erreichbarkeiten Excel report.
- `contact_check.py` — Compares Fox112 addresses and contact details (phone, email, fax) with FeuerON Erreichbarkeiten report; outputs FeuerON CSV import. Phone numbers are sanitized to national German format using `phonenumbers`.
- `passive_import.py` — Imports passive members (Fördernde Mitglieder) from Fox112 into FeuerON. Cross-references Fox112 XML export to skip formerly active members with Dienstgrade/Funktionen. Includes address, contacts, bank, Abteilung, and Beiträge.
- `models/` — Pydantic v2 models for the FeuerON CSV import format.

**FeuerON reports**: Generated from search results in the Persons management view. Each report type has configurable filter parameters, sorting, and export formats. Export format availability varies per report — e.g. "Bankverbindungen" supports CSV/Excel/PDF/HTML/Word/RTF/Text, while "Erreichbarkeiten" only supports Excel (xlsx). CSV and Excel exports have different structures even for the same report. The CSV-based migration tools consume semicolon-delimited paginated exports (with metadata headers/footers and page-1 column offset quirk); the Erreichbarkeiten tool consumes the Excel export directly.

**FeuerON REST API client** (`scripts/feueron/api/`):

Typed Python client for the FeuerON REST API using `httpx` + Pydantic v2 models. Structured as mixin classes matching the FeuerON UI tab layout:

- `client.py` — `FeuerONClient` (inherits all mixins), authentication, core request helpers, `FeuerONAPIError`/`FeuerONAuthError` exceptions.
- `person.py` — `PersonMixin`: CRUD for persons, edit locking, erreichbarkeiten.
- `feuerwehr.py` — `FeuerwehrMixin`: abteilungen, dienstgrade.
- `einsatzdienst.py` — `EinsatzdienstMixin`: züge/gruppen.
- `finanzen.py` — `FinanzenMixin`: bankverbindungen, beiträge.
- `reference.py` — `ReferenceMixin`: general-menus, beitragsarten, dienstgrade values, abteilungen values, organisation tree, personalnummer generation/validation, person creation.
- `models.py` — All Pydantic v2 models (response + request).
- `__init__.py` — Re-exports all public symbols.

Authentication flow:

1. `GET /` — pick up initial session cookies
2. `POST /login.do` — form login (needs `submitName=login` hidden field)
3. `GET /modul-switch.do?modul=personalverwaltung` — activate "Personen (neu)" module (required for REST API)
4. `GET /csrfguard` — fetch OWASP CSRFGuard JS, extract `masterTokenValue`
5. Send `OWASP-CSRFTOKEN` header on all subsequent API requests

Key API patterns and gotchas:

- **Edit locking**: Must acquire lock before mutations: `PUT /api/personen/{id}/lock` → mutation → `DELETE /api/personen/{id}/lock` (always in try/finally).
- **JSON Patch for list removal**: `PATCH` with `application/json-patch+json` (RFC 6902) for removing items from lists (dienstgrade, abteilungen, bankverbindungen, erreichbarkeiten). Regular `PATCH` with `application/json` for updating individual entities.
- **`X-Requested-With: XMLHttpRequest`** must be on API requests but NOT on login/module-switch (otherwise server returns AJAX fragments instead of full HTML).
- **`exclude_unset=True`** is used for update/create methods on entities where partial payloads are valid (bankverbindungen, person updates). NOT used for beiträge creation — the server requires all 12 `zahlungen` month fields even if `0.0`.
- **`populate_by_name = True`** is required on models used for PATCH updates with `exclude_unset=True`, otherwise setting fields via Python snake_case names isn't tracked as "set" by Pydantic when the model uses `alias=` fields.
- **Person creation duplicate detection**: The API returns 409 Conflict if a person with the same Vorname + Nachname + Geburtsdatum already exists. The 409 response body contains the existing person's details including their ID.
- **Personalnummer generation**: `POST /api/personen/personalnummer-generation` returns the next number in sequence but does NOT reserve it. If person creation fails (e.g. 409), the number may be reused for the next request.
- **Bankverbindung creation** requires `iban`, `bic` (must not be blank), `lastschriftart`. Mandatsreferenz format is validated (no underscores — use alphanumeric + hyphens).
- **Beitragsart `LASTSCHRIFT`** requires a Bankverbindung with `mandatsreferenz` and `mandatErteilt` already set.
- **Geschlecht enum values**: `MALE` (Männlich), `FEMALE` (Weiblich), `OTHER` (Divers), `LEGAL_ENTITY` (Juristisch).
- **Abteilung is mandatory** for person creation — `organisation.abteilungen` must have at least one entry (e.g. `"Einsatzabteilung FF"`).
- **Demo server**: `https://demo.feueron.de/spielversion-feueron` with `region_id="155"`. Production uses `region_id="156"`.
- **`/api/beitragsarten`** is NOT under `/api/personen/` — it's a top-level endpoint.

**Separation of concerns**: `tools/` contains reusable utilities (annotation engine, browser frame compositor). `scripts/` contains application-specific code (FeuerON login flow, marker coordinate definitions, migration logic, API client).

**Deployment**: GitHub Actions (`.github/workflows/docs.yml`) builds and deploys to GitHub Pages on push to main.

## Key Configuration

- `zensical.toml` — site config (navigation, theme, features)
- `pyproject.toml` — Python dependencies; requires Python 3.13+
- Package manager is `uv` (all Python commands use `uv run`)
