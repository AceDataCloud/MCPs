"""Public MCP tool schema contracts."""

import tools  # noqa: F401
from core.server import mcp


async def test_create_video_accepts_optional_uuid_task_id() -> None:
    tool = next(tool for tool in await mcp.list_tools() if tool.name == "maestro_create_video")
    schema = tool.inputSchema

    assert "task_id" not in schema["required"]
    task_id = schema["properties"]["task_id"]
    assert {item.get("format") for item in task_id["anyOf"]} == {"uuid", None}
    assert task_id["default"] is None
