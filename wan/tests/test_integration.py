"""
Integration tests for Wan MCP Server.

These tests make REAL API calls to verify all tools work correctly.
Run with: pytest tests/test_integration.py -v -s

Note: These tests require ACEDATACLOUD_API_TOKEN to be set.
They are skipped in CI environments without the token.
"""

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
    async def test_generate_video_basic(self):
        """Test basic video generation with real API."""
        from tools.video_tools import wan_generate_video

        result = await wan_generate_video(
            prompt="A simple test video, blue sky with clouds",
        )

        print("\n=== Generate Video Result ===")
        print(result)

        assert "Task ID:" in result
        if "Error:" not in result:
            assert "Video ID:" in result or "State:" in result


class TestInfoTools:
    """Integration tests for informational tools."""

    @pytest.mark.asyncio
    async def test_list_models(self):
        """Test wan_list_models tool."""
        from tools.info_tools import wan_list_models

        result = await wan_list_models()

        print("\n=== List Models Result ===")
        print(result)

        assert "wan" in result.lower()

    @pytest.mark.asyncio
    async def test_list_actions(self):
        """Test wan_list_actions tool."""
        from tools.info_tools import wan_list_actions

        result = await wan_list_actions()

        print("\n=== List Actions Result ===")
        print(result)

        assert "wan_generate_video" in result
        assert "wan_get_task" in result


class TestTaskTools:
    """Integration tests for task query tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_get_task_with_real_id(self):
        """Test querying a task - first generate, then query."""
        from tools.task_tools import wan_get_task
        from tools.video_tools import wan_generate_video

        gen_result = await wan_generate_video(
            prompt="Quick test video",
        )

        print("\n=== Generation Result ===")
        print(gen_result)

        if "Task ID:" in gen_result:
            lines = gen_result.split("\n")
            task_id = None
            for line in lines:
                if line.startswith("Task ID:"):
                    task_id = line.replace("Task ID:", "").strip()
                    break

            if task_id and task_id != "N/A":
                print(f"\n=== Querying Task: {task_id} ===")
                task_result = await wan_get_task(task_id)
                print(task_result)

                assert "Task ID:" in task_result


class TestClientDirectly:
    """Test the client module directly."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_client_generate_video(self):
        """Test client.generate_video directly."""
        from core.client import WanClient

        client = WanClient()

        result = await client.generate_video(
            action="text2video",
            prompt="Very short test video",
        )

        print("\n=== Client Direct Result ===")
        print(result)

        assert result.get("success") is True or "error" in result
        if result.get("success"):
            assert "task_id" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--tb=short"])
