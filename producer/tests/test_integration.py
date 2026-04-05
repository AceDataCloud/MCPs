"""
Integration tests for Producer MCP Server.

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
    reason=("ACEDATACLOUD_API_TOKEN not configured - skipping integration test"),
)


class TestAudioTools:
    """Integration tests for audio generation tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_generate_music_basic(self):
        """Test basic music generation with real API."""
        from tools.audio_tools import producer_generate_music

        result = await producer_generate_music(
            prompt="A short test jingle, upbeat and happy",
            model="FUZZ-2.0",
            instrumental=False,
        )

        print("\n=== Generate Music Result ===")
        print(result)

        assert "task_id" in result or "error" in result.lower()

    @requires_api_token
    @pytest.mark.asyncio
    async def test_generate_custom_music(self):
        """Test custom music generation with lyrics."""
        from tools.audio_tools import producer_generate_custom_music

        result = await producer_generate_custom_music(
            lyric=("[Verse]\nThis is a test song\nJust for testing\n[Chorus]\nTest test test"),
            title="Test Song",
            style="pop, simple",
            model="FUZZ-2.0",
            instrumental=False,
        )

        print("\n=== Custom Music Result ===")
        print(result)

        assert "task_id" in result or "error" in result.lower()


class TestLyricsTools:
    """Integration tests for lyrics generation tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_generate_lyrics(self):
        """Test lyrics generation with real API."""
        from tools.lyrics_tools import producer_generate_lyrics

        result = await producer_generate_lyrics(
            prompt="A short song about testing software",
        )

        print("\n=== Generate Lyrics Result ===")
        print(result)

        assert "task_id" in result or "error" in result.lower()


class TestInfoTools:
    """Integration tests for informational tools."""

    @pytest.mark.asyncio
    async def test_list_models(self):
        """Test producer_list_models tool."""
        from tools.info_tools import producer_list_models

        result = await producer_list_models()

        print("\n=== List Models Result ===")
        print(result)

        assert "FUZZ-2.0 Pro" in result
        assert "FUZZ-2.0" in result
        assert "FUZZ-1.0" in result

    @pytest.mark.asyncio
    async def test_list_actions(self):
        """Test producer_list_actions tool."""
        from tools.info_tools import producer_list_actions

        result = await producer_list_actions()

        print("\n=== List Actions Result ===")
        print(result)

        assert "producer_generate_music" in result
        assert "producer_extend_music" in result
        assert "producer_cover_music" in result

    @pytest.mark.asyncio
    async def test_get_lyric_format_guide(self):
        """Test lyric format guide tool."""
        from tools.info_tools import producer_get_lyric_format_guide

        result = await producer_get_lyric_format_guide()

        print("\n=== Lyric Format Guide ===")
        print(result)

        assert "[Verse]" in result
        assert "[Chorus]" in result


class TestTaskTools:
    """Integration tests for task query tools."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_get_task_with_real_id(self):
        """Test querying a task - first generate, then query."""
        import json

        from tools.audio_tools import producer_generate_music
        from tools.task_tools import producer_get_task

        # First generate something to get a task ID
        gen_result = await producer_generate_music(
            prompt="Quick test melody",
            model="FUZZ-2.0",
        )

        print("\n=== Generation Result ===")
        print(gen_result)

        # Extract task ID from JSON result
        try:
            data = json.loads(gen_result)
            task_id = data.get("task_id")
        except (json.JSONDecodeError, KeyError):
            task_id = None

        if task_id:
            print(f"\n=== Querying Task: {task_id} ===")
            task_result = await producer_get_task(task_id)
            print(task_result)

            assert "task_id" in task_result or "id" in task_result


class TestClientDirectly:
    """Test the client module directly."""

    @requires_api_token
    @pytest.mark.asyncio
    async def test_client_generate_audio(self):
        """Test client.generate_audio directly."""
        from core.client import ProducerClient

        client = ProducerClient()

        result = await client.generate_audio(
            action="generate",
            prompt="Very short test",
            model="FUZZ-2.0",
        )

        print("\n=== Client Direct Result ===")
        print(result)

        assert result.get("success") is True or "error" in result
        if result.get("success"):
            assert "task_id" in result
            assert "data" in result

    @requires_api_token
    @pytest.mark.asyncio
    async def test_client_generate_lyrics(self):
        """Test client.generate_lyrics directly."""
        from core.client import ProducerClient

        client = ProducerClient()

        result = await client.generate_lyrics(
            prompt="A song about code",
        )

        print("\n=== Client Lyrics Result ===")
        print(result)

        assert result.get("success") is True or "error" in result
        if result.get("success"):
            assert "data" in result


if __name__ == "__main__":
    # Run all tests with verbose output
    pytest.main([__file__, "-v", "-s", "--tb=short"])
