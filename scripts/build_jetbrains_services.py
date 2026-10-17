"""Generate service-first JetBrains artifacts; reuse existing MCP servers and IDs."""

import argparse
import json
import re
import shutil
from pathlib import Path

from marketing_readmes import contract, render, render_jetbrains_description, tagged_url
from mcp_catalog import load_catalog
from token_onboarding import token_guide

ROOT = Path(__file__).resolve().parents[1]
SERVICES = json.loads((ROOT / "scripts/jetbrains_services.json").read_text())[
    "services"
]


def scaffold(service):
    destination = ROOT / service["directory"]
    if destination.exists():
        return
    original = ROOT / "seedance/jetbrains"
    shutil.copytree(
        original,
        destination,
        ignore=shutil.ignore_patterns("build", ".gradle", ".intellijPlatform"),
    )
    old_package = destination / "src/main/kotlin/com/acedatacloud/mcp/seedance"
    package_path = (
        destination / "src/main/kotlin" / service["package"].replace(".", "/")
    )
    package_path.parent.mkdir(parents=True, exist_ok=True)
    old_package.rename(package_path)
    for path in destination.rglob("*"):
        if path.suffix not in {".kt", ".kts", ".xml", ".properties", ".md"}:
            continue
        text = path.read_text()
        text = text.replace("com.acedatacloud.mcp.seedance", service["package"])
        text = text.replace("Seedance", service["brand"]).replace(
            "seedance", service["alias"]
        )
        path.write_text(text)
    settings = package_path / "McpSettings.kt"
    text = settings.read_text().replace(
        service["alias"] + ".mcp.acedata.cloud", service["endpoint"].split("/")[2]
    )
    text = text.replace('"mcp-' + service["alias"] + '"', '"' + service["pypi"] + '"')
    settings.write_text(text)
    properties = destination / "gradle.properties"
    text = properties.read_text()
    text = re.sub(
        r"pluginRepositoryUrl = .*",
        "pluginRepositoryUrl = https://github.com/AceDataCloud/" + service["repo"],
        text,
    )
    properties.write_text(text)


def generate():
    rules, catalog = contract(), load_catalog()
    catalog["gpt-image"] = catalog["openai"]
    for service in SERVICES:
        alias = service["alias"]
        destination = ROOT / service["directory"]
        package_path = (
            destination / "src/main/kotlin" / service["package"].replace(".", "/")
        )

        def url(target):
            return tagged_url(target, alias, "jetbrains_marketplace", rules, catalog)

        substitutions = {
            "__PACKAGE__": service["package"],
            "__ALIAS__": alias,
            "__TITLE__": service["title"],
            "__BRAND__": service["brand"],
            "__KIND__": service["kind"],
            "__MODEL_TOOL__": service["model_tool"],
            "__MODEL_PREFIX__": service.get("model_prefix", ""),
            "__GENERATE_TOOL__": service["generate_tool"],
            "__TASK_TOOL__": service["task_tool"],
            "__TASK_ARG__": service["task_arg"],
            "__ENDPOINT__": service["endpoint"],
            "__KEY_URL__": url("https://platform.acedata.cloud/console/applications"),
            "__PRICE_URL__": url("https://platform.acedata.cloud/models"),
        }
        for name in ["AceServiceClient.kt", "AceServicePanel.kt"]:
            text = (ROOT / "scripts/jetbrains_templates" / name).read_text()
            for key, value in substitutions.items():
                text = text.replace(key, value)
            yield package_path / name, text

        configurable = package_path / (service["configurable"] + ".kt")
        text = configurable.read_text()
        text = re.sub(
            r'override fun getDisplayName\(\): String = "[^"]+"',
            'override fun getDisplayName(): String = "' + service["brand"] + ' MCP"',
            text,
        )
        text = re.sub(
            r'browserLink\("Documentation", "https://platform\.acedata\.cloud[^"]*"\)',
            'browserLink("Documentation", "' + url(service["docs"]) + '")',
            text,
        )
        # Transform the existing settings page without changing its registered ID/class.
        if "private var nativePanel:" not in text:
            text = text.replace(
                '    private var apiToken: String = ""',
                '    private var nativePanel: AceServicePanel? = null\n    private var apiToken: String = ""',
            )
            text = text.replace(
                "        return myPanel!!",
                """        nativePanel = AceServicePanel()
        return javax.swing.JTabbedPane().apply {
            addTab("__BRAND__", nativePanel)
            addTab("AI Assistant MCP (optional)", myPanel)
        }""".replace("__BRAND__", service["brand"]),
            )
            text = text.replace(
                "    override fun disposeUIResources() {",
                "    override fun disposeUIResources() {\n        nativePanel?.dispose()\n        nativePanel = null",
            )
        yield configurable, text

        properties = destination / "gradle.properties"
        yield (
            properties,
            re.sub(
                r"pluginName = .*",
                "pluginName = " + service["title"],
                properties.read_text(),
            ),
        )
        descriptor = destination / "src/main/resources/META-INF/plugin.xml"
        text = descriptor.read_text()
        text = re.sub(
            r"<name>.*?</name>", "<name>" + service["title"] + "</name>", text, count=1
        )
        text = re.sub(
            r'(displayName=")[^"]+("\s+parentId="tools")',
            lambda match: match[1] + service["brand"] + " MCP" + match[2],
            text,
        )
        description = f'''<description><![CDATA[
<p>{service["brand"]} {service["kind"]} generation and task lookup, provided by Ace Data Cloud.</p>
<p>Install this independent integration, open Settings → Tools → {service["brand"]} MCP, enter an application API key, list models, choose one explicitly and submit a prompt. Use the returned task ID to check the same task until a terminal result. Generation uses your Ace balance; installation does not include free API usage.</p>
<p>The native service panel works without AI Assistant. Optional MCP setup also connects these tools to AI Assistant; it does not add an LLM provider preset.</p>
<p>This is an independent Ace Data Cloud integration, not an official {service["brand"]} or JetBrains product. Models, access and current pricing are controlled by your Ace account.</p>
<p><a href="{service["docs"]}">Service documentation</a> · <a href="https://platform.acedata.cloud/models">Current pricing</a></p>
]]></description>'''
        text = re.sub(
            r"<description>.*?</description>",
            lambda _: description,
            text,
            count=1,
            flags=re.S,
        )
        yield descriptor, render_jetbrains_description(text, alias, rules, catalog)

        listing = service[
            "listing"
        ] or "https://plugins.jetbrains.com/search?search=" + service["brand"].replace(
            " ", "%20"
        )
        availability = (
            "Official Marketplace entry exists; new panel awaits an approved release."
            if service["listing"]
            else "Marketplace submission package prepared; this independent plugin is not publicly approved yet. The search link is not a claim of availability."
        )
        readme = f'''# {service["title"]}

Independent {service["brand"]} {service["kind"]} integration provided by Ace Data Cloud for JetBrains IDEs. Not an official {service["brand"]} or JetBrains product.

## Install from Marketplace

[Open the official installation entry]({listing}), or search **{service["brand"]}** in **Settings → Plugins → Marketplace** and check publisher **AceDataCloud**. {availability}

The new native panel is under **Settings → Tools → {service["brand"]} MCP → {service["brand"]}**. It provides model discovery, an explicit model field, prompt submission, existing-task lookup and the raw service result. It does not require AI Assistant. Plugin installation is free; API operations use your Ace application's permissions and balance.

![Official JetBrains Marketplace installation screen](_assets/marketplace-official.png)

Source: [JetBrains installation documentation](https://www.jetbrains.com/help/idea/managing-plugins.html), official 2026.2 documentation image downloaded 2026-10-18. It shows another plugin, not an Ace installation or runtime result.

## Get an application API key

<!-- BEGIN TOKEN ONBOARDING -->
{token_guide(alias)}<!-- END TOKEN ONBOARDING -->

The new native panel keeps its key in memory and clears it when the settings page closes. Paste the raw key into **Application API Key** in the {service["brand"]} tab. The older optional MCP helper stores its separate settings key locally; do not put credentials in shared project files.

## First use and existing task lookup

1. Click **List models**. Review [current pricing](https://platform.acedata.cloud/models), then enter the exact model ID you want. The plugin does not silently select a substitute.
2. Enter a prompt and click **Generate {service["kind"]}**. Review the one-request charge confirmation. Cancel if the model, access or balance is unclear. No automatic generation or retry runs.
3. Copy the returned `task_id` to **Existing task ID** if it is not filled automatically. Click **Check existing task** on that same ID until the response reports a terminal state. Keep the result/URL and verify it opens before calling the job successful. A pending response or accepted request is not completed media.
4. If a submission times out, do not submit again blindly. Find the original task in your Ace account first to avoid duplicate charges. A failed/content-restricted/rate-limited result must remain distinct.

Read-only first-use tool: `{service["model_tool"]}`. Generation tool: `{service["generate_tool"]}`. Same-task query: `{service["task_tool"]}({service["task_arg"]}="EXISTING_TASK_ID")`. This guide contains no proof of a newly paid generation or revenue.

## Optional AI Assistant tools

If you use AI Assistant, the second tab can still copy the HTTP/STDIO configuration. Paste it into **Settings → Tools → AI Assistant → Model Context Protocol → HTTP**, then Apply and review the available tools. This optional route is separate from an LLM provider.

![Official AI Assistant HTTP MCP dialog](_assets/mcp-http-official.png)

Source: [JetBrains MCP documentation](https://www.jetbrains.com/help/ai-assistant/mcp.html), official 2026.2 image downloaded 2026-10-18. Empty official dialog, not a screenshot of Ace connected. No fabricated screenshot of the new panel is included; real panel screenshots remain a release acceptance item.

```json
{{"mcpServers": {{"{alias}": {{"url": "{service["endpoint"]}", "headers": {{"Authorization": "Bearer YOUR_API_KEY"}}}}}}}}
```

## Troubleshooting

- **401:** check raw copied key, expiration and Allowed APIs. A `platform-` management token cannot replace an application API key.
- **403:** check service access or content restrictions. Do not change to another model without choosing and pricing it explicitly.
- **429:** wait before a later manual attempt; the plugin does not retry generation.
- **Pending task:** query the same ID. Never treat HTTP 200 or an accepted task as completed media.
- **Plugin missing from search:** only approved public versions can be installed normally. Source, local ZIPs and uploaded review candidates are separate stages.
- **Want an Ace model in AI Assistant's provider dropdown?** This is a service plugin, not a default LLM preset. JetBrains currently documents a separate [third-party model setup](https://www.jetbrains.com/help/ai-assistant/use-custom-models.html).

## 中文上手

在官方 Marketplace 搜索 **{service["brand"]}** 并确认发布者 AceDataCloud；待新版本批准后，打开 **Tools → {service["brand"]} MCP → {service["brand"]}**。先注册/登录 [Ace Applications](https://platform.acedata.cloud/console/applications)，初始化 General application，复制或创建专用 API Token，并检查 Allowed APIs、过期、余额和当前价。把原始 Key 粘到原生面板；点击 List models，明确选择模型再填提示词，提交前确认只发一次收费请求。返回任务 ID 后在 Existing task ID 查询同一个任务直到终态，再核媒体 URL。401 查 Key/权限，429 等待；不因超时重复生成。可选 AI Assistant 页仍需复制配置；它不是默认 LLM Provider。原生新面板尚待正式发版与真实界面验收，本文不把官方参考图当已运行截图。

## Source and support

[Source repository](https://github.com/AceDataCloud/{service["repo"]}) · [Service documentation]({service["docs"]}) · [Current pricing](https://platform.acedata.cloud/models). Source of truth: [AceDataCloud/MCPs](https://github.com/AceDataCloud/MCPs). Existing MCP server and billing are reused. MIT.
'''
        yield (
            destination / "README.md",
            render(readme, alias, "jetbrains_marketplace", rules, catalog),
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if not args.check:
        for service in SERVICES:
            scaffold(service)
    stale = []
    for service in SERVICES:
        for name in ("marketplace-official.png", "mcp-http-official.png"):
            source = ROOT / "scripts/jetbrains_templates/assets" / name
            destination = ROOT / service["directory"] / "_assets" / name
            if (
                not destination.exists()
                or source.read_bytes() != destination.read_bytes()
            ):
                if args.check:
                    stale.append(str(destination.relative_to(ROOT)))
                else:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, destination)
    for path, expected in generate():
        if not path.exists() or path.read_text() != expected:
            if args.check:
                stale.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(expected)
    if stale:
        raise SystemExit("Stale JetBrains artifacts: " + ", ".join(stale))
    print(
        "JetBrains service artifacts verified"
        if args.check
        else "JetBrains service artifacts generated"
    )


if __name__ == "__main__":
    main()
