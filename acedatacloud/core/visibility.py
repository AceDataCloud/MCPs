"""Expose management tools using the current credential's canonical permissions."""

from mcp.types import Tool

from contracts.platform_operations import OPERATIONS
from core.client import client, get_request_api_token, get_request_subject
from core.exceptions import PlatformError
from core.server import mcp


async def list_visible_tools() -> list[Tool]:
    tools = await mcp.list_tools()
    if not (get_request_api_token() or client.api_token):
        return tools  # Local schema/installation inspection without a configured credential.
    try:
        subject = await get_request_subject()
    except PlatformError:
        subject = {}
    granted = set(subject.get("permissions", []))
    by_tool = {operation.tool: operation for operation in OPERATIONS if operation.tool}
    visible = []
    for tool in tools:
        operation = by_tool.get(tool.name)
        if (
            operation is None
            or operation.authentication == "public"
            or subject.get("id")
            and set(operation.required_permissions).issubset(granted)
        ):
            visible.append(tool)
    return visible


mcp._mcp_server.list_tools()(list_visible_tools)
