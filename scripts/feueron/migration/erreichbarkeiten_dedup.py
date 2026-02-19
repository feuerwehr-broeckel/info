"""Deduplicate Erreichbarkeiten entries created by CSV import.

The FeuerON CSV import *adds* contact entries rather than updating existing
ones.  This script detects duplicates of the same ``art`` (e.g. two
"E-Mail privat" entries) via the REST API and removes the duplicate,
keeping the sanitised value where applicable.
"""

from __future__ import annotations

import logging
from collections import defaultdict

import phonenumbers
import typer

from scripts.feueron.api import FeuerONClient
from scripts.feueron.api.models import Erreichbarkeit

logger = logging.getLogger(__name__)

# art values that contain phone numbers (vs. emails)
_PHONE_ARTS = {
    "Telefon privat",
    "Telefon dienstlich",
    "Mobil privat",
    "Mobil dienstlich",
    "Telefax privat",
    "Telefax dienstlich",
}


def _normalise_phone(raw: str) -> str:
    """Parse a phone string to E.164 for comparison purposes."""
    try:
        parsed = phonenumbers.parse(raw, "DE")
        return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    except phonenumbers.NumberParseException:
        return raw


def _is_national_format(raw: str) -> bool:
    """Return True if *raw* is already in German national format."""
    try:
        parsed = phonenumbers.parse(raw, "DE")
        national = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.NATIONAL
        )
        return raw == national
    except phonenumbers.NumberParseException:
        return False


def _pick_removal(art: str, entries: list[Erreichbarkeit]) -> list[Erreichbarkeit]:
    """Decide which entries to remove from a group of same-art duplicates.

    Returns a list of entries to remove (may be empty).
    """
    to_remove: list[Erreichbarkeit] = []

    # Compare all pairs; for N>2 duplicates, iteratively remove obvious dupes.
    kept: list[Erreichbarkeit] = list(entries)

    for i in range(len(kept)):
        for j in range(i + 1, len(kept)):
            a, b = kept[i], kept[j]
            if a in to_remove or b in to_remove:
                continue

            val_a = a.kontaktdaten
            val_b = b.kontaktdaten

            if art in _PHONE_ARTS:
                norm_a = _normalise_phone(val_a)
                norm_b = _normalise_phone(val_b)
                if norm_a == norm_b:
                    # Same number — keep the one in national format,
                    # or the lower ID (original) if both are equal.
                    a_ok = _is_national_format(val_a)
                    b_ok = _is_national_format(val_b)
                    if a_ok and not b_ok:
                        to_remove.append(b)
                    elif b_ok and not a_ok:
                        to_remove.append(a)
                    else:
                        # Both formatted the same — remove higher ID (import).
                        victim = b if int(b.id) > int(a.id) else a
                        to_remove.append(victim)
                else:
                    logger.warning(
                        "  %s: values differ (%s vs %s) — skipped",
                        art,
                        val_a,
                        val_b,
                    )
            else:
                # Email or other: case-insensitive comparison
                if val_a.lower() == val_b.lower():
                    victim = b if int(b.id) > int(a.id) else a
                    to_remove.append(victim)
                else:
                    logger.warning(
                        "  %s: values differ (%s vs %s) — skipped",
                        art,
                        val_a,
                        val_b,
                    )

    return to_remove


def dedup_erreichbarkeiten(
    client: FeuerONClient,
    *,
    dry_run: bool = False,
    yes: bool = False,
) -> None:
    """Find and remove duplicate Erreichbarkeiten for all persons."""
    persons = client.get_personen()
    logger.info("Found %d persons", len(persons))

    total_removed = 0
    total_skipped = 0

    for person in persons:
        pid = person.id
        name = f"{person.vorname} {person.nachname}"

        entries = client.get_erreichbarkeiten(pid)
        if not entries:
            continue

        # Group by art
        by_art: dict[str, list[Erreichbarkeit]] = defaultdict(list)
        for entry in entries:
            by_art[entry.art].append(entry)

        # Find removals across all arts
        removals: list[Erreichbarkeit] = []
        for art, group in by_art.items():
            if len(group) < 2:
                continue
            removals.extend(_pick_removal(art, group))

        if not removals:
            continue

        # Display proposed changes (show keep vs remove per art group)
        removal_ids = {e.id for e in removals}
        logger.info("%s (id=%s):", name, pid)
        for art, group in by_art.items():
            if len(group) < 2:
                continue
            for entry in group:
                if entry.id in removal_ids:
                    logger.info(
                        "  REMOVE %s: %s (id=%s)",
                        entry.art,
                        entry.kontaktdaten,
                        entry.id,
                    )
                else:
                    logger.info(
                        "  KEEP   %s: %s (id=%s)",
                        entry.art,
                        entry.kontaktdaten,
                        entry.id,
                    )

        if dry_run:
            total_removed += len(removals)
            continue

        if not yes and not typer.confirm("  Delete these entries?", default=False):
            total_skipped += len(removals)
            continue

        # Execute removal (lock → delete → unlock)
        removed_ids = {e.id for e in removals}
        client.lock_person(pid)
        try:
            result = client.delete_erreichbarkeiten(pid, list(removed_ids))
        finally:
            client.unlock_person(pid)

        # Verify the removed entries are actually gone
        remaining_ids = {e.id for e in result}
        still_present = removed_ids & remaining_ids
        if still_present:
            logger.error(
                "  FAILED: entries %s still present after PATCH", still_present
            )
            for e in result:
                logger.error("  RESPONSE: %s: %s (id=%s)", e.art, e.kontaktdaten, e.id)
        else:
            for e in removals:
                logger.info("  DELETED %s: %s (id=%s)", e.art, e.kontaktdaten, e.id)
            total_removed += len(removals)

    if dry_run:
        logger.info("Dry run: %d entries would be removed", total_removed)
    else:
        logger.info("Done: %d removed, %d skipped", total_removed, total_skipped)
