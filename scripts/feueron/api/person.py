"""Person tab: personen CRUD, lock/unlock, erreichbarkeiten."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from scripts.feueron.api.models import (
    Erreichbarkeit,
    Person,
    PersonDetail,
)

if TYPE_CHECKING:
    from scripts.feueron.api.client import FeuerONClient


class PersonMixin:
    """API methods for the Person top-level tab."""

    self: FeuerONClient

    def get_personen(
        self,
        *,
        search: str = "",
        person_ids: list[int | str] | None = None,
        organisation_id: int | None = None,
    ) -> list[Person]:
        """Fetch persons via ``/api/personen``.

        Either search by name or fetch specific persons by ID.
        """
        org_id = organisation_id or self._organisation_id
        params: dict[str, Any] = {"organisationId": org_id}
        if person_ids is not None:
            params["personIds"] = ",".join(str(pid) for pid in person_ids)
        else:
            params["search"] = search
        return self._get_list("/personen", Person, params=params)

    def get_person(self, person_id: int | str) -> PersonDetail:
        """Fetch full person detail via ``GET /api/personen/{id}``."""
        return self._get_object(f"/personen/{person_id}", PersonDetail)

    def update_person(self, person: PersonDetail) -> PersonDetail:
        """Update a person via ``PATCH /api/personen/{id}`` (partial JSON merge).

        Only fields that were explicitly set on the model are sent.
        """
        resp = self._request(
            "PATCH",
            f"/personen/{person.id}",
            json=person.model_dump(by_alias=True, exclude_unset=True),
        )
        return PersonDetail.model_validate(resp.json())

    def is_locked(self, person_id: int | str) -> bool:
        """Check whether a person is currently locked for editing."""
        from scripts.feueron.api.client import FeuerONAPIError

        try:
            self._request("GET", f"/personen/{person_id}/lock")
        except FeuerONAPIError as exc:
            if exc.status_code == 404:
                return False
            raise
        return True

    def lock_person(self, person_id: int | str) -> None:
        """Acquire an edit lock on a person (PUT /personen/{id}/lock)."""
        self._request("PUT", f"/personen/{person_id}/lock")

    def unlock_person(self, person_id: int | str) -> None:
        """Release the edit lock on a person (DELETE /personen/{id}/lock)."""
        self._request("DELETE", f"/personen/{person_id}/lock")

    def get_erreichbarkeiten(self, person_id: int | str) -> list[Erreichbarkeit]:
        """Return contact details for a person."""
        return self._get_list(f"/personen/{person_id}/erreichbarkeiten", Erreichbarkeit)

    def delete_erreichbarkeiten(
        self, person_id: int | str, erreichbarkeit_ids: list[int | str]
    ) -> list[Erreichbarkeit]:
        """Remove one or more Erreichbarkeiten entries."""
        ops = [{"op": "remove", "path": f"/{eid}"} for eid in erreichbarkeit_ids]
        return self._patch(
            f"/personen/{person_id}/erreichbarkeiten", ops, Erreichbarkeit
        )
