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

[中文完整教程](README.zh-CN.md)

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

请参阅[中文完整教程](README.zh-CN.md)：包含注册、专用 Key 图文步骤、本平台填写位置、首用与同 ID 查询、结果和排错。新原生面板仍待正式发版与真实界面验收；下方官方参考图不代表 Ace 已连接。

## Source and support

[Source repository](https://github.com/AceDataCloud/{service["repo"]}) · [Service documentation]({service["docs"]}) · [Current pricing](https://platform.acedata.cloud/models). Source of truth: [AceDataCloud/MCPs](https://github.com/AceDataCloud/MCPs). Existing MCP server and billing are reused. MIT.
'''
        yield (
            destination / "README.md",
            render(readme, alias, "jetbrains_marketplace", rules, catalog),
        )

        availability_zh = (
            "已有官方市场条目；本教程描述的新原生面板仍待新版本批准发布。当前旧版不能视为已经包含该面板。"
            if service["listing"]
            else "已准备独立插件源码与本地测试包；尚无获批公开版本。搜索链接是官方查询入口，不代表已上架，当前不能从普通市场安装。"
        )
        lookup_zh = (
            "点击 List models 会读取生成工具的模型字段 schema，不调用生成操作。"
            if service["model_tool"].startswith("@schema:")
            else "点击 List models 会调用该服务的模型信息工具，不提交生成。"
        )
        chinese = f'''# {service["title"]}：中文完整教程

[English](README.md)

Ace Data Cloud 提供的独立 {service["brand"]} {service["kind"]} 集成，并非 {service["brand"]} 或 JetBrains 官方插件。复用已有 Ace 服务和计费，不新增模型或价格。

## 1. 从官方入口安装

打开[JetBrains 官方安装或搜索入口]({listing})；在 IDE 中进入 **Settings → Plugins → Marketplace**，搜索 **{service["brand"]}** 并核对发布者 **AceDataCloud**。{availability_zh}

![JetBrains 官方插件市场安装界面](_assets/marketplace-official.png)

图片来自 [JetBrains 插件安装文档](https://www.jetbrains.com/help/idea/managing-plugins.html)，2026.2 官方资源，2026-10-18 下载核验，原始拍摄日期未披露。图中为其他插件的真实安装入口，不是本服务已安装或调用成功的截图。

新版本批准发布后打开 **Settings → Tools → {service["brand"]} MCP → {service["brand"]}**。这是新原生服务页签，不需要 AI Assistant 或 uv；原生面板的实际 GUI 截图尚待验收，不用官方空白图冒充新界面。

## 2. 注册、登录并取得专用 API Token

1. 打开 [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications)，先注册或登录自己的 Ace 账号。
2. 找到 **General application**。尚未初始化时选择 **Initialize General Application**；通用应用 Key 可使用账号已开放的服务，专用应用 Key 受其服务范围限制。确认 {service["brand"]} 的服务/模型权限，并查看[当前模型与价格](https://platform.acedata.cloud/models)，不要使用旧文章的报价或假定有免费额度。
3. 在应用卡片复制 **API Key**；或进入 **Keys / Manage Keys → Create**，创建一个独立命名的 Key，例如 `{alias}-jetbrains`，便于单独撤销、轮换和核对使用。
4. 创建时检查 **Expiration Time、Set Usage Limitation、Allowed APIs**。仅开放自己需要的操作；只允许任务查询不代表允许生成。检查应用当前余额能覆盖准备提交的请求，再点 Create 并从 Key 列表复制 Token。
5. 只复制原始 Token，不要带引号、空格或 `Bearer `。`platform-...` 是账号管理 Token，不能替代本服务生成 API Key；仅手动配置 HTTP Authorization 时加 `Bearer ` 前缀。

![真实应用卡片：复制 Key 或进入 Manage Keys](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/get-api-key-en.png)

![真实创建 Key 界面：名称、权限和限制](https://raw.githubusercontent.com/AceDataCloud/NanoBananaDify/2522b2f57210597af2db866445319334a1677a23/_assets/tutorial/create-api-key-en.png)

两张 Key 图复用既有 Dify 仓中的真实平台教程截图，固定于提交 `2522b2f57210597af2db866445319334a1677a23`；2026-10-18 复用，原始拍摄日期未记录。它们用于说明平台操作，不证明本插件已运行或产生注册/付费。

## 3. 在本平台填写 Key

在 **Tools → {service["brand"]} MCP → {service["brand"]}** 的 **Application API Key** 密码框粘贴原始 Key。新原生页签的 Key 仅留内存，关闭设置页后清空。不要把 Key 放进提示词、截图、共享项目或 Git。

第二个 **AI Assistant MCP (optional)** 页签是另一条可选配置路径，旧 helper 的独立 Key 仍采用原有本地存储；不要把这个旧行为误解为新原生面板保存了 Key。

## 4. 首次使用：先查模型，再明确提交一次

1. 点击 **List models**。{lookup_zh}先核对返回的模型和[当前价](https://platform.acedata.cloud/models)，再把自己选择的精确模型 ID 填入 **Model (choose explicitly)**。插件不默认替换或添加 fallback。
2. 在 **Prompt** 填写自己的要求。{service["brand"]} 新面板只提供现有生成工具的基础模型/提示词入口，服务的其他参数与高级能力请查看[服务文档]({service["docs"]})，不能从基础界面推断全套高级功能均已接入。
3. 点击 **Generate {service["kind"]}** 后，核对一次请求的模型与计费提醒；只有明确同意消耗自己的应用余额才选择 **Submit once**，否则选择 Cancel。插件不会自动生成或自动重试。
4. 本教程没有让用户照抄固定收费样例，也没有证明新的生产生成。静态模型列表、连接或 HTTP 200 都不能当作生成成功。

## 5. 用同一个任务 ID 查询终态与结果

提交返回 `task_id` 后，界面尝试填入 **Existing task ID**；未自动填写时从返回内容复制该 ID。点击 **Check existing task**，对应 `{service["task_tool"]}({service["task_arg"]}="EXISTING_TASK_ID")`，每次查询原来的 ID，直到终态。

- accepted、pending 或处理中都不是媒体完成，不要再次点 Generate 制造重复订单。
- 只有终态成功、返回内容与请求匹配、媒体 URL 实际可打开才完成该次使用；失败、内容限制和限流分别保留原含义。
- 提交超时且不确定是否已受理时，先去 Ace 账号找到原任务，再查其 ID。没有找到 ID 前不要盲目重新提交。
- 账单需另核唯一记录、Credits 消耗和当前套餐换算；本插件的安装数、原始结果或本地测试不等于营收。

## 6. 可选：把同一服务接入 AI Assistant

若使用 AI Assistant，可在第二个页签先 Apply 保存其 helper Key，再 Copy HTTP Config，粘到 **Settings → Tools → AI Assistant → Model Context Protocol → HTTP**，点 OK / Apply 后查看状态和可用工具。该步骤可选；原生服务页签无需它。它也不把 Ace 加到默认 LLM Provider 下拉列表。

![JetBrains 官方 HTTP MCP 配置对话框](_assets/mcp-http-official.png)

图片来自 [JetBrains MCP 文档](https://www.jetbrains.com/help/ai-assistant/mcp.html)，2026.2 官方资源，2026-10-18 下载核验。图中为空白官方对话框，不是本插件新原生页签或 Ace 已连接的截图。

```json
{{"mcpServers": {{"{alias}": {{"url": "{service["endpoint"]}", "headers": {{"Authorization": "Bearer YOUR_API_KEY"}}}}}}}}
```

## 7. 常见问题

| 情况 | 检查与处理 |
|---|---|
| 401 / 认证失败 | 检查原始 Key、过期、应用范围和 Allowed APIs；不要用账号管理 Token 代替生成 Key。 |
| 403 | 检查服务权限或内容限制，不能以切换未选择的模型绕过限制。 |
| 429 | 等待后由用户决定是否再次操作；生成不自动重试。 |
| 任务一直 pending | 查同一个任务 ID；不要把查询结果的 HTTP 200 当生成完成。 |
| 市场搜不到 | 检查该条目是否已有批准的公开版本；源码、本地包与投稿待审核不是正式上架。 |
| 多个插件覆盖 | 当前市场旧包曾有同目录问题，#982 候选修复已验证，但仍须等批准新包并做普通 GUI 共存验收。 |
| 想直接选择 Ace 模型 Provider | 这是独立服务插件。AI Assistant 的[第三方模型设置](https://www.jetbrains.com/help/ai-assistant/use-custom-models.html)另有机制；手填兼容 URL 不算默认 Ace preset 已收录。 |

## 来源与支持

[现有服务源仓](https://github.com/AceDataCloud/{service["repo"]}) · [服务说明]({service["docs"]}) · [当前价](https://platform.acedata.cloud/models)。唯一源码为 [AceDataCloud/MCPs](https://github.com/AceDataCloud/MCPs)，由既有 mirror 发布。安装免费不代表 API 免费，试用额度以当前账号展示为准。MIT。
'''
        yield (
            destination / "README.zh-CN.md",
            render(chinese, alias, "jetbrains_marketplace", rules, catalog),
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
