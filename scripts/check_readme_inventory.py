#!/usr/bin/env python3
"""Validate the published MCP inventory and canonical documentation links."""

from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

from mcp_catalog import documentation_target, load_catalog

ROOT = Path(__file__).resolve().parents[1]

PLATFORM_ROOT = "https://platform.acedata.cloud"
LEGACY_DOCS_ROOT = "https://docs.acedata.cloud"


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    catalog = load_catalog()
    package_dirs = {path.parent.name for path in ROOT.glob("*/pyproject.toml")}
    catalog_dirs = set(catalog)
    if missing := sorted(package_dirs - catalog_dirs):
        fail(errors, f"catalog missing package directories: {', '.join(missing)}")
    if extra := sorted(catalog_dirs - package_dirs):
        fail(
            errors,
            f"catalog lists directories without pyproject.toml: {', '.join(extra)}",
        )

    targets: dict[str, tuple[str | None, str | None]] = {}
    for alias, entry in catalog.items():
        try:
            targets[alias] = documentation_target(entry)
        except ValueError as exc:
            fail(errors, f"{alias}: {exc}")

    mappings = set(
        re.findall(
            r"^  ([a-z0-9_-]+):\s*$", (ROOT / "sync.yaml").read_text(), re.MULTILINE
        )
    )
    root_readme = (ROOT / "README.md").read_text()
    active_listed = set(
        re.findall(
            r"^\| `([^/`]+)/`.*\| \[(?:Documentation|Service details)\]\(",
            root_readme,
            re.MULTILINE,
        )
    )
    expected_active = {
        alias
        for alias in mappings
        if alias in catalog and catalog[alias]["status"] == "active"
    }
    if missing := sorted(expected_active - active_listed):
        fail(errors, f"README missing active mapped servers: {', '.join(missing)}")
    if extra := sorted(active_listed - expected_active):
        fail(errors, f"README lists unexpected active servers: {', '.join(extra)}")
    if not re.search(r"^\| `sora/` .*\| Retired;", root_readme, re.MULTILINE):
        fail(errors, "README must list sora only in the retired table")
    for alias in expected_active:
        url, label = targets[alias]
        if f"| [{label}]({url}) |" not in root_readme:
            fail(errors, f"README uses the wrong documentation target for {alias}")

    for alias in sorted(package_dirs):
        entry = catalog[alias]
        url, label = targets.get(alias, (None, None))
        pyproject_path = ROOT / alias / "pyproject.toml"
        project = tomllib.loads(pyproject_path.read_text())["project"]
        actual_url = (project.get("urls") or {}).get("Documentation")
        if actual_url != url:
            fail(
                errors,
                f"{alias}/pyproject.toml: Documentation must be {url!r}, found {actual_url!r}",
            )

        readme_path = ROOT / alias / "README.md"
        readme = readme_path.read_text()
        if url:
            expected = f"<!-- canonical-documentation -->\n[{label}]({url})"
            if expected not in readme:
                fail(errors, f"{alias}/README.md: missing canonical {label} link")
        elif "<!-- canonical-documentation -->" in readme:
            fail(
                errors, f"{alias}/README.md: retired MCP must not expose documentation"
            )

        for relative in (Path("vscode/README.md"), Path("jetbrains/README.md")):
            path = ROOT / alias / relative
            if not path.exists():
                continue
            text = path.read_text()
            if url and url not in text:
                fail(
                    errors,
                    f"{alias}/{relative}: missing canonical documentation target",
                )
            if not url and re.search(
                r"(?:MCP|API) documentation|Service details", text, re.IGNORECASE
            ):
                fail(
                    errors,
                    f"{alias}/{relative}: retired MCP still exposes documentation",
                )

        jetbrains = ROOT / alias / "jetbrains" / "src" / "main" / "kotlin"
        for path in (
            jetbrains.glob("**/*SettingsConfigurable.kt") if jetbrains.exists() else []
        ):
            text = path.read_text()
            if url and f'browserLink("{label}", "{url}")' not in text:
                fail(
                    errors, f"{path.relative_to(ROOT)}: missing canonical browser link"
                )
            if not url and "API Documentation" in text:
                fail(
                    errors,
                    f"{path.relative_to(ROOT)}: retired MCP still exposes documentation",
                )

    public_patterns = (
        "*/README.md",
        "*/pyproject.toml",
        "*/vscode/README.md",
        "*/jetbrains/README.md",
    )
    for pattern in public_patterns:
        for path in ROOT.glob(pattern):
            text = path.read_text()
            if LEGACY_DOCS_ROOT in text:
                fail(
                    errors,
                    f"{path.relative_to(ROOT)}: contains legacy docs.acedata.cloud URL",
                )
            if f"{PLATFORM_ROOT}/service/" in text:
                fail(
                    errors,
                    f"{path.relative_to(ROOT)}: contains invalid singular /service/ URL",
                )
            if re.search(
                rf"{re.escape(PLATFORM_ROOT)}/documents/[0-9a-f-]{{36}}", text
            ):
                fail(
                    errors,
                    f"{path.relative_to(ROOT)}: contains a non-canonical document UUID",
                )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print(
        f"README inventory and documentation links match {len(catalog)} catalog entries"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
