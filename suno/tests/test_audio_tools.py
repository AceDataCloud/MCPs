"""Unit tests for audio tools (mocked client, no network)."""

from unittest.mock import AsyncMock, patch

import pytest

from tools.audio_tools import suno_generate_inspo


class TestInspoTool:
    """Tests for the suno_generate_inspo tool."""

    @pytest.mark.asyncio
    async def test_inspo_builds_expected_payload(self, mock_audio_response):
        """Inspo tool should send action=inspo with audio_urls and optional params."""
        with patch(
            "tools.audio_tools.client.generate_audio",
            new=AsyncMock(return_value=mock_audio_response),
        ) as mock_generate:
            result = await suno_generate_inspo(
                audio_urls=["https://cdn1.suno.ai/ref.mp3"],
                prompt="warm acoustic folk",
                style="acoustic, folk, warm",
                title="Inspo Demo",
                model="chirp-v5",
                audio_weight=0.6,
            )

        mock_generate.assert_awaited_once()
        payload = mock_generate.await_args.kwargs
        assert payload["action"] == "inspo"
        assert payload["audio_urls"] == ["https://cdn1.suno.ai/ref.mp3"]
        assert payload["model"] == "chirp-v5"
        assert payload["audio_weight"] == 0.6
        assert payload["style"] == "acoustic, folk, warm"
        assert "test-task-123" in result

    @pytest.mark.asyncio
    async def test_inspo_omits_unset_optional_params(self, mock_audio_response):
        """Optional params left empty should not be sent in the payload."""
        with patch(
            "tools.audio_tools.client.generate_audio",
            new=AsyncMock(return_value=mock_audio_response),
        ) as mock_generate:
            await suno_generate_inspo(audio_urls=["https://cdn1.suno.ai/ref.mp3"])

        payload = mock_generate.await_args.kwargs
        assert payload["action"] == "inspo"
        assert "audio_weight" not in payload
        assert "style" not in payload
        assert "prompt" not in payload
