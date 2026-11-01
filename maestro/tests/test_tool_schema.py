"""Public MCP tool schema contracts."""

import tools  # noqa: F401
from core.server import mcp


async def test_create_video_schema_matches_openapi_body() -> None:
    tool = next(tool for tool in await mcp.list_tools() if tool.name == "maestro_create_video")
    schema = tool.inputSchema

    assert "prompt" in schema["required"]
    assert "task_id" not in schema["properties"]
    assert "quality" not in schema["properties"]
    assert schema["properties"]["file_urls"]["anyOf"][0]["maxItems"] == 20
    assert schema["properties"]["langs"]["anyOf"][0]["minItems"] == 1
    assert schema["properties"]["langs"]["anyOf"][0]["maxItems"] == 1
    assert "One task delivers one video in one language" in tool.description
    assert "0.7 Credits per actual" in tool.description
    assert "never above the requested duration" in tool.description
    assert "no scenario or language surcharge" in tool.description
    assert "Failed jobs and task polling are free" in tool.description


async def test_list_tasks_schema_matches_history_contract() -> None:
    tool = next(tool for tool in await mcp.list_tools() if tool.name == "maestro_list_tasks")
    schema = tool.inputSchema

    assert schema["properties"]["limit"]["default"] == 20
    assert schema["properties"]["limit"]["minimum"] == 1
    assert schema["properties"]["limit"]["maximum"] == 100
    assert "created_at_min" in schema["properties"]
    assert "created_at_max" in schema["properties"]
    assert "strictly after" in schema["properties"]["created_at_min"]["description"]
    assert "strictly before" in schema["properties"]["created_at_max"]["description"]
    assert not schema.get("required")


async def test_public_custom_style_and_voice_are_forwarded_but_invalid_voice_is_rejected():
    from unittest.mock import AsyncMock, patch

    import pytest

    with patch(
        "tools.video_tools.client.create_video", new=AsyncMock(return_value={"task_id": "t"})
    ) as call:
        await mcp.call_tool(
            "maestro_create_video",
            {
                "prompt": "A documentary",
                "style": "watercolor documentary",
                "voice": "0123456789abcdef0123456789abcdef",
            },
        )
        assert call.await_args.args[0]["style"] == "watercolor documentary"
        assert call.await_args.args[0]["voice"] == "0123456789abcdef0123456789abcdef"
        call.reset_mock()
        for voice in ("arbitrary narrator", "abc", "g" * 32):
            with pytest.raises(Exception, match="validation error"):
                await mcp.call_tool(
                    "maestro_create_video", {"prompt": "A documentary", "voice": voice}
                )
        call.assert_not_awaited()
