from unittest.mock import AsyncMock, patch

import pytest

from tools.audio_tools import suno_generate_custom_music, suno_generate_music


@pytest.mark.parametrize("value", [None, False, True])
@pytest.mark.parametrize("custom", [False, True])
async def test_personalization_preserves_explicit_false(value, custom, mock_audio_response):
    with patch(
        "tools.audio_tools.client.generate_audio", new=AsyncMock(return_value=mock_audio_response)
    ) as call:
        if custom:
            await suno_generate_custom_music(lyric="lyrics", personalization=value)
        else:
            await suno_generate_music(prompt="acoustic", personalization=value)
    body = call.await_args.kwargs
    assert body["action"] == "generate"
    assert "use_personalization" not in body
    assert ("personalization" in body) is (value is not None)
    if value is not None:
        assert body["personalization"] is value
