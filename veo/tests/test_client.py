"""Unit tests for async submission behavior in the HTTP client."""

from core.client import VeoClient


def test_with_async_callback_injects_default_callback() -> None:
    """Long-running Veo operations should default to async submission."""
    client = VeoClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback({"action": "text2video"})
    assert payload["callback_url"] == "https://api.acedata.cloud/health"


def test_with_async_callback_preserves_explicit_callback() -> None:
    """User-provided callbacks should not be overwritten."""
    client = VeoClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback(
        {"action": "text2video", "callback_url": "https://example.com/webhook"}
    )
    assert payload["callback_url"] == "https://example.com/webhook"


def test_new_endpoint_methods_exist() -> None:
    """The 4 new mountsea-backed endpoints (upsample / extend / reshoot /
    objects) must each have a dedicated convenience method on VeoClient.
    """
    client = VeoClient(api_token="test-token", base_url="https://api.test.com")
    for method in (
        "upsample_video",
        "extend_video",
        "reshoot_video",
        "manipulate_object",
    ):
        assert callable(getattr(client, method)), f"VeoClient is missing {method}"


def test_get_1080p_kept_for_backcompat() -> None:
    """The legacy get_1080p() method must remain callable so existing MCP
    clients keep working after the new /veo/upsample tool ships.
    """
    client = VeoClient(api_token="test-token", base_url="https://api.test.com")
    assert callable(client.get_1080p)
