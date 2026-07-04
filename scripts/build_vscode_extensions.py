#!/usr/bin/env python3
"""
Regenerate `<service>/vscode/{package.json, extension.js, README.md, .vscodeignore}`
for every MCP listed in `scripts/vscode_extensions.yaml`.

The extension registers an HTTP MCP server via the proper VS Code API
(`contributes.mcpServerDefinitionProviders` + `vscode.lm.registerMcp\
ServerDefinitionProvider`). On first use it prompts for an Ace Data Cloud
API key via `vscode.window.showInputBox` and persists it through
`SecretStorage`. Two commands (`<svc>: Set/Clear API Key`) let users
rotate or remove the key from the command palette.

Usage:
  python3 scripts/build_vscode_extensions.py                 # all services
  python3 scripts/build_vscode_extensions.py --only suno     # one service
  python3 scripts/build_vscode_extensions.py --dry-run       # diff only
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "scripts" / "vscode_extensions.yaml"


@dataclass(frozen=True)
class Service:
    alias: str
    display_name: str
    repo: str
    tagline: str
    description: str
    keywords: list[str]
    examples: list[str]
    models: list[str]
    pricing_note: str
    domain: str
    pypi_pkg: str
    ext_name: str
    publisher: str
    signup_url: str
    docs_url: str
    vscode_engine: str
    common_categories: list[str]
    common_keywords: list[str]
    hosted_url_override: str | None
    token_env: str

    @property
    def hosted_url(self) -> str:
        return self.hosted_url_override or f"https://{self.alias}.mcp.acedata.cloud/mcp"

    @property
    def provider_id(self) -> str:
        # ID exposed to VS Code's MCP machinery. Keep it stable per service so
        # bookmarks / Configure-Tools state survive reinstalls.
        return f"acedatacloud.{self.alias}"

    @property
    def set_token_cmd(self) -> str:
        return f"acedatacloud.{self.alias}.setApiToken"

    @property
    def clear_token_cmd(self) -> str:
        return f"acedatacloud.{self.alias}.clearApiToken"

    @property
    def repo_url(self) -> str:
        return f"https://github.com/AceDataCloud/{self.repo}"

    @property
    def pypi_url(self) -> str:
        return f"https://pypi.org/project/{self.pypi_pkg}/"

    @property
    def categories(self) -> list[str]:
        return list(self.common_categories)

    @property
    def all_keywords(self) -> list[str]:
        seen: set[str] = set()
        out: list[str] = []
        for k in [*self.common_keywords, *self.keywords]:
            if k not in seen:
                seen.add(k)
                out.append(k)
        return out


def load_services() -> list[Service]:
    with CONFIG.open() as fh:
        raw = yaml.safe_load(fh)
    defaults = raw["defaults"]
    services: list[Service] = []
    for alias, cfg in raw["services"].items():
        repo = cfg["repo"]
        pypi_override = cfg.get("pypi_override")
        if pypi_override:
            pypi_pkg = pypi_override
        else:
            pyproject = ROOT / alias / "pyproject.toml"
            with pyproject.open("rb") as fh:
                pkg_data = tomllib.load(fh)
            pypi_pkg = pkg_data["project"]["name"]
        # VS Code extension id namespace is independent of PyPI. Default to
        # `mcp-<alias>` to match the marketplace IDs we already own; allow an
        # explicit override for future services whose alias diverges.
        ext_name = cfg.get("ext_name") or f"mcp-{alias}"
        services.append(
            Service(
                alias=alias,
                display_name=cfg["display_name"],
                repo=repo,
                tagline=cfg["tagline"].strip(),
                description=" ".join(cfg["description"].split()),
                keywords=list(cfg.get("keywords", [])),
                examples=list(cfg.get("examples", [])),
                models=list(cfg.get("models", [])),
                pricing_note=cfg.get("pricing_note", "").strip(),
                domain=cfg.get("domain", "general"),
                pypi_pkg=pypi_pkg,
                ext_name=ext_name,
                publisher=defaults["publisher"],
                signup_url=defaults["signup_url"],
                docs_url=defaults["docs_url"],
                vscode_engine=defaults["vscode_engine"],
                common_categories=list(defaults["common_categories"]),
                common_keywords=list(defaults["common_keywords"]),
                hosted_url_override=cfg.get("hosted_url"),
                token_env=cfg.get("token_env") or "ACEDATACLOUD_API_TOKEN",
            )
        )
    return services


TOOL_TABLE_RE = re.compile(
    r"^## Tool Reference\s*\n+\| Tool \| Description \|\s*\n\|[^\n]+\|\s*\n((?:\|[^\n]+\|\s*\n)+)",
    re.MULTILINE,
)


def extract_tools(main_readme: Path) -> list[tuple[str, str]]:
    """Parse the first `## Tool Reference` table out of the main README."""
    text = main_readme.read_text(encoding="utf-8")
    m = TOOL_TABLE_RE.search(text)
    if not m:
        return []
    rows: list[tuple[str, str]] = []
    for line in m.group(1).strip().splitlines():
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 2:
            continue
        tool, desc = parts[0], parts[1]
        tool = tool.strip("`")
        rows.append((tool, desc))
    return rows


def render_package_json(svc: Service) -> str:
    pkg: dict[str, object] = {
        "name": svc.ext_name,
        "displayName": svc.display_name,
        "description": svc.tagline,
        "version": "0.3.0",
        "publisher": svc.publisher,
        "icon": "icon.png",
        "license": "MIT",
        "engines": {"vscode": svc.vscode_engine},
        "categories": svc.categories,
        "keywords": svc.all_keywords,
        "galleryBanner": {"color": "#0E1117", "theme": "dark"},
        "homepage": svc.repo_url,
        "repository": {"type": "git", "url": svc.repo_url},
        "bugs": {"url": f"{svc.repo_url}/issues"},
        "activationEvents": [],
        "main": "./extension.js",
        "contributes": {
            "mcpServerDefinitionProviders": [
                {
                    "id": svc.provider_id,
                    "label": svc.display_name,
                },
            ],
            "commands": [
                {
                    "command": svc.set_token_cmd,
                    "title": f"{svc.display_name}: Set Ace Data Cloud API Key",
                    "category": "MCP",
                },
                {
                    "command": svc.clear_token_cmd,
                    "title": f"{svc.display_name}: Clear Ace Data Cloud API Key",
                    "category": "MCP",
                },
            ],
        },
    }
    # Pretty + trailing newline.
    return json.dumps(pkg, indent=2, ensure_ascii=False) + "\n"


def render_extension_js(svc: Service) -> str:
    return f"""// Auto-generated by scripts/build_vscode_extensions.py — DO NOT EDIT BY HAND.
//
// Registers the hosted Ace Data Cloud "{svc.alias}" MCP server with VS Code
// via the stable `vscode.lm.registerMcpServerDefinitionProvider` API. The
// Bearer API key is read from (in order):
//   1. process.env.{svc.token_env}
//   2. VS Code SecretStorage (key "{svc.alias}.apiToken")
//   3. An interactive showInputBox prompt on first use
//
// Two commands are exposed for managing the API key from the command palette:
//   - {svc.set_token_cmd}
//   - {svc.clear_token_cmd}

const vscode = require("vscode");

const PROVIDER_ID = "{svc.provider_id}";
const SERVER_LABEL = "{svc.display_name}";
const SERVER_URL = "{svc.hosted_url}";
const SET_TOKEN_CMD = "{svc.set_token_cmd}";
const CLEAR_TOKEN_CMD = "{svc.clear_token_cmd}";
// Per-extension SecretStorage namespace; we keep one key per service so
// rotating one API key doesn't affect siblings.
const SECRET_KEY = "{svc.alias}.apiToken";
const SIGNUP_URL = "{svc.signup_url}";

async function readToken(context) {{
  const env = process.env.{svc.token_env};
  if (env && env.trim()) return env.trim();
  const stored = await context.secrets.get(SECRET_KEY);
  return stored ? stored.trim() : undefined;
}}

async function promptForToken(context) {{
  const token = await vscode.window.showInputBox({{
    title: `${{SERVER_LABEL}} — Ace Data Cloud API key`,
        prompt: `Paste an API key from ${{SIGNUP_URL}}/console/applications (Applications -> API Key). Stored in the OS keychain.`,
        placeHolder: "API key from /console/applications",
    password: true,
    ignoreFocusOut: true,
  }});
  if (!token) return undefined;
  const trimmed = token.trim();
  if (!trimmed) return undefined;
  await context.secrets.store(SECRET_KEY, trimmed);
  return trimmed;
}}

function activate(context) {{
  const onDidChange = new vscode.EventEmitter();

  context.subscriptions.push(
    onDidChange,
    vscode.commands.registerCommand(SET_TOKEN_CMD, async () => {{
      const t = await promptForToken(context);
      if (t) {{
        vscode.window.showInformationMessage(`${{SERVER_LABEL}}: API key saved.`);
        onDidChange.fire();
      }}
    }}),
    vscode.commands.registerCommand(CLEAR_TOKEN_CMD, async () => {{
      await context.secrets.delete(SECRET_KEY);
    vscode.window.showInformationMessage(`${{SERVER_LABEL}}: API key cleared.`);
      onDidChange.fire();
    }}),
    context.secrets.onDidChange((e) => {{
      if (e.key === SECRET_KEY) onDidChange.fire();
    }}),
    vscode.lm.registerMcpServerDefinitionProvider(PROVIDER_ID, {{
      onDidChangeMcpServerDefinitions: onDidChange.event,
      provideMcpServerDefinitions: () => [
        new vscode.McpHttpServerDefinition(SERVER_LABEL, vscode.Uri.parse(SERVER_URL)),
      ],
      resolveMcpServerDefinition: async (server) => {{
        let token = await readToken(context);
        if (!token) token = await promptForToken(context);
        if (!token) {{
          throw new Error(
                        `${{SERVER_LABEL}} needs an Ace Data Cloud API key. ` +
                            `Run "${{SERVER_LABEL}}: Set Ace Data Cloud API Key" from the command palette.`
          );
        }}
        return new vscode.McpHttpServerDefinition(server.label, server.uri, {{
          Authorization: `Bearer ${{token}}`,
        }});
      }},
    }})
  );
}}

function deactivate() {{}}

module.exports = {{ activate, deactivate }};
"""


def render_readme(svc: Service, tools: list[tuple[str, str]]) -> str:
    badge_line = (
        f"[![VS Code Marketplace]"
        f"(https://img.shields.io/visual-studio-marketplace/v/{svc.publisher}.{svc.pypi_pkg}?label=VS%20Code)]"
        f"(https://marketplace.visualstudio.com/items?itemName={svc.publisher}.{svc.pypi_pkg}) "
        f"[![PyPI]"
        f"(https://img.shields.io/pypi/v/{svc.pypi_pkg}.svg?label=PyPI)]"
        f"({svc.pypi_url}) "
        f"[![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)]({svc.hosted_url})"
    )

    examples_md = (
        "\n".join(f'- "{ex}"' for ex in svc.examples) or "_(see Tool Reference below)_"
    )

    if tools:
        tool_table = ["| Tool | Description |", "| --- | --- |"]
        for name, desc in tools:
            tool_table.append(f"| `{name}` | {desc} |")
        tool_table_md = "\n".join(tool_table)
        tool_count_line = f"**{len(tools)} tools** available via this server."
    else:
        tool_table_md = "_Tool list is dynamically loaded from the server. Run a query to discover available tools._"
        tool_count_line = ""

    models_section = ""
    if svc.models:
        models_section = (
            "## Supported Models\n\n" + ", ".join(f"`{m}`" for m in svc.models) + "\n\n"
        )

    pricing = svc.pricing_note or "See Ace Data Cloud pricing for details."

    return f"""# {svc.display_name}

{svc.tagline}

{badge_line}

{svc.description}

This extension registers the **{svc.alias}** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `{svc.alias}` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud]({svc.signup_url}/console/applications) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a {svc.domain} task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **{svc.display_name}: Set Ace Data Cloud API Key**
- **{svc.display_name}: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `{svc.hosted_url}` — no Python, no `uvx`, no local install needed.

### Example prompts

{examples_md}

---

## Tool Reference

{tool_count_line}

{tool_table_md}

{models_section}## Pricing

{pricing} See full pricing at [{svc.docs_url}]({svc.docs_url}).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : {svc.provider_id}
Server label: {svc.display_name}
Server URL  : {svc.hosted_url}
Transport   : Streamable HTTP
Auth        : Bearer API key from VS Code SecretStorage (or ${svc.token_env})
```

You don't need to edit `mcp.json` — the extension handles registration and
token handling automatically. If you'd rather configure things by hand, the
sections below show equivalent `mcp.json` snippets you can use **instead of**
this extension.

### Alternative: manual `mcp.json` (hosted)

```jsonc
{{
  "servers": {{
    "{svc.alias}": {{
      "type": "http",
      "url": "{svc.hosted_url}",
      "headers": {{ "Authorization": "Bearer ${{input:acedatacloud_api_token}}" }}
    }}
  }},
  "inputs": [
    {{
      "type": "promptString",
      "id": "acedatacloud_api_token",
            "description": "Ace Data Cloud API key",
      "password": true
    }}
  ]
}}
```

### Alternative: local stdio (no network roundtrip)

For offline dev, air-gapped environments, or pinning to a specific PyPI
version, install [`uv`](https://docs.astral.sh/uv/) and use:

```jsonc
{{
  "servers": {{
    "{svc.alias}": {{
      "type": "stdio",
      "command": "uvx",
      "args": ["{svc.pypi_pkg}"],
      "env": {{ "{svc.token_env}": "${{input:acedatacloud_api_token}}" }}
    }}
  }}
}}
```

`uvx` will download and run the latest [`{svc.pypi_pkg}`]({svc.pypi_url}) on demand.

---

## Links

- **Hosted endpoint:** {svc.hosted_url}
- **PyPI package:** [`{svc.pypi_pkg}`]({svc.pypi_url})
- **Source repository:** {svc.repo_url}
- **Ace Data Cloud platform:** {svc.signup_url}
- **MCP documentation:** {svc.docs_url}

## License

MIT — see [LICENSE](LICENSE).
"""


VSCODEIGNORE = """.vscode/**
.vscode-test/**
node_modules/**
*.vsix
.git/**
.gitignore
.eslintrc.json
.prettierrc
**/*.map
**/tsconfig.json
**/.editorconfig
"""


def write_if_changed(path: Path, content: str, *, dry_run: bool) -> bool:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    if existing == content:
        return False
    if not dry_run:
        path.write_text(content, encoding="utf-8")
    return True


def process(svc: Service, *, dry_run: bool) -> list[str]:
    changes: list[str] = []
    vscode_dir = ROOT / svc.alias / "vscode"
    vscode_dir.mkdir(parents=True, exist_ok=True)

    tools = extract_tools(ROOT / svc.alias / "README.md")
    pkg_text = render_package_json(svc)
    ext_text = render_extension_js(svc)
    readme_text = render_readme(svc, tools)

    if write_if_changed(vscode_dir / "package.json", pkg_text, dry_run=dry_run):
        changes.append(f"  {svc.alias}/vscode/package.json")
    if write_if_changed(vscode_dir / "extension.js", ext_text, dry_run=dry_run):
        changes.append(f"  {svc.alias}/vscode/extension.js")
    if write_if_changed(vscode_dir / "README.md", readme_text, dry_run=dry_run):
        changes.append(f"  {svc.alias}/vscode/README.md")
    if write_if_changed(vscode_dir / ".vscodeignore", VSCODEIGNORE, dry_run=dry_run):
        changes.append(f"  {svc.alias}/vscode/.vscodeignore")
    return changes


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="Comma-separated service aliases to regenerate.")
    parser.add_argument(
        "--dry-run", action="store_true", help="Don't write; just list changes."
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    selected: set[str] | None = None
    if args.only:
        selected = {s.strip() for s in args.only.split(",") if s.strip()}

    services = load_services()
    total_changes = 0
    for svc in services:
        if selected and svc.alias not in selected:
            continue
        changes = process(svc, dry_run=args.dry_run)
        if changes:
            total_changes += len(changes)
            print(
                f"[{svc.alias}] {len(changes)} file(s) {'would change' if args.dry_run else 'updated'}:"
            )
            for c in changes:
                print(c)
        else:
            print(f"[{svc.alias}] up-to-date")

    print()
    verb = "would change" if args.dry_run else "changed"
    print(
        f"{total_changes} file(s) {verb} across {len(services) if selected is None else len(selected)} service(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
