#!/usr/bin/env python3
"""Limit this goose plugin to its service tools; reuse the published MCP package."""

import asyncio
import copy
import os
import shutil
import sys

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server

PACKAGE = "mcp-openai-pro==2026.10.17.0"
ENTRYPOINT = "mcp-openai-pro"
PLUGIN = "gpt-image-by-acedatacloud"
ALLOWED_TOOLS = frozenset(
    {
        "openai_generate_image",
        "openai_edit_image",
        "openai_get_task",
        "openai_list_image_models",
    }
)


def image_tool(tool: types.Tool) -> types.Tool:
    """Keep the GPT Image profile from accepting other image model families."""
    result = copy.deepcopy(tool)
    if tool.name in {"openai_generate_image", "openai_edit_image"}:
        model = result.inputSchema.get("properties", {}).get("model", {})
        model["pattern"] = "^gpt-image-"
        model["description"] = "A public gpt-image-* model supported by your account."
    return result


async def serve() -> None:
    if not os.environ.get("ACEDATACLOUD_API_TOKEN", "").strip():
        raise ValueError("Set ACEDATACLOUD_API_TOKEN to a service API key before starting goose")
    command = shutil.which("uvx")
    if not command:
        raise ValueError("Install uv first; uvx must be on PATH")
    params = StdioServerParameters(
        command=command,
        args=["--from", PACKAGE, ENTRYPOINT],
        env=dict(os.environ),
    )
    async with (
        stdio_client(params) as (reader, writer),
        ClientSession(reader, writer) as client,
    ):
        await client.initialize()
        tools = []
        cursor = None
        while True:
            page = await client.list_tools(cursor=cursor)
            tools.extend(image_tool(tool) for tool in page.tools if tool.name in ALLOWED_TOOLS)
            cursor = page.nextCursor
            if not cursor:
                break
        names = {tool.name for tool in tools}
        missing = ALLOWED_TOOLS - names
        if missing:
            raise ValueError(f"Published MCP package is missing required tools: {sorted(missing)}")
        server = Server(PLUGIN)

        @server.list_tools()
        async def list_tools() -> list[types.Tool]:
            return tools

        @server.call_tool()
        async def call_tool(name: str, arguments: dict) -> types.CallToolResult:
            if name not in ALLOWED_TOOLS:
                return types.CallToolResult(
                    isError=True,
                    content=[
                        types.TextContent(type="text", text="Tool not exposed by this plugin")
                    ],
                )
            if name in {"openai_generate_image", "openai_edit_image"}:
                model = arguments.get("model", "gpt-image-1")
                if not isinstance(model, str) or not model.startswith("gpt-image-"):
                    return types.CallToolResult(
                        isError=True,
                        content=[types.TextContent(type="text", text="Choose a gpt-image-* model")],
                    )
            return await client.call_tool(name, arguments)

        async with stdio_server() as (stdin, stdout):
            await server.run(stdin, stdout, server.create_initialization_options())


def main() -> int:
    try:
        asyncio.run(serve())
    except (ValueError, OSError) as exc:
        print(f"{PLUGIN}: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
