"""Exercise the goose image-only MCP boundary against a fake, local package."""

import os
import sys
from pathlib import Path

import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.mark.asyncio
async def test_goose_profile_limits_tools_models_and_preserves_errors(tmp_path):
    backend = tmp_path / "backend.py"
    backend.write_text(
        """from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent
m = FastMCP("fixture")
@m.tool()
def openai_generate_image(prompt: str, model: str = "gpt-image-1") -> str:
    return "local fixture image result"
@m.tool()
def openai_edit_image(image: str, prompt: str, model: str = "gpt-image-1") -> str:
    return "local fixture edit result"
@m.tool()
def openai_get_task(id: str) -> CallToolResult:
    return CallToolResult(isError=True, content=[TextContent(type="text", text="fixture task failure")])
@m.tool()
def openai_list_image_models() -> str:
    return "gpt-image-1"
@m.tool()
def openai_chat_completion(prompt: str) -> str:
    return "must not be exposed"
m.run()
"""
    )
    launcher = tmp_path / "uvx"
    launcher.write_text(f'#!/bin/sh\nexec "{sys.executable}" "{backend}"\n')
    launcher.chmod(0o755)
    env = {
        key: value
        for key, value in os.environ.items()
        if key in {"HOME", "PATH", "TMPDIR", "SYSTEMROOT"}
    }
    env.update(
        PATH=str(tmp_path) + os.pathsep + env.get("PATH", ""),
        ACEDATACLOUD_API_TOKEN="local-fixture-only",
        ACEDATACLOUD_API_BASE_URL="http://127.0.0.1:9/blocked",
    )
    adapter = Path(__file__).resolve().parents[1] / "goose" / "filtered_server.py"
    params = StdioServerParameters(command=sys.executable, args=[str(adapter)], env=env)
    async with stdio_client(params) as (reader, writer), ClientSession(reader, writer) as client:
        await client.initialize()
        result = await client.list_tools()
        assert {tool.name for tool in result.tools} == {
            "openai_generate_image",
            "openai_edit_image",
            "openai_get_task",
            "openai_list_image_models",
        }
        hidden = await client.call_tool("openai_chat_completion", {"prompt": "hello"})
        assert hidden.isError
        other_model = await client.call_tool(
            "openai_generate_image", {"prompt": "test", "model": "nano-banana"}
        )
        assert other_model.isError
        good = await client.call_tool("openai_generate_image", {"prompt": "test"})
        assert not good.isError
        assert "local fixture image result" in str(good.content)
        failed = await client.call_tool("openai_get_task", {"id": "existing-fixture-id"})
        assert failed.isError
        assert "fixture task failure" in str(failed.content)
