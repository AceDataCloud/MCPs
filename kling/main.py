#!/usr/bin/env python3
"""
MCP Kling Server - AI Video Generation via AceDataCloud API.

A Model Context Protocol (MCP) server that provides tools for generating
AI videos using Kling through the AceDataCloud platform.
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
        logger.debug(f"[MCP Kling] {text}")
        return

    try:
        print(text, file=sys.stderr)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode(), file=sys.stderr)


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("mcp-kling")
    except metadata.PackageNotFoundError:
        return "dev"


def main() -> None:
    """Run the MCP Kling server."""
    parser = argparse.ArgumentParser(
        description="MCP Kling Server - AI Video Generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mcp-kling                    # Run with stdio transport (default)
  mcp-kling --transport http   # Run with HTTP transport
  mcp-kling --version          # Show version

Environment Variables:
  ACEDATACLOUD_API_TOKEN     API token from AceDataCloud (required)
  KLING_DEFAULT_MODEL        Default model (default: kling-v2-master)
  KLING_DEFAULT_MODE         Default mode (default: std)
  KLING_DEFAULT_ASPECT_RATIO Default aspect ratio (default: 16:9)
  KLING_REQUEST_TIMEOUT      Request timeout in seconds (default: 1800)
  LOG_LEVEL                  Logging level (default: INFO)
        """,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"mcp-kling {get_version()}",
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
    safe_print("  MCP Kling Server - AI Video Generation")
    safe_print("=" * 50)
    safe_print("")
    safe_print(f"  Version:      {get_version()}")
    safe_print(f"  Transport:    {args.transport}")
    safe_print(f"  Model:        {settings.default_model}")
    safe_print(f"  Mode:         {settings.default_mode}")
    safe_print(f"  Aspect Ratio: {settings.default_aspect_ratio}")
    safe_print(f"  Log Level:    {settings.log_level}")
    safe_print("")

    # Validate configuration
    if not settings.is_configured and args.transport != "http":
        safe_print("  [ERROR] ACEDATACLOUD_API_TOKEN not configured!")
        safe_print("  Get your token from https://platform.acedata.cloud")
        safe_print("")
        sys.exit(1)

    if args.transport == "http":
        safe_print("  [OK] HTTP mode - tokens from request headers")
    else:
        safe_print("  [OK] API token configured")
    safe_print("")

    # Import tools and prompts to register them
    safe_print("  Loading tools and prompts...")
    import prompts  # noqa: F401, I001
    import tools  # noqa: F401

    safe_print("  [OK] Tools and prompts loaded")
    safe_print("")
    safe_print("  Available tools:")
    safe_print("    - kling_generate_video")
    safe_print("    - kling_generate_video_from_image")
    safe_print("    - kling_extend_video")
    safe_print("    - kling_generate_motion")
    safe_print("    - kling_get_task")
    safe_print("    - kling_get_tasks_batch")
    safe_print("    - kling_list_models")
    safe_print("    - kling_list_actions")
    safe_print("")
    safe_print("  Available prompts:")
    safe_print("    - kling_video_generation_guide")
    safe_print("    - kling_workflow_examples")
    safe_print("    - kling_prompt_suggestions")
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
            from starlette.routing import Mount, Route

            from core.server import oauth_provider

            async def health(_request: Request) -> JSONResponse:
                return JSONResponse({"status": "ok"})

            async def favicon(_request: Request) -> RedirectResponse:
                return RedirectResponse("https://cdn.acedata.cloud/kling-icon.png", status_code=301)

            async def server_card(_request: Request) -> JSONResponse:
                """MCP Server Card for Smithery and other registries."""
                return JSONResponse(
                    {
                        "serverInfo": {"name": "MCP Kling"},
                        "authentication": {"required": True, "schemes": ["bearer"]},
                        "tools": [
                            {
                                "name": "kling_generate_video",
                                "description": "Generate video from text",
                            },
                            {
                                "name": "kling_generate_video_from_image",
                                "description": "Generate video from image",
                            },
                            {
                                "name": "kling_extend_video",
                                "description": "Extend existing video",
                            },
                            {
                                "name": "kling_generate_motion",
                                "description": "Transfer motion to character",
                            },
                            {"name": "kling_get_task", "description": "Query task status"},
                            {"name": "kling_get_tasks_batch", "description": "Query multiple tasks"},
                            {"name": "kling_list_models", "description": "List available models"},
                            {"name": "kling_list_actions", "description": "List available actions"},
                        ],
                        "prompts": [
                            {
                                "name": "kling_video_generation_guide",
                                "description": "Guide for video generation",
                            },
                            {
                                "name": "kling_workflow_examples",
                                "description": "Example workflows",
                            },
                            {
                                "name": "kling_prompt_suggestions",
                                "description": "Prompt suggestions",
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
            routes: list[Route | Mount] = [
                Route("/health", health),
                Route("/favicon.ico", favicon),
                Route("/.well-known/mcp/server-card.json", server_card),
            ]

            # Add OAuth callback route if OAuth is enabled
            if oauth_provider:
                routes.append(Route("/oauth/callback", oauth_provider.handle_callback))

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
