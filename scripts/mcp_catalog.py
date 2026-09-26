"""Load canonical customer-facing documentation targets for MCP packages."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

CATALOG_PATH = Path(__file__).with_name("mcp_catalog.json")
PLATFORM_ROOT = "https://platform.acedata.cloud"
ACQUISITION_MARKER = "<!-- canonical-acquisition -->"
UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def load_catalog() -> dict[str, dict[str, Any]]:
    return json.loads(CATALOG_PATH.read_text())["services"]


def acquisition_target(alias: str, entry: dict[str, Any]) -> str | None:
    status = entry.get("status")
    if status == "retired":
        return None
    if status != "active":
        raise ValueError(f"invalid status {status!r}")
    if not re.fullmatch(r"[a-z0-9-]+", alias):
        raise ValueError(f"invalid acquisition alias {alias!r}")
    return f"{PLATFORM_ROOT}/?utm_source=github&utm_medium=repo&utm_campaign=mcp-{alias}"


def documentation_target(entry: dict[str, Any]) -> tuple[str | None, str | None]:
    status = entry.get("status")
    if status == "retired":
        return None, None
    if status != "active":
        raise ValueError(f"invalid status {status!r}")

    target_type = entry.get("type")
    if target_type == "document":
        alias = entry.get("alias")
        if not isinstance(alias, str) or not alias or UUID_RE.fullmatch(alias):
            raise ValueError("document target requires a canonical alias")
        return f"{PLATFORM_ROOT}/documents/{alias}", "Documentation"
    if target_type == "service":
        service_id = entry.get("id")
        if not isinstance(service_id, str) or not UUID_RE.fullmatch(service_id):
            raise ValueError("service target requires a UUID")
        return f"{PLATFORM_ROOT}/services/{service_id}", "Service details"
    raise ValueError(f"active target has unsupported type {target_type!r}")
