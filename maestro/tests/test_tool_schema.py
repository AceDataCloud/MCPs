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
