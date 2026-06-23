"""Meta tool — list the other AceData Cloud MCP servers."""

import json
from functools import lru_cache
from pathlib import Path

from core.server import mcp

_DATA = Path(__file__).parent.parent / "core" / "data" / "mcp_servers.json"


@lru_cache(maxsize=1)
def _servers() -> dict:
    # Generated from MCPs/*/server.json (the single source of truth) — see
    # scripts/gen_mcp_servers.py. Not hand-maintained.
    try:
        return json.loads(_DATA.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"count": 0, "servers": []}


@mcp.tool()
async def acedatacloud_list_mcp_servers() -> str:
    """List AceData Cloud's other MCP servers and how to connect to them.

    Each entry includes the remote streamable-http URL (zero-install) and the
    PyPI package (for a local stdio install via uvx).
    """
    data = _servers()
    return json.dumps(
        {"count": data.get("count", 0), "servers": data.get("servers", [])},
        ensure_ascii=False,
        indent=2,
    )
