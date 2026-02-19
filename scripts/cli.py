"""Feuerwehr Bröckel CLI — Typer application."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import typer

app = typer.Typer(help="Feuerwehr Bröckel tools.", no_args_is_help=True)
screenshots_app = typer.Typer(help="Screenshot pipeline.", no_args_is_help=True)
migration_app = typer.Typer(
    help="Fox112 → FeuerON data migration.", no_args_is_help=True
)

api_app = typer.Typer(help="FeuerON REST API client.", no_args_is_help=True)

app.add_typer(screenshots_app, name="screenshots")
app.add_typer(migration_app, name="migration")
app.add_typer(api_app, name="api")


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


@migration_app.command("bank-check")
def bank_check(
    fox112_excel: Path = typer.Argument(help="Fox112 Excel export (.xlsx)."),
    feueron_bankverbindungen: Path = typer.Argument(
        help="FeuerON Bankverbindungen report (.csv)."
    ),
    output: Path = typer.Option(
        "bank_update.csv", "--output", "-o", help="Output CSV file path."
    ),
    organisation: str = typer.Option(
        "Bröckel, OF", "--organisation", help="FeuerON organisation name."
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts."),
) -> None:
    """Build a FeuerON bank-detail-update CSV from Fox112 master data."""
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
    )

    from scripts.feueron.migration.bank_check import build_bank_update

    build_bank_update(
        fox112_excel,
        feueron_bankverbindungen,
        output,
        organisation=organisation,
        yes=yes,
    )
    typer.echo(f"Written to {output}")


@migration_app.command("contact-check")
def contact_check(
    fox112_excel: Path = typer.Argument(help="Fox112 Excel export (.xlsx)."),
    feueron_erreichbarkeiten: Path = typer.Argument(
        help="FeuerON Erreichbarkeiten report (.xlsx)."
    ),
    output: Path = typer.Option(
        "contact_update.csv", "--output", "-o", help="Output CSV file path."
    ),
    organisation: str = typer.Option(
        "Bröckel, OF", "--organisation", help="FeuerON organisation name."
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts."),
) -> None:
    """Build a FeuerON contact-update CSV (address + phone + email) from Fox112."""
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
    )

    from scripts.feueron.migration.contact_check import build_contact_update

    build_contact_update(
        fox112_excel,
        feueron_erreichbarkeiten,
        output,
        organisation=organisation,
        yes=yes,
    )
    typer.echo(f"Written to {output}")


@migration_app.command("passive-import")
def passive_import(
    fox112_excel: Path = typer.Argument(help="Fox112 Excel export (.xlsx)."),
    feueron_erreichbarkeiten: Path = typer.Argument(
        help="FeuerON Erreichbarkeiten report (.xlsx)."
    ),
    fox112_xml: Path = typer.Argument(help="Fox112 Personaldaten XML export."),
    output: Path = typer.Option(
        "passive_import.csv",
        "--output",
        "-o",
        help="Output CSV (persons with Beiträge).",
    ),
    output_no_beitrag: Path = typer.Option(
        "passive_import_no_beitrag.csv",
        "--output-no-beitrag",
        help="Output CSV (persons without Beiträge).",
    ),
    organisation: str = typer.Option(
        "Bröckel, OF", "--organisation", help="FeuerON organisation name."
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts."),
) -> None:
    """Import passive Fox112 members (Fördernde Mitglieder) into FeuerON.

    Produces two CSV files: one for persons with Beiträge data and one for
    persons without, since FeuerON cannot handle mixed rows.
    """
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
    )

    from scripts.feueron.migration.passive_import import build_passive_import

    build_passive_import(
        fox112_excel,
        feueron_erreichbarkeiten,
        fox112_xml,
        output,
        output_no_beitrag,
        organisation=organisation,
        yes=yes,
    )
    typer.echo(f"Written to {output} and {output_no_beitrag}")


@migration_app.command("dedup-erreichbarkeiten")
def dedup_erreichbarkeiten_cmd(
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Only show what would be removed."
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompts."),
    base_url: str = typer.Option(
        "https://www.feueron.de/feueron",
        "--base-url",
        help="FeuerON base URL.",
    ),
) -> None:
    """Remove duplicate Erreichbarkeiten entries created by CSV import."""
    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
    )

    from scripts.feueron.api import FeuerONClient
    from scripts.feueron.migration.erreichbarkeiten_dedup import (
        dedup_erreichbarkeiten,
    )

    with FeuerONClient(base_url) as client:
        dedup_erreichbarkeiten(client, dry_run=dry_run, yes=yes)


# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------


@api_app.command("search")
def api_search(
    query: str = typer.Argument(help="Search string for person lookup."),
    org_id: int | None = typer.Option(
        None, "--org-id", help="FeuerON organisation ID (auto-detected if omitted)."
    ),
    base_url: str = typer.Option(
        "https://www.feueron.de/feueron",
        "--base-url",
        help="FeuerON base URL.",
    ),
) -> None:
    """Search persons in FeuerON via the REST API."""
    import json

    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
    )

    from scripts.feueron.api import FeuerONClient

    kwargs: dict[str, Any] = {}
    if org_id is not None:
        kwargs["organisation_id"] = org_id

    with FeuerONClient(base_url, **kwargs) as client:
        results = client.get_personen(search=query)
        typer.echo(
            json.dumps(
                [r.model_dump(by_alias=True) for r in results],
                indent=2,
                ensure_ascii=False,
            )
        )


@api_app.command("erreichbarkeiten")
def api_erreichbarkeiten(
    person_id: int = typer.Argument(help="FeuerON person ID."),
    base_url: str = typer.Option(
        "https://www.feueron.de/feueron",
        "--base-url",
        help="FeuerON base URL.",
    ),
) -> None:
    """Fetch contact details (Erreichbarkeiten) for a person."""
    import json

    from rich.logging import RichHandler

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False)],
    )

    from scripts.feueron.api import FeuerONClient

    with FeuerONClient(base_url) as client:
        results = client.get_erreichbarkeiten(person_id)
        typer.echo(
            json.dumps(
                [r.model_dump(by_alias=True) for r in results],
                indent=2,
                ensure_ascii=False,
            )
        )
