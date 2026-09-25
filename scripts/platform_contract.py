#!/usr/bin/env python3
"""Prepare a scoped consumer sync report from a PlatformBackend contract bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def mapping_directories(path: Path) -> set[str]:
    directories: set[str] = set()
    in_mappings = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line == "mappings:":
            in_mappings = True
            continue
        if in_mappings and line.startswith("  ") and not line.startswith("    ") and line.rstrip().endswith(":"):
            directories.add(line.strip()[:-1])
    return directories


def resolve_targets(bundle: Path, mapping: Path, kind: str, requested: list[str]) -> list[dict[str, Any]]:
    manifest = load_json(bundle / "manifest.json")
    available = set(manifest["services"])
    selected = sorted(available if requested == ["all"] else set(requested))
    unknown = set(selected) - available
    if unknown:
        raise ValueError(f"unknown PlatformBackend services: {sorted(unknown)}")
    directories = mapping_directories(mapping)
    targets: dict[str, dict[str, Any]] = {}
    for alias in selected:
        contract = load_json(bundle / f"services/{alias}.json")
        target = contract.get("targets", {}).get(kind, alias)
        if target not in directories:
            continue
        current = targets.setdefault(target, {"directory": target, "services": [], "contract_files": []})
        current["services"].append(alias)
        current["contract_files"].extend([f"services/{alias}.json", contract.get("openapi")])
    return [
        {**item, "services": sorted(item["services"]), "contract_files": sorted({name for name in item["contract_files"] if name})}
        for item in sorted(targets.values(), key=lambda value: value["directory"])
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--mapping", type=Path, required=True)
    parser.add_argument("--kind", choices=("mcp", "cli"), required=True)
    parser.add_argument("--services", default="all")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    requested = [item.strip() for item in args.services.split(",") if item.strip()] or ["all"]
    targets = resolve_targets(args.bundle, args.mapping, args.kind, requested)
    args.output.write_text(json.dumps({"kind": args.kind, "targets": targets}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(",".join(item["directory"] for item in targets))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
