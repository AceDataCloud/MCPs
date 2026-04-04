"""Integration tests for Sora API.

These tests require a valid ACEDATACLOUD_API_TOKEN to run.
Run with: pytest tests/test_integration.py -m integration
"""

import pytest

from core.client import SoraClient


@pytest.mark.integration
@pytest.mark.slow
class TestSoraIntegration:
    """Integration tests that require a real API token."""

    @pytest.fixture
    def real_client(self, api_token):
        """Create a client with real API token."""
        return SoraClient(api_token=api_token)

    @pytest.mark.asyncio
    async def test_generate_video(self, real_client):
        """Test actual video generation (async, returns quickly)."""
        result = await real_client.generate_video(
            prompt="A cat sitting on a windowsill",
            model="sora-2",
            size="small",
            duration=10,
            orientation="landscape",
        )

        assert "task_id" in result or "success" in result
        # Note: Full generation takes 1-2 minutes, so we just check the API accepts the request

    @pytest.mark.asyncio
    async def test_query_nonexistent_task(self, real_client):
        """Test querying a task that doesn't exist."""
        result = await real_client.query_task(
            id="nonexistent-task-id",
            action="retrieve",
        )

        # Should return an error or empty result
        assert result is not None
