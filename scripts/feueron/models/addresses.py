"""FeuerON CSV import models for address data (Adressen)."""

from __future__ import annotations

from scripts.feueron.models.base import (
    AdrTelArt,
    FeuerONBase,
    FeuerONDate,
    FeuerONRecord,
    FeuerONTimestamp,
    Geschlecht,
    Str10,
    Str40,
    Str50,
    Str80,
)


# ---------------------------------------------------------------------------
# 6.1 Adressstammdaten
# ---------------------------------------------------------------------------


class AdrSta(FeuerONBase):
    """Adressstammdaten (ADR_STA) - core address data."""

    @classmethod
    def table_name(cls) -> str:
        return "ADR_STA"

    # Required
    NAME1: Str80
    GESCHLECHT: Geschlecht

    # Optional
    TITEL_ADRESSE: Str80 | None = None
    NAME2: Str80 | None = None
    NAME3: Str80 | None = None
    NAME4: Str80 | None = None
    STRASSE: Str80 | None = None
    HAUSNUMMER: Str10 | None = None
    LAND: Str50 | None = None
    PLZ: Str10 | None = None
    ORT: Str80 | None = None
    TITEL: Str40 | None = None
    ANREDE: Str80 | None = None
    BRIEFTITEL: Str40 | None = None
    ANREDEKURZ: Str10 | None = None
    VORNAME: Str50 | None = None
    NACHNAME: Str50 | None = None
    GEBURT: FeuerONDate | None = None
    FUNKTION: Str80 | None = None


# ---------------------------------------------------------------------------
# 6.2 Erreichbarkeiten
# ---------------------------------------------------------------------------


class AdrErb(FeuerONBase):
    """Erreichbarkeiten (ADR_ERB) - contact details for an address."""

    @classmethod
    def table_name(cls) -> str:
        return "ADR_ERB"

    # Required
    ART: AdrTelArt
    NUMMER: Str80

    # Optional
    BESCHR: Str80 | None = None
    INFO: str | None = None  # Memo


# ---------------------------------------------------------------------------
# 6.3 Kontakte
# ---------------------------------------------------------------------------


class AdrKontakte(FeuerONBase):
    """Kontakte (ADR_KONTAKTE) - contact history for an address."""

    @classmethod
    def table_name(cls) -> str:
        return "ADR_KONTAKTE"

    # Required
    BETREFF: Str80
    SORTID: int

    # Optional
    DATUM: FeuerONTimestamp | None = None
    ART: Str40 | None = None
    BESCHREIBUNG: str | None = None  # Memo


# ---------------------------------------------------------------------------
# Top-level record
# ---------------------------------------------------------------------------


class AddressRecord(FeuerONRecord):
    """A complete address record for FeuerON CSV import."""

    stammdaten: AdrSta
    erreichbarkeiten: list[AdrErb] = []
    kontakte: list[AdrKontakte] = []
