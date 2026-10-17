"""Prepare brand-first Smithery metadata and per-service onboarding.

Only writes local, reviewable files. This command never publishes or calls tools.
"""

import argparse
import json
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]


def load_catalog():
    return json.loads((ROOT / "scripts/smithery_listings.json").read_text())


def tagged_url(path, alias, placement):
    # opensource/referral is recognized by the pinned Backend producer contract.
    # Keep the actual Smithery placement explicit without inventing a global source.
    tags = {
        "utm_source": "opensource",
        "utm_medium": "referral",
        "utm_campaign": "evergreen",
        "utm_content": f"{alias}_smithery_{placement}",
    }
    return "https://platform.acedata.cloud" + path + "?" + urlencode(tags)


def config_schema(service):
    return {
        "type": "object",
        "properties": {
            "apiKey": {
                "type": "string",
                "description": "Ace Data Cloud application API Token. Get it at "
                + tagged_url("/console/applications", service["alias"], "api_key")
                + ". Paste the token only, without Bearer.",
                "x-from": {"header": "x-api-key"},
                "x-to": {"header": "Authorization", "prefix": "Bearer "},
            }
        },
        "required": ["apiKey"],
    }


def metadata(service):
    name = service["service"]
    limitation = (
        " This entry reuses OpenAI MCP, which also exposes chat and audio tools."
        if service["alias"] == "openai"
        else ""
    )
    return {
        "displayName": name + " by Ace Data Cloud",
        "description": service["summary"]
        + " Independently provided by Ace Data Cloud; not the model vendor's official integration."
        + limitation
        + "\n\n1. Install this server from Smithery in your client.\n"
        + "2. Register or sign in to [Ace Data Cloud Applications]("
        + tagged_url("/console/applications", service["alias"], "api_key")
        + "). Initialize General application if needed, then copy its API Key or "
        + "create a dedicated key. Check service access, expiry, limits and balance.\n"
        + "3. In the connection's apiKey / API Token field, paste only the token, "
        + "without Bearer. Complete sign-in when prompted.\n"
        + f"4. Query {service['task_tool']} with an existing task's "
        + f"{service['task_field']}; do not submit generation again while pending.\n\n"
        + "Generation is metered; see [current pricing]("
        + tagged_url(service["price_path"], service["alias"], "pricing")
        + "). A platform- account token cannot replace the application API Key.",
        "homepage": tagged_url(service["price_path"], service["alias"], "listing"),
        "repositoryUrl": "https://github.com/AceDataCloud/" + service["repository"],
        "license": "MIT",
        "iconUrl": service["icon_url"],
    }


def render_readme(service, catalog, zh=False):
    name, alias = service["service"], service["alias"]
    listing = "https://smithery.ai/servers/" + service["qualified_name"]
    key = tagged_url("/console/applications", alias, "api_key")
    pricing = tagged_url(service["price_path"], alias, "pricing")
    other = "README.md" if zh else "README_zh-CN.md"
    switch = "English" if zh else "简体中文"
    pending = service["status"] == "candidate"
    if zh:
        status = (
            "这是待发布候选资料；未证明官方目录已可安装。请先打开目录核对发布状态。"
            if pending
            else "公开条目已存在；2026-10-18仍需独立完成授权和首用验收，不能把看到条目当作连接成功。"
        )
        text = f"""# {name} by Ace Data Cloud：Smithery 使用指南

[{switch}]({other}) · [API 与当前价格]({pricing})

{service["summary_zh"]} 这是 Ace Data Cloud 提供的独立集成，不是模型厂商的官方插件。{status}

## 1. 从官方目录安装

打开 [{name} by Ace Data Cloud]({listing})，核对发布者命名空间是 `acedatacloud-mcp`。搜索词可用 `{service["search_terms"][0]}`；点击 **Try now** 或客户端安装入口，选择自己的客户端。界面文字可能随版本变化。

已有同服务连接时复用它，不重复创建。下面的命令是官方 CLI 的另一种安装入口，不能代替正常安装的验收：

```bash
npx -y smithery mcp add {service["qualified_name"]}
```

## 2. 注册、登录并取得应用 API Token

1. 打开 [Ace Data Cloud → Applications]({key})，注册或登录。如果没有 **General application**，先点 **Initialize General Application**。
2. 在 General application 复制 API Key，或点 **Manage Keys → Create** 创建单独的 `Smithery {name}` 密钥；专用服务应用的密钥只允许其对应服务。
3. 检查到期时间、用量上限、Allowed APIs、服务权限、[当前价格和余额]({pricing})。本流程的接口为 `{", ".join(service["api_paths"])}`；查询权限不等于生成权限。
4. 只复制 Token 原文，不加 `Bearer `、引号或空格。`platform-...` 账号管理 Token 不能代替应用生成密钥。

![Applications 中复制或管理 API Key]({catalog["token_images"][0]})

![创建独立密钥与设置限制]({catalog["token_images"][1]})

上图为 Ace 官方 SunoDify 教程的真实截图（固定源码版本，引用核验日期2026-10-18），凭据已遮挡；不是 Smithery 授权成功截图。

## 3. 在 Smithery 的哪里填写

连接页面按提示登录；如果出现 **apiKey / API Token** 字段，粘贴上面的原文并保存。该值按发布配置从 `x-api-key` 转发为服务端 Bearer Token。不要在客户端手填 Smithery 保留的 Authorization 字段；它还用于 Smithery 自身登录。

如果没有密钥字段而是浏览器登录页面，按现有连接的授权流程完成登录；不要把两种方式同时配置。当前已有扫描授权超时和连接需授权记录；无法授权时保留错误，不再次提交生成。

![Smithery 官方客户端选择界面](https://mintcdn.com/smithery/r4y1nsnAhcafdzOF/images/clients.png)

官方原始参考图，来自 [Smithery 客户端文档](https://smithery.ai/docs/use/listing_your_client)，2026-10-18引用，截图原日期/版本未注明。它只说明选择客户端的位置，不证明本服务已连接。

## 4. 先做不会生成的新手检查

在客户端输入：**{service["first_prompt_zh"]}**

"""
    else:
        status = (
            "This is a publication candidate; normal installation from the directory has not been verified. Check the listing's release status first."
            if pending
            else "The public entry exists. Authorization and the first successful call still need independent verification as of 2026-10-18. Seeing a listing does not mean connected."
        )
        text = f"""# {name} by Ace Data Cloud for Smithery

[{switch}]({other}) · [API and current pricing]({pricing})

{service["summary"]} This is an independent Ace Data Cloud integration, not an official integration from the model vendor. {status}

## 1. Install from the official directory

Open [{name} by Ace Data Cloud]({listing}) and check the publisher namespace is `acedatacloud-mcp`. Search for `{service["search_terms"][0]}`; choose **Try now** or the client installation entry, then select your client. Controls may move between versions.

Reuse an existing connection for this service. The official CLI provides another directory installation entry; this command is not evidence that normal installation has passed:

```bash
npx -y smithery mcp add {service["qualified_name"]}
```

## 2. Register, sign in, and get an application API Token

1. Open [Ace Data Cloud → Applications]({key}) and register or sign in. If **General application** does not exist, choose **Initialize General Application** first.
2. Copy its API Key, or open **Manage Keys → Create** for a separate `Smithery {name}` key. A service-specific application's key is limited to that service.
3. Check expiration, usage limits, Allowed APIs, service access, [current pricing and balance]({pricing}). This flow uses `{", ".join(service["api_paths"])}`. Task lookup access does not grant generation access.
4. Copy only the raw token, without `Bearer `, quotes, or whitespace. A `platform-...` account-management token cannot replace this application key.

![Copy the application key or open Manage Keys]({catalog["token_images"][0]})

![Create an optional dedicated key and review restrictions]({catalog["token_images"][1]})

These are real, redacted screenshots from Ace's SunoDify tutorial at a pinned source revision, referenced on 2026-10-18. They are not screenshots of successful Smithery authorization.

## 3. Where to paste the token in Smithery

Follow the connection's sign-in prompt. If the configuration form shows **apiKey / API Token**, paste the raw application token and save. The published schema maps `x-api-key` to the service's Bearer header. Do not manually overwrite Smithery's reserved Authorization field; it is also used for Smithery authentication.

If the connection opens a browser sign-in flow instead of a token field, finish that existing authorization flow. Do not configure both routes. Existing scan releases have timed out waiting for authorization, and the verification connection still needs sign-in; keep the error and do not resubmit generation to fix authentication.

![Smithery's official client selection screenshot](https://mintcdn.com/smithery/r4y1nsnAhcafdzOF/images/clients.png)

Unmodified official reference from [Smithery's client documentation](https://smithery.ai/docs/use/listing_your_client), referenced on 2026-10-18; original capture date/version unspecified. It illustrates client selection, not a successful connection to this service.

## 4. Start with a check that does not generate content

Ask the client: **{service["first_prompt"]}**

"""
    if service["read_tool"]:
        text += f"Read-only tool: `{service['read_tool']}`.\n\n"
    else:
        text += "Use the client's tool/schema listing; do not call the generation tool.\n\n"
    if alias == "openai":
        text += (
            "This directory entry reuses OpenAI MCP: it also exposes chat/audio tools. "
            "Choose GPT Image tools explicitly; it is not an image-only runtime.\n\n"
        )
    if alias == "suno":
        text += (
            "![Actual Ace Smithery listing, 2026-10-17](assets/listing-20261017.jpg)\n\n"
            "Historical real page screenshot, before the brand-first title update on "
            "2026-10-18. It proves the listing and Try now entry existed, not a successful "
            "connection or generation. Capture provenance: [source.json](assets/source.json).\n\n"
        )
    if zh:
        text += f"""## 5. 生成与查询必须分开

确认模型、参数、价格和当次额度后，才允许调用 `{service["generation_tool"]}`。保存返回的 `task_id`；accepted/pending 不是成功。后续仅调用 `{service["task_tool"]}`，把同一个值填到 `{service["task_field"]}`，直到服务的终态成功且有可访问媒体。失败或pending时不要重跑生成。

```json
{{"{service["task_field"]}": "YOUR_EXISTING_TASK_ID"}}
```

这是查询参数示例，没有执行请求。不要把任务接受、客户端绿色状态或旧结果当成新生成成功。截图和演示不得包含密钥、账号信息或带签名媒体URL。

## 常见问题

- **搜索没找到**：尝试上面的服务词或直接打开官方条目；候选页、搜索索引和可安装状态分别核验，不承诺排名。
- **401 / auth_required**：检查现有连接登录、Token原文、到期和权限。扫描发布需要的授权与消费者连接是两个环节。
- **AUTH_TIMEOUT**：发布扫描等待授权超时；不代表模型生成失败，也不要重复发布来绕过。
- **结果仍pending**：只查原task_id，不再次生成；查询返回成功和可打开产物后才算完成。
- **费用和支持**：使用账户当前价格，不承诺免费额度。到 [Ace服务文档]({pricing}) 查看限制和支持入口。
"""
    else:
        text += f"""## 5. Separate generation from task lookup

Only call `{service["generation_tool"]}` after reviewing the model, parameters, current price, and your budget. Save the returned `task_id`; accepted/pending is not completion. Query `{service["task_tool"]}` using that same value in `{service["task_field"]}` until the service reaches a successful terminal state and returns accessible media. Never rerun generation because a task is pending or failed.

```json
{{"{service["task_field"]}": "YOUR_EXISTING_TASK_ID"}}
```

This is a lookup-argument example, not an executed request. A client success indicator or an old media result does not prove a new generation completed. Never include keys, account details, or signed media URLs in screenshots.

## Troubleshooting

- **Search does not find it:** try the service terms above or open the exact listing. Candidate records, search indexing, and installability are separate; no ranking is promised.
- **401 / auth_required:** check the existing connection's sign-in, raw token, expiry, and permissions. Publisher scan authorization and consumer connection authorization are separate.
- **AUTH_TIMEOUT:** the publishing scan timed out waiting for authorization. It is not a generation failure; do not keep republishing to bypass it.
- **Still pending:** query the original task ID. Count completion only after a successful terminal result and accessible media.
- **Pricing and support:** use the account's current rate and allowance; no free allowance is promised. See [Ace service documentation]({pricing}) for limits and support.
"""
    return text


def outputs():
    catalog = load_catalog()
    for service in catalog["services"]:
        folder = ROOT / service["alias"] / "smithery"
        yield (
            folder / "listing.json",
            json.dumps(metadata(service), ensure_ascii=False, indent=2) + "\n",
        )
        yield (
            folder / "release.json",
            json.dumps(
                {
                    "type": "external",
                    "upstreamUrl": service["endpoint"],
                    "configSchema": config_schema(service),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
        )
        yield folder / "README.md", render_readme(service, catalog)
        yield folder / "README_zh-CN.md", render_readme(service, catalog, zh=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    stale = []
    for path, text in outputs():
        if path.exists() and path.read_text() == text:
            continue
        if args.check:
            stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
    if stale:
        parser.exit(1, "Stale Smithery materials: " + ", ".join(stale) + "\n")


if __name__ == "__main__":
    main()
