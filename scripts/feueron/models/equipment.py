"""FeuerON CSV import models for equipment data (Technik)."""

from __future__ import annotations

from scripts.feueron.models.base import (
    FeuerONBase,
    FeuerONBool,
    FeuerONDate,
    FeuerONRecord,
    FeuerONTimestamp,
    PrModul,
    Str2,
    Str3,
    Str5,
    Str10,
    Str15,
    Str20,
    Str30,
    Str35,
    Str39,
    Str40,
    Str50,
    Str80,
    Str100,
    Str200,
)


# ---------------------------------------------------------------------------
# 5.1 Gerätestammdaten
# ---------------------------------------------------------------------------


class PrStamm(FeuerONBase):
    """Gerätestammdaten (PR_STAMM) - core equipment data."""

    @classmethod
    def table_name(cls) -> str:
        return "PR_STAMM"

    # Required
    FK_PR_MODUL: PrModul
    FK_PR_ART: Str80
    FK_PR_TYP: Str80
    GERAETENR: Str50

    # Optional
    BARCODE: Str35 | None = None
    RFID: Str35 | None = None
    STATISTIK1: Str80 | None = None
    HERSTELL: Str50 | None = None
    HERSTELLNR: Str30 | None = None
    HERSTELLD: FeuerONDate | None = None
    LIEFERAN: Str50 | None = None
    LIEFERD: FeuerONDate | None = None
    ANSCHKOST: float | None = None
    GARANTIE: FeuerONDate | None = None
    FUNKTION: FeuerONBool | None = None
    INVENTARNR: Str30 | None = None
    EIGENTUE: Str50 | None = None
    BESITZER: Str50 | None = None
    BEMERKUNG: str | None = None  # Memo
    AUSGEMUST: FeuerONDate | None = None
    AUSGEGRUND: Str30 | None = None
    INDIENST: FeuerONDate | None = None
    SELEKTION1: Str80 | None = None
    SELEKTION2: Str80 | None = None
    ABGENOMMEN: FeuerONDate | None = None
    RECHNUNGSNR: Str50 | None = None
    RECHNUNGSDATUM: FeuerONDate | None = None
    LAGERSTANDORT: Str100 | None = None
    STANDORTZUSATZ: Str50 | None = None
    REIHE: Str80 | None = None
    EBENE: Str80 | None = None
    FREIGABEUORG: FeuerONBool | None = None
    AKT_KM: float | None = None
    AKT_KM_DATE: FeuerONDate | None = None
    VERSICHERUNGAB: FeuerONBool | None = None
    VERSPOLICE: Str80 | None = None
    VERSKLASSE: Str80 | None = None
    LEASKENNZEICHEN: Str100 | None = None
    LEASERSTBESCHAFFDAT: FeuerONDate | None = None
    LEASABLAUFDAT: FeuerONDate | None = None
    SERIENNR: Str30 | None = None
    AMTPRUEFNR: Str15 | None = None


# ---------------------------------------------------------------------------
# 5.2 / 5.3 Stammdaten für Geräte allgemein / Persönliche Ausrüstung
# ---------------------------------------------------------------------------


class PrsEm(FeuerONBase):
    """Stammdaten Geräte allgemein / Persönliche Ausrüstung (PRS_EM).

    For 'Geräte allgemein': all fields may be used.
    For 'Persönliche Ausrüstung': only GROESSE is relevant.
    """

    @classmethod
    def table_name(cls) -> str:
        return "PRS_EM"

    # All optional
    LEISTUNG: float | None = None
    LSTG_OUT: float | None = None
    LSTG_EINH: Str5 | None = None
    LAENGE: float | None = None
    GROESSE: float | None = None
    BREITE: float | None = None
    VOLUMEN: float | None = None
    HOEHE: float | None = None
    GEWICHT: float | None = None
    DURCHMESS: float | None = None
    MATERIAL: Str20 | None = None
    BESONDER: Str30 | None = None
    BETRIEBSSTUNDEN: float | None = None
    FABRIKMARKE: Str50 | None = None
    FABRIKNUMMER: Str50 | None = None


# ---------------------------------------------------------------------------
# 5.4 Stammdaten für Funkmeldeempfänger
# ---------------------------------------------------------------------------


class PrsFme(FeuerONBase):
    """Stammdaten Funkmeldeempfänger (PRS_FME) - pager devices."""

    @classmethod
    def table_name(cls) -> str:
        return "PRS_FME"

    # Required
    BEREICH: Str10

    # Optional
    FREQUENZ: Str30 | None = None
    LADEGTYP: Str40 | None = None
    ZUSATZGERAT1: Str30 | None = None
    ZUSATZGERAT2: Str30 | None = None
    ZUSATZGERAT3: Str30 | None = None
    AMT_REGNR: Str15 | None = None
    FEUERALARM: Str80 | None = None
    HEULTON: Str80 | None = None
    PROBEALARM: Str80 | None = None


# ---------------------------------------------------------------------------
# 5.5 Stammdaten für Funkgeräte
# ---------------------------------------------------------------------------


class PrsFuge(FeuerONBase):
    """Stammdaten Funkgeräte (PRS_FUGE) - radio devices."""

    @classmethod
    def table_name(cls) -> str:
        return "PRS_FUGE"

    # All optional
    ORTSFEST: FeuerONBool | None = None
    KANAL: Str3 | None = None
    SENDE_P: Str2 | None = None
    SERIENNUS: Str39 | None = None
    BEDIENTYP: Str15 | None = None
    SERIENNUB: Str39 | None = None
    ANT_TYP: Str30 | None = None
    LADEGTYP: Str40 | None = None
    AMT_REGNR: Str15 | None = None
    ZUSATZG_1: Str30 | None = None
    ZUSATZG_2: Str30 | None = None
    ZUSATZG_3: Str30 | None = None
    HAFMSTYP: Str20 | None = None
    HAFMSHERST: Str50 | None = None
    HAFMSNR: Str20 | None = None
    FMSKENN: Str20 | None = None
    HANDAPPAUSF: Str80 | None = None
    FUNKNAME: Str50 | None = None


# ---------------------------------------------------------------------------
# 5.6 Stammdaten für Fahrzeuge
# ---------------------------------------------------------------------------


class PrsFp(FeuerONBase):
    """Stammdaten Fahrzeuge (PRS_FP) - vehicle details."""

    @classmethod
    def table_name(cls) -> str:
        return "PRS_FP"

    # All optional
    HAT_BESATZUNG: FeuerONBool | None = None
    FMS_CODE: Str20 | None = None
    KENNZEICHEN: Str15 | None = None
    EZ: FeuerONDate | None = None
    TREIBS_ART: Str20 | None = None
    KATS_EINHEIT: Str80 | None = None
    KATS_EINHEIT_KURZ: Str80 | None = None
    HYDRAULISCHER_RETTUNGSSATZ: FeuerONBool | None = None
    BAT1_TYP: Str80 | None = None
    BAT1_ORT: Str35 | None = None
    BAT1_HERST: Str50 | None = None
    BAT1_MASS: Str35 | None = None
    BAT1_DATUM: FeuerONDate | None = None
    ZUSATZBATTERIE: Str80 | None = None
    ZBATEINBAUDATUM: FeuerONDate | None = None
    ZAHL_ACHS: int | None = None
    LANGE: float | None = None
    BREITE: float | None = None
    HOHE: float | None = None
    MOT_HUBRAU: float | None = None
    MOT_LEIST: float | None = None
    LEERGEW: float | None = None
    ZUL_GEW: float | None = None
    BEREIFUNG: str | None = None  # Memo
    BESCHAFFUNG_KM: float | None = None
    LEASING: FeuerONBool | None = None
    LEASING_ABLAUF_KM: float | None = None
    LEASING_ABLAUF_DATE: FeuerONDate | None = None
    FAHRGESTELLNR: Str80 | None = None
    FAHRGESTELLTYP: Str80 | None = None
    LOESCHWASSERTANK: Str80 | None = None
    SCHAUMMITTELTANK: Str80 | None = None
    PULVERVORRAT: Str80 | None = None
    AUFBAUNR: Str80 | None = None
    AUFBAUTYP: Str80 | None = None
    AUFBAUHERSTELLER: Str80 | None = None
    AUFBHERSTELLDATUM: FeuerONDate | None = None
    MOTORTYP: Str80 | None = None
    BETRIEBSSTUNDEN: float | None = None
    FZGBRIEFNR: Str80 | None = None
    BRIEF_NR: Str80 | None = None
    BESONDERHEIT: Str80 | None = None
    SCHL_NR_1: Str20 | None = None
    SCHL_NR_2: Str20 | None = None
    ALASTGEBREMST: float | None = None
    ALASTUNGEBREMST: float | None = None
    BEREIFVORN: Str80 | None = None
    MONTIERTVORN: FeuerONDate | None = None
    BEREIFHERSTELLDATUMV: FeuerONDate | None = None
    BEREIFKMSTANDV: float | None = None
    BEREIFH: Str80 | None = None
    MONTIERTH: FeuerONDate | None = None
    BEREIFHERSTELLDATUMH: FeuerONDate | None = None
    BEREIFKMSTANDH: float | None = None
    FUNKNAME: Str50 | None = None


# ---------------------------------------------------------------------------
# 5.7 Stammdaten für Lagerartikel
# ---------------------------------------------------------------------------


class PrsLager(FeuerONBase):
    """Stammdaten Lagerartikel (PRS_LAGER) - inventory items."""

    @classmethod
    def table_name(cls) -> str:
        return "PRS_LAGER"

    # Required
    CHARGEN_BEZEICHNUNG: Str80
    CHARGEN_ABLAUFDAT: FeuerONDate

    # Optional
    BEZEICH: Str80 | None = None
    STANDORT: Str100 | None = None
    REGAL: Str100 | None = None
    REIHE: Str100 | None = None
    EBENE: Str100 | None = None
    BESTAND: int | None = None
    SOLL: int | None = None
    MELDE: int | None = None
    MINDEST: int | None = None
    VERKAUFS_EINHEIT: Str80 | None = None
    VERKAUFS_EINHEIT_ANZAHL: int | None = None
    VERPACKUNGS_EINHEIT: int | None = None
    ART_VERPACKUNGS_EINHEIT: Str80 | None = None
    VERPACKUNGS_EINHEIT_ANZAHL: int | None = None
    MENGE_IN_VERPACKUNGSEINHEIT: int | None = None
    LADE_HILFSMITTEL: Str80 | None = None
    LADE_EINHEIT: int | None = None
    LADE_HILFSMITTEL_STUECK: int | None = None
    LADEHILFSMITTEL_VERPACKTE_EINHEITEN: int | None = None
    EINHEIT: Str80 | None = None
    NETTO_GEWICHT: int | None = None
    EIGEN_GEWICHT: int | None = None
    NETTO_GESAMT: int | None = None
    TARA_GEWICHT: int | None = None
    BRUTTO_GEWICHT: int | None = None


# ---------------------------------------------------------------------------
# 5.7.1 Prüfung/Tätigkeit
# ---------------------------------------------------------------------------


class PrPruf(FeuerONBase):
    """Prüfung/Tätigkeit (PR_PRUF) - inspections and tests."""

    @classmethod
    def table_name(cls) -> str:
        return "PR_PRUF"

    # Required
    PRUFGRUND: Str30
    DATUM: FeuerONTimestamp

    # Optional
    PRUEFER: Str50 | None = None
    BEURTEILUNGSTEXT: Str200 | None = None
    BEMERKUNG: str | None = None  # Memo
    ANZAHL: float | None = None
    EINHEIT: Str50 | None = None
    AKT_BETR_H: float | None = None
    PAUSCHAL_BETRAG: float | None = None
    FUNKTION: FeuerONBool | None = None


# ---------------------------------------------------------------------------
# Top-level record
# ---------------------------------------------------------------------------


class EquipmentRecord(FeuerONRecord):
    """A complete equipment record for FeuerON CSV import."""

    # Required
    stammdaten: PrStamm

    # Module-specific detail (only one applies per device)
    em: PrsEm | None = None
    fme: PrsFme | None = None
    fuge: PrsFuge | None = None
    fp: PrsFp | None = None
    lager: PrsLager | None = None

    # Multiple allowed
    pruefungen: list[PrPruf] = []
