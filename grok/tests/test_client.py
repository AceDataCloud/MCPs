"""Unit tests for async submission behavior in the HTTP client."""

import pytest

from core.client import GrokClient


@pytest.mark.asyncio
async def test_chat_completions_builds_payload_and_drops_none(monkeypatch) -> None:
    """chat_completions should target /grok/chat/completions and drop None params."""
    captured: dict = {}

    async def fake_request(endpoint, payload, timeout=None):  # noqa: ARG001
        captured["endpoint"] = endpoint
        captured["payload"] = payload
        return {"ok": True}

    client = GrokClient(api_token="test-token", base_url="https://api.test.com")
    monkeypatch.setattr(client, "request", fake_request)

    await client.chat_completions(
        messages=[{"role": "user", "content": "hi"}],
        model="grok-4-1-fast",
        temperature=0.7,
        max_tokens=None,
    )

    assert captured["endpoint"] == "/grok/chat/completions"
    assert captured["payload"]["model"] == "grok-4-1-fast"
    assert captured["payload"]["temperature"] == 0.7
    assert "max_tokens" not in captured["payload"]  # None dropped


def test_with_async_callback_injects_default_callback() -> None:
    """Long-running Grok operations should default to async submission."""
    client = GrokClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback({"model": "grok-imagine-video"})
    assert payload["callback_url"] == "https://api.acedata.cloud/health"


def test_with_async_callback_preserves_explicit_callback() -> None:
    """User-provided callbacks should not be overwritten."""
    client = GrokClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback(
        {"model": "grok-imagine-video", "callback_url": "https://example.com/webhook"}
    )
    assert payload["callback_url"] == "https://example.com/webhook"
