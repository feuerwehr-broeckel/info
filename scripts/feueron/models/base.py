"""Shared base classes, custom types, enums, and CSV generation for FeuerON import models."""

from __future__ import annotations

import csv
import datetime
import io
import types
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import Annotated, Any, get_args, get_origin

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    PlainSerializer,
    StringConstraints,
)

# ---------------------------------------------------------------------------
# Reusable constrained string types
# ---------------------------------------------------------------------------

Str2 = Annotated[str, StringConstraints(max_length=2)]
Str3 = Annotated[str, StringConstraints(max_length=3)]
Str5 = Annotated[str, StringConstraints(max_length=5)]
Str6 = Annotated[str, StringConstraints(max_length=6)]
Str8 = Annotated[str, StringConstraints(max_length=8)]
Str10 = Annotated[str, StringConstraints(max_length=10)]
Str15 = Annotated[str, StringConstraints(max_length=15)]
Str20 = Annotated[str, StringConstraints(max_length=20)]
Str25 = Annotated[str, StringConstraints(max_length=25)]
Str30 = Annotated[str, StringConstraints(max_length=30)]
Str32 = Annotated[str, StringConstraints(max_length=32)]
Str35 = Annotated[str, StringConstraints(max_length=35)]
Str39 = Annotated[str, StringConstraints(max_length=39)]
Str40 = Annotated[str, StringConstraints(max_length=40)]
Str46 = Annotated[str, StringConstraints(max_length=46)]
Str50 = Annotated[str, StringConstraints(max_length=50)]
Str67 = Annotated[str, StringConstraints(max_length=67)]
Str80 = Annotated[str, StringConstraints(max_length=80)]
Str100 = Annotated[str, StringConstraints(max_length=100)]
Str200 = Annotated[str, StringConstraints(max_length=200)]
Str300 = Annotated[str, StringConstraints(max_length=300)]

# ---------------------------------------------------------------------------
# FeuerON date / time / boolean custom types
# ---------------------------------------------------------------------------


def _parse_feueron_date(value: str | datetime.date) -> datetime.date:
    if isinstance(value, datetime.date):
        return value
    return datetime.datetime.strptime(value, "%d.%m.%Y").date()


def _serialize_feueron_date(value: datetime.date) -> str:
    return value.strftime("%d.%m.%Y")


FeuerONDate = Annotated[
    datetime.date,
    BeforeValidator(_parse_feueron_date),
    PlainSerializer(_serialize_feueron_date),
]


def _parse_feueron_time(value: str | datetime.time) -> datetime.time:
    if isinstance(value, datetime.time):
        return value
    return datetime.datetime.strptime(value, "%H:%M").time()


def _serialize_feueron_time(value: datetime.time) -> str:
    return value.strftime("%H:%M")


FeuerONTime = Annotated[
    datetime.time,
    BeforeValidator(_parse_feueron_time),
    PlainSerializer(_serialize_feueron_time),
]


def _parse_feueron_timestamp(value: str | datetime.datetime) -> datetime.datetime:
    if isinstance(value, datetime.datetime):
        return value
    return datetime.datetime.strptime(value, "%d.%m.%Y %H:%M")


def _serialize_feueron_timestamp(value: datetime.datetime) -> str:
    return value.strftime("%d.%m.%Y %H:%M")


FeuerONTimestamp = Annotated[
    datetime.datetime,
    BeforeValidator(_parse_feueron_timestamp),
    PlainSerializer(_serialize_feueron_timestamp),
]


def _parse_feueron_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(int(value))
    if isinstance(value, str):
        return bool(int(value))
    return bool(value)


def _serialize_feueron_bool(value: bool) -> str:
    return "1" if value else "0"


FeuerONBool = Annotated[
    bool,
    BeforeValidator(_parse_feueron_bool),
    PlainSerializer(_serialize_feueron_bool),
]

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class Geschlecht(StrEnum):
    MAENNLICH = "M"
    WEIBLICH = "F"
    JURISTISCH = "J"


class AusbildungErfolg(IntEnum):
    """Training outcome codes (PV_AUSB.ERFOLG)."""

    TEILGENOMMEN = 0
    ERFOLGREICH = 1
    ANGEMELDET = 2
    TEILNAHMEWUNSCH = 3
    NICHT_BERUECKSICHTIGT = 4


class BeitragArt(IntEnum):
    """Payment method (PV_BEITRAG.ART)."""

    RECHNUNG = 0
    LASTSCHRIFT = 1
    KASSIERER = 2
    SELBSTUEBERWEISER = 3


class Zahlungsweise(IntEnum):
    """Payment frequency (PV_BEITRAG.ZAHLUNGSWEISE)."""

    JAEHRLICH = 1
    HALBJAEHRLICH = 2
    VIERTELJAEHRLICH = 4
    MONATLICH = 12


class TelArt(StrEnum):
    """Contact type for PV_TELEP."""

    EMAIL_DIENSTLICH = "E-Mail dienstlich"
    EMAIL_PRIVAT = "E-Mail privat"
    MOBIL_DIENSTLICH = "Mobil dienstlich"
    MOBIL_PRIVAT = "Mobil privat"
    TELEFAX_DIENSTLICH = "Telefax dienstlich"
    TELEFAX_PRIVAT = "Telefax privat"
    TELEFON_DIENSTLICH = "Telefon dienstlich"
    TELEFON_PRIVAT = "Telefon privat"


class AdrTelArt(StrEnum):
    """Contact type for ADR_ERB (includes Notfalltelefon)."""

    EMAIL_DIENSTLICH = "E-Mail dienstlich"
    EMAIL_PRIVAT = "E-Mail privat"
    MOBIL_DIENSTLICH = "Mobil dienstlich"
    MOBIL_PRIVAT = "Mobil privat"
    TELEFAX_DIENSTLICH = "Telefax dienstlich"
    TELEFAX_PRIVAT = "Telefax privat"
    TELEFON_DIENSTLICH = "Telefon dienstlich"
    TELEFON_PRIVAT = "Telefon privat"
    NOTFALLTELEFON = "Notfalltelefon (24/7)"


class PrModul(StrEnum):
    """Equipment module types (PR_STAMM.FK_PR_MODUL)."""

    ATEMSCHUTZ = "Atemschutz"
    FAHRZEUGE = "Fahrzeuge"
    FUNKTECHNIK = "Funktechnik"
    GERAETE_ALLGEMEIN = "Geräte allgemein"
    LAGERBESTAENDE = "Lagerbestände"
    PERSOENLICHE_AUSRUESTUNG = "Persönliche Ausrüstung"


# ---------------------------------------------------------------------------
# Base model classes
# ---------------------------------------------------------------------------


class FeuerONBase(BaseModel):
    """Base for all FeuerON sub-table models."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
    )

    @classmethod
    def table_name(cls) -> str:
        """Return the FeuerON table name (e.g. 'PV_DB'). Must be overridden."""
        raise NotImplementedError

    @classmethod
    def csv_field_names(cls) -> list[str]:
        """Return the ordered list of field names matching the CSV header."""
        return list(cls.model_fields.keys())


class FeuerONRecord(BaseModel):
    """Base for top-level record types (PersonRecord, EquipmentRecord, AddressRecord)."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
    )


# ---------------------------------------------------------------------------
# CSV generation
# ---------------------------------------------------------------------------


def _resolve_sub_table_info(
    record_cls: type[FeuerONRecord],
) -> list[tuple[str, type[FeuerONBase], bool]]:
    """Introspect a FeuerONRecord subclass to discover its sub-table fields.

    Returns a list of (field_name, sub_table_model_class, is_list) in declaration order.
    """
    result: list[tuple[str, type[FeuerONBase], bool]] = []
    for name, field_info in record_cls.model_fields.items():
        annotation = field_info.annotation
        model_cls, is_list = _extract_model_class(annotation)
        if model_cls is not None:
            result.append((name, model_cls, is_list))
    return result


def _extract_model_class(
    annotation: Any,
) -> tuple[type[FeuerONBase] | None, bool]:
    """Extract the FeuerONBase subclass and list-ness from a type annotation."""
    origin = get_origin(annotation)

    # list[SomeModel]
    if origin is list:
        args = get_args(annotation)
        if args and isinstance(args[0], type) and issubclass(args[0], FeuerONBase):
            return args[0], True
        return None, False

    # Optional[SomeModel] = Union[SomeModel, None]
    if origin is types.UnionType:
        args = get_args(annotation)
        for arg in args:
            if isinstance(arg, type) and issubclass(arg, FeuerONBase):
                return arg, False
        return None, False

    # Direct SomeModel
    if isinstance(annotation, type) and issubclass(annotation, FeuerONBase):
        return annotation, False

    return None, False


def _get_entries(
    record: FeuerONRecord,
    field_name: str,
    is_list: bool,
) -> list[FeuerONBase]:
    """Get the sub-table entries for a field as a list."""
    value = getattr(record, field_name)
    if value is None:
        return []
    if is_list:
        return list(value)
    return [value]


def _serialize_value(value: Any) -> str | int | float:
    """Convert a single field value to its CSV representation.

    Returns int/float for numeric values so that csv.QUOTE_NONNUMERIC
    writes them unquoted (FeuerON requires this for fields like
    ZAHLUNGSWEISE and ART).
    """
    if value is None:
        return ""
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return value
    return str(value)


def generate_csv(
    records: list[FeuerONRecord],
    output: Path | io.StringIO,
    *,
    delimiter: str = ";",
    encoding: str = "utf-8",
) -> None:
    """Generate a FeuerON-compatible CSV file from a list of records.

    All records must be of the same type (e.g. all PersonRecord).
    """
    if not records:
        return

    record_cls = type(records[0])
    sub_table_info = _resolve_sub_table_info(record_cls)

    # 1. Determine max count of each sub-table across all records
    max_counts: dict[str, int] = {}
    for field_name, _model_cls, is_list in sub_table_info:
        max_n = 0
        for record in records:
            entries = _get_entries(record, field_name, is_list)
            max_n = max(max_n, len(entries))
        # Ensure at least 1 for sub-tables that have data somewhere
        if max_n > 0:
            max_counts[field_name] = max_n

    # 2. Determine which fields per sub-table actually have data
    used_fields: dict[str, list[str]] = {}
    for field_name, model_cls, is_list in sub_table_info:
        if field_name not in max_counts:
            continue
        all_csv_fields = model_cls.csv_field_names()
        populated: set[str] = set()
        for record in records:
            for entry in _get_entries(record, field_name, is_list):
                data = entry.model_dump(mode="json")
                for csv_field in all_csv_fields:
                    if data.get(csv_field) is not None:
                        populated.add(csv_field)
        # Keep original declaration order, but only populated fields
        used_fields[field_name] = [f for f in all_csv_fields if f in populated]

    # 3. Build headers
    headers: list[str] = []
    for field_name, model_cls, _is_list in sub_table_info:
        count = max_counts.get(field_name, 0)
        csv_fields = used_fields.get(field_name, [])
        if count == 0 or not csv_fields:
            continue
        table = model_cls.table_name()
        for n in range(1, count + 1):
            for csv_field in csv_fields:
                headers.append(f"{table}.{n}.{csv_field}")

    # 4. Build rows
    rows: list[list[str | int | float]] = []
    for record in records:
        row: list[str | int | float] = []
        for field_name, model_cls, is_list in sub_table_info:
            count = max_counts.get(field_name, 0)
            csv_fields = used_fields.get(field_name, [])
            if count == 0 or not csv_fields:
                continue
            entries = _get_entries(record, field_name, is_list)
            num_fields = len(csv_fields)
            for n in range(count):
                if n < len(entries):
                    data = entries[n].model_dump(mode="json")
                    for csv_field in csv_fields:
                        row.append(_serialize_value(data.get(csv_field)))
                else:
                    row.extend([""] * num_fields)
        rows.append(row)

    # 5. Write CSV
    if isinstance(output, Path):
        with open(output, "w", newline="", encoding=encoding) as f:
            writer = csv.writer(f, delimiter=delimiter, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(headers)
            writer.writerows(rows)
    else:
        writer = csv.writer(output, delimiter=delimiter, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(headers)
        writer.writerows(rows)
