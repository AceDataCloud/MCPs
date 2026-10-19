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
from urllib.parse import urlencode, urlsplit, urlunsplit

import yaml
from marketing_readmes import contract as attribution_contract
from marketing_readmes import render as render_marketing_readme
from mcp_catalog import documentation_target, load_catalog
from token_onboarding import token_guide

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
    docs_url: str | None
    docs_label: str | None
    status: str
    vscode_engine: str
    common_categories: list[str]
    common_keywords: list[str]
    hosted_url_override: str | None
    token_env: str

    @property
    def hosted_url(self) -> str:
        return self.hosted_url_override or f"https://{self.alias}.mcp.acedata.cloud/mcp"

    @property
    def credential_label(self) -> str:
        return (
            "Platform Token"
            if self.token_env == "ACEDATACLOUD_PLATFORM_TOKEN"
            else "API Key"
        )

    @property
    def credential_url(self) -> str:
        rules = attribution_contract()
        account = self.token_env == "ACEDATACLOUD_PLATFORM_TOKEN"
        parts = urlsplit(self.signup_url)
        path = "/console/platform-tokens" if account else "/console/applications"
        placement = "platform_token" if account else "api_key"
        content = rules["link_defaults"]["content_template"].format(
            entry=self.alias.replace("-", "_") + "_mcp",
            surface="extension",
            placement=placement,
        )
        tags = {
            "utm_source": "vscode",
            "utm_medium": rules["sources"]["vscode"],
            "utm_campaign": rules["link_defaults"]["campaign"],
            "utm_content": content,
        }
        if any(
            len(value) > rules["max_tag_length"]
            or not re.fullmatch(rules["tag_pattern"], value)
            for value in tags.values()
        ):
            raise ValueError("Invalid VS Code credential attribution")
        return urlunsplit((parts.scheme, parts.netloc, path, urlencode(tags), ""))

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
    catalog = load_catalog()
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
        docs_url, docs_label = documentation_target(catalog[alias])
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
                docs_url=docs_url,
                docs_label=docs_label,
                status=catalog[alias]["status"],
                vscode_engine=defaults["vscode_engine"],
                common_categories=list(defaults["common_categories"]),
                common_keywords=list(defaults["common_keywords"]),
                hosted_url_override=cfg.get("hosted_url"),
                token_env=cfg.get("token_env") or "ACEDATACLOUD_API_TOKEN",
            )
        )
    return services


TOOL_TABLE_RE = re.compile(
    r"^## (?:Tool Reference|Available Tools|Tools)\s*\n+\| Tool \| (?:Description|Purpose) \|\s*\n\|[^\n]+\|\s*\n((?:\|[^\n]+\|\s*\n)+)",
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
                    "title": f"{svc.display_name}: Set Ace Data Cloud {svc.credential_label}",
                    "category": "MCP",
                },
                {
                    "command": svc.clear_token_cmd,
                    "title": f"{svc.display_name}: Clear Ace Data Cloud {svc.credential_label}",
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
const CREDENTIAL_URL = "{svc.credential_url}";

async function readToken(context) {{
  const env = process.env.{svc.token_env};
  if (env && env.trim()) return env.trim();
  const stored = await context.secrets.get(SECRET_KEY);
  return stored ? stored.trim() : undefined;
}}

async function promptForToken(context) {{
  const token = await vscode.window.showInputBox({{
    title: `${{SERVER_LABEL}} — Ace Data Cloud {svc.credential_label.lower()}`,
        prompt: `Paste an Ace Data Cloud {svc.credential_label.lower()} from ${{CREDENTIAL_URL}}. Stored in VS Code SecretStorage.`,
        placeHolder: "{svc.credential_label} from {urlsplit(svc.credential_url).path}",
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
        vscode.window.showInformationMessage(`${{SERVER_LABEL}}: {svc.credential_label.lower()} saved.`);
        onDidChange.fire();
      }}
    }}),
    vscode.commands.registerCommand(CLEAR_TOKEN_CMD, async () => {{
      await context.secrets.delete(SECRET_KEY);
    vscode.window.showInformationMessage(`${{SERVER_LABEL}}: {svc.credential_label.lower()} cleared.`);
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
        if (!server?.uri || server.uri.toString() !== SERVER_URL) {{
          throw new Error("Unexpected MCP server endpoint.");
        }}
        let token = await readToken(context);
        if (!token) token = await promptForToken(context);
        if (!token) {{
          throw new Error(
                        `${{SERVER_LABEL}} needs an Ace Data Cloud {svc.credential_label.lower()}. ` +
                            `Run "${{SERVER_LABEL}}: Set Ace Data Cloud {svc.credential_label}" from the command palette.`
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
        f"(https://img.shields.io/visual-studio-marketplace/v/{svc.publisher}.{svc.ext_name}?label=VS%20Code)]"
        f"(https://marketplace.visualstudio.com/items?itemName={svc.publisher}.{svc.ext_name}) "
        f"[![PyPI]"
        f"(https://img.shields.io/pypi/v/{svc.pypi_pkg}.svg?label=PyPI)]"
        f"({svc.pypi_url}) "
        f"[![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)]({svc.hosted_url})"
    )

    examples_md = (
        "\n".join(f'- "{ex}"' for ex in svc.examples) or "_(see Tool Reference below)_"
    )

    if svc.alias == "openai":
        # The hosted server also has chat/audio tools; this card documents only
        # the image/task subset and must not claim it filters the remote schema.
        tools = [
            (
                "openai_list_image_models",
                "Read image-model reference information without generating an image.",
            ),
            (
                "openai_generate_image",
                "Submit one image-generation task after reviewing model, quality, count and price.",
            ),
            (
                "openai_edit_image",
                "Submit an image-editing task after reviewing the request and price.",
            ),
            (
                "openai_get_task",
                "Read the status and result of the same original task ID.",
            ),
            (
                "openai_get_tasks_batch",
                "Read several existing task IDs without generating new images.",
            ),
        ]

    if tools:
        tool_table = ["| Tool | Description |", "| --- | --- |"]
        for name, desc in tools:
            tool_table.append(f"| `{name}` | {desc} |")
        tool_table_md = "\n".join(tool_table)
        tool_count_line = (
            "**Image/task tools to enable for this card.** The existing hosted server "
            "also advertises chat/audio tools; this extension does not filter its schema."
            if svc.alias == "openai"
            else f"**{len(tools)} tools** available via this server."
        )
    else:
        tool_table_md = "_Tool list is dynamically loaded from the server. Run a query to discover available tools._"
        tool_count_line = ""

    models_section = ""
    if svc.models:
        models_section = (
            "## Supported Models\n\n" + ", ".join(f"`{m}`" for m in svc.models) + "\n\n"
        )

    pricing = svc.pricing_note or "See Ace Data Cloud pricing for details."
    documentation_line = (
        f" See [{svc.docs_label}]({svc.docs_url})." if svc.docs_url else ""
    )
    pricing = pricing.rstrip(".") + "." if not svc.docs_url else pricing
    documentation_link = (
        f"- **{svc.docs_label}:** {svc.docs_url}\n" if svc.docs_url else ""
    )
    lifecycle_notice = (
        "\n> **Retired:** This MCP integration is no longer actively offered.\n"
        if svc.status == "retired"
        else ""
    )

    credential_step = (
        "**Get an account token** from [Account Tokens](https://platform.acedata.cloud/console/platform-tokens). This server requires a `platform-...` token."
        if svc.token_env == "ACEDATACLOUD_PLATFORM_TOKEN"
        else "**Get an application API key** using the detailed steps below. Check service access and your current balance before the first request."
    )
    guide = token_guide(svc.alias)
    credential_label = (
        "account token" if svc.token_env == "ACEDATACLOUD_PLATFORM_TOKEN" else "API key"
    )
    brand_note = ""
    if svc.alias in {"suno", "seedance", "happyhorse", "openai", "nanobanana"}:
        brand_note = (
            f"[简体中文]({svc.repo_url}/blob/main/vscode/README.zh-CN.md)\n\n"
            "This integration is published and operated by **Ace Data Cloud**. "
            "It is not an official extension from the model or service owner. "
            "An Ace Data Cloud application API key is required; a key from another provider is not interchangeable.\n\n"
            "**First, verify without generating:** use the read-only tool in the "
            "first-use section below. Generation and your Chat model may be billed separately.\n"
        )

    content = f"""# {svc.display_name}

{svc.tagline}
{brand_note}{lifecycle_notice}

{badge_line}

{svc.description}

This extension registers the **{svc.alias}** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `{svc.alias}` MCP server automatically.
2. {credential_step}
3. **Select a model with tool calling in VS Code Chat.** You can use your existing model, or install [Ace Data Cloud Chat Models](https://marketplace.visualstudio.com/items?itemName=acedatacloud.chat-models). For the Ace model, first follow its [setup guide](https://github.com/AceDataCloud/VSCodeModelProvider#4-show-the-model-in-chat), open **Chat: Manage Language Models**, make the model visible, and select it in Chat. BYOK Chat does not require GitHub sign-in or a Copilot plan; organization policies still apply.
4. **Enable this server's tools.** Open **Chat → Agent → Configure Tools** and select only the tools you need under **{svc.display_name}**. If the list is empty, choose **Update Tools**. The extension prompts for the {credential_label} on first use and saves it in VS Code's `SecretStorage`. Disable another copy of the same server from the Ace MCP bundle or manual `mcp.json` to avoid duplicate tools.
5. **Verify one result.** Check the Tool Reference below and current pricing before running a request. If you already have a task ID, enable its task-query tool and query that same ID first. An accepted generation is not a completed result: poll the original task until it reaches a successful terminal state, open the returned media, and match the task ID in [Usage](https://platform.acedata.cloud/console/usage). Do not resubmit generation to poll. Model Chat and background utility calls can add separate charges to the service request.

You can rotate or remove the {credential_label} any time from the command palette:

- **{svc.display_name}: Set Ace Data Cloud {svc.credential_label}**
- **{svc.display_name}: Clear Ace Data Cloud {svc.credential_label}**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `{svc.hosted_url}` — no Python, no `uvx`, no local install needed.

### Get your credential

<!-- BEGIN TOKEN ONBOARDING -->
{guide}<!-- END TOKEN ONBOARDING -->

### Example prompts

{examples_md}

---

## Tool Reference

{tool_count_line}

{tool_table_md}

{models_section}## Pricing

{pricing}{documentation_line}

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : {svc.provider_id}
Server label: {svc.display_name}
Server URL  : {svc.hosted_url}
Transport   : Streamable HTTP
Auth        : Bearer {credential_label} from VS Code SecretStorage (or ${svc.token_env})
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
{documentation_link}
## License

MIT — see [LICENSE](LICENSE).
"""

    if svc.alias in BRAND_TOOLS:
        content += first_use(svc)
    return render_marketing_readme(content, svc.alias, "vscode_marketplace")


BRAND_TOOLS = {
    "suno": ("suno_list_models", "suno_get_task"),
    "seedance": ("seedance_list_models", "seedance_get_task"),
    "happyhorse": ("happyhorse_list_models", "happyhorse_get_task"),
    "openai": ("openai_list_image_models", "openai_get_task"),
    "nanobanana": (None, "nanobanana_get_task"),
}


def first_use(svc: Service) -> str:
    reference, query = BRAND_TOOLS[svc.alias]
    prompt = (
        f"Call {reference} only. Show supported models/actions. Do not generate anything."
        if reference
        else f"Use {query} only for my existing task TASK_ID. Do not generate another image."
    )
    note = (
        "The model-list tool returns reference information without generating media. It does not prove that your key has generation access."
        if reference
        else "Replace TASK_ID with a task already completed by your own application. If you have no task, stop after tool discovery; do not invent a task ID or generate just to test installation."
    )
    text = f"""
## First use: discover, then read an existing result

1. Install [{svc.display_name}](https://marketplace.visualstudio.com/items?itemName={svc.publisher}.{svc.ext_name}). This is an independent service extension; the Ace toolbox is optional. Do not enable two copies of the same server.
2. Complete the application-key steps above. Run **{svc.display_name}: Set Ace Data Cloud API Key** and paste only the token. No workspace configuration file is needed.
3. In **Chat: Manage Language Models**, show and select a tool-capable model. If you use the separate Ace Chat Models extension, follow its [model setup](https://github.com/AceDataCloud/VSCodeModelProvider#4-show-the-model-in-chat). Then open **Chat → Agent → Configure Tools** and enable only `{reference or query}` for this first check.
4. Send the prompt below and inspect the confirmation's tool name and arguments. Your Chat model and background requests may be billed even when the service tool is read-only.

```text
{prompt}
```

{note}

For an existing media task, enable only `{query}`, replace `TASK_ID` with your original task ID, and query that same ID until terminal success or failure. Open the returned media link and match the original generation task to its charge in [Usage](https://platform.acedata.cloud/console/usage). An accepted task or green Chat turn alone is not a completed artifact. Never resubmit generation just to check progress.

### Real VS Code reference screenshots

![Manage Models in the Ace Chat Models extension](https://raw.githubusercontent.com/AceDataCloud/VSCodeModelProvider/667593eb14bf15d434a1c41d47ef1f39199f7d68/assets/tutorial/02-manage-models.png)

![Tool selection in the GPT Image MCP example](https://raw.githubusercontent.com/AceDataCloud/MCPs/537d5767aea410db930e4b01faf5dd14580c8ba7/vscode-bundle/assets/tutorial/04-tools.png)

Historical real VS Code 1.141 screenshots, included in tutorials on 2026-10-09 (Asia/Shanghai). The tool-selection image uses the OpenAI server as a reference: choose this extension's server and the exact tool named above. These images do not show a newly published version or prove this independent service was called.

### Troubleshooting your first call

| Symptom | Check |
| --- | --- |
| Model missing / sign-in prompt | Complete Manage Language Models and the model extension's setup; respect organizational BYOK policy. |
| Tools missing | Update Tools, check workspace/server trust, and disable duplicate bundle or manual registrations. |
| 401 / 403 | Check application/service access, expiry, Allowed APIs, usage limit and balance. Use an application key rather than a platform management token. |
| Pending task | Query the same original ID; do not submit generation again. |
| 429 / 5xx | Preserve task/trace ID, inspect original task and Usage, and do not automatically retry a paid operation. |
"""
    return text


def render_chinese_readme(svc: Service) -> str:
    reference, query = BRAND_TOOLS[svc.alias]
    prompt = (
        f"只调用 {reference}，显示模型/动作说明，不要生成任何媒体。"
        if reference
        else f"只用 {query} 查询我已有的任务 TASK_ID，不要提交新的图片生成。"
    )
    text = f"""# {svc.display_name} · VS Code 中文教程

[English]({svc.repo_url}/blob/main/vscode/README.md) · [官方扩展市场安装](https://marketplace.visualstudio.com/items?itemName={svc.publisher}.{svc.ext_name})

本扩展由 **Ace Data Cloud** 提供和运营，接入对应模型/服务；不是模型或服务品牌方的官方扩展。使用 Ace 的应用 API Token，不能用其他供应方的 Key 替代。安装本服务独立扩展即可注册工具，合集只作可选补充；仍需选择支持工具调用的聊天模型并配置凭据。

## 1. 安装和找到入口

在 VS Code 扩展市场搜索本服务名称，确认发布者为 `acedatacloud`，打开上述安装入口并点击 Install。要求 VS Code 1.101+。安装后不必手写 `mcp.json`。停用合集或手工配置中的同一服务副本，避免工具重复。

## 2. 注册并复制应用 API Token

1. 打开 [Ace Applications](https://platform.acedata.cloud/console/applications)，先注册或登录 Ace。
2. 找到 **General application（通用应用）**；若不存在，先点 **Initialize General Application**。可复制卡片上的 API Key，或进入 **Keys / Manage Keys → Create** 创建本扩展专用 Key。
3. 创建时检查有效期、使用限额、Allowed APIs。只开放需要的生成/查询接口，确认服务权限、[当前价格](https://platform.acedata.cloud/models)及余额。生成和任务查询是两个操作，允许查询不等于允许生成。
4. 复制裸 token，不加引号或 `Bearer `。`platform-...` 是账号管理令牌，不能替代图片、视频或音乐服务的应用 Key。

![通用应用的API Key复制入口，真实界面参考](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![创建独立Key和可选权限限制，真实界面参考](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

上图来自 Ace SunoDify 已有真实平台截图，固定到原始提交；界面标签为英文，仅说明取 Key，不证明本扩展已发布。不要把真实 Key 放到截图、提示词或Git提交。

## 3. 粘贴到VS Code并选工具

运行命令 **{svc.display_name}: Set Ace Data Cloud API Key**，粘贴应用 Token；保存于 VS Code SecretStorage。服务器地址为 `{svc.hosted_url}`。若要求信任服务器，先核对地址。

打开 **Chat: Manage Language Models**，使所选模型可见，再在 Chat 选择它；可安装独立的 [Ace Chat Models](https://marketplace.visualstudio.com/items?itemName=acedatacloud.chat-models)。打开 **Agent → Configure Tools**，只勾选 `{reference or query}`，列表为空时先 Update Tools。组织禁用 BYOK 时遵守管理员政策。

![真实VS Code模型管理界面参考](https://raw.githubusercontent.com/AceDataCloud/VSCodeModelProvider/667593eb14bf15d434a1c41d47ef1f39199f7d68/assets/tutorial/02-manage-models.png)

![真实VS Code工具选择界面参考](https://raw.githubusercontent.com/AceDataCloud/MCPs/537d5767aea410db930e4b01faf5dd14580c8ba7/vscode-bundle/assets/tutorial/04-tools.png)

VS Code 1.141历史真实截图于2026-10-09收入教程；工具图以OpenAI为例，实际选择本服务和上面指定的工具。不是当前新版本截图，也不能当作本独立卡片已经实测。完整模型设置见 [Ace模型教程](https://github.com/AceDataCloud/VSCodeModelProvider#4-show-the-model-in-chat)。

## 4. 首次验证与同ID结果查询

```text
{prompt}
```

模型说明工具不生成媒体，也不证明生成权限；没有已完成任务时，图片服务停在工具发现，不要为验安装新发生成。聊天模型和辅助请求仍可能收费，先查模型价格。已有任务只用 `{query}` 查询同一个原ID（将 `TASK_ID` 替换为自己的原任务ID），直至成功或失败；打开结果媒体，并在 [Usage](https://platform.acedata.cloud/console/usage) 对应原生成任务及Credits账单。accepted、绿色聊天回合都不等于最终媒体成功，不要重新生成来轮询。

## 5. 常见问题

- 看不到模型：先完成 Manage Language Models 和模型扩展设置；不要绕过组织政策。
- 看不到工具：Update Tools、确认工作区和服务器信任，停用重复的合集/手工副本。
- 401/403：查Key完整性、应用/服务访问权限、有效期、限额、Allowed APIs与余额。
- 任务未完成：保留原ID继续查；429或5xx先核原任务和Usage，不自动付费重试。

更多服务说明见 [{svc.docs_label}]({svc.docs_url})。支持排查时提供task/trace ID，不提供Key。
"""
    return render_marketing_readme(text, svc.alias, "vscode_marketplace")


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
    if svc.alias in BRAND_TOOLS and write_if_changed(
        vscode_dir / "README.zh-CN.md", render_chinese_readme(svc), dry_run=dry_run
    ):
        changes.append(f"  {svc.alias}/vscode/README.zh-CN.md")
    if write_if_changed(vscode_dir / ".vscodeignore", VSCODEIGNORE, dry_run=dry_run):
        changes.append(f"  {svc.alias}/vscode/.vscodeignore")
    return changes


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", help="Comma-separated service aliases to regenerate.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--dry-run", action="store_true", help="Don't write; just list changes."
    )
    mode.add_argument(
        "--check",
        action="store_true",
        help="Fail if VS Code README documentation links differ from the catalog.",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    selected: set[str] | None = None
    if args.only:
        selected = {s.strip() for s in args.only.split(",") if s.strip()}

    services = load_services()
    if args.check:
        errors: list[str] = []
        for svc in services:
            if selected and svc.alias not in selected:
                continue
            readme = (ROOT / svc.alias / "vscode" / "README.md").read_text()
            if svc.docs_url and svc.docs_url not in readme:
                errors.append(f"{svc.alias}/vscode/README.md: missing {svc.docs_url}")
            if not svc.docs_url and "https://docs.acedata.cloud" in readme:
                errors.append(
                    f"{svc.alias}/vscode/README.md: retired MCP still links legacy docs"
                )
        if errors:
            print("\n".join(errors), file=sys.stderr)
            return 1
        print("VS Code README documentation links match the MCP catalog.")
        return 0

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
