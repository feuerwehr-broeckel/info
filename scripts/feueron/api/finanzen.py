"""Finanzen tab: bankverbindungen, beitraege."""

from __future__ import annotations

from typing import TYPE_CHECKING

from scripts.feueron.api.models import (
    Bankverbindung,
    Beitrag,
    CreateBankverbindungEntry,
    CreateBeitragEntry,
)

if TYPE_CHECKING:
    from scripts.feueron.api.client import FeuerONClient


class FinanzenMixin:
    """API methods for the Finanzen top-level tab."""

    self: FeuerONClient

    def get_bankverbindungen(self, person_id: int | str) -> list[Bankverbindung]:
        """Return bank details for a person."""
        return self._get_list(f"/personen/{person_id}/bankverbindungen", Bankverbindung)

    def delete_bankverbindungen(
        self, person_id: int | str, bankverbindung_ids: list[int | str]
    ) -> list[Bankverbindung]:
        """Remove one or more Bankverbindungen entries."""
        ops = [{"op": "remove", "path": f"/{bid}"} for bid in bankverbindung_ids]
        return self._patch(
            f"/personen/{person_id}/bankverbindungen", ops, Bankverbindung
        )

    def create_bankverbindung(
        self, person_id: int | str, entry: CreateBankverbindungEntry
    ) -> Bankverbindung:
        """Create a Bankverbindung via ``POST /api/personen/{id}/bankverbindungen``."""
        resp = self._request(
            "POST",
            f"/personen/{person_id}/bankverbindungen",
            json=entry.model_dump(by_alias=True, exclude_unset=True),
        )
        return Bankverbindung.model_validate(resp.json())

    def update_bankverbindung(
        self, person_id: int | str, bankverbindung: Bankverbindung
    ) -> Bankverbindung:
        """Update a Bankverbindung via ``PATCH /api/personen/{id}/bankverbindungen/{bvId}``."""
        resp = self._request(
            "PATCH",
            f"/personen/{person_id}/bankverbindungen/{bankverbindung.id}",
            json=bankverbindung.model_dump(by_alias=True, exclude_unset=True),
        )
        return Bankverbindung.model_validate(resp.json())

    def create_beitrag(
        self, person_id: int | str, entry: CreateBeitragEntry
    ) -> Beitrag:
        """Create a Beitrag via ``POST /api/personen/{id}/beitraege``."""
        resp = self._request(
            "POST",
            f"/personen/{person_id}/beitraege",
            json=entry.model_dump(by_alias=True),
        )
        return Beitrag.model_validate(resp.json())

    def get_beitraege(
        self,
        person_id: int | str,
        *,
        hide_inactive: bool = True,
        hide_outdated: bool = True,
    ) -> list[Beitrag]:
        """Return Beiträge (fees/contributions) for a person."""
        return self._get_list(
            f"/personen/{person_id}/beitraege",
            Beitrag,
            params={
                "hideInactive": str(hide_inactive).lower(),
                "hideOutdated": str(hide_outdated).lower(),
            },
        )
