"""Unit tests for async submission behavior in the HTTP client."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from core.client import NanoBananaClient
from core.exceptions import NanoBananaAPIError


def test_with_async_callback_injects_default_callback() -> None:
    """Long-running NanoBanana operations should default to async submission."""
    client = NanoBananaClient(api_token="test-token", base_url="https://api.test.com")
    payload = client._with_async_callback({"action": "generate"})
    assert payload["async"] is True


@pytest.mark.asyncio
async def test_generate_image_async_returns_submission_without_polling(mock_image_response) -> None:
    """Async MCP mode should return task submission immediately instead of polling."""
    client = NanoBananaClient(api_token="test-token", base_url="https://api.test.com")
    client.generate_image = AsyncMock(return_value=mock_image_response)
    client.query_task = AsyncMock()

    result = await client.generate_image_async(action="generate", prompt="test")

    assert result == mock_image_response
    client.query_task.assert_not_called()


@pytest.mark.asyncio
async def test_request_forbidden_error_403_uses_api_error() -> None:
    """Content-safety 403 responses are API errors, not auth failures."""
    client = NanoBananaClient(api_token="test-token", base_url="https://api.test.com")
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.json.return_value = {
        "success": False,
        "error": {
            "code": "forbidden",
            "message": "The request was blocked by content safety checks.",
        },
    }
    mock_response.text = "Forbidden"

    with patch("httpx.AsyncClient") as mock_client:
        mock_instance = AsyncMock()
        mock_instance.post.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_instance

        with pytest.raises(NanoBananaAPIError, match="content safety") as exc_info:
            await client.request("/nano-banana/images", {"action": "generate"})

    assert exc_info.value.code == "forbidden"
    assert exc_info.value.status_code == 403
