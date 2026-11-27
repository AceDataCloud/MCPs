"""Run the Tripo MCP over stdio or authenticated HTTP."""

import argparse
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from importlib.metadata import PackageNotFoundError, version

import uvicorn
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import BaseRoute, Mount, Route

import tools  # noqa: F401
from core.config import settings
from core.server import mcp, oauth_provider
from core.server_card import registered_tool_cards


def get_version() -> str:
    try:
        return version("mcp-tripo")
    except PackageNotFoundError:
        return "dev"


def http_app() -> Starlette:
    if oauth_provider is None:
        raise ValueError("Set MCP_SERVER_URL to the hosted HTTPS origin for HTTP transport")

    async def health(_request: Request) -> JSONResponse:
        return JSONResponse({"status": "ok"})

    async def server_card(_request: Request) -> JSONResponse:
        return JSONResponse(
            {
                "serverInfo": {"name": "Tripo 3D", "version": get_version()},
                "authentication": {"required": True, "schemes": ["bearer"]},
                "tools": registered_tool_cards(mcp),
                "prompts": [],
                "resources": [],
            }
        )

    @asynccontextmanager
    async def lifespan(_app: Starlette) -> AsyncIterator[None]:
        async with mcp.session_manager.run():
            yield

    mcp.settings.stateless_http = True
    mcp.settings.json_response = True
    mcp.settings.streamable_http_path = "/mcp"
    routes: list[BaseRoute] = [
        Route("/health", health),
        Route("/.well-known/mcp/server-card.json", server_card),
        Route("/oauth/callback", oauth_provider.handle_callback),
        *mcp.sse_app().routes,
        Mount("/", app=mcp.streamable_http_app()),
    ]
    return Starlette(routes=routes, lifespan=lifespan)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tripo 3D MCP server")
    parser.add_argument("--version", action="version", version=f"mcp-tripo {get_version()}")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()
    if args.transport == "http":
        uvicorn.run(http_app(), host="0.0.0.0", port=args.port)
    else:
        settings.validate()
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
