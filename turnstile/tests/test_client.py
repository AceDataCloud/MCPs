"""Targeted tests for Turnstile client request payloads."""

import pytest

from core.client import TurnstileClient


@pytest.mark.asyncio
async def test_get_token_omits_async_when_not_provided():
    client = TurnstileClient(api_token="test-token")
    captured: dict[str, object] = {}

    async def fake_request(method: str, endpoint: str, *, payload=None, timeout=None):
        captured["method"] = method
        captured["endpoint"] = endpoint
        captured["payload"] = payload
        _ = timeout
        return {"ok": True}

    client.request = fake_request  # type: ignore[method-assign]

    await client.get_token(website_key="site-key", website_url="https://example.com")

    assert captured["method"] == "POST"
    assert captured["endpoint"] == "/captcha/token/turnstile"
    assert captured["payload"] == {
        "website_key": "site-key",
        "website_url": "https://example.com",
    }


@pytest.mark.asyncio
async def test_get_token_passes_async_flag_when_provided():
    client = TurnstileClient(api_token="test-token")
    captured: dict[str, object] = {}

    async def fake_request(_method: str, _endpoint: str, *, payload=None, timeout=None):
        captured["payload"] = payload
        _ = timeout
        return {"ok": True}

    client.request = fake_request  # type: ignore[method-assign]

    await client.get_token(
        website_key="site-key", website_url="https://example.com", async_=False
    )

    assert captured["payload"] == {
        "website_key": "site-key",
        "website_url": "https://example.com",
        "async": False,
    }
