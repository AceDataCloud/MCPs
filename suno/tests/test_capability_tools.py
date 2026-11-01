"""Exercise the new public audio operations through FastMCP dispatch."""

from unittest.mock import AsyncMock, patch

import pytest

from core.server import mcp
from tools import capability_tools  # noqa: F401
from tools.audio_tools import suno_generate_custom_music, suno_generate_music


@pytest.mark.parametrize(
    ("name", "arguments", "action"),
    [
        (
            "suno_add_stem",
            {
                "audio_id": "source",
                "stem_type": "drums",
                "audio_weight": 0,
                "max_mode": False,
                "variety": "off",
            },
            "add_stem",
        ),
        (
            "suno_extract_stem",
            {"audio_id": "source", "stem_type": "bass", "audio_format": "mp3"},
            "extract_stem",
        ),
        (
            "suno_generate_sound",
            {"sound": "rain", "sound_type": "loop", "bpm": 120, "key": "C#m"},
            "sounds",
        ),
        (
            "suno_adjust_speed",
            {"audio_id": "source", "title": "Slow", "speed_multiplier": 0.5, "keep_pitch": False},
            "adjust_speed",
        ),
    ],
)
async def test_public_actions_dispatch_and_preserve_explicit_values(name, arguments, action):
    with patch(
        "tools.capability_tools.client.generate_audio",
        new=AsyncMock(return_value={"task_id": "task"}),
    ) as call:
        await mcp.call_tool(name, arguments)
    payload = call.await_args.kwargs
    assert payload["action"] == action
    assert all(payload[k] == v for k, v in arguments.items())
    if "max_mode" not in arguments:
        assert "max_mode" not in payload


async def test_generate_controls_leave_enhanced_mode_opt_in():
    with patch(
        "tools.audio_tools.client.generate_audio", new=AsyncMock(return_value={"task_id": "task"})
    ) as call:
        await suno_generate_music(prompt="rain", variety="extra")
        assert call.await_args.kwargs["variety"] == "extra"
        assert "max_mode" not in call.await_args.kwargs
        await suno_generate_custom_music(
            lyric="[Verse] hello", audio_weight=0, variety="off", max_mode=False
        )
        payload = call.await_args.kwargs
        assert payload["custom"] is True
        assert payload["audio_weight"] == 0
        assert payload["max_mode"] is False
        assert payload["variety"] == "off"


async def test_invalid_stem_rejected_before_submission():
    with (
        patch("tools.capability_tools.client.generate_audio", new=AsyncMock()) as call,
        pytest.raises(Exception, match="stem_type"),
    ):
        await mcp.call_tool("suno_extract_stem", {"audio_id": "source", "stem_type": "unknown"})
    call.assert_not_awaited()
