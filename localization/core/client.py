"""HTTP client for Localization API."""

import contextvars
import json
from typing import Any, Literal

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import (
    LocalizationAPIError,
    LocalizationAuthError,
    LocalizationError,
    LocalizationTimeoutError,
)

LocalizationInput = str | dict[str, Any]
LocalizationModel = Literal["gpt-3.5", "gpt-4"]
LocalizationLocale = Literal[
    "en",
    "de",
    "pt",
    "es",
    "fr",
    "zh-CN",
    "zh-TW",
    "it",
    "ko",
    "ja",
    "ru",
    "pl",
    "fi",
    "sv",
    "el",
    "uk",
    "ar",
    "sr",
]
LocalizationExtension = Literal["md", "json"]

_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar(
    "_request_api_token", default=None
)


def set_request_api_token(token: str | None) -> None:
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    return _request_api_token.get()


class LocalizationClient:
    """Async HTTP client for the AceDataCloud Localization API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout
        logger.info(f"LocalizationClient initialized with base_url: {self.base_url}")

    def _get_headers(self) -> dict[str, str]:
        token = get_request_api_token() or self.api_token
        if not token:
            raise LocalizationAuthError("API token not configured")
        return {
            "accept": "application/json",
            "authorization": "Bearer " + token,
            "content-type": "application/json",
        }

    def _handle_error_response(self, response: httpx.Response) -> None:
        status = response.status_code
        try:
            body = response.json()
        except Exception:
            body = {}
        error_obj = body.get("error", {}) if isinstance(body, dict) else {}
        code = error_obj.get("code", f"http_{status}")
        message = (
            error_obj.get("message")
            or (body.get("detail") if isinstance(body, dict) else None)
            or response.text
            or f"HTTP {status}"
        )
        if status in (401, 403):
            raise LocalizationAuthError(message)
        raise LocalizationAPIError(message=message, code=code, status_code=status)

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        payload: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> dict[str, Any]:
        method_upper = method.upper()
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout
        if payload is not None:
            logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.request(
                    method_upper,
                    url,
                    json=payload,
                    headers=self._get_headers(),
                    timeout=request_timeout,
                )
                if response.status_code >= 400:
                    self._handle_error_response(response)
                return response.json()  # type: ignore[no-any-return]
            except httpx.TimeoutException as e:
                raise LocalizationTimeoutError(
                    f"Request to {endpoint} timed out after {request_timeout}s"
                ) from e
            except LocalizationError:
                raise
            except Exception as e:
                raise LocalizationAPIError(message=str(e)) from e

    async def translate(
        self,
        input: LocalizationInput,
        locale: LocalizationLocale,
        extension: LocalizationExtension = "md",
        model: LocalizationModel | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {"input": input, "locale": locale, "extension": extension}
        if model is not None:
            payload["model"] = model
        return await self.request("POST", "/localization/translate", payload=payload)


client = LocalizationClient()
