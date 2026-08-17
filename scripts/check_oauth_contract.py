#!/usr/bin/env python3
"""Guard the shared Hosted MCP OAuth Credential contract."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLATFORM_TOKEN_EXEMPTION = "acedatacloud"


def main() -> None:
    failures: list[str] = []
    applicable: list[str] = []

    for path in sorted(ROOT.glob("*/core/oauth.py")):
        name = path.parts[-3]
        source = path.read_text()
        tree = ast.parse(source, filename=str(path))
        functions = {
            node.name
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        }

        if name == PLATFORM_TOKEN_EXEMPTION:
            if "_get_platform_token" not in source or '"name": "OAuth MCP"' in source:
                failures.append(
                    f"{name}: PlatformToken exemption drifted into API Credential mode"
                )
            continue
        if "_get_user_credential" not in source:
            continue

        applicable.append(name)
        checks = {
            "shared OAuth MCP name sent": '"name": "OAuth MCP"' in source,
            "Global Usage application lookup": '"scope": "Global"' in source
            and '"type": "Usage"' in source,
            "query-first pattern": 'params={"application_id": application_id, "name": "OAuth MCP"}'
            in source
            or 'params={\'application_id\': application_id, \'name\': \'OAuth MCP\'}'
            in source,
            "arbitrary selector removed": "_is_reusable_credential" not in source,
            "per-server managed key removed": "managed_key" not in source
            and "_managed_credential_key" not in functions,
            "nested credential fallback removed": "app_creds" not in source
            and "app_credentials" not in source,
        }
        for label, passed in checks.items():
            if not passed:
                failures.append(f"{name}: {label}")

    if not applicable:
        failures.append("no API Credential OAuth implementations discovered")
    if failures:
        raise SystemExit("OAuth contract violations:\n- " + "\n- ".join(failures))
    print(
        f"OAuth contract OK: {len(applicable)} shared-Credential MCPs; 1 PlatformToken exemption"
    )


if __name__ == "__main__":
    main()
