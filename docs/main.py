#!/usr/bin/env python3
"""AceDataCloud Docs MCP Server.

A public, zero-install MCP server that exposes the AceData Cloud documentation,
API catalog, OpenAPI specs, model list, pricing, and runnable code examples as
tools. No API token required — it only reads public, read-only endpoints.
"""

import argparse
import logging
import sys
from importlib import metadata

from dotenv import load_dotenv

load_dotenv()

from core.config import settings  # noqa: E402
from core.server import mcp  # noqa: E402

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def get_version() -> str:
    try:
        return metadata.version("mcp-docs")
    except metadata.PackageNotFoundError:
        return "dev"


def main() -> None:
    parser = argparse.ArgumentParser(description="AceDataCloud Docs MCP Server")
    parser.add_argument("--version", action="version", version=f"mcp-docs {get_version()}")
    parser.add_argument(
        "--transport", choices=["stdio", "http"], default="stdio", help="Transport (default stdio)"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP transport")
    args = parser.parse_args()

    logger.info(
        f"AceDataCloud Docs MCP {get_version()} — transport={args.transport} (public, no-auth)"
    )

    # Register tools + prompts.
    import prompts  # noqa: F401
    import tools  # noqa: F401

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
                return JSONResponse(
                    {
                        "serverInfo": {"name": "AceDataCloud Docs"},
                        "authentication": {"required": False},
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

            routes: list[BaseRoute] = [
                Route("/health", health),
                Route("/favicon.ico", favicon),
                Route("/.well-known/mcp/server-card.json", server_card),
            ]
            for sse_route in mcp.sse_app().routes:
                routes.append(sse_route)
            routes.append(Mount("/", app=mcp.streamable_http_app()))

            app = Starlette(routes=routes, lifespan=lifespan)
            uvicorn.run(app, host="0.0.0.0", port=args.port)
        else:
            mcp.run(transport="stdio")
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
