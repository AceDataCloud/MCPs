"""Unit tests for async submission behavior in the HTTP client."""

from core.client import GrokClient


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
