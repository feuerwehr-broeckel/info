"""Einsatzdienst tab: züge/gruppen, dienststellungen, tauglichkeiten, etc."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scripts.feueron.api.models import (
    CreateGruppeEntry,
    Gruppe,
)

if TYPE_CHECKING:
    from scripts.feueron.api.client import FeuerONClient


class EinsatzdienstMixin:
    """API methods for the Einsatzdienst top-level tab."""

    self: FeuerONClient

    # -- Züge/Gruppen ------------------------------------------------------

    def get_gruppen(self, person_id: int | str) -> list[Gruppe]:
        """Return Züge/Gruppen assignments for a person."""
        return self._get_list(f"/personen/{person_id}/gruppen", Gruppe)

    def create_gruppe(
        self, person_id: int | str, entry: CreateGruppeEntry
    ) -> Gruppe:
        """Create a Zug/Gruppe assignment via ``POST /api/personen/{id}/gruppen``."""
        resp = self._request(
            "POST",
            f"/personen/{person_id}/gruppen",
            json=entry.model_dump(by_alias=True),
        )
        return Gruppe.model_validate(resp.json())

    def delete_gruppe(
        self, person_id: int | str, gruppe_id: int | str
    ) -> list[Gruppe]:
        """Remove a Zug/Gruppe assignment."""
        return self._patch(
            f"/personen/{person_id}/gruppen",
            [{"op": "remove", "path": f"/{gruppe_id}"}],
            Gruppe,
        )
