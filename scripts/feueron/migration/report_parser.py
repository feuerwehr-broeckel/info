"""Generic parser for paginated FeuerON CSV reports.

FeuerON reports share a common structure:
- Page 1 has metadata lines (title, selection criteria, count) followed by
  column headers and data rows.  Data cells have an extra empty column
  compared to subsequent pages (e.g. 9 columns vs 8).
- Each page ends with a ``Gesamtsumme`` footer and a ``Bearbeiter`` line.
- Pages 2+ repeat a shortened header (title + column headers) before data.

This module provides an iterator that yields only the data rows, together
with the current page-1 flag so callers can apply the correct column offset.
"""

from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import Iterator, NamedTuple


class ReportRow(NamedTuple):
    """A single data row from a FeuerON report."""

    cells: list[str]
    is_page1: bool


def iter_report_rows(path: Path) -> Iterator[ReportRow]:
    """Yield data rows from a paginated FeuerON CSV report.

    Strips all non-data rows: metadata headers, column headers (``Pos.``
    and any sub-header rows that follow), page footers (``Gesamtsumme``,
    ``Bearbeiter``), and report-title repetitions.

    The ``is_page1`` flag indicates whether the row belongs to page 1
    (which has an extra empty column compared to subsequent pages).
    """
    with open(path, encoding="utf-8-sig") as f:
        content = f.read()

    reader = csv.reader(io.StringIO(content), delimiter=";")
    is_page1 = True
    in_header = True  # True until we see the first data row on a page

    for row in reader:
        if not row:
            continue

        first = row[0].strip()

        # Footer marks end of a page
        if first.startswith("Gesamtsumme"):
            in_header = True
            continue

        # Bearbeiter line follows the footer — next data belongs to page 2+
        if first.startswith("Bearbeiter"):
            is_page1 = False
            in_header = True
            continue

        # A position number signals the start of data
        if first.isdigit():
            in_header = False
            yield ReportRow(cells=row, is_page1=is_page1)
            continue

        # While in the header zone, skip everything (metadata, column
        # headers, sub-headers, report-title repetitions)
        if in_header:
            continue

        # Continuation rows (e.g. multi-row entries in Bankverbindungen)
        yield ReportRow(cells=row, is_page1=is_page1)
