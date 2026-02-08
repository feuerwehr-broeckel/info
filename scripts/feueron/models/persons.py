"""FeuerON CSV import models for personnel data (Personen)."""

from __future__ import annotations

from scripts.feueron.models.base import (
    AusbildungErfolg,
    BeitragArt,
    FeuerONBase,
    FeuerONBool,
    FeuerONDate,
    FeuerONRecord,
    FeuerONTime,
    Geschlecht,
    Str6,
    Str8,
    Str10,
    Str15,
    Str20,
    Str25,
    Str30,
    Str32,
    Str40,
    Str46,
    Str50,
    Str67,
    Str80,
    Str100,
    Str300,
    TelArt,
    Zahlungsweise,
)


# ---------------------------------------------------------------------------
# 4.1 Personenstammdaten
# ---------------------------------------------------------------------------


class PvDb(FeuerONBase):
    """Personenstammdaten (PV_DB) - core personnel data. One per person."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_DB"

    # Required
    ORGANISATION: Str80
    NACHNAME: Str30
    VORNAME: Str50
    PERS_NR: Str10
    GEBURT: FeuerONDate
    GESCHLECHT: Geschlecht

    # Optional
    BRIEFTITEL: Str40 | None = None
    FWK: str | None = None
    SPIND_NR: Str10 | None = None
    TITEL: Str30 | None = None
    ANREDE: Str32 | None = None
    GEBURT_ORT: Str80 | None = None
    GEBURT_NAME: Str50 | None = None
    STRASSE: Str80 | None = None
    HAUSNR: Str10 | None = None
    NATION: Str50 | None = None
    PLZ: Str6 | None = None
    ORT: Str80 | None = None
    BLUTGR: Str6 | None = None
    FAMSTAND: Str20 | None = None
    MEMO: str | None = None
    EINSTELLUNG: FeuerONDate | None = None
    ANZ_KINDER: int | None = None
    STAATSANG: Str20 | None = None
    STELLENNUMMER: Str15 | None = None
    ORTSTEIL: Str30 | None = None
    BARCODE: str | None = None
    HAUSHALTSSTELLE: Str15 | None = None
    STELLENWERT: Str15 | None = None
    STELLENWERT_PERS: Str15 | None = None
    STUNDEN_LT_SP: Str15 | None = None
    STUNDEN_PERS: Str15 | None = None
    AS_UEBERWACH: str | None = None
    AUSTRITT: FeuerONDate | None = None
    TOD: FeuerONDate | None = None
    NOT_IN_STATISTIC: FeuerONBool | None = None
    EINSATZFAHRER: FeuerONBool | None = None
    DELETED: FeuerONDate | None = None


# ---------------------------------------------------------------------------
# 4.2 Abteilungen
# ---------------------------------------------------------------------------


class PvAbt(FeuerONBase):
    """Abteilungen (PV_ABT) - department memberships."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_ABT"

    # Required
    ABTEILUNG: Str80
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    ORT: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.3 Abwesenheiten
# ---------------------------------------------------------------------------


class PvAbwes(FeuerONBase):
    """Abwesenheiten (PV_ABWES) - absences."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_ABWES"

    # Required
    STICHWORT: Str80

    # Optional
    VON: FeuerONDate | None = None
    BIS: FeuerONDate | None = None
    TELEPHON: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.4 Abzeichen / Nachweise
# ---------------------------------------------------------------------------


class PvAbzna(FeuerONBase):
    """Abzeichen / Nachweise (PV_ABZNA) - badges and certificates."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_ABZNA"

    # Required
    ABZNACHW: Str80
    AM: FeuerONDate

    # Optional
    ORT: Str80 | None = None
    EW_ABZNW1: Str80 | None = None
    EW_ABZNW2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.5 Angehörige
# ---------------------------------------------------------------------------


class PvAngehoer(FeuerONBase):
    """Angehörige (PV_ANGEHOER) - relatives / emergency contacts."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_ANGEHOER"

    # Required
    ART: Str80
    VORNAME: Str50
    NAME: Str30

    # Optional
    PRIO: int | None = None
    TITEL: Str40 | None = None
    ANREDE: Str80 | None = None
    BRIEFANREDE: Str40 | None = None
    STRASSE: Str80 | None = None
    HAUSNR: Str10 | None = None
    NATION: Str50 | None = None
    PLZ: Str10 | None = None
    ORT: Str80 | None = None
    ERREICHB1: Str80 | None = None
    ERREICHB2: Str80 | None = None
    ERREICHB3: Str80 | None = None
    ERREICHB4: Str80 | None = None
    ERREICHB5: Str80 | None = None
    ERREICHB6: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.6 Arbeitgeber
# ---------------------------------------------------------------------------


class PvArbgb(FeuerONBase):
    """Arbeitgeber (PV_ARBGB) - employer. Single entry only."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_ARBGB"

    # Required
    ARBEITG: Str46

    # Optional
    ABTEILUNG: Str50 | None = None
    TITELANSPRECH: Str40 | None = None
    ANREDEANSPRECH: Str80 | None = None
    BRIEFTITELANSPRECH: Str40 | None = None
    ANSPRECH: Str30 | None = None
    STRASSE: Str80 | None = None
    HAUSNR: Str10 | None = None
    NATION: Str50 | None = None
    PLZ: Str10 | None = None
    ORT: Str80 | None = None
    FUNKTDO: Str30 | None = None
    ERREICHB1: Str80 | None = None
    ERREICHB2: Str80 | None = None
    ERREICHB3: Str80 | None = None
    ERREICHB4: Str80 | None = None
    ERREICHB5: Str80 | None = None
    ERREICHB6: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.7 Ausbildungen / Lehrgänge
# ---------------------------------------------------------------------------


class PvAusb(FeuerONBase):
    """Ausbildungen / Lehrgänge (PV_AUSB) - training courses."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_AUSB"

    # Required
    AUSBILDG: Str80
    AUSBILDG_KURZ: Str25
    VON: FeuerONDate
    BIS: FeuerONDate
    ERFOLG: AusbildungErfolg

    # Optional
    LEHRGORT: Str80 | None = None
    EW_AUSB_1: Str80 | None = None
    EW_AUSB_2: Str80 | None = None
    ANMERKUNGEN: Str300 | None = None
    VERANSTALTER: Str80 | None = None
    ANM_ANZAHL: int | None = None
    ANGEM: FeuerONDate | None = None


# ---------------------------------------------------------------------------
# 4.8 Ausweise
# ---------------------------------------------------------------------------


class PvAusw(FeuerONBase):
    """Ausweise (PV_AUSW) - IDs / passes."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_AUSW"

    # Required
    BEZEICH: Str30
    AUSWEISNR: Str50
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    VERSAND_D: FeuerONDate | None = None
    RUECKERHALT_D: FeuerONDate | None = None
    VERNICHTUNG_D: FeuerONDate | None = None
    EW_AUSW_1: Str80 | None = None
    EW_AUSW_2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.9 Bankverbindung
# ---------------------------------------------------------------------------


class PvBank(FeuerONBase):
    """Bankverbindung (PV_BANK) - bank details. Single entry only."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_BANK"

    # All optional
    BANKVERB: Str80 | None = None
    ORT: Str80 | None = None
    BLZ: Str8 | None = None
    BIC: Str80 | None = None
    INHABER: Str80 | None = None
    KONTO: Str10 | None = None
    IBAN: Str80 | None = None
    MANDATSREFERENZ: Str100 | None = None
    MANDATSREFERENZ_ERTEILT: FeuerONDate | None = None
    RZ_ZEICHEN: Str15 | None = None


# ---------------------------------------------------------------------------
# 4.10 Beiträge
# ---------------------------------------------------------------------------


class PvBeitrag(FeuerONBase):
    """Beiträge (PV_BEITRAG) - membership fees."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_BEITRAG"

    # Required
    BETRAG: float
    TYP: Str80
    ART: BeitragArt
    ZAHLUNGSWEISE: Zahlungsweise
    GULTIG_AB: FeuerONDate
    ERSTE_FAELLIGKEIT: FeuerONDate

    # Optional
    NAECHSTE_ZAHLUNG: FeuerONDate | None = None
    MONAT1: float | None = None
    MONAT2: float | None = None
    MONAT3: float | None = None
    MONAT4: float | None = None
    MONAT5: float | None = None
    MONAT6: float | None = None
    MONAT7: float | None = None
    MONAT8: float | None = None
    MONAT9: float | None = None
    MONAT10: float | None = None
    MONAT11: float | None = None
    MONAT12: float | None = None


# ---------------------------------------------------------------------------
# 4.11 Ausbildung/Beruf
# ---------------------------------------------------------------------------


class PvBeruf(FeuerONBase):
    """Ausbildung/Beruf (PV_BERUF) - professions."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_BERUF"

    # Required
    BERUFBILD: Str30

    # Optional
    LAND: Str50 | None = None
    VON: FeuerONDate | None = None
    BIS: FeuerONDate | None = None
    EW_BERUF1: Str80 | None = None
    EW_BERUF2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.12 Beurlaubung
# ---------------------------------------------------------------------------


class PvBeurl(FeuerONBase):
    """Beurlaubung (PV_BEURL) - leave of absence."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_BEURL"

    # Required
    BEURLAUB: Str80
    VON: FeuerONDate
    BIS: FeuerONDate
    GRUND_B: Str80


# ---------------------------------------------------------------------------
# 4.13 Zusatz Biografie
# ---------------------------------------------------------------------------


class PvBiog(FeuerONBase):
    """Zusatz Biografie (PV_BIOG) - additional biography entries."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_BIOG"

    # Required
    BIOGRAFIE: Str30
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    ORT: Str80 | None = None
    ABLAUF1: Str80 | None = None
    ABLAUF2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.14 Dienstgrad
# ---------------------------------------------------------------------------


class PvDnGr(FeuerONBase):
    """Dienstgrad (PV_DN_GR) - rank."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_DN_GR"

    # Required
    DNST_GR: Str30
    DNST_GRK: Str10
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    HAUPTAMTLICHER_DIENST: Str80 | None = None
    OR: Str80 | None = None
    EW_DNSTG1: Str80 | None = None
    EW_DNSTG2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.15 Dienststellung
# ---------------------------------------------------------------------------


class PvDnSt(FeuerONBase):
    """Dienststellung (PV_DN_ST) - position / appointment."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_DN_ST"

    # Required
    DNST_ST: Str80
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    DAT_WAHL_VORST: FeuerONDate | None = None
    ORT: Str80 | None = None
    EW_DNSTS1: Str80 | None = None
    EW_DNSTS2: Str80 | None = None
    AUSWERTUNG_WIDERSPROCHEN: FeuerONBool | None = None


# ---------------------------------------------------------------------------
# 4.16 Ehrungen
# ---------------------------------------------------------------------------


class PvEhrg(FeuerONBase):
    """Ehrungen (PV_EHRG) - honors / awards."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_EHRG"

    # Required
    EHRUNGEN: Str100
    AM: FeuerONDate

    # Optional
    ANTRAG_AM: FeuerONDate | None = None
    EHRUNG_STATUS: Str80 | None = None
    ORT: Str80 | None = None
    EW_EHRU_1: Str80 | None = None
    EW_EHRU_2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.17 Familienereignisse
# ---------------------------------------------------------------------------


class PvFamst(FeuerONBase):
    """Familienereignisse (PV_FAMST) - family events."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_FAMST"

    # Required
    EREIGNIS: Str80

    # Optional
    AM: FeuerONDate | None = None
    ORT: Str80 | None = None
    FSBEMERK1: Str67 | None = None
    FSBEMERK2: Str67 | None = None


# ---------------------------------------------------------------------------
# 4.18 Fahrerlaubnisse
# ---------------------------------------------------------------------------


class PvFsche(FeuerONBase):
    """Fahrerlaubnisse (PV_FSCHE) - driving licenses."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_FSCHE"

    # Required
    FSCHEIN: Str80
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    AUSST_BEH: Str80 | None = None
    EW_FSCH_1: Str80 | None = None
    EW_FSCH_2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.19 Funktionen
# ---------------------------------------------------------------------------


class PvFunkt(FeuerONBase):
    """Funktionen (PV_FUNKT) - functions / roles."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_FUNKT"

    # Required
    FUNKTION: Str80
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    ORT: Str80 | None = None
    EW_FUNKT1: Str300 | None = None
    EW_FUNKT2: Str300 | None = None


# ---------------------------------------------------------------------------
# 4.20 Zug/Gruppe
# ---------------------------------------------------------------------------


class PvGrupp(FeuerONBase):
    """Zug/Gruppe (PV_GRUPP) - platoon / group."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_GRUPP"

    # Required
    GRUPPE: Str80
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    ORT: Str80 | None = None
    EW_GRUPP1: Str80 | None = None
    EW_GRUPP2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.21 Zutrittsberechtigungen
# ---------------------------------------------------------------------------


class PvMagaz(FeuerONBase):
    """Zutrittsberechtigungen (PV_MAGAZ) - access authorizations."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_MAGAZ"

    # Required
    MAGAZIN_S: Str80
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    S_NUMMER: Str30 | None = None
    EW_MAGAZ1: Str80 | None = None
    EW_MAGAZ2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.22 Fremdsprachen
# ---------------------------------------------------------------------------


class PvSprach(FeuerONBase):
    """Fremdsprachen (PV_SPRACH) - foreign languages."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_SPRACH"

    # Required
    SPRACHE: Str50

    # Optional
    VERSTEHEN: Str80 | None = None
    LESEN: Str80 | None = None
    SPRECHEN: Str80 | None = None
    SCHREIBEN: Str80 | None = None
    ANMERKUNG: Str80 | None = None
    MUTTERSPRACHE: FeuerONBool | None = None


# ---------------------------------------------------------------------------
# 4.23 Erreichbarkeiten
# ---------------------------------------------------------------------------


class PvTelep(FeuerONBase):
    """Erreichbarkeiten (PV_TELEP) - contact details."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_TELEP"

    # Required
    TEL_ART: TelArt
    TELEPHON: Str80

    # Optional
    EW_TELE_1: Str80 | None = None
    EW_TELE_2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.24 Überörtliche Tätigkeit
# ---------------------------------------------------------------------------


class PvUbort(FeuerONBase):
    """Überörtliche Tätigkeit (PV_UBORT) - supra-local activities."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_UBORT"

    # Required
    UBERORTL: Str80
    UBERORTL_KURZ: Str80
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    ORT: Str80 | None = None
    EW_UBERO1: Str80 | None = None
    EW_UEBRO2: Str80 | None = None


# ---------------------------------------------------------------------------
# 4.25 Tauglichkeiten
# ---------------------------------------------------------------------------


class PvUntsu(FeuerONBase):
    """Tauglichkeiten (PV_UNTSU) - medical fitness examinations."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_UNTSU"

    # Required
    UNTERSUCH: Str80
    VON: FeuerONDate

    # Optional
    BIS: FeuerONDate | None = None
    ORT: Str80 | None = None
    AUFLAGE: Str80 | None = None
    EW_UNTER1: Str300 | None = None
    EW_UNTER2: Str80 | None = None
    TATIGKEIT: Str80 | None = None
    DAUER: int | None = None
    UAS_INFO: str | None = None  # Memo


# ---------------------------------------------------------------------------
# 4.26 Verfügbarkeit
# ---------------------------------------------------------------------------


class PvVerf(FeuerONBase):
    """Verfügbarkeit (PV_VERF) - availability per weekday."""

    @classmethod
    def table_name(cls) -> str:
        return "PV_VERF"

    # Required
    NACHNAME: Str30  # Weekday name despite the field name

    # Optional
    VONZ1: FeuerONTime | None = None
    BISZ1: FeuerONTime | None = None
    VONZ2: FeuerONTime | None = None
    BISZ2: FeuerONTime | None = None
    SCHICHT: Str80 | None = None
    EW_VERF_1: Str80 | None = None
    EW_VERF_2: Str80 | None = None


# ---------------------------------------------------------------------------
# Top-level record
# ---------------------------------------------------------------------------


class PersonRecord(FeuerONRecord):
    """A complete person record for FeuerON CSV import."""

    # Required (single)
    stammdaten: PvDb

    # Optional single-entry sub-tables
    arbeitgeber: PvArbgb | None = None
    bank: PvBank | None = None

    # Optional multi-entry sub-tables
    abteilungen: list[PvAbt] = []
    abwesenheiten: list[PvAbwes] = []
    abzeichen: list[PvAbzna] = []
    angehoerige: list[PvAngehoer] = []
    ausbildungen: list[PvAusb] = []
    ausweise: list[PvAusw] = []
    beitraege: list[PvBeitrag] = []
    berufe: list[PvBeruf] = []
    beurlaubungen: list[PvBeurl] = []
    biografie: list[PvBiog] = []
    dienstgrade: list[PvDnGr] = []
    dienststellungen: list[PvDnSt] = []
    ehrungen: list[PvEhrg] = []
    familienereignisse: list[PvFamst] = []
    fahrerlaubnisse: list[PvFsche] = []
    funktionen: list[PvFunkt] = []
    gruppen: list[PvGrupp] = []
    zutrittsberechtigungen: list[PvMagaz] = []
    sprachen: list[PvSprach] = []
    erreichbarkeiten: list[PvTelep] = []
    ueberortliche: list[PvUbort] = []
    tauglichkeiten: list[PvUntsu] = []
    verfuegbarkeit: list[PvVerf] = []
