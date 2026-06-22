"""MCP Server initialization (public, no-auth by default)."""

import logging

from mcp.server.fastmcp import FastMCP

from core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# The docs server is public: OAuth is only wired up if MCP_SERVER_URL is set
# (it is intentionally left unset in deployment so a naked `initialize` works).
mcp_kwargs: dict = {"host": "0.0.0.0"}
oauth_provider = None

mcp = FastMCP(settings.server_name, **mcp_kwargs)

logger.info(f"Initialized MCP server: {settings.server_name}")
