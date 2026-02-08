"""Feuerwehr Bröckel CLI — Typer application."""

from __future__ import annotations

import logging
from pathlib import Path

import typer

app = typer.Typer(help="Feuerwehr Bröckel tools.", no_args_is_help=True)
screenshots_app = typer.Typer(help="Screenshot pipeline.", no_args_is_help=True)
migration_app = typer.Typer(help="Fox112 → FeuerON data migration.", no_args_is_help=True)

app.add_typer(screenshots_app, name="screenshots")
app.add_typer(migration_app, name="migration")


# ---------------------------------------------------------------------------
# Screenshots
# ---------------------------------------------------------------------------


@screenshots_app.command()
def generate() -> None:
    """Run the full screenshot pipeline (capture → annotate → frame)."""
    from scripts.feueron.generate import (
        apply_annotations,
        apply_frames,
        generate_screenshots,
    )

    generate_screenshots()
    apply_annotations()
    apply_frames()


@screenshots_app.command()
def capture() -> None:
    """Take FeuerON screenshots with Playwright."""
    from scripts.feueron.generate import generate_screenshots

    generate_screenshots()


@screenshots_app.command()
def annotate() -> None:
    """Apply annotations to existing screenshots."""
    from scripts.feueron.generate import apply_annotations

    apply_annotations()


@screenshots_app.command()
def frame() -> None:
    """Wrap screenshots in browser frames."""
    from scripts.feueron.generate import apply_frames

    apply_frames()


# ---------------------------------------------------------------------------
# Migration
# ---------------------------------------------------------------------------


@migration_app.command("address-check")
def address_check(
    fox112_excel: Path = typer.Argument(help="Fox112 Excel export (.xlsx)."),
    feueron_adressenliste: Path = typer.Argument(
        help="FeuerON Adressenliste report (.csv)."
    ),
    output: Path = typer.Option(
        "address_update.csv", "--output", "-o", help="Output CSV file path."
    ),
    organisation: str = typer.Option(
        "Bröckel, OF", "--organisation", help="FeuerON organisation name."
    ),
) -> None:
    """Build a FeuerON address-update CSV from Fox112 master data."""
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
    )

    from scripts.feueron.migration.address_check import build_address_update

    build_address_update(
        fox112_excel, feueron_adressenliste, output, organisation=organisation
    )
    typer.echo(f"Written to {output}")
