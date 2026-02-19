"""FeuerON REST API client with session-cookie authentication."""

from __future__ import annotations

import json as _json
import logging
import re
from typing import Any, TypeVar

import httpx
from pydantic import BaseModel

from scripts.feueron.api.einsatzdienst import EinsatzdienstMixin
from scripts.feueron.api.feuerwehr import FeuerwehrMixin
from scripts.feueron.api.finanzen import FinanzenMixin
from scripts.feueron.api.models import ContextInfo
from scripts.feueron.api.person import PersonMixin
from scripts.feueron.api.reference import ReferenceMixin
from scripts.feueron.credentials import get_credentials

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://www.feueron.de/feueron"
API_PREFIX = "/api"

T = TypeVar("T", bound=BaseModel)


class FeuerONAuthError(Exception):
    """Raised when login fails or the session has expired."""


class FeuerONAPIError(Exception):
    """Raised when an API request returns an error status."""

    def __init__(self, status_code: int, detail: str = "") -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"HTTP {status_code}: {detail}")


class FeuerONClient(
    PersonMixin, FeuerwehrMixin, EinsatzdienstMixin, FinanzenMixin, ReferenceMixin
):
    """HTTP client for the FeuerON REST API.

    Authenticates via the FeuerON login form, activates the
    ``personalverwaltung`` module, and reuses session cookies for
    subsequent API calls.  Wraps ``httpx.Client`` and is usable as a
    context manager::

        with FeuerONClient() as client:
            results = client.get_personen(search="Müller")
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        *,
        username: str | None = None,
        password: str | None = None,
        region_id: str | None = None,
        organisation_id: int | None = None,
        timeout: float = 30.0,
    ) -> None:
        if username is None or password is None:
            env_user, env_pass, env_region = get_credentials()
            username = username or env_user
            password = password or env_pass
            region_id = region_id or env_region

        self._base_url = base_url.rstrip("/")
        self._username = username
        self._password = password
        self._region_id = region_id or "156"
        self._organisation_id = organisation_id
        self._http = httpx.Client(
            base_url=self._base_url,
            timeout=timeout,
            follow_redirects=True,
        )
        self._authenticated = False

    # -- context manager ---------------------------------------------------

    def __enter__(self) -> FeuerONClient:
        self.login()
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        self._http.close()

    # -- authentication ----------------------------------------------------

    def login(self) -> None:
        """Authenticate via the FeuerON login form."""
        # GET the login page first (pick up initial cookies)
        self._http.get("/")

        form_data = {
            "submitName": "login",
            "zmsLoginName": self._username,
            "zmsLoginPassword": self._password,
            "selectedOrganisationIndex": self._region_id,
            "localeCode": "de_DE",
            "clientData": '{"screen":{"w":1920,"h":1080},'
            '"window":{"iw":1920,"ih":1080,"ow":1920,"oh":1080}}',
            "login": "Anmelden",
        }
        response = self._http.post("/login.do", data=form_data)
        response.raise_for_status()

        # After a successful login the server redirects to profile.do.
        # If we end up back on the login page, credentials were wrong.
        if "login" in str(response.url).rsplit("/", 1)[-1].lower():
            raise FeuerONAuthError("Login failed — check credentials and region_id")

        # Activate the "Personen (neu)" module — the REST API endpoints
        # under /api/personen* are only available in this module context.
        self._http.get("/modul-switch.do", params={"modul": "personalverwaltung"})

        # Acquire OWASP CSRFGuard master token from the /csrfguard servlet.
        # The servlet returns JavaScript containing:
        #   var masterTokenValue = 'XXXX-XXXX-XXXX-...';
        # This token must be sent as an OWASP-CSRFTOKEN header on API calls.
        cg = self._http.get("/csrfguard")
        csrf_match = re.search(r"masterTokenValue\s*=\s*'([^']+)'", cg.text)
        if csrf_match:
            self._http.headers["OWASP-CSRFTOKEN"] = csrf_match.group(1)
            logger.info("CSRF token acquired")
        else:
            logger.warning("Could not obtain OWASP CSRF token")

        # Auto-discover the organisation ID from the session context.
        if self._organisation_id is None:
            ctx = ContextInfo.model_validate(
                self._http.get(f"{API_PREFIX}/context-info").json()
            )
            self._organisation_id = int(ctx.organisation.id)
            logger.info(
                "Organisation: %s (id=%d)",
                ctx.organisation.name,
                self._organisation_id,
            )

        self._authenticated = True
        logger.info("Logged in to FeuerON as %s", self._username)

    # -- low-level request helpers -----------------------------------------

    _API_HEADERS = {
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json, text/plain, */*",
    }

    def _request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        """Make an authenticated API request."""
        if not self._authenticated:
            raise FeuerONAuthError("Not authenticated — call login() first")

        headers = {**self._API_HEADERS, **kwargs.pop("headers", {})}
        response = self._http.request(
            method, f"{API_PREFIX}{path}", headers=headers, **kwargs
        )

        if response.status_code == 401:
            self._authenticated = False
            raise FeuerONAuthError("Session expired")
        if response.status_code >= 400:
            raise FeuerONAPIError(response.status_code, response.text[:500])

        return response

    def _get_json(self, path: str, params: dict[str, Any] | None = None) -> Any:
        """GET an API endpoint and return parsed JSON."""
        return self._request("GET", path, params=params).json()

    def _get_list(self, path: str, model: type[T], **kwargs: Any) -> list[T]:
        """GET an API endpoint and return a list of typed models."""
        return [model.model_validate(item) for item in self._get_json(path, **kwargs)]

    def _get_object(self, path: str, model: type[T], **kwargs: Any) -> T:
        """GET an API endpoint and return a single typed model."""
        return model.model_validate(self._get_json(path, **kwargs))

    def _post_text(self, path: str, **kwargs: Any) -> str:
        """POST to an API endpoint and return the response as plain text."""
        return self._request("POST", path, **kwargs).text

    def _patch(
        self,
        path: str,
        operations: list[dict[str, Any]],
        model: type[T],
    ) -> list[T]:
        """Send a JSON Patch request and return the updated list of typed models."""
        resp = self._request(
            "PATCH",
            path,
            content=_json.dumps(operations),
            headers={"Content-Type": "application/json-patch+json"},
        )
        return [model.model_validate(item) for item in resp.json()]

    # -- API methods -------------------------------------------------------

    @property
    def organisation_id(self) -> int:
        """The active organisation ID (auto-discovered or explicit)."""
        if self._organisation_id is None:
            raise ValueError("Not logged in yet — organisation_id unknown")
        return self._organisation_id

    def get_context_info(self) -> ContextInfo:
        """Return session context (user, organisation, settings)."""
        return self._get_object("/context-info", ContextInfo)
