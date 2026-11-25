"""Deprecate existing Sora records after checking source and mirror are frozen.

Fixed target and status; this tool cannot publish, reactivate, delete, build or
deploy a server. Default mode is read-only. Only the main-branch manual workflow
may apply changes using its existing organization-owned GitHub OIDC identity.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = "https://registry.modelcontextprotocol.io"
SERVER = "io.github.AceDataCloud/mcp-sora"
SERVER_PATH = urllib.parse.quote(SERVER, safe="")
VERSIONS_URL = f"{REGISTRY}/v0.1/servers/{SERVER_PATH}/versions?include_deleted=true"
OFFICIAL = "io.modelcontextprotocol.registry/official"
MESSAGE = "This integration is retired and is no longer actively offered."


def request_json(
    url: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    token: str | None = None,
) -> Any:
    headers = {"Accept": "application/json", "User-Agent": "AceRegistryRetirement/1"}
    if token:
        headers["Authorization"] = "Bearer " + token
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(
        url,
        data=json.dumps(body).encode() if body is not None else None,
        headers=headers,
        method=method,
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        # Do not echo credential-bearing requests, upstream bodies or URLs.
        raise RuntimeError(f"Remote request failed (HTTP {exc.code})") from None
    except (OSError, ValueError):
        raise RuntimeError("Remote request failed or returned invalid JSON") from None


def assert_frozen(source: str, job: str) -> None:
    if not re.search(
        rf"(?m)^  {re.escape(job)}:\n(?:    #.*\n)*    if: \$\{{\{{ false \}}\}}$",
        source,
    ):
        raise RuntimeError("Retired Sora publish/deploy freeze is missing")


def verify_freeze() -> dict[str, Any]:
    catalog = json.loads((ROOT / "scripts/mcp_catalog.json").read_text())
    if catalog["services"]["sora"]["status"] != "retired":
        raise RuntimeError("Sora must remain retired in the source catalog")
    mirror = request_json(
        "https://api.github.com/repos/AceDataCloud/SoraMCP/commits/main",
        token=os.getenv("GH_TOKEN"),
    )
    mirror_sha = mirror["sha"]
    for filename, job in (("publish.yml", "build"), ("deploy.yaml", "run")):
        assert_frozen((ROOT / "sora/.github/workflows" / filename).read_text(), job)
        data = request_json(
            f"https://api.github.com/repos/AceDataCloud/SoraMCP/contents/.github/workflows/{filename}?ref={mirror_sha}",
            token=os.getenv("GH_TOKEN"),
        )
        assert_frozen(base64.b64decode(data["content"]).decode(), job)
    return {
        "source_retired": True,
        "source_frozen": True,
        "mirror_frozen": True,
        "mirror_commit": mirror_sha,
    }


def version_status(item: dict[str, Any]) -> tuple[str, str]:
    if item.get("server", {}).get("name") != SERVER:
        raise RuntimeError("Refusing a record outside the fixed Sora target")
    version = item["server"].get("version")
    status = item.get("_meta", {}).get(OFFICIAL, {}).get("status")
    if (
        not isinstance(version, str)
        or not version
        or status not in {"active", "deprecated", "deleted"}
    ):
        raise RuntimeError("Invalid Sora lifecycle record")
    return version, status


def versions() -> dict[str, str]:
    url = VERSIONS_URL
    found: dict[str, str] = {}
    seen: set[str] = set()
    while True:
        data = request_json(url)
        for item in data.get("servers", []):
            version, status = version_status(item)
            if version in found:
                raise RuntimeError("Duplicate version in retirement inventory")
            found[version] = status
        cursor = data.get("metadata", {}).get("nextCursor")
        if not cursor:
            break
        if cursor in seen:
            raise RuntimeError("Repeated inventory cursor")
        seen.add(cursor)
        url = VERSIONS_URL + "&" + urllib.parse.urlencode({"cursor": cursor})
    if not found:
        raise RuntimeError("No existing Sora records found; publishing is forbidden")
    return found


def oidc_registry_token() -> str:
    if any(
        os.getenv(key) != expected
        for key, expected in {
            "GITHUB_REPOSITORY": "AceDataCloud/MCPs",
            "GITHUB_REF": "refs/heads/main",
            "GITHUB_EVENT_NAME": "workflow_dispatch",
        }.items()
    ):
        raise RuntimeError(
            "Apply requires the organization-owned main-branch manual workflow"
        )
    url = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL", "")
    token = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN", "")
    if not url.startswith("https://") or not token:
        raise RuntimeError("Existing GitHub Actions OIDC environment is required")
    oidc = request_json(
        url + "&" + urllib.parse.urlencode({"audience": REGISTRY}), token=token
    )["value"]
    exchanged = request_json(
        f"{REGISTRY}/v0.1/auth/github-oidc", method="POST", body={"oidc_token": oidc}
    )
    result = exchanged.get("registry_token")
    if not isinstance(result, str) or not result:
        raise RuntimeError("Registry OIDC exchange did not return a token")
    return result


def retire(report: dict[str, Any], apply: bool) -> None:
    report["freeze"] = verify_freeze()
    before = versions()
    report["before"] = before
    report["changed_versions"] = []
    if not apply or "active" not in before.values():
        report["status"] = "dry-run" if not apply else "already-retired"
        return
    token = oidc_registry_token()
    for version, old_status in before.items():
        if old_status != "active":
            continue
        url = f"{REGISTRY}/v0.1/servers/{SERVER_PATH}/versions/{urllib.parse.quote(version, safe='')}"
        current_version, current_status = version_status(
            request_json(url + "?include_deleted=true", token=token)
        )
        if current_version != version:
            raise RuntimeError("Version detail changed target identity; refusing write")
        if current_status != "active":
            continue
        request_json(
            url + "/status",
            method="PATCH",
            body={"status": "deprecated", "statusMessage": MESSAGE},
            token=token,
        )
        report["changed_versions"].append(version)
    after = versions()
    report["after"] = after
    if "active" in after.values():
        raise RuntimeError(
            "Active Sora records remain; inspect receipt before retrying"
        )
    if not set(before).issubset(after):
        raise RuntimeError("Existing Sora records disappeared; inspect before retrying")
    if any(
        after.get(version) != status
        for version, status in before.items()
        if status == "deleted"
    ):
        raise RuntimeError("Deleted records must not be reactivated or modified")
    report["status"] = "deprecated"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report: dict[str, Any] = {
        "target": SERVER,
        "apply": args.apply,
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }
    try:
        retire(report, args.apply)
        exit_code = 0
    except (RuntimeError, ValueError, KeyError) as exc:
        report.update(status="failed", error=str(exc))
        exit_code = 1
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
