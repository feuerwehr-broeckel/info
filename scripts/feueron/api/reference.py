"""Reference data: dienstgrade values, abteilungen values, org tree, personalnummer, person creation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scripts.feueron.api.models import (
    AbteilungValue,
    CreatePersonRequest,
    DienstgradValue,
    GeneralMenu,
    OrganisationTree,
    PersonDetail,
)

if TYPE_CHECKING:
    from scripts.feueron.api.client import FeuerONClient


class ReferenceMixin:
    """API methods for reference data and person creation."""

    self: FeuerONClient

    def get_general_menus(self, *names: str) -> list[GeneralMenu]:
        """Return named menus from ``/api/personen/general-menus``.

        Pass one or more menu names, e.g.
        ``get_general_menus("ZUG_GRUPPE", "ZUG_GRUPPE_FUNKTION")``.
        """
        params = [("name", n) for n in names]
        return self._get_list("/personen/general-menus", GeneralMenu, params=params)

    def get_beitragsarten(self) -> list[str]:
        """Return available Beitragsarten from ``/api/beitragsarten``."""
        return self._get_json("/beitragsarten")

    def get_dienstgrade_values(self) -> list[DienstgradValue]:
        """Return all Dienstgrade with gender-specific labels."""
        return self._get_list(
            "/personen/dienstgrade-gender-specific-values", DienstgradValue
        )

    def get_abteilungen_values(
        self, access_type: str = "PERSON_CREATE"
    ) -> list[AbteilungValue]:
        """Return available Abteilungen for person creation."""
        return self._get_list(
            "/personen/abteilungen-values",
            AbteilungValue,
            params={"accessType": access_type},
        )

    def get_organisationen_tree(
        self,
        from_organisation_id: int | str | None = None,
    ) -> OrganisationTree:
        """Return the organisation tree for person creation."""
        org_id = from_organisation_id or self._organisation_id
        return self._get_object(
            "/organisationen-tree",
            OrganisationTree,
            params={
                "fromOrganisationIdAndBelow": org_id,
                "requiredRechteForSelectability": "DARF_FUER_ENTITAETEN_ERSTELLUNG_GENUTZT_WERDEN",
            },
        )

    def generate_personalnummer(
        self,
        organisation_id: int | str | None = None,
        current: str = "",
    ) -> str:
        """Generate the next Personalnummer via the API."""
        org_id = organisation_id or self._organisation_id
        return self._post_text(
            "/personen/personalnummer-generation",
            json={"organisationId": str(org_id), "currentPersonalnummer": current},
        )

    def validate_personalnummer(
        self,
        personalnummer: str,
        organisation_id: int | str | None = None,
    ) -> None:
        """Validate a Personalnummer (raises FeuerONAPIError on conflict)."""
        org_id = organisation_id or self._organisation_id
        self._request(
            "POST",
            "/personen/personalnummer-validation",
            json={
                "currentPersonalnummer": personalnummer,
                "organisationId": str(org_id),
            },
        )

    def create_person(self, person: CreatePersonRequest) -> PersonDetail:
        """Create a new person via ``POST /api/personen``."""
        resp = self._request(
            "POST",
            "/personen",
            json=person.model_dump(by_alias=True, exclude_none=True),
        )
        return PersonDetail.model_validate(resp.json())
