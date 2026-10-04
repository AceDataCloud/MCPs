"""Generate the combined VS Code extension's service list from MCP metadata."""

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]


def bundle_services(root=ROOT):
    catalog = json.loads((root / "scripts/mcp_catalog.json").read_text())["services"]
    servers = []
    defaults = []
    for alias, entry in sorted(catalog.items()):
        config = entry.get("vscode_bundle")
        if entry["status"] != "active" or config is None:
            continue
        label = config.get("label")
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"{alias}: bundle label is required")
        server = json.loads((root / alias / "server.json").read_text())
        remotes = [
            item
            for item in server.get("remotes", [])
            if item["type"] == "streamable-http"
        ]
        if len(remotes) != 1:
            raise ValueError(f"{alias}: exactly one hosted HTTP endpoint is required")
        url = remotes[0]["url"]
        parts = urlsplit(url)
        host = (
            "mcp.acedata.cloud"
            if alias == "acedatacloud"
            else f"{alias}.mcp.acedata.cloud"
        )
        if (
            parts.scheme != "https"
            or parts.netloc != host
            or parts.path != "/mcp"
            or parts.query
            or parts.fragment
        ):
            raise ValueError(f"{alias}: unexpected hosted endpoint {url}")
        credentials = {
            variable["name"]
            for package in server.get("packages", [])
            for variable in package.get("environmentVariables", [])
            if variable["name"]
            in {"ACEDATACLOUD_API_TOKEN", "ACEDATACLOUD_PLATFORM_TOKEN"}
        }
        if credentials == {"ACEDATACLOUD_API_TOKEN"} and alias != "acedatacloud":
            credential = "api"
        elif credentials == {"ACEDATACLOUD_PLATFORM_TOKEN"} and alias == "acedatacloud":
            credential = "platform"
        else:
            raise ValueError(f"{alias}: ambiguous or incorrect credential contract")
        servers.append(
            {"id": alias, "label": label, "url": url, "credential": credential}
        )
        if config.get("default", False):
            defaults.append(alias)
    if not servers:
        raise ValueError("The bundle must contain at least one verified service")
    return servers, defaults


def outputs(root=ROOT):
    bundle = root / "vscode-bundle"
    servers, defaults = bundle_services(root)
    yield bundle / "servers.json", json.dumps(servers, indent=2) + "\n"
    package = json.loads((bundle / "package.json").read_text())
    package["description"] = (
        "One MCP toolbox for AI chat, images, video, music, search and account management. "
        f"Choose from {len(servers)} hosted Ace Data Cloud services."
    )
    setting = package["contributes"]["configuration"]["properties"][
        "acedatacloud.bundle.services"
    ]
    setting["items"]["enum"] = [service["id"] for service in servers]
    setting["items"]["enumDescriptions"] = [service["label"] for service in servers]
    setting["default"] = defaults
    yield bundle / "package.json", json.dumps(package, indent=2) + "\n"
    readme = (bundle / "README.md").read_text()
    readme = re.sub(
        r"\*\*\d+ hosted MCP services\*\*",
        f"**{len(servers)} hosted MCP services**",
        readme,
    )
    table = "| Service | Credential |\n| --- | --- |\n"
    for service in servers:
        credential = (
            "Platform token" if service["credential"] == "platform" else "API key"
        )
        table += f"| {service['label']} | {credential} |\n"
    pattern = r"<!-- BEGIN GENERATED SERVICES -->\n.*?<!-- END GENERATED SERVICES -->"
    readme, replaced = re.subn(
        pattern,
        "<!-- BEGIN GENERATED SERVICES -->\n"
        + table
        + "<!-- END GENERATED SERVICES -->",
        readme,
        flags=re.DOTALL,
    )
    if replaced != 1:
        raise ValueError("README must have exactly one generated service table")
    yield bundle / "README.md", readme


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path, expected in outputs():
        if path.exists() and path.read_text() == expected:
            continue
        stale.append(str(path.relative_to(ROOT)))
        if not args.check:
            path.write_text(expected)
    if args.check and stale:
        raise SystemExit("Stale VS Code bundle files: " + ", ".join(stale))
    print(f"VS Code bundle: {len(stale)} {'stale' if args.check else 'updated'} files")


if __name__ == "__main__":
    main()
