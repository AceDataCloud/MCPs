"""Load canonical customer-facing documentation targets for MCP packages."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

CATALOG_PATH = Path(__file__).with_name("mcp_catalog.json")
PLATFORM_ROOT = "https://platform.acedata.cloud"
UUID_RE = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")


def load_manifest() -> dict[str, Any]:
    manifest = json.loads(CATALOG_PATH.read_text())
    if manifest.get("schema_version") != 2:
        raise ValueError("MCP catalog schema_version must be 2")
    return manifest


def load_catalog() -> dict[str, dict[str, Any]]:
    return load_manifest()["services"]


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
