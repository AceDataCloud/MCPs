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
NAMESPACE = "io.github.AceDataCloud/"
OFFICIAL_META = "io.modelcontextprotocol.registry/official"
EXCEPTIONS_PATH = Path(__file__).with_name("registry_health_exceptions.json")
CATALOG_PATH = Path(__file__).with_name("mcp_catalog.json")


@dataclass(frozen=True)
class Surface:
    alias: str
    name: str
    package: str
    remote: str
    status: str
    package_version: str = ""


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
        if data["name"] in surfaces:
            raise RuntimeError(f"duplicate local Registry name: {data['name']}")
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
        if not data["name"].startswith(NAMESPACE):
            continue
        official = item.get("_meta", {}).get(OFFICIAL_META, {})
        status = official.get("status")
        if status not in {"active", "deprecated", "deleted"}:
            raise RuntimeError(f"{data['name']}: missing or invalid official status")
        if official.get("isLatest") is not True:
            raise RuntimeError(f"{data['name']}: response is not latest")
        if data["name"] in surfaces:
            raise RuntimeError(f"duplicate latest Registry name: {data['name']}")
        packages = data.get("packages") or []
        remotes = data.get("remotes") or []
        package = packages[0]["identifier"] if len(packages) == 1 else ""
        remote = remotes[0]["url"] if len(remotes) == 1 else ""
        surfaces[data["name"]] = Surface(
            alias="",
            name=data["name"],
            package=package,
            remote=remote,
            status=status,
            package_version=packages[0].get("version", "")
            if len(packages) == 1
            else "",
        )
    return surfaces


def load_registry() -> dict[str, Any]:
    """Read every latest page; never silently truncate a namespace audit."""
    servers: list[dict[str, Any]] = []
    url = REGISTRY_URL
    seen: set[str] = set()
    while True:
        payload = load_json_url(url)
        servers.extend(payload.get("servers") or [])
        cursor = payload.get("metadata", {}).get("nextCursor")
        if not cursor:
            return {"servers": servers}
        if cursor in seen:
            raise RuntimeError("Registry returned a repeated pagination cursor")
        seen.add(cursor)
        url = REGISTRY_URL + "&" + urllib.parse.urlencode({"cursor": cursor})


def compare_surfaces(
    local: dict[str, Surface], registry: dict[str, Surface]
) -> list[Finding]:
    findings: list[Finding] = []
    for name, surface in local.items():
        published = registry.get(name)
        if surface.status == "active" and (
            not published or published.status != "active"
        ):
            findings.append(
                Finding(
                    f"registry_missing:{surface.alias}",
                    "registry_missing",
                    surface.alias,
                    name,
                )
            )
        if surface.status == "retired" and published and published.status == "active":
            findings.append(
                Finding(
                    f"retired_registry_active:{surface.alias}",
                    "retired_registry_active",
                    surface.alias,
                    name,
                )
            )
        if not published or surface.status == "retired":
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


def live_findings(
    local: dict[str, Surface], registry: dict[str, Surface]
) -> list[Finding]:
    findings: list[Finding] = []
    for surface in local.values():
        if surface.status != "active":
            continue
        published = registry.get(surface.name)
        if not published or published.status != "active":
            continue
        try:
            if not published.package_version:
                raise ValueError("Registry package version is missing")
            package = urllib.parse.quote(published.package, safe="")
            version = urllib.parse.quote(published.package_version, safe="")
            release = load_json_url(f"https://pypi.org/pypi/{package}/{version}/json")
            files = release.get("urls") or []
            if not any(not file.get("yanked", False) for file in files):
                raise ValueError(
                    "Registry package version has no installable artifacts"
                )
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
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Validate source manifests without reading any external service",
    )
    args = parser.parse_args()

    local = local_surfaces()
    registry = {} if args.local_only else registry_surfaces(load_registry())
    findings = [] if args.local_only else compare_surfaces(local, registry)
    if not args.skip_live and not args.local_only:
        findings.extend(live_findings(local, registry))
    exceptions = json.loads(EXCEPTIONS_PATH.read_text())["exceptions"]
    active, blocking = classify(findings, exceptions, date.today())
    catalog = json.loads(CATALOG_PATH.read_text())["services"]
    manifest_aliases = {surface.alias for surface in local.values()}
    report = {
        "schema_version": 2,
        "checked_on": date.today().isoformat(),
        "mode": "local"
        if args.local_only
        else "contract"
        if args.skip_live
        else "live",
        "local_manifests": len(local),
        "registry_latest": None if args.local_only else len(registry),
        "registry_active": None
        if args.local_only
        else sum(s.status == "active" for s in registry.values()),
        "active_without_manifest": sorted(
            alias
            for alias, entry in catalog.items()
            if entry["status"] == "active" and alias not in manifest_aliases
        ),
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
