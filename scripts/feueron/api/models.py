"""Pydantic models for FeuerON REST API responses."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

# UI: Männlich=MALE, Weiblich=FEMALE, Divers=OTHER, Juristisch=LEGAL_ENTITY
Geschlecht = Literal["MALE", "FEMALE", "OTHER", "LEGAL_ENTITY"]


class Organisation(BaseModel):
    """Organisation (Feuerwehr) as returned by the API."""

    id: str
    name: str
    legacy_fwk: str | None = Field(None, alias="legacyFwk")
    organisations_ebene: str | None = Field(None, alias="organisationsEbene")
    organisations_typ: str | None = Field(None, alias="organisationsTyp")


class UserSettings(BaseModel):
    """User export settings from ``/api/context-info``."""

    export_charset: str = Field("UTF-8", alias="exportCharset")
    csv_field_separator: str = Field(";", alias="csvFieldSeparator")
    csv_text_qualifier: str = Field('"', alias="csvTextQualifier")


class ContextInfo(BaseModel):
    """Session context from ``/api/context-info``."""

    user_id: str = Field(alias="userId")
    username: str
    user_realname: str = Field(alias="userRealname")
    organisation: Organisation
    default_organisation_id_for_entity_creation: str = Field(
        alias="defaultOrganisationIdForEntityCreation"
    )
    default_bundesland: str = Field(alias="defaultBundesland")
    user_settings: UserSettings = Field(alias="userSettings")


class Person(BaseModel):
    """Person search result from ``/api/personen``."""

    id: str
    personalnummer: str
    vorname: str
    nachname: str
    geburtsdatum: str | None = None
    geschlecht: Geschlecht | None = None
    organisation: Organisation | None = None
    zweit_organisation: Organisation | None = Field(None, alias="zweitOrganisation")


class AbteilungValue(BaseModel):
    """Abteilung option from ``/api/personen/abteilungen-values``."""

    type: str
    name: str


class OrganisationsEbene(BaseModel):
    """Organisation level within the tree."""

    id: str
    name: str


class OrganisationTreeNode(BaseModel):
    """Node in the organisation tree from ``/api/organisationen-tree``."""

    organisation_id: str | None = Field(None, alias="organisationId")
    bezeichnung: str | None = None
    legacy_fwk: str | None = Field(None, alias="legacyFwk")
    legacy_fwk_tree_leaf: bool | None = Field(None, alias="legacyFwkTreeLeaf")
    organisations_ebene: OrganisationsEbene | None = Field(
        None, alias="organisationsEbene"
    )
    selectable: bool = False
    children: list[OrganisationTreeNode] = []


class OrganisationTree(BaseModel):
    """Root of the organisation tree response."""

    children: list[OrganisationTreeNode] = []
    selectable: bool = False


# -- person creation request models ----------------------------------------


class CreateAbteilung(BaseModel):
    """Abteilung membership in a person creation request."""

    name: str
    mitglied_seit: str = Field(alias="mitgliedSeit")

    model_config = {"populate_by_name": True}


class CreateOrganisation(BaseModel):
    """Organisation block in a person creation request."""

    id: str
    abteilungen: list[CreateAbteilung] = []

    model_config = {"populate_by_name": True}


class CreateAbteilungEntry(BaseModel):
    """Request body for ``POST /api/personen/{id}/abteilungen``."""

    abteilung: str
    von: str
    bis: str = ""
    organisation: CreateOrganisation
    bundesland: str = "Niedersachsen"
    organisation_ausserhalb_von_land: bool = Field(
        False, alias="organisationAusserhalbVonLand"
    )
    nicht_in_statistik_auswerten: bool = Field(False, alias="nichtInStatistikAuswerten")

    model_config = {"populate_by_name": True}


class CreateAdresse(BaseModel):
    """Address block in a person creation request."""

    strasse: str = ""
    hausnummer: str = ""
    plz: str = ""
    ort: str = ""
    ortsteil: str = ""

    model_config = {"populate_by_name": True}


class CreateErreichbarkeiten(BaseModel):
    """Flat contact details in a person creation request."""

    telefon_privat: str = Field("", alias="telefonPrivat")
    telefon_dienstlich: str = Field("", alias="telefonDienstlich")
    mobil_privat: str = Field("", alias="mobilPrivat")
    mobil_dienstlich: str = Field("", alias="mobilDienstlich")
    email_privat: str = Field("", alias="emailPrivat")
    email_dienstlich: str = Field("", alias="emailDienstlich")
    telefax_privat: str = Field("", alias="telefaxPrivat")
    telefax_dienstlich: str = Field("", alias="telefaxDienstlich")

    model_config = {"populate_by_name": True}


class CreatePersonRequest(BaseModel):
    """Request body for ``POST /api/personen``."""

    nachname: str
    vorname: str
    personalnummer: str
    geburtsdatum: str
    geschlecht: Geschlecht
    organisation: CreateOrganisation
    adresse: CreateAdresse | None = None
    geburtsort: str | None = None
    geburtsname: str | None = None
    erreichbarkeiten: CreateErreichbarkeiten | None = None

    model_config = {"populate_by_name": True}


# -- person creation response models --------------------------------------


class ResponseAbteilung(BaseModel):
    """Abteilung in a created person response."""

    id: str
    name: str
    mitglied_seit: str = Field(alias="mitgliedSeit")


class ResponseOrganisation(BaseModel):
    """Organisation in a created person response."""

    id: str
    name: str
    legacy_fwk: str | None = Field(None, alias="legacyFwk")
    organisations_ebene: str | None = Field(None, alias="organisationsEbene")
    organisations_typ: str | None = Field(None, alias="organisationsTyp")
    abteilungen: list[ResponseAbteilung] = []
    parent_id: str | None = Field(None, alias="parentId")


class ResponseAdresse(BaseModel):
    """Address in a created person response."""

    strasse: str | None = None
    hausnummer: str | None = None
    plz: str | None = None
    ort: str | None = None
    ortsteil: str | None = None
    land: str | None = None


class ResponseFeuerwehr(BaseModel):
    """Feuerwehr-specific fields in a created person response."""

    dienstgrad: str | None = None
    dienststellung: str | None = None
    einsatzfahrer: str | None = None
    nicht_in_personalstatistik_beruecksichtigen: bool = Field(
        False, alias="nichtInPersonalstatistikBeruecksichtigen"
    )
    fuer_einsaetze_der_gesamten_stadt_gemeinde_sichtbar: bool = Field(
        False, alias="fuerEinsaetzeDerGesamtenStadtGemeindeSichtbar"
    )
    datenweitergabe_widersprochen: bool = Field(
        False, alias="datenweitergabeWidersprochen"
    )


class ChangeInfo(BaseModel):
    """Created/last-changed metadata."""

    editor_full_name: str | None = Field(None, alias="editorFullName")
    date: str | None = None


class PersonDetail(BaseModel):
    """Full person detail returned by ``POST /api/personen`` (create)."""

    id: str
    personalnummer: str
    vorname: str
    nachname: str
    geschlecht: Geschlecht | None = None
    geburtsort: str | None = None
    geburtsname: str | None = None
    geburtsdatum: str | None = None
    erreichbarkeiten: CreateErreichbarkeiten | None = None
    feuerwehr: ResponseFeuerwehr | None = None
    organisation: ResponseOrganisation | None = None
    zweit_organisation: ResponseOrganisation | None = Field(
        None, alias="zweitOrganisation"
    )
    adresse: ResponseAdresse | None = None
    einstellungs_datum: str | None = Field(None, alias="einstellungsDatum")
    ausgetreten_am: str | None = Field(None, alias="ausgetretenAm")
    austrittsgrund: str | None = None
    spind_nr: str | None = Field(None, alias="spindNr")
    anrede: str | None = None
    brieftitel: str | None = None
    familienstand: str | None = None
    anzahl_kinder: int | None = Field(None, alias="anzahlKinder")
    staatsangehoerigkeit: str | None = None
    blutgruppe: str | None = None
    created: ChangeInfo | None = None
    last_changed: ChangeInfo | None = Field(None, alias="lastChanged")
    antrago_token: str | None = Field(None, alias="antragoToken")

    model_config = {"populate_by_name": True}


# -- reference data models --------------------------------------------------


class I18nText(BaseModel):
    """Internationalised text value."""

    de_DE: str | None = None
    en_GB: str | None = None
    it_IT: str | None = None


class MenuItem(BaseModel):
    """Single item within a GeneralMenu."""

    id: str
    value: I18nText
    sort_id: int = Field(0, alias="sortId")


class GeneralMenu(BaseModel):
    """Named menu from ``/api/personen/general-menus``."""

    name: str
    items: list[MenuItem] = []


class DienstgradLabel(BaseModel):
    """Bezeichnung and short form for a single gender variant."""

    bezeichnung: I18nText = Field(default_factory=I18nText)
    bezeichnung_kurz: I18nText = Field(
        default_factory=I18nText, alias="bezeichnungKurz"
    )


class DienstgradValue(BaseModel):
    """Gender-specific Dienstgrad entry from ``/api/personen/dienstgrade-gender-specific-values``."""

    MALE: DienstgradLabel = Field(default_factory=DienstgradLabel)
    FEMALE: DienstgradLabel = Field(default_factory=DienstgradLabel)
    LEGAL_ENTITY: DienstgradLabel = Field(default_factory=DienstgradLabel)


# -- per-person sub-resource models ----------------------------------------


class Dienstgrad(BaseModel):
    """Dienstgrad entry from ``/api/personen/{id}/dienstgrade``."""

    id: str
    zweit_organisation: str | None = Field(None, alias="zweitOrganisation")
    bezeichnung: str
    bezeichnung_kurz: str | None = Field(None, alias="bezeichnungKurz")
    von: str
    bis: str | None = None
    ort: str | None = None
    befoerderungsgrund1: str | None = None
    befoerderungsgrund2: str | None = None
    person_dokumente: list[Any] = Field(default_factory=list, alias="personDokumente")

    model_config = {"populate_by_name": True}


class CreateDienstgradEntry(BaseModel):
    """Request body for ``POST /api/personen/{id}/dienstgrade``."""

    bezeichnung: str
    von: str
    bis: str = ""


class Gruppe(BaseModel):
    """Zug/Gruppe entry from ``/api/personen/{id}/gruppen``."""

    id: str
    zweit_organisation: str | None = Field(None, alias="zweitOrganisation")
    bezeichnung: str
    von: str
    bis: str | None = None
    ort: str | None = None
    funktion1: str | None = None
    funktion2: str | None = None


class CreateGruppeEntry(BaseModel):
    """Request body for ``POST /api/personen/{id}/gruppen``."""

    bezeichnung: str
    von: str
    bis: str = ""
    ort: str = ""
    funktion1: str = ""
    funktion2: str = ""

    model_config = {"populate_by_name": True}


class Abteilung(BaseModel):
    """Abteilung membership from ``/api/personen/{id}/abteilungen``."""

    id: str
    zweit_organisation: str | None = Field(None, alias="zweitOrganisation")
    abteilung: str
    von: str
    bis: str | None = None
    organisation_ausserhalb_von_land: bool = Field(
        False, alias="organisationAusserhalbVonLand"
    )
    bundesland: str | None = None
    instanzfremde_organisation_name: str | None = Field(
        None, alias="instanzfremdeOrganisationName"
    )
    organisation: Organisation | None = None
    austrittsgrund: str | None = None
    nicht_in_statistik_auswerten: bool = Field(False, alias="nichtInStatistikAuswerten")
    naehere_informationen1: str | None = Field(None, alias="naehereInformationen1")
    naehere_informationen2: str | None = Field(None, alias="naehereInformationen2")

    model_config = {"populate_by_name": True}


class Erreichbarkeit(BaseModel):
    """Contact detail entry from ``/api/personen/{id}/erreichbarkeiten``."""

    id: str
    zweit_organisation: str | None = Field(None, alias="zweitOrganisation")
    art: str
    kontaktdaten: str
    erreichbarkeit1: str | None = None
    erreichbarkeit2: str | None = None


class Verfahren(BaseModel):
    """Payment procedure (Ein-/Auszahlungsverfahren)."""

    bezeichnung: str | None = None
    bezeichnung_kurz: str | None = Field(None, alias="bezeichnungKurz")


class Bankverbindung(BaseModel):
    """Bank details from ``/api/personen/{id}/bankverbindungen``."""

    id: str
    zweit_organisation: str | None = Field(None, alias="zweitOrganisation")
    bankname: str | None = None
    bic: str | None = None
    iban: str | None = None
    inhaber: str | None = None
    ort: str | None = None
    mandatsreferenz: str | None = None
    mandat_erteilt: str | None = Field(None, alias="mandatErteilt")
    lastschriftart: str | None = None
    kreditorennummer: str | None = None
    zusatzfeld: str | None = None
    einzahlungsverfahren: Verfahren | None = None
    auszahlungsverfahren: Verfahren | None = None

    model_config = {"populate_by_name": True}


class CreateBankverbindungEntry(BaseModel):
    """Request body for ``POST /api/personen/{id}/bankverbindungen``."""

    iban: str
    lastschriftart: Literal["ERST_LASTSCHRIFT", "FOLGE_LASTSCHRIFT"] = "ERST_LASTSCHRIFT"
    bic: str = ""
    bankname: str = ""
    inhaber: str = ""
    ort: str = ""
    mandatsreferenz: str = ""
    mandat_erteilt: str = Field("", alias="mandatErteilt")
    kreditorennummer: str = ""
    zusatzfeld: str = ""

    model_config = {"populate_by_name": True}


class Zahlungen(BaseModel):
    """Monthly payment breakdown within a Beitrag."""

    januar: float = 0.0
    februar: float = 0.0
    maerz: float = 0.0
    april: float = 0.0
    mai: float = 0.0
    juni: float = 0.0
    juli: float = 0.0
    august: float = 0.0
    september: float = 0.0
    oktober: float = 0.0
    november: float = 0.0
    dezember: float = 0.0


class Beitrag(BaseModel):
    """Fee/contribution from ``/api/personen/{id}/beitraege``."""

    id: str
    zweit_organisation: str | None = Field(None, alias="zweitOrganisation")
    bearbeiter: str | None = None
    gueltig_ab: str | None = Field(None, alias="gueltigAb")
    gueltig_bis: str | None = Field(None, alias="gueltigBis")
    geaendert_am: str | None = Field(None, alias="geaendertAm")
    jahresbeitrag: float | None = None
    beitragstyp: str | None = None
    beitragsart: str | None = None
    zahlungsweise: str | None = None
    erste_faelligkeit: str | None = Field(None, alias="ersteFaelligkeit")
    naechste_zahlung: str | None = Field(None, alias="naechsteZahlung")
    letzte_rechnung: str | None = Field(None, alias="letzteRechnung")
    kostenstelle: str | None = None
    erhaelt_zeitung: bool = Field(False, alias="erhaeltZeitung")
    zahlungen: Zahlungen | None = None
    outdated: bool = False
    inactive: bool = False

    model_config = {"populate_by_name": True}


class CreateBeitragEntry(BaseModel):
    """Request body for ``POST /api/personen/{id}/beitraege``."""

    zahlungen: Zahlungen = Field(default_factory=Zahlungen)
    erhaelt_zeitung: bool = Field(False, alias="erhaeltZeitung")
    erste_faelligkeit: str = Field(alias="ersteFaelligkeit")
    gueltig_ab: str = Field(alias="gueltigAb")
    zahlungsweise: str
    beitragsart: str
    beitragstyp: str
    jahresbeitrag: float

    model_config = {"populate_by_name": True}
