"""Expose management tools using the current credential's canonical permissions."""

from mcp.types import Tool

from contracts.platform_operations import OPERATIONS
from contracts.tool_catalog import (
    CROSS_ACCOUNT_TOOLS,
    INFO_TOOL,
    TOOL_CATALOG,
    advertised_tools,
    tool_description,
)
from core.client import client, get_request_api_token, get_request_subject
from core.config import settings
from core.exceptions import PlatformError
from core.server import mcp


def _describe(tool: Tool) -> Tool:
    entry = TOOL_CATALOG.get(tool.name)
    if entry is None:
        return tool
    description = tool_description(tool.name, tool.description or "")
    if tool.name in CROSS_ACCOUNT_TOOLS:
        description += (
            "\nAdministrative cross-account collection query. Requires "
            + CROSS_ACCOUNT_TOOLS[tool.name]
            + ". Use the native account tool for your own data."
        )
    metadata = {
        **(tool.meta or {}),
        "acedatacloud/category": entry.category,
        "acedatacloud/audience": entry.audience,
    }
    return tool.model_copy(update={"description": description, "meta": metadata})


async def list_visible_tools() -> list[Tool]:
    tools = await mcp.list_tools()
    advertised = advertised_tools(settings.tool_profile)
    tools = [_describe(tool) for tool in tools if tool.name in advertised]
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
            tool.name == INFO_TOOL
            or operation is not None
            and (
                operation.authentication == "public"
                or subject.get("id")
                and set(TOOL_CATALOG[tool.name].required_permissions).issubset(granted)
            )
        ):
            visible.append(tool)
    return visible


mcp._mcp_server.list_tools()(list_visible_tools)
