"""The no-generation first check stays aligned with the actual model contract."""

import json
from typing import get_args
from unittest.mock import AsyncMock, patch

import pytest

from core.client import client
from core.server import mcp
from core.types import NanoBananaModel
from tools.info_tools import nanobanana_list_models


@pytest.mark.asyncio
async def test_model_reference_uses_actual_literal_without_network():
    with patch.object(client, "generate_image", new_callable=AsyncMock) as generate:
        response = json.loads(await nanobanana_list_models())
    assert response["models"] == list(get_args(NanoBananaModel))
    assert "authentication is not checked" in response["verification"]
    assert "current account pricing" in response["pricing"]
    assert "existing task ID" in response["task_queries"]
    generate.assert_not_awaited()


@pytest.mark.asyncio
async def test_registered_reference_tool_is_discoverable_and_callable():
    tools = await mcp.list_tools()
    assert "nanobanana_list_models" in {tool.name for tool in tools}
    result = await mcp.call_tool("nanobanana_list_models", {})
    assert "nano-banana-2.1" in str(result)
