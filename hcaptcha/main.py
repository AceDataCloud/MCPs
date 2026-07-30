#!/usr/bin/env python3
"""MCP HCaptcha Server - Captcha solving via AceDataCloud."""

import argparse
import logging
import sys
from importlib import metadata

from dotenv import load_dotenv

load_dotenv()

from core.config import settings
from core.server import mcp

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def safe_print(text: str) -> None:
    if not sys.stderr.isatty():
        logger.debug(f"[MCP HCaptcha] {text}")
        return
    try:
        print(text, file=sys.stderr)
    except UnicodeEncodeError:
        print(text.encode("ascii", errors="replace").decode(), file=sys.stderr)


def get_version() -> str:
    try:
        return metadata.version("mcp-hcaptcha")
    except metadata.PackageNotFoundError:
        return "dev"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MCP HCaptcha Server - Captcha solving via AceDataCloud",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  mcp-hcaptcha                    # Run with stdio transport (default)
  mcp-hcaptcha --transport http   # Run with HTTP transport
  mcp-hcaptcha --version          # Show version

Environment Variables:
  ACEDATACLOUD_API_TOKEN     API token from AceDataCloud (required)
  HCAPTCHA_REQUEST_TIMEOUT   Request timeout in seconds (default: 120)
  LOG_LEVEL                  Logging level (default: INFO)
        """,
    )
    parser.add_argument("--version", action="version", version=f"mcp-hcaptcha {get_version()}")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    safe_print("")
    safe_print("=" * 50)
    safe_print("  MCP HCaptcha Server")
    safe_print("=" * 50)
    safe_print("")
    safe_print(f"  Version:   {get_version()}")
    safe_print(f"  Transport: {args.transport}")
    safe_print(f"  Log Level: {settings.log_level}")
    safe_print("")

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

    safe_print("  Loading tools and prompts...")
    import prompts  # noqa: F401, I001
    import tools  # noqa: F401

    safe_print("  [OK] Tools and prompts loaded")
    safe_print("")
    safe_print("  Available tools:")
    safe_print("    - hcaptcha_recognize")
    safe_print("    - hcaptcha_get_token")
    safe_print("    - hcaptcha_get_task")
    safe_print("    - hcaptcha_get_usage_guide")
    safe_print("    - hcaptcha_get_api_info")
    safe_print("")
    safe_print("  Available prompts:")
    safe_print("    - hcaptcha_guide")
    safe_print("    - hcaptcha_workflow_examples")
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
            from starlette.responses import JSONResponse, RedirectResponse
            from starlette.routing import BaseRoute, Mount, Route

            from core.server import oauth_provider

            async def health(_request: Request) -> JSONResponse:
                return JSONResponse({"status": "ok"})

            async def favicon(_request: Request) -> RedirectResponse:
                return RedirectResponse("https://cdn.acedata.cloud/acedata-logo.png", status_code=301)

            async def server_card(_request: Request) -> JSONResponse:
                return JSONResponse({
                    "serverInfo": {"name": "MCP HCaptcha"},
                    "authentication": {"required": True, "schemes": ["bearer"]},
                    "tools": [{"name": "hcaptcha_recognize", "description": "Recognize hCaptcha image challenges"},
                    {"name": "hcaptcha_get_token", "description": "Get an hCaptcha token for a website"},
                    {"name": "hcaptcha_get_task", "description": "Poll a captcha task result"},
                    {"name": "hcaptcha_get_usage_guide", "description": "Get hCaptcha usage guide"},
                    {"name": "hcaptcha_get_api_info", "description": "Get hCaptcha API information"}],
                    "prompts": [{"name": "hcaptcha_guide", "description": "hCaptcha tool selection guide"},
                    {"name": "hcaptcha_workflow_examples", "description": "Example hCaptcha workflows"}],
                    "resources": [],
                })

            @contextlib.asynccontextmanager
            async def lifespan(_app: Starlette):  # type: ignore[no-untyped-def]
                async with mcp.session_manager.run():
                    yield

            mcp.settings.stateless_http = True
            mcp.settings.json_response = True
            mcp.settings.streamable_http_path = "/mcp"
            routes: list[BaseRoute] = [
                Route("/health", health),
                Route("/favicon.ico", favicon),
                Route("/.well-known/mcp/server-card.json", server_card),
            ]
            if oauth_provider:
                routes.append(Route("/oauth/callback", oauth_provider.handle_callback))
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
