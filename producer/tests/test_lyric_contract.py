"""Lyrics must select the custom API path; instrumental extensions need no lyrics."""

from unittest.mock import AsyncMock, patch

import pytest

from core.server import mcp
from tools.audio_tools import producer_extend_music, producer_replace_section


@pytest.mark.parametrize(
    "name,arguments",
    [
        (
            "producer_extend_music",
            {
                "audio_id": "source",
                "continue_at": 10,
                "lyric": "[Verse] exact words",
                "async": False,
            },
        ),
        (
            "producer_replace_section",
            {
                "audio_id": "source",
                "replace_section_start": 10,
                "replace_section_end": 20,
                "lyric": "[Verse] exact words",
                "async": False,
            },
        ),
    ],
)
async def test_lyrics_use_custom_path_in_actual_mcp_dispatch(name, arguments):
    with patch(
        "tools.audio_tools.client.generate_audio", new=AsyncMock(return_value={"task_id": "task"})
    ) as call:
        await mcp.call_tool(name, arguments)
    payload = call.await_args.kwargs
    assert payload["custom"] is True
    assert payload["lyric"] == arguments["lyric"]
    assert payload["async"] is False


async def test_instrumental_extension_without_lyrics():
    with patch(
        "tools.audio_tools.client.generate_audio", new=AsyncMock(return_value={"task_id": "task"})
    ) as call:
        await producer_extend_music(audio_id="source", continue_at=10, instrumental=True)
    assert call.await_args.kwargs["instrumental"] is True


async def test_missing_lyrics_rejected_before_paid_submission():
    with patch("tools.audio_tools.client.generate_audio", new=AsyncMock()) as call:
        with pytest.raises(ValueError, match="lyric is required"):
            await producer_extend_music(audio_id="source", continue_at=10)
        with pytest.raises(ValueError, match="continue_at"):
            await producer_extend_music(audio_id="source", continue_at=0, instrumental=True)
    call.assert_not_awaited()


async def test_prompt_only_replacement_does_not_change_to_lyric_mode():
    with patch(
        "tools.audio_tools.client.generate_audio", new=AsyncMock(return_value={"task_id": "task"})
    ) as call:
        await producer_replace_section(
            audio_id="source", replace_section_start=1, replace_section_end=3, prompt="piano"
        )
    assert "custom" not in call.await_args.kwargs
    assert call.await_args.kwargs["prompt"] == "piano"
