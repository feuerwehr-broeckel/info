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
uv run info migration address-check FOX112.xlsx ADRESSENLISTE.csv -o output.csv
```

## Architecture

**Screenshot pipeline** (three-stage process orchestrated by `scripts/feueron/generate.py`):

1. **Capture** (`scripts/feueron/screenshots.py`): Playwright automates Chromium to log into FeuerON.de and capture pages at 1920x1080. Raw PNGs saved to `docs/assets/feueron/screenshots/raw/`.

2. **Annotate** (`scripts/feueron/annotations.py` + `tools/annotation.py`): Marker definitions (rectangles/circles with labels, colors, opacity) are applied to raw screenshots using Pillow. Output goes to `docs/assets/feueron/screenshots/annotated/`.

3. **Frame** (`tools/browserframe.py`): Screenshots are composited into browser window chrome using 9-slice scaling with template images from `tools/assets/`. Output goes to `docs/assets/feueron/screenshots/framed/`.

**Separation of concerns**: `tools/` contains reusable utilities (annotation engine, browser frame compositor). `scripts/` contains application-specific code (FeuerON login flow, marker coordinate definitions).

**Deployment**: GitHub Actions (`.github/workflows/docs.yml`) builds and deploys to GitHub Pages on push to main.

## Key Configuration

- `zensical.toml` — site config (navigation, theme, features)
- `pyproject.toml` — Python dependencies; requires Python 3.13+
- Package manager is `uv` (all Python commands use `uv run`)
