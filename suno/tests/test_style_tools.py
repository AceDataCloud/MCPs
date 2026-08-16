"""Unit tests for style and voice tools (mocked client, no network)."""

import json
from unittest.mock import AsyncMock, patch

import pytest

from tools.style_tools import suno_create_voice, suno_optimize_style


@pytest.mark.asyncio
async def test_create_voice_allows_name_to_be_omitted(mock_audio_response):
    """The upstream voices schema only requires audio_url."""
    with patch(
        "tools.style_tools.client.create_voice",
        new=AsyncMock(return_value=mock_audio_response),
    ) as mock_create:
        result = await suno_create_voice(audio_url="https://example.com/voice.wav")

    assert mock_create.await_args.kwargs == {"audio_url": "https://example.com/voice.wav"}
    assert json.loads(result)["mcp_async_submission"]["poll_tool"] == "suno_get_task"


@pytest.mark.asyncio
async def test_optimize_style_adds_polling_guidance(mock_audio_response):
    with patch(
        "tools.style_tools.client.get_style",
        new=AsyncMock(return_value=mock_audio_response),
    ) as mock_style:
        result = await suno_optimize_style(prompt="rock guitar")

    mock_style.assert_awaited_once_with(prompt="rock guitar")
    assert json.loads(result)["mcp_async_submission"]["poll_tool"] == "suno_get_task"
