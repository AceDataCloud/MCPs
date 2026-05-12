"""Unit tests for async submission behavior in the HTTP client."""

import pytest

from core.client import MidjourneyClient


def test_with_async_callback_injects_default_callback() -> None:
    """Long-running Midjourney operations should default to async submission."""
    client = MidjourneyClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback({"action": "generate"})
    assert payload["callback_url"] == "https://api.acedata.cloud/health"


def test_with_async_callback_preserves_explicit_callback() -> None:
    """User-provided callbacks should not be overwritten."""
    client = MidjourneyClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback(
        {"action": "generate", "callback_url": "https://example.com/webhook"}
    )
    assert payload["callback_url"] == "https://example.com/webhook"


@pytest.mark.asyncio
async def test_shorten_calls_shorten_endpoint() -> None:
    """Shorten convenience method should target /midjourney/shorten."""
    client = MidjourneyClient(api_token="test-token", base_url="https://api.test.com")
    captured: dict[str, object] = {}

    async def fake_request(endpoint: str, payload: dict, timeout: float | None = None) -> dict:
        captured["endpoint"] = endpoint
        captured["payload"] = payload
        captured["timeout"] = timeout
        return {"prompts": ["short prompt"]}

    client.request = fake_request  # type: ignore[method-assign]
    result = await client.shorten(prompt="a very long prompt")

    assert captured["endpoint"] == "/midjourney/shorten"
    assert captured["payload"] == {"prompt": "a very long prompt"}
    assert result == {"prompts": ["short prompt"]}
