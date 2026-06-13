"""
Integration tests for Grok MCP Server.

These tests make REAL API calls to verify all tools work correctly.
Run with: pytest tests/test_integration.py -v -s

Note: These tests require ACEDATACLOUD_API_TOKEN to be set.
They are skipped in CI environments without the token.
"""

import json
import os
import sys

import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Load environment variables
from dotenv import load_dotenv

load_dotenv()

# Check if API token is configured
HAS_API_TOKEN = bool(os.getenv("ACEDATACLOUD_API_TOKEN"))

# Decorator to skip tests that require API token
requires_api_token = pytest.mark.skipif(
    not HAS_API_TOKEN,
    reason="ACEDATACLOUD_API_TOKEN not configured - skipping integration test",
)


class TestVideoTools:
    """Integration tests for video generation tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_text_to_video_basic(self) -> None:
        """Test basic text-to-video generation with real API."""
        from tools.video_tools import grok_text_to_video

        result = await grok_text_to_video(
            prompt="A simple blue sky with white clouds drifting slowly",
            model="grok-imagine-video",
            aspect_ratio="16:9",
            resolution="480p",
            duration=3,
        )

        print("\n=== Text to Video Result ===")
        print(result)

        assert "task_id" in result


class TestInfoTools:
    """Integration tests for informational tools."""

    @pytest.mark.asyncio
    async def test_list_models(self) -> None:
        """Test grok_list_models tool."""
        from tools.info_tools import grok_list_models

        result = await grok_list_models()

        print("\n=== List Models Result ===")
        print(result)

        assert "grok-imagine-video" in result
        assert "grok-imagine-video-1.5-preview" in result

    @pytest.mark.asyncio
    async def test_list_actions(self) -> None:
        """Test grok_list_actions tool."""
        from tools.info_tools import grok_list_actions

        result = await grok_list_actions()

        print("\n=== List Actions Result ===")
        print(result)

        assert "grok_text_to_video" in result
        assert "grok_image_to_video" in result
        assert "grok_get_task" in result

    @pytest.mark.asyncio
    async def test_get_prompt_guide(self) -> None:
        """Test grok_get_prompt_guide tool."""
        from tools.info_tools import grok_get_prompt_guide

        result = await grok_get_prompt_guide()

        print("\n=== Prompt Guide Result ===")
        print(result)

        assert len(result) > 0


class TestTaskTools:
    """Integration tests for task query tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_get_task_with_real_id(self) -> None:
        """Test querying a task - first generate, then query."""
        from tools.task_tools import grok_get_task
        from tools.video_tools import grok_text_to_video

        # Generate a video first
        gen_result = await grok_text_to_video(
            prompt="A simple test scene with blue sky",
            model="grok-imagine-video",
            aspect_ratio="16:9",
            resolution="480p",
            duration=3,
        )

        print("\n=== Generate Result ===")
        print(gen_result)

        gen_data = json.loads(gen_result)
        task_id = gen_data.get("task_id")
        if task_id:
            # Query the task
            task_result = await grok_get_task(task_id=task_id)
            print("\n=== Task Result ===")
            print(task_result)
            assert task_id in task_result
