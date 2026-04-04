#!/usr/bin/env python3
"""
MCP Serp Server - Google Search Results via AceDataCloud API.

A Model Context Protocol (MCP) server that provides tools for performing
Google searches using the SERP API through the AceDataCloud platform.
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
        logger.debug(f"[MCP Serp] {text}")
        return

    try:
        print(text, file=sys.stderr)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode(), file=sys.stderr)


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("mcp-serp")
    except metadata.PackageNotFoundError:
        return "dev"


def main() -> None:
    """Run the MCP Serp server."""
    parser = argparse.ArgumentParser(
        description="MCP Serp Server - Google Search Results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mcp-serp                    # Run with stdio transport (default)
  mcp-serp --transport http   # Run with HTTP transport
  mcp-serp --version          # Show version

Environment Variables:
  ACEDATACLOUD_API_TOKEN      API token from AceDataCloud (required)
  SERP_REQUEST_TIMEOUT        Request timeout in seconds (default: 30)
  LOG_LEVEL                   Logging level (default: INFO)
        """,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"mcp-serp {get_version()}",
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
    safe_print("  MCP Serp Server - Google Search Results")
    safe_print("=" * 50)
    safe_print("")
    safe_print(f"  Version:   {get_version()}")
    safe_print(f"  Transport: {args.transport}")
    safe_print(f"  Log Level: {settings.log_level}")
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
    safe_print("    - serp_google_search")
    safe_print("    - serp_google_images")
    safe_print("    - serp_google_news")
    safe_print("    - serp_google_videos")
    safe_print("    - serp_google_places")
    safe_print("    - serp_google_maps")
    safe_print("    - serp_list_search_types")
    safe_print("    - serp_list_countries")
    safe_print("    - serp_list_languages")
    safe_print("    - serp_list_time_ranges")
    safe_print("    - serp_get_usage_guide")
    safe_print("")
    safe_print("  Available prompts:")
    safe_print("    - serp_search_guide")
    safe_print("    - serp_workflow_examples")
    safe_print("    - serp_query_tips")
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
                return RedirectResponse("https://cdn.acedata.cloud/2870040497.png", status_code=301)

            async def server_card(_request: Request) -> JSONResponse:
                """MCP Server Card for Smithery and other registries."""
                return JSONResponse(
                    {
                        "serverInfo": {"name": "MCP Serp"},
                        "authentication": {"required": True, "schemes": ["bearer"]},
                        "tools": [
                            {
                                "name": "serp_google_search",
                                "description": "Search Google for web results",
                            },
                            {"name": "serp_google_images", "description": "Search Google Images"},
                            {"name": "serp_google_news", "description": "Search Google News"},
                            {"name": "serp_google_videos", "description": "Search Google Videos"},
                            {"name": "serp_google_places", "description": "Search Google Places"},
                            {"name": "serp_google_maps", "description": "Search Google Maps"},
                            {
                                "name": "serp_list_search_types",
                                "description": "List available search types",
                            },
                            {
                                "name": "serp_list_countries",
                                "description": "List supported countries",
                            },
                            {
                                "name": "serp_list_languages",
                                "description": "List supported languages",
                            },
                            {
                                "name": "serp_list_time_ranges",
                                "description": "List time range options",
                            },
                            {"name": "serp_get_usage_guide", "description": "Get API usage guide"},
                        ],
                        "prompts": [
                            {
                                "name": "serp_search_guide",
                                "description": "Guide for search queries",
                            },
                            {"name": "serp_workflow_examples", "description": "Example workflows"},
                            {"name": "serp_query_tips", "description": "Tips for better queries"},
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
