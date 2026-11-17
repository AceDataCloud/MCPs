#!/usr/bin/env python3
"""Explicit first-install OAuth key provisioning; never run by ordinary deploys."""

import argparse
import json
import secrets
import subprocess
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def bootstrap(alias: str, context: str, root: Path = ROOT) -> None:
    catalog = json.loads((root / "scripts/mcp_catalog.json").read_text())["services"]
    if catalog.get(alias, {}).get("status") != "active":
        raise ValueError("Only active hosted packages can be initialized")
    package = (root / alias).resolve()
    if package.parent != root.resolve():
        raise ValueError("Invalid package directory")
    deployment = yaml.safe_load(
        (package / "deploy/production/deployment.yaml").read_text()
    )
    name = deployment["metadata"]["name"]
    namespace = deployment["metadata"].get("namespace", "acedatacloud")
    if not name.startswith("mcp-"):
        raise ValueError("Invalid hosted MCP deployment")
    shared = (package / "deploy/production/oauth-redis.yaml").exists()
    secret = "mcp-acedatacloud-oauth-redis" if shared else f"{name}-oauth-state"
    command = ["kubectl", "--context", context, "-n", namespace]

    def get(kind: str, resource: str) -> dict:
        result = subprocess.run(
            [*command, "get", kind, resource, "--ignore-not-found", "-o", "json"],
            check=False,
            capture_output=True,
            text=True,
        )
        if result.returncode:
            raise RuntimeError(
                f"Cannot inspect {kind}/{resource}; no key was generated"
            )
        return json.loads(result.stdout) if result.stdout.strip() else {}

    existing = get("secret", secret)
    required = ("password", "state_key") if shared else ("state_key",)
    if existing:
        if not all(existing.get("data", {}).get(key) for key in required):
            raise RuntimeError(f"Restore {secret}: required key data is missing")
        print(f"Preserved existing Secret {secret}")
        return
    # An existing deployment (with or without the old marker) has already used a key.
    # The Redis PVC is an additional durable guard for the shared store.
    if get("deployment", name) or (
        shared and get("pvc", "data-mcp-acedatacloud-oauth-redis-0")
    ):
        raise RuntimeError(f"OAuth key is missing; restore {secret} before deployment")
    result = subprocess.run(
        [
            *command,
            "create",
            "secret",
            "generic",
            secret,
            *(f"--from-literal={key}={secrets.token_hex(32)}" for key in required),
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        # Do not include subprocess arguments or Secret material in errors.
        raise RuntimeError(
            f"Could not create {secret}; inspect and restore before retrying"
        )
    print(f"Created first-install Secret {secret}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", help="Hosted package directory, such as suno")
    parser.add_argument("--context", required=True)
    args = parser.parse_args()
    try:
        bootstrap(args.package, args.context)
    except (ValueError, RuntimeError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
