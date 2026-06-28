#!/usr/bin/env python3
"""
AceDataCloud MCP Server — manage your AceDataCloud account via the console API.

A Model Context Protocol (MCP) server exposing the AceDataCloud platform
management API (balances, usage, API keys, services, orders, platform tokens,
models, announcements) as tools.
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
        logger.debug(f"[MCP AceDataCloud] {text}")
        return
    try:
        print(text, file=sys.stderr)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode(), file=sys.stderr)


def get_version() -> str:
    """Get the package version."""
    try:
        return metadata.version("mcp-acedatacloud")
    except metadata.PackageNotFoundError:
        return "dev"


def main() -> None:
    """Run the AceDataCloud MCP server."""
    parser = argparse.ArgumentParser(
        description="AceDataCloud MCP Server — account management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mcp-acedatacloud                  # Run with stdio transport (default)
  mcp-acedatacloud --transport http # Run with HTTP transport
  mcp-acedatacloud --version        # Show version

Environment Variables:
  ACEDATACLOUD_PLATFORM_TOKEN     Platform token (required)
  PLATFORM_API_BASE_URL           API base (default: https://platform.acedata.cloud)
  PLATFORM_REQUEST_TIMEOUT        Request timeout in seconds (default: 30)
  LOG_LEVEL                       Logging level (default: INFO)
        """,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"mcp-acedatacloud {get_version()}",
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
    safe_print("  AceDataCloud MCP Server — Account Management")
    safe_print("=" * 50)
    safe_print("")
    safe_print(f"  Version:   {get_version()}")
    safe_print(f"  Transport: {args.transport}")
    safe_print(f"  Log Level: {settings.log_level}")
    safe_print("")

    # Validate configuration
    if not settings.is_configured and args.transport != "http":
        safe_print("  [ERROR] ACEDATACLOUD_PLATFORM_TOKEN not configured!")
        safe_print("  Create one at https://platform.acedata.cloud/console/platform-tokens")
        safe_print("")
        sys.exit(1)

    if args.transport == "http":
        safe_print("  [OK] HTTP mode - tokens from request headers")
    else:
        safe_print("  [OK] Platform token configured")
    safe_print("")

    # Import tools and prompts to register them
    safe_print("  Loading tools and prompts...")
    import prompts  # noqa: F401, I001
    import tools  # noqa: F401

    safe_print("  [OK] Tools and prompts loaded")
    safe_print("")
    safe_print("=" * 50)
    safe_print("  Ready for MCP connections")
    safe_print("=" * 50)
    safe_print("")

    try:
        if args.transport == "http":
            import contextlib

            import uvicorn
            from starlette.applications import Starlette
            from starlette.requests import Request
            from starlette.responses import JSONResponse
            from starlette.routing import BaseRoute, Mount, Route

            from core.client import set_request_api_token
            from core.server import oauth_provider

            class BearerTokenMiddleware:
                """Pure-ASGI fallback (used only when OAuth is disabled): lift the
                request's bearer token into the per-request context so a caller
                can authenticate with a platform token directly. When OAuth is
                enabled, the provider's load_access_token does this instead.
                """

                def __init__(self, app):  # type: ignore[no-untyped-def]
                    self.app = app

                async def __call__(self, scope, receive, send):  # type: ignore[no-untyped-def]
                    if scope.get("type") == "http":
                        headers = dict(scope.get("headers") or [])
                        auth = headers.get(b"authorization", b"").decode()
                        if auth.lower().startswith("bearer "):
                            set_request_api_token(auth[7:].strip())
                    await self.app(scope, receive, send)

            async def health(_request: Request) -> JSONResponse:
                return JSONResponse({"status": "ok"})

            @contextlib.asynccontextmanager
            async def lifespan(_app: Starlette):  # type: ignore[no-untyped-def]
                async with mcp.session_manager.run():
                    yield

            mcp.settings.stateless_http = True
            mcp.settings.json_response = True
            mcp.settings.streamable_http_path = "/mcp"

            routes: list[BaseRoute] = [Route("/health", health)]
            # When OAuth is enabled, FastMCP serves the discovery + DCR + token
            # endpoints automatically; we only add the consent callback route.
            if oauth_provider is not None:
                routes.append(Route("/oauth/callback", oauth_provider.handle_callback))
            routes.append(Mount("/", app=mcp.streamable_http_app()))

            app = Starlette(routes=routes, lifespan=lifespan)
            if oauth_provider is None:
                # BYOC fallback only — OAuth path sets the token via the provider.
                app.add_middleware(BearerTokenMiddleware)
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
