"""HTTP client for AceDataCloud public read endpoints.

Public + read-only: every call is an unauthenticated GET against
api.acedata.cloud. No API token, no per-request auth context.
"""

from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import DocsAPIError, DocsNotFoundError, DocsTimeoutError


def _unwrap(data: Any) -> Any:
    """Return the list payload whether the endpoint paginates or not.

    PlatformBackend paginators use ``items``; DRF defaults use ``results``.
    """
    if isinstance(data, dict):
        for key in ("items", "results"):
            if isinstance(data.get(key), list):
                return data[key]
    return data


class DocsClient:
    """Async client for AceDataCloud public documentation/catalog endpoints."""

    def __init__(self, base_url: str | None = None):
        # Read endpoints (docs/models/services/apis/search) are served by the
        # platform backend, NOT the api.acedata.cloud Kong gateway.
        self.base_url = base_url or settings.platform_base_url
        self.timeout = settings.request_timeout

    async def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        lang: str | None = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        headers = {"accept": "application/json"}
        if lang:
            # The backend resolves $t(key) content via Accept-Language.
            headers["accept-language"] = lang
        logger.info(f"GET {url} params={params}")
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(
                    url, params=params, headers=headers, timeout=self.timeout
                )
        except httpx.TimeoutException as e:
            raise DocsTimeoutError(f"Request to {path} timed out after {self.timeout}s") from e
        except Exception as e:  # noqa: BLE001 - surface as a typed error
            raise DocsAPIError(message=str(e)) from e

        if resp.status_code == 404:
            raise DocsNotFoundError(f"Not found: {path}")
        if resp.status_code >= 400:
            try:
                body = resp.json()
                message = body.get("error", {}).get("message") or body.get("detail") or resp.text
            except Exception:  # noqa: BLE001
                message = resp.text or f"HTTP {resp.status_code}"
            raise DocsAPIError(message=message, status_code=resp.status_code)

        try:
            return resp.json()
        except ValueError as e:
            # A 200 that isn't JSON (proxy/HTML/empty) — degrade, don't crash.
            raise DocsAPIError(message=f"Upstream returned non-JSON from {path}") from e

    # --- documentation -----------------------------------------------------
    async def search_docs(self, query: str, lang: str = "zh-cn", limit: int = 10) -> Any:
        return await self.get(
            "/api/v1/search/", params={"q": query, "lang": lang, "limit": limit}
        )

    async def list_documents(
        self, limit: int = 20, offset: int = 0, doc_type: str | None = None
    ) -> Any:
        params: dict[str, Any] = {"private": "false", "limit": limit, "offset": offset}
        if doc_type:
            params["type"] = doc_type
        return _unwrap(await self.get("/api/v1/documents/", params=params))

    async def get_document(self, ref: str, lang: str = "zh-cn") -> Any:
        return await self.get(f"/api/v1/documents/{ref}", lang=lang)

    # --- catalog -----------------------------------------------------------
    async def list_services(self, service_type: str | None = None) -> Any:
        params: dict[str, Any] = {"private": "false"}
        if service_type:
            params["type"] = service_type
        return _unwrap(await self.get("/api/v1/services/", params=params))

    async def list_apis(
        self,
        service: str | None = None,
        path: str | None = None,
        stages: list[str] | None = None,
    ) -> Any:
        params: dict[str, Any] = {}
        if service:
            params["service"] = service
        if path:
            params["path"] = path
        if stages:
            params["stage"] = stages
        return _unwrap(await self.get("/api/v1/apis/", params=params))

    # --- models ------------------------------------------------------------
    async def list_models(self, with_pricing: bool = True) -> Any:
        params = {"with_pricing": "1"} if with_pricing else {}
        return await self.get("/api/v1/models/", params=params)


client = DocsClient()
