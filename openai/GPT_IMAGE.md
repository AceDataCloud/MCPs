# GPT Image by Ace Data Cloud

[简体中文完整安装与首用指南](https://github.com/AceDataCloud/OpenAIMCP/blob/main/readme/GPT_IMAGE_zh_Hans.md)

This is the GPT Image-only MCP profile maintained in the existing OpenAIMCP package. It exposes image creation, editing, the same task's retrieval, task lookup and model information. Chat, audio, embeddings, DALL-E and Nano Banana are excluded from this profile. It is an Ace Data Cloud integration, not an OpenAI-endorsed application.

The `io.github.AceDataCloud/mcp-gpt-image` [official Registry entry](https://registry.modelcontextprotocol.io/?q=io.github.AceDataCloud%2Fmcp-gpt-image) is **active at 2026.10.18.2**, matching the public `mcp-openai-pro` package (read back 2026-10-19). A catalog-consuming client should install that package with the manifest's `--profile gpt-image` arguments. Source and public release artifacts were verified separately; normal GUI catalog installation is still an independent client check, not implied by Registry presence.

## 1. Get a token with image and task permissions

1. [Register or sign in to Ace Data Cloud](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_readme_api_key).
2. Open **Applications → General application**. If absent, select **Initialize General Application**. Copy its API token or choose **Keys / Manage Keys → Create** for a separately named integration token.
3. Review expiration, usage limits and Allowed APIs. Allow the image operation you need and `/openai/tasks` for retrieving its result. Check model access, current balance and [current pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_readme_pricing). An account-management `platform-...` token is not an application API token.

![Real Ace Applications screenshot: copy an existing key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![Real Ace key creation screenshot: use a separately named restricted key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These are existing Ace platform screenshots from the pinned SunoDify tutorial source, reused for the same Applications/key flow. They do not show GPT Image installed or a new image generated. Never expose the real copied key in a screenshot, prompt, workflow or commit.

## 2. Install the service profile

Install the exact package version advertised by the Registry; the first verified profile release is `2026.10.18.2`. The package remains `mcp-openai-pro`; the profile is selected explicitly:

```json
{
  "mcpServers": {
    "gpt-image-by-ace": {
      "command": "uvx",
      "args": ["mcp-openai-pro", "--profile", "gpt-image"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_ACE_APPLICATION_TOKEN"}
    }
  }
}
```

This is a local stdio profile with five tools. There is no separate hosted GPT Image URL; pointing at the generic OpenAI remote would expose the general tool set. A client consuming the Registry should apply its package/environment fields directly. For a client without catalog support, merge the configuration into that client's user-level MCP settings and keep it private. Replace `YOUR_ACE_APPLICATION_TOKEN` with the raw token, without `Bearer `. If the client supports secret storage, use it rather than sharing a literal config.

The original `mcp-openai-pro` command without `--profile` keeps its general OpenAI tools. The profile adds no fallback model and does not change prices.

## 3. First use and asynchronous result

Start with `gpt_image_list_models`; it reads local metadata and sends no generation request. Choose a listed model explicitly before a paid generation. For example, after approving the current price and budget, ask the client to call `gpt_image_generate` with `prompt`, `model: "gpt-image-2"` and `async: true`. Editing uses `gpt_image_edit` with an ordered URL list in `image`.

Save the returned `task_id`. Call `gpt_image_get_task` with that same `id` until a terminal result is present; inspect the returned `response`/media links and error if any. A `pending` task or a green client message is not a completed image. Never rerun generation merely to poll. Querying another task ID does not grant generation permission.

No paid generation was performed for this guide. Local protocol tests use mocked image responses; they verify profile dispatch and task handling, not production media or billing.

## 4. Troubleshooting

| Symptom | Action |
|---|---|
| Entry not found | Search the exact `io.github.AceDataCloud/mcp-gpt-image` name in the official Registry. A downstream catalog may not have ingested the entry; do not count manual import as downstream listing. |
| Unknown `--profile` option | The installed package predates this profile; wait for or select the version advertised in the published manifest. |
| Authentication / 403 | Verify raw application token, service/model access, expiration and Allowed APIs; check task-query permission separately. |
| Chat or Nano Banana requested | Use the existing general OpenAI or Nano Banana integration; this profile intentionally excludes them. |
| No model supplied | Select a GPT Image model explicitly after checking its current price. |
| Pending or missing image | Query the same `task_id`; do not repeat creation. Preserve task/trace IDs for diagnosis, never the key. |

## 中文说明

这是 Ace Data Cloud 提供的 GPT Image 独立工具入口，复用现有 OpenAIMCP 的接口、错误与任务查询实现，不是把通用服务器换个名字重复上架。2026-10-19已从官方目录和公开PyPI读回匹配版本2026.10.18.2；目录已收录不代表所有客户端普通安装或收费结果都已验证。

进入 **Applications → General application** 复制或创建专用 API Token，核对权限、余额及当前价格。目录客户端按包字段安装；手动客户端使用上面的 `--profile gpt-image`，将原始 Token 放进 `ACEDATACLOUD_API_TOKEN`。先调用免费本地模型说明；收费生成需要明确选择模型和预算。拿到 `task_id` 后只查同一 ID 到终态，不为轮询重复生成。
