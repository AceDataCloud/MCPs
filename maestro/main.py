#!/usr/bin/env python3
"""Maestro MCP server entrypoint."""

import argparse
import contextlib
import logging
import sys
from importlib import metadata

from dotenv import load_dotenv

load_dotenv()

from core.config import settings
from core.server import mcp

logger = logging.getLogger(__name__)


def get_version() -> str:
    """Return the installed package version."""
    try:
        return metadata.version("mcp-maestro")
    except metadata.PackageNotFoundError:
        return "dev"


def safe_print(text: str) -> None:
    """Write status messages to stderr without corrupting stdio transport."""
    if not sys.stderr.isatty():
        logger.debug("[Maestro MCP] %s", text)
        return
    print(text, file=sys.stderr)


def main() -> None:
    """Run Maestro MCP over stdio or HTTP."""
    parser = argparse.ArgumentParser(description="Maestro MCP Server - end-to-end AI video")
    parser.add_argument("--version", action="version", version=f"mcp-maestro {get_version()}")
    parser.add_argument("--transport", choices=["stdio", "http"], default=settings.transport)
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if not settings.is_configured and args.transport != "http":
        safe_print("ACEDATACLOUD_API_TOKEN is required for stdio mode")
        raise SystemExit(1)

    import prompts  # noqa: F401, I001
    import tools  # noqa: F401

    if args.transport == "stdio":
        mcp.run(transport="stdio")
        return

    import uvicorn
    from starlette.applications import Starlette
    from starlette.requests import Request
    from starlette.responses import JSONResponse, RedirectResponse
    from starlette.routing import BaseRoute, Mount, Route

    from core.server import oauth_provider

    async def health(_request: Request) -> JSONResponse:
        return JSONResponse({"status": "ok"})

    async def favicon(_request: Request) -> RedirectResponse:
        return RedirectResponse("https://cdn.acedata.cloud/df0e7b7eea.svg", status_code=301)

    async def server_card(_request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "serverInfo": {"name": "Maestro MCP"},
                "authentication": {"required": True, "schemes": ["bearer", "oauth2"]},
                "tools": [
                    {
                        "name": "maestro_create_video",
                        "description": "Produce or revise a complete video",
                    },
                    {
                        "name": "maestro_get_task",
                        "description": "Get video progress and outputs",
                    },
                    {
                        "name": "maestro_list_tasks",
                        "description": "List recent Maestro tasks",
                    },
                ],
                "prompts": [
                    {
                        "name": "maestro_video_workflow",
                        "description": "Recommended asynchronous video workflow",
                    }
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

    routes: list[BaseRoute] = [
        Route("/health", health),
        Route("/favicon.ico", favicon),
        Route("/.well-known/mcp/server-card.json", server_card),
    ]
    if oauth_provider:
        routes.append(Route("/oauth/callback", oauth_provider.handle_callback))
    routes.extend(mcp.sse_app().routes)
    routes.append(Mount("/", app=mcp.streamable_http_app()))

    uvicorn.run(Starlette(routes=routes, lifespan=lifespan), host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
