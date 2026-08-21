"""Unit tests for motion transfer tools."""

from unittest.mock import AsyncMock, patch

import pytest


@pytest.fixture
def mock_client_generate_motion(mock_motion_response):
    """Patch client.generate_motion with a mock that returns a canned response."""
    with patch("tools.motion_tools.client") as mock_client:
        mock_client.generate_motion = AsyncMock(return_value=mock_motion_response)
        yield mock_client


@pytest.mark.asyncio
async def test_callback_url_is_omitted_when_unset(mock_client_generate_motion):
    from tools.motion_tools import kling_generate_motion

    await kling_generate_motion(
        image_url="https://example.com/character.jpg",
        video_url="https://example.com/motion.mp4",
    )

    _, kwargs = mock_client_generate_motion.generate_motion.call_args
    assert "callback_url" not in kwargs
