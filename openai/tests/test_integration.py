"""Integration tests for OpenAI API.

These tests require a valid API token and will make real API calls.
Run with: pytest tests/test_integration.py -m integration
"""

import pytest

from core.client import OpenaiClient


@pytest.mark.integration
class TestOpenaiIntegration:
    """Integration tests for OpenAI API."""

    @pytest.mark.asyncio
    async def test_chat_completion(self, api_token):
        """Test basic chat completion."""
        c = OpenaiClient(api_token=api_token)
        result = await c.chat_completion(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Say hello in one word."}],
        )

        assert "choices" in result
        assert len(result["choices"]) > 0
        assert "message" in result["choices"][0]

    @pytest.mark.asyncio
    async def test_embeddings(self, api_token):
        """Test embeddings creation."""
        c = OpenaiClient(api_token=api_token)
        result = await c.embeddings(
            model="text-embedding-3-small",
            input="Hello world",
        )

        assert "data" in result
        assert len(result["data"]) > 0
        assert "embedding" in result["data"][0]

    @pytest.mark.asyncio
    async def test_image_generation(self, api_token):
        """Test image generation."""
        c = OpenaiClient(api_token=api_token)
        result = await c.image_generate(
            model="dall-e-3",
            prompt="A simple red circle on white background",
            n=1,
        )

        assert "data" in result
        assert len(result["data"]) > 0

    @pytest.mark.asyncio
    async def test_responses_api(self, api_token):
        """Test the responses API."""
        c = OpenaiClient(api_token=api_token)
        result = await c.responses(
            model="gpt-4o",
            input="Say hello.",
        )

        assert result is not None
