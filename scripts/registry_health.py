#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_URL = (
    "https://registry.modelcontextprotocol.io/v0.1/servers"
    "?search=io.github.AceDataCloud&limit=100&version=latest"
)
EXCEPTIONS_PATH = Path(__file__).with_name("registry_health_exceptions.json")
CATALOG_PATH = Path(__file__).with_name("mcp_catalog.json")


@dataclass(frozen=True)
class Surface:
    alias: str
    name: str
    package: str
    remote: str
    status: str


@dataclass(frozen=True)
class Finding:
    key: str
    kind: str
    alias: str
    detail: str


def load_json_url(url: str, timeout: int = 30) -> Any:
    request = urllib.request.Request(
        url, headers={"User-Agent": "acedatacloud-registry-health"}
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def local_surfaces() -> dict[str, Surface]:
    statuses = json.loads(CATALOG_PATH.read_text())["services"]
    surfaces: dict[str, Surface] = {}
    for path in sorted(ROOT.glob("*/server.json")):
        alias = path.parent.name
        data = json.loads(path.read_text())
        packages = data.get("packages") or []
        remotes = data.get("remotes") or []
        if len(packages) != 1 or len(remotes) != 1:
            raise RuntimeError(f"{alias}: expected exactly one package and remote")
        surfaces[data["name"]] = Surface(
            alias=alias,
            name=data["name"],
            package=packages[0]["identifier"],
            remote=remotes[0]["url"],
            status=statuses[alias]["status"],
        )
    return surfaces


def registry_surfaces(payload: dict[str, Any]) -> dict[str, Surface]:
    surfaces: dict[str, Surface] = {}
    for item in payload.get("servers") or []:
        data = item["server"]
        packages = data.get("packages") or []
        remotes = data.get("remotes") or []
        package = packages[0]["identifier"] if len(packages) == 1 else ""
        remote = remotes[0]["url"] if len(remotes) == 1 else ""
        surfaces[data["name"]] = Surface(
            alias="",
            name=data["name"],
            package=package,
            remote=remote,
            status="active",
        )
    return surfaces


def compare_surfaces(
    local: dict[str, Surface], registry: dict[str, Surface]
) -> list[Finding]:
    findings: list[Finding] = []
    for name, surface in local.items():
        published = registry.get(name)
        if surface.status == "active" and not published:
            findings.append(
                Finding(
                    f"registry_missing:{surface.alias}",
                    "registry_missing",
                    surface.alias,
                    name,
                )
            )
        if surface.status == "retired" and published:
            findings.append(
                Finding(
                    f"retired_registry_active:{surface.alias}",
                    "retired_registry_active",
                    surface.alias,
                    name,
                )
            )
        if not published:
            continue
        if surface.package != published.package:
            findings.append(
                Finding(
                    f"package_mismatch:{surface.alias}",
                    "package_mismatch",
                    surface.alias,
                    f"{surface.package} != {published.package}",
                )
            )
        if surface.remote != published.remote:
            findings.append(
                Finding(
                    f"remote_mismatch:{surface.alias}",
                    "remote_mismatch",
                    surface.alias,
                    f"{surface.remote} != {published.remote}",
                )
            )
    for name in sorted(set(registry) - set(local)):
        findings.append(Finding(f"local_missing:{name}", "local_missing", name, name))
    return findings


def health_url(remote: str) -> str:
    parsed = urllib.parse.urlparse(remote)
    return urllib.parse.urlunparse(
        (parsed.scheme, parsed.netloc, "/health", "", "", "")
    )


def live_findings(local: dict[str, Surface]) -> list[Finding]:
    findings: list[Finding] = []
    for surface in local.values():
        if surface.status != "active":
            continue
        try:
            load_json_url(f"https://pypi.org/pypi/{surface.package}/json")
        except (OSError, ValueError, urllib.error.HTTPError) as exc:
            findings.append(
                Finding(
                    f"pypi_unhealthy:{surface.alias}",
                    "pypi_unhealthy",
                    surface.alias,
                    str(exc),
                )
            )
        try:
            request = urllib.request.Request(
                health_url(surface.remote),
                headers={"User-Agent": "acedatacloud-registry-health"},
            )
            with urllib.request.urlopen(request, timeout=20) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}")
        except (OSError, RuntimeError, urllib.error.HTTPError) as exc:
            findings.append(
                Finding(
                    f"remote_unhealthy:{surface.alias}",
                    "remote_unhealthy",
                    surface.alias,
                    str(exc),
                )
            )
    return findings


def classify(
    findings: list[Finding], exceptions: dict[str, Any], today: date
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    active: list[dict[str, Any]] = []
    blocking: list[dict[str, Any]] = []
    for finding in findings:
        row = asdict(finding)
        exception = exceptions.get(finding.key)
        if exception:
            row["exception"] = exception
            row["exception_active"] = (
                date.fromisoformat(exception["expires_on"]) >= today
            )
        else:
            row["exception_active"] = False
        active.append(row)
        if not row["exception_active"]:
            blocking.append(row)
    return active, blocking


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit AceDataCloud MCP Registry, package, and remote health"
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--skip-live", action="store_true")
    args = parser.parse_args()

    local = local_surfaces()
    registry = registry_surfaces(load_json_url(REGISTRY_URL))
    findings = compare_surfaces(local, registry)
    if not args.skip_live:
        findings.extend(live_findings(local))
    exceptions = json.loads(EXCEPTIONS_PATH.read_text())["exceptions"]
    active, blocking = classify(findings, exceptions, date.today())
    report = {
        "schema_version": 1,
        "checked_on": date.today().isoformat(),
        "local_manifests": len(local),
        "registry_latest": len(registry),
        "findings": active,
        "blocking": blocking,
    }
    rendered = json.dumps(report, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n")
    print(rendered)
    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
