# Seedance by Ace Data Cloud for Cline

Use Seedance video tools inside Cline through the existing Ace Data Cloud MCP server. This is an Ace Data Cloud integration, not an official Seedance or Cline first-party plugin.

English guide · [中文步骤](#中文步骤) · [API access and current pricing](https://platform.acedata.cloud/documents/seedance-mcp?utm_source=cli&utm_medium=referral&utm_campaign=evergreen&utm_content=cline_seedance_pricing)

## 1. Install from the Cline directory

Open Cline's **Marketplace**, search **Seedance**, and select **Seedance by Ace Data Cloud**. Check the author is **Ace Data Cloud** and the repository is [AceDataCloud/SeedanceMCP](https://github.com/AceDataCloud/SeedanceMCP).

**Submission status (2026-10-18): this directory entry is being proposed; it is not yet an approved/public listing.** If the card is unavailable, use this manual equivalent while review is pending:

```bash
cline mcp add seedance-acedatacloud https://seedance.mcp.acedata.cloud/mcp --transport http --yes
```

This installs one named server, not all Ace services. It does not create an account, supply a key or run a generation. Cline's native MCP marketplace is used; no separate code package is copied. [Official MCP configuration](https://docs.cline.bot/mcp/mcp-overview) · [Official directory](https://github.com/cline/marketplace).

## 2. Register or sign in and obtain your API Token

1. Open [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=cli&utm_medium=referral&utm_campaign=evergreen&utm_content=cline_seedance_api_key). Register/sign in if needed.
2. Open **General application**; if none exists, choose **Initialize General Application**. A general key can access services enabled for your account; a service-specific key is limited to that service. Confirm **Seedance** access, current pricing and a sufficient account balance.
3. Copy the API Key on the application card, or open **Manage Keys → Create** to make a dedicated key named `Cline Seedance`.

![Copy a key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

4. Review **Expiration Time**, **Set Usage Limitation**, and **Allowed APIs**. Restrict only as needed and allow both the Seedance generation and task-query APIs. Create the key, return to the list, and copy the complete value.

![Create a dedicated API key with optional restrictions](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These are existing redacted Ace console screenshots from the pinned Dify guide (collected 2026-10-18), reused only for the same Ace key controls; the Dify installation steps do not apply to Cline. No live secret is displayed. Copy the token string only: no quotes, spaces or `Bearer `. A `platform-...` account-management token is not this service API key. Any trial balance is what your account currently shows, not a promised allowance.

## 3. Paste the Token in Cline's MCP settings

In the Cline panel, open **MCP Servers → Configure → Configure MCP Servers**. Merge the following named server into that user-level JSON file and preserve your other servers:

```json
{
  "mcpServers": {
    "seedance-acedatacloud": {
      "type": "streamableHttp",
      "url": "https://seedance.mcp.acedata.cloud/mcp",
      "headers": {
        "Authorization": "Bearer YOUR_API_TOKEN"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

Replace **only** `YOUR_API_TOKEN` with your copied token. The `Authorization` header requires `Bearer ` once. The file contains a secret: keep it private and out of Git and screenshots. Cline CLI uses `~/.cline/data/settings/cline_mcp_settings.json` by default; `CLINE_MCP_SETTINGS_PATH` can override it. Project `.cline/` rules are not a project MCP settings file. Save, reconnect the server and confirm tools appear.

If you prefer browser authorization, remove the entire fixed `headers` property, then use **Authorize OAuth** in the `cline mcp` wizard. The hosted server publishes OAuth metadata, but a successful account consent flow must still be verified for your Cline version. Do not combine a fixed Bearer header with OAuth for the same server. Authentication does not waive API charges.

![Official Cline settings reference](https://raw.githubusercontent.com/cline/cline/b549ceb4bb4247284c975f6d6ca0979decec097c/docs/assets/free-models/free-models-vscode-cline-provider.png)

**Official original reference, not an Ace run.** This Cline document screenshot shows the original Cline Usage-Billing provider and its own model list; it was collected 2026-10-17 and its capture date/version are unspecified (Nightly). It identifies the native Cline panel only, not an Ace selection, MCP settings screenshot or successful connection. Click the panel's **MCP Servers** control for the tool configuration above; do not put `https://seedance.mcp.acedata.cloud/mcp` into the model Provider Base URL.

Model setup is separate: use a model provider already configured in Cline. Ace chat models use **OpenAI Compatible**, Base URL `https://api.acedata.cloud/v1`, your own Key and a model that supports Chat Completions and tool calls. This MCP entry does not add a named Ace model provider.

## 4. First use and asynchronous results

For a no-generation installation check, ask Cline to use the static `seedance_list_models` reference tool. Static reference results or a loaded schema prove tool loading only, not valid paid access or balance. In the IDE, leave MCP `autoApprove` empty and check global approval settings; CLI headless tasks may auto-approve, so use `cline --tui --auto-approve false` when you require interactive approval.

When **you decide to generate** after reviewing the [current service contract and prices](https://platform.acedata.cloud/documents/seedance-mcp?utm_source=cli&utm_medium=referral&utm_campaign=evergreen&utm_content=cline_seedance_first_use), ask Cline to call `seedance_generate_video` for one request with a currently supported model and parameters. This can be charged. Keep the returned **task_id**, then call `seedance_get_task` with **that same ID** until its task result is terminal. Do not repeat the generation merely because the task is pending. A completed chat turn or a playable preview is not task completion.

Read the returned task status, success/error and media fields according to the tool schema. On success, open the returned audio/video/image URL; do not invent a URL, reuse another account's task or treat an empty media field as success. Check [usage history](https://platform.acedata.cloud/console/usages?utm_source=cli&utm_medium=referral&utm_campaign=evergreen&utm_content=cline_seedance_usage) for the original request and its charge; list/configuration commands are not billable-generation evidence. This guide contains no claimed Seedance generation result or new paid test.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| No directory card | The proposal is pending; use the named manual MCP command, not an unrelated similarly named integration. |
| Tools missing | Check server URL, `streamableHttp`, saved file and reconnect. For a local `uvx` setup, allow a longer per-server timeout (for example 30s) on first startup. |
| 401 / 403 | Check raw Token, one Bearer prefix, application access, expiration, Allowed APIs, usage limit and balance. Remove a stale fixed header before OAuth. |
| 400 parameter error | Use the current tool model enum/schema; do not copy parameters from another service or old model. |
| Pending task | Query the same task ID. Do not regenerate or enable automatic paid retries. |
| 429 | Wait and reduce concurrency; inspect the service's limits. |
| Timeout / 5xx / failed task | Inspect original task and usage before considering a new submission; retain task/trace ID, never share the Token. |

## Privacy, cost and source

The MCP integration is free to install; the server receives your selected prompts/media and authorization and calls Ace Data Cloud. Service calls follow current account/service pricing. Keep credentials in Cline's private user configuration, not prompts, shared workflows or exports. Use only content you may process.

[Source](https://github.com/AceDataCloud/SeedanceMCP) · [Current models and prices](https://platform.acedata.cloud/models?utm_source=cli&utm_medium=referral&utm_campaign=evergreen&utm_content=cline_seedance_models) · dev@acedata.cloud. Development/source PRs and local checks are separate from official directory acceptance, actual install, task completion, billing and attributed users.

## 中文步骤

1. 在 Cline Marketplace 搜索 **Seedance**，核对标题 **Seedance by Ace Data Cloud** 和作者。2026-10-18 仍在投稿准备/审核流程，未收录时用第 1 节的命令，不把手动安装当成官方上架。
2. [注册/登录 Ace 并打开 Applications](https://platform.acedata.cloud/console/applications?utm_source=cli&utm_medium=referral&utm_campaign=evergreen&utm_content=cline_seedance_api_key_zh)，进入或初始化 **General application**；复制 API Key，或 **Manage Keys → Create** 创建专用 Token。检查该服务权限、余额、有效期和生成/查询 API 限制。上方两张脱敏控制台图仅说明 Ace 的取 Key 步骤。
3. Cline **MCP Servers → Configure → Configure MCP Servers**，把第 3 节 JSON 合并到用户设置，仅替换 `YOUR_API_TOKEN`；`Authorization` 是 `Bearer ` 加 Token。不要把 MCP URL 填到模型 Provider，也不要把密钥提交 Git。
4. 先看工具 schema 或只读参考列表，验证加载；真正生成前看当前价格并确认额度。保存返回的 **同一个 task_id**，用 `seedance_get_task` 查到终态和媒体链接；pending 时不重复生成。模型/工具配置成功不等于付费任务、账单或增长已验收。
