#!/usr/bin/env python3
"""Build the sanitized MCP lifecycle contract consumed by discovery surfaces."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tomllib
from pathlib import Path
from typing import Any

from mcp_catalog import CATALOG_PATH, load_manifest

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = Path(__file__).with_name("mcp_discovery_export.json")
ALLOWED_AUTH_ENVS = {
    "ACEDATACLOUD_API_TOKEN",
    "ACEDATACLOUD_PLATFORM_TOKEN",
    "DISCORD_BOT_TOKEN",
}


def _catalog_digest() -> str:
    return f"sha256:{hashlib.sha256(CATALOG_PATH.read_bytes()).hexdigest()}"


def build_export() -> dict[str, Any]:
    manifest = load_manifest()
    services = []
    for service_id, entry in sorted(manifest["services"].items()):
        package = entry["package"]
        project = tomllib.loads((ROOT / service_id / "pyproject.toml").read_text())["project"]
        scripts = project.get("scripts") or {}
        if package["name"] != project["name"]:
            raise ValueError(f"{service_id}: package name does not match pyproject.toml")
        if package["command"] not in scripts:
            raise ValueError(f"{service_id}: command is not declared by pyproject.toml")
        env = entry["local_auth"]["env"]
        if env not in ALLOWED_AUTH_ENVS:
            raise ValueError(f"{service_id}: unsupported credential environment {env}")
        item = {
            "id": service_id,
            "lifecycle": entry["status"],
            "package": package,
            "local_auth": entry["local_auth"],
            "documentation": {
                key: entry[key]
                for key in ("type", "alias", "id")
                if key in entry
            },
        }
        if "hosted" in entry:
            item["hosted"] = entry["hosted"]
        services.append(item)
    return {
        "schema_version": 1,
        "source": "AceDataCloud/MCPs",
        "source_digest": _catalog_digest(),
        "services": services,
    }


def render() -> str:
    return json.dumps(build_export(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = render()
    if args.check:
        if not args.output.is_file() or args.output.read_text() != expected:
            print(f"{args.output} is stale; run {Path(__file__).name}", file=sys.stderr)
            return 1
        print(f"MCP discovery export is current ({len(build_export()['services'])} services)")
        return 0
    args.output.write_text(expected)
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
