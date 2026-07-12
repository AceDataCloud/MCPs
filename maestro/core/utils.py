"""Formatting helpers for MCP tool results."""

import json
from typing import Any


def format_result(data: dict[str, Any]) -> str:
    """Serialize an API response for MCP clients."""
    return json.dumps(data, ensure_ascii=False, indent=2)
