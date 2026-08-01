#!/usr/bin/env python3
"""
MCP Discord Bot Server - Discord automation via Discord Agent Proxy.

A Model Context Protocol (MCP) server that provides tools for interacting
with Discord through a self-hosted Discord Agent Proxy instance.
"""

import argparse
import logging
import sys
from importlib import metadata

from dotenv import load_dotenv

# Load environment variables before importing other modules
load_dotenv()

from core.config import settings
from core.server import mcp

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def safe_print(text: str) -> None:
    """Print to stderr safely, handling encoding issues."""
    if not sys.stderr.isatty():
        logger.debug(f"[MCP Discord Bot] {text}")
        return

    try:
        print(text, file=sys.stderr)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode(), file=sys.stderr)


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("mcp-discord-bot")
    except metadata.PackageNotFoundError:
        return "dev"


def main() -> None:
    """Run the MCP Discord Bot server."""
    parser = argparse.ArgumentParser(
        description="MCP Discord Bot Server - Discord automation via Agent Proxy",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mcp-discord-bot                    # Run with stdio transport (default)
  mcp-discord-bot --transport http   # Run with HTTP transport
  mcp-discord-bot --version          # Show version

Environment Variables:
  DISCORD_BOT_BASE_URL          URL of the deployed Discord Agent Proxy (required)
  DISCORD_BOT_TOKEN             Access token for the Discord Agent Proxy (required)
  DISCORD_BOT_REQUEST_TIMEOUT   Request timeout in seconds (default: 30)
  LOG_LEVEL                     Logging level (default: INFO)
        """,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"mcp-discord-bot {get_version()}",
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http"],
        default="stdio",
        help="Transport mode (default: stdio)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for HTTP transport (default: 8000)",
    )
    args = parser.parse_args()

    # Print startup banner
    safe_print("")
    safe_print("=" * 50)
    safe_print("  MCP Discord Bot Server")
    safe_print("=" * 50)
    safe_print("")
    safe_print(f"  Version:   {get_version()}")
    safe_print(f"  Transport: {args.transport}")
    safe_print(f"  Log Level: {settings.log_level}")
    safe_print("")

    # Validate configuration
    if not settings.is_configured:
        safe_print("  [ERROR] Discord Bot not configured!")
        safe_print("  DISCORD_BOT_BASE_URL and DISCORD_BOT_TOKEN are required.")
        safe_print("  Deploy a Discord Agent Proxy at https://platform.acedata.cloud")
        safe_print("")
        if args.transport != "http":
            sys.exit(1)
    else:
        safe_print(f"  [OK] Bot URL: {settings.bot_base_url}")
        safe_print("  [OK] Bot token configured")
    safe_print("")

    # Import tools and prompts to register them
    safe_print("  Loading tools and prompts...")
    import prompts  # noqa: F401, I001
    import tools  # noqa: F401

    safe_print("  [OK] Tools and prompts loaded")
    safe_print("")
    safe_print("  Available tools:")
    safe_print("    - discord_whoami")
    safe_print("    - discord_list_guilds")
    safe_print("    - discord_list_channels")
    safe_print("    - discord_create_text_channel")
    safe_print("    - discord_list_members")
    safe_print("    - discord_send_message")
    safe_print("    - discord_read_messages")
    safe_print("    - discord_edit_message")
    safe_print("    - discord_delete_message")
    safe_print("    - discord_search_messages")
    safe_print("    - discord_add_reaction")
    safe_print("    - discord_pin_message")
    safe_print("    - discord_create_dm")
    safe_print("    - discord_send_dm")
    safe_print("    - discord_get_usage_guide")
    safe_print("")
    safe_print("  Available prompts:")
    safe_print("    - discord_usage_guide")
    safe_print("    - discord_workflow_examples")
    safe_print("")
    safe_print("=" * 50)
    safe_print("  Ready for MCP connections")
    safe_print("=" * 50)
    safe_print("")

    # Run the server
    try:
        if args.transport == "http":
            import contextlib

            import uvicorn
            from starlette.applications import Starlette
            from starlette.requests import Request
            from starlette.responses import JSONResponse, RedirectResponse
            from starlette.routing import BaseRoute, Mount, Route

            async def health(_request: Request) -> JSONResponse:
                return JSONResponse({"status": "ok"})

            async def favicon(_request: Request) -> RedirectResponse:
                return RedirectResponse("https://cdn.acedata.cloud/2870040497.png", status_code=301)

            async def server_card(_request: Request) -> JSONResponse:
                """MCP Server Card for Smithery and other registries."""
                return JSONResponse(
                    {
                        "serverInfo": {"name": "MCP Discord Bot"},
                        "authentication": {"required": True, "schemes": ["bearer"]},
                        "tools": [
                            {
                                "name": "discord_whoami",
                                "description": "Get the proxied Discord account info",
                            },
                            {
                                "name": "discord_list_guilds",
                                "description": "List all Discord servers",
                            },
                            {
                                "name": "discord_list_channels",
                                "description": "List channels in a Discord server",
                            },
                            {
                                "name": "discord_create_text_channel",
                                "description": "Create a text channel in a Discord server",
                            },
                            {
                                "name": "discord_list_members",
                                "description": "List members of a Discord server",
                            },
                            {
                                "name": "discord_send_message",
                                "description": "Send a message to a Discord channel",
                            },
                            {
                                "name": "discord_read_messages",
                                "description": "Read recent messages from a channel",
                            },
                            {
                                "name": "discord_edit_message",
                                "description": "Edit a message in a Discord channel",
                            },
                            {
                                "name": "discord_delete_message",
                                "description": "Delete a message from a Discord channel",
                            },
                            {
                                "name": "discord_search_messages",
                                "description": "Search for messages in a Discord channel",
                            },
                            {
                                "name": "discord_add_reaction",
                                "description": "Add an emoji reaction to a Discord message",
                            },
                            {
                                "name": "discord_pin_message",
                                "description": "Pin a message in a Discord channel",
                            },
                            {
                                "name": "discord_create_dm",
                                "description": "Open a direct message channel with a user",
                            },
                            {
                                "name": "discord_send_dm",
                                "description": "Send a direct message to a Discord user",
                            },
                            {
                                "name": "discord_get_usage_guide",
                                "description": "Get a usage guide for the Discord Bot tools",
                            },
                        ],
                        "prompts": [
                            {
                                "name": "discord_usage_guide",
                                "description": "Guide for Discord Bot tools",
                            },
                            {
                                "name": "discord_workflow_examples",
                                "description": "Common Discord automation workflow examples",
                            },
                        ],
                        "resources": [],
                    }
                )

            @contextlib.asynccontextmanager
            async def lifespan(_app: Starlette):  # type: ignore[no-untyped-def]
                async with mcp.session_manager.run():
                    yield

            mcp.settings.stateless_http = True
            mcp.settings.json_response = True
            mcp.settings.streamable_http_path = "/mcp"

            # Build routes
            routes: list[BaseRoute] = [
                Route("/health", health),
                Route("/favicon.ico", favicon),
                Route("/.well-known/mcp/server-card.json", server_card),
            ]

            # Mount legacy SSE transport (/sse + /messages) alongside Streamable HTTP (/mcp)
            for sse_route in mcp.sse_app().routes:
                routes.append(sse_route)
            routes.append(Mount("/", app=mcp.streamable_http_app()))

            app = Starlette(routes=routes, lifespan=lifespan)
            uvicorn.run(app, host="0.0.0.0", port=args.port)
        else:
            mcp.run(transport="stdio")
    except KeyboardInterrupt:
        safe_print("\nShutdown requested")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
