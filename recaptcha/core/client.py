"""HTTP client for ReCaptcha API."""

import contextvars
import json
from typing import Any

import httpx
from loguru import logger

from core.config import settings
from core.exceptions import (
    ReCaptchaAPIError,
    ReCaptchaAuthError,
    ReCaptchaError,
    ReCaptchaTimeoutError,
)

_request_api_token: contextvars.ContextVar[str | None] = contextvars.ContextVar("_request_api_token", default=None)


def set_request_api_token(token: str | None) -> None:
    _request_api_token.set(token)


def get_request_api_token() -> str | None:
    return _request_api_token.get()


def _apply_submission_mode(payload: dict[str, Any], mode: str | None) -> None:
    if mode == "sync":
        return
    payload["async"] = True


class ReCaptchaClient:
    """Async HTTP client for the AceDataCloud ReCaptcha API."""

    def __init__(self, api_token: str | None = None, base_url: str | None = None):
        self.api_token = api_token if api_token is not None else settings.api_token
        self.base_url = base_url or settings.api_base_url
        self.timeout = settings.request_timeout
        logger.info(f"ReCaptchaClient initialized with base_url: {self.base_url}")

    def _get_headers(self) -> dict[str, str]:
        token = get_request_api_token() or self.api_token
        if not token:
            raise ReCaptchaAuthError("API token not configured")
        return {
            "accept": "application/json",
            "authorization": "******",
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
        message = error_obj.get("message") or (body.get("detail") if isinstance(body, dict) else None) or response.text or f"HTTP {status}"
        if status in (401, 403):
            raise ReCaptchaAuthError(message)
        raise ReCaptchaAPIError(message=message, code=code, status_code=status)

    async def request(self, method: str, endpoint: str, *, payload: dict[str, Any] | None = None, timeout: float | None = None) -> dict[str, Any]:
        method_upper = method.upper()
        url = f"{self.base_url}{endpoint}"
        request_timeout = timeout or self.timeout
        if payload is not None:
            logger.debug(f"Request payload: {json.dumps(payload, ensure_ascii=False, indent=2)}")
        async with httpx.AsyncClient() as http_client:
            try:
                response = await http_client.request(method_upper, url, json=payload, headers=self._get_headers(), timeout=request_timeout)
                if response.status_code >= 400:
                    self._handle_error_response(response)
                return response.json()  # type: ignore[no-any-return]
            except httpx.TimeoutException as e:
                raise ReCaptchaTimeoutError(f"Request to {endpoint} timed out after {request_timeout}s") from e
            except ReCaptchaError:
                raise
            except Exception as e:
                raise ReCaptchaAPIError(message=str(e)) from e

    async def recognize2(self, image: str, question: str, mode: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"image": image, "question": question}
        _apply_submission_mode(payload, mode)
        return await self.request("POST", "/captcha/recognition/recaptcha2", payload=payload)

    async def get_token2(self, website_key: str, website_url: str, proxy: str | None = None, mode: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"website_key": website_key, "website_url": website_url}
        if proxy is not None:
            payload["proxy"] = proxy
        _apply_submission_mode(payload, mode)
        return await self.request("POST", "/captcha/token/recaptcha2", payload=payload)

    async def get_token3(self, page_action: str, website_key: str, website_url: str, mode: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {"page_action": page_action, "website_key": website_key, "website_url": website_url}
        _apply_submission_mode(payload, mode)
        return await self.request("POST", "/captcha/token/recaptcha3", payload=payload)

    async def get_task(self, task_id: str) -> dict[str, Any]:
        return await self.request("POST", "/captcha/tasks", payload={"task_id": task_id})


client = ReCaptchaClient()
