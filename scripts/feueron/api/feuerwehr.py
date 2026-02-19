"""Feuerwehr tab: abteilungen, dienstgrade."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scripts.feueron.api.models import (
    Abteilung,
    CreateAbteilungEntry,
    CreateDienstgradEntry,
    Dienstgrad,
)

if TYPE_CHECKING:
    from scripts.feueron.api.client import FeuerONClient


class FeuerwehrMixin:
    """API methods for the Feuerwehr top-level tab."""

    self: FeuerONClient

    # -- Abteilungen -----------------------------------------------------------

    def get_abteilungen(self, person_id: int | str) -> list[Abteilung]:
        """Return Abteilung memberships for a person."""
        return self._get_list(f"/personen/{person_id}/abteilungen", Abteilung)

    def delete_abteilung(
        self, person_id: int | str, abteilung_id: int | str
    ) -> list[Abteilung]:
        """Remove an Abteilung membership."""
        return self._patch(
            f"/personen/{person_id}/abteilungen",
            [{"op": "remove", "path": f"/{abteilung_id}"}],
            Abteilung,
        )

    def create_abteilung(
        self, person_id: int | str, entry: CreateAbteilungEntry
    ) -> Abteilung:
        """Create a new Abteilung membership via ``POST /api/personen/{id}/abteilungen``."""
        resp = self._request(
            "POST",
            f"/personen/{person_id}/abteilungen",
            json=entry.model_dump(by_alias=True),
        )
        return Abteilung.model_validate(resp.json())

    # -- Dienstgrade -----------------------------------------------------------

    def get_dienstgrade(self, person_id: int | str) -> list[Dienstgrad]:
        """Return Dienstgrade for a person."""
        return self._get_list(f"/personen/{person_id}/dienstgrade", Dienstgrad)

    def delete_dienstgrad(
        self, person_id: int | str, dienstgrad_id: int | str
    ) -> list[Dienstgrad]:
        """Remove a Dienstgrad entry."""
        return self._patch(
            f"/personen/{person_id}/dienstgrade",
            [{"op": "remove", "path": f"/{dienstgrad_id}"}],
            Dienstgrad,
        )

    def create_dienstgrad(
        self, person_id: int | str, entry: CreateDienstgradEntry
    ) -> Dienstgrad:
        """Create a new Dienstgrad via ``POST /api/personen/{id}/dienstgrade``."""
        resp = self._request(
            "POST",
            f"/personen/{person_id}/dienstgrade",
            json=entry.model_dump(by_alias=True),
        )
        return Dienstgrad.model_validate(resp.json())

    def update_dienstgrad(
        self, person_id: int | str, dienstgrad: Dienstgrad
    ) -> Dienstgrad:
        """Update a Dienstgrad via ``PATCH /api/personen/{id}/dienstgrade/{dgId}``."""
        resp = self._request(
            "PATCH",
            f"/personen/{person_id}/dienstgrade/{dienstgrad.id}",
            json=dienstgrad.model_dump(by_alias=True, exclude_unset=True),
        )
        return Dienstgrad.model_validate(resp.json())
