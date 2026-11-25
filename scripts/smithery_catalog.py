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


def tagged_url(path):
    # opensource/referral is recognized by the pinned Backend producer contract.
    tags = {
        "utm_source": "opensource",
        "utm_medium": "referral",
        "utm_campaign": "evergreen",
    }
    return "https://platform.acedata.cloud" + path + "?" + urlencode(tags)


def config_schema():
    return {
        "type": "object",
        "properties": {
            "apiKey": {
                "type": "string",
                "description": "Ace Data Cloud application API Token. Get it at "
                + tagged_url("/console/applications")
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
        + f" Connect using the Streamable HTTP URL: {service['endpoint']}. "
        + "Authorize with your MCP client and check your account access and "
        + f"[current pricing]({tagged_url(service['price_path'])}) before generating.",
        "homepage": tagged_url(service["price_path"]),
        "repositoryUrl": "https://github.com/AceDataCloud/" + service["repository"],
        "license": "MIT",
        "iconUrl": service["icon_url"],
    }


def render_readme(service, zh=False):
    name = service["service"]
    endpoint = service["endpoint"]
    client_guide = "../README.md"
    pricing = tagged_url(service["price_path"])
    if zh:
        return f"""# {name} 的 MCP 直连配置

Smithery 在 2026 年 10 月 31 日关闭了托管连接及账号服务，保留公开目录。[平台公告](https://smithery.ai/future)

在支持 Streamable HTTP 的 MCP 客户端中添加 `{endpoint}`，按客户端提示完成服务授权。已有连接如使用旧的 Smithery 代理地址，请改用这个 Ace Data Cloud 端点。安装和密钥设置见[本服务说明]({client_guide})。

生成前检查[当前价格与访问权限]({pricing})。查询进度时，将原任务的 `{service["task_field"]}` 传给 `{service["task_tool"]}`。
"""
    return f"""# Connect to {name} directly

Smithery retired its managed connections and accounts on October 31, 2026. Its public directory remains available. [Platform announcement](https://smithery.ai/future)

Add `{endpoint}` as a Streamable HTTP server in your MCP client and follow the client's authorization prompt. Update existing connections that use a Smithery proxy URL to this Ace Data Cloud endpoint. See the [service setup guide]({client_guide}) for installation and application keys.

Check [current pricing and account access]({pricing}) before generating. To check progress, pass the original task's `{service["task_field"]}` to `{service["task_tool"]}`.
"""


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
                    "configSchema": config_schema(),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
        )
        yield folder / "README.md", render_readme(service)
        yield folder / "README_zh-CN.md", render_readme(service, zh=True)


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
