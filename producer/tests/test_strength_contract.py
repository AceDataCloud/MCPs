"""Validate Producer strength bounds through the public FastMCP dispatcher."""

from unittest.mock import AsyncMock, patch

import pytest
from mcp.server.fastmcp.exceptions import ToolError

from core.server import mcp
from tools import audio_tools  # noqa: F401

CASES = [
    ("producer_generate_music", {"prompt": "warm acoustic folk"}),
    (
        "producer_generate_custom_music",
        {"title": "Spring", "lyric": "[Verse] Spring is here", "prompt": "acoustic folk"},
    ),
]


@pytest.mark.parametrize("tool,arguments", CASES)
async def test_sound_strength_zero_is_rejected_before_submission(tool, arguments):
    with (
        patch("tools.audio_tools.client.generate_audio", new=AsyncMock()) as client,
        pytest.raises(ToolError, match="0.2"),
    ):
        await mcp.call_tool(tool, {**arguments, "sound_strength": 0})
    client.assert_not_awaited()


@pytest.mark.parametrize("tool,arguments", CASES)
@pytest.mark.parametrize("strength", [0.2, 1, None])
async def test_supported_sound_strength_preserves_other_valid_zero_controls(
    tool, arguments, strength
):
    payload = {**arguments, "weirdness": 0, "lyrics_strength": 0}
    if strength is not None:
        payload["sound_strength"] = strength
    with patch(
        "tools.audio_tools.client.generate_audio", new=AsyncMock(return_value={"task_id": "task"})
    ) as client:
        await mcp.call_tool(tool, payload)
    submitted = client.await_args.kwargs
    assert submitted["weirdness"] == 0
    assert submitted["lyrics_strength"] == 0
    if strength is None:
        assert "sound_strength" not in submitted
    else:
        assert submitted["sound_strength"] == strength
