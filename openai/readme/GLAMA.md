# GPT Image by Ace Data Cloud in Glama

[简体中文](#中文操作指南) · [GPT Image profile source](../GPT_IMAGE.md) · [Current models and price](https://platform.acedata.cloud/models?utm_source=glama&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_glama_pricing)

Use the **GPT Image-only profile**, not the generic OpenAI remote server. The published `mcp-openai-pro` package accepts `--profile gpt-image` and exposes exactly five tools: `gpt_image_generate`, `gpt_image_edit`, `gpt_image_get_task`, `gpt_image_list_tasks`, and `gpt_image_list_models`. It reuses the maintained Ace client and task/error handling. This integration is provided by Ace Data Cloud, not endorsed by OpenAI.

## 1. Find the correct entry and distinguish publication stages

The [official MCP Registry entry](https://registry.modelcontextprotocol.io/?q=io.github.AceDataCloud%2Fmcp-gpt-image) is the dedicated `io.github.AceDataCloud/mcp-gpt-image` profile. Its manifest installs `mcp-openai-pro` with `--profile gpt-image`; use the package version actually shown there.

Glama can ingest Registry and source-repository metadata, but that does not prove it has indexed this dedicated profile. Search Glama for [GPT Image](https://glama.ai/mcp/servers?query=GPT%20Image), verify the author is **AceDataCloud**, and inspect the advertised tools and package arguments. A dedicated GPT Image Glama listing and ordinary installation remain **unverified** as of 2026-10-19. Do not interpret a missing search result as permission to install an unrelated provider.

The existing [OpenAIMCP Glama page](https://glama.ai/mcp/servers/AceDataCloud/OpenAIMCP) and its remote connector describe the general server, which includes chat/audio/embedding and other image tools. They are not a dedicated GPT Image install. There is **no separate hosted GPT Image URL** in this release; do not invent one or point a profile-only configuration at `openai.mcp.acedata.cloud/mcp`.

This real **2026-10-17 Suno page** illustrates Glama's directory navigation only. It is not a GPT Image listing, authorization screen or successful image result. Glama may change its controls.

![Real Glama Suno listing used only as a directory navigation reference](images/glama-suno-20261017.jpg)

## 2. Obtain an application API Token

1. [Register/sign in to Ace Data Cloud](https://platform.acedata.cloud/?utm_source=glama&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_glama_signup), then open [Applications](https://platform.acedata.cloud/console/applications?utm_source=glama&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_glama_api_key).
2. Open **General application**, or choose **Initialize General Application** if it is absent. Check GPT Image model access, the chosen API, expiration, usage limit, current balance and price. No fixed trial allowance is promised.
3. Copy an existing API Key using **①**, or choose **② Manage Keys → Create** to create a separate `Glama GPT Image` key. Values in the source image are redacted.

![Real Ace Applications screenshot: copy an API Key or open Manage Keys](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

4. When using **Allowed APIs**, allow the image operation you actually need (`/openai/images/generations` or `/openai/images/edits`) and `/openai/tasks` to retrieve the same task. Creation and task-query permission are separate. Copy the token after creation.

![Real optional dedicated-key creation screen](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

These unchanged screenshots come from the [SunoDify source pinned at 8d3d0357](https://github.com/AceDataCloud/SunoDify/blob/8d3d03570e73324220f111f7fe343da0792a8071/README.md), visually checked 2026-10-18. The source example name `Dify tutorial` is not a required Glama name. They show Ace key acquisition, not Glama authorization. Use the raw application API Token; do not copy redaction blocks, prefix it with `Bearer ` in the environment variable, or substitute an account-management platform token.

## 3. Install the five-tool profile

A Glama catalog install is ready only when its **package** configuration supports the profile arguments and per-user environment variable below. If a dedicated profile record appears, check these exact fields before installing. The following local stdio configuration is also usable by compatible external clients; manually importing it is **not** evidence of a Glama catalog install:

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

`uvx` requires uv on the machine running the process. A Glama-hosted package deployment is a separate action: confirm the actual UI supports these arguments and secret environment storage, and check its terms or cost before deployment. This guide does not assume a new cloud deployment, accept its agreement, or claim that a signed-in package form has been verified.

Keep the token in that client's private credential/environment storage. Do not put it in a prompt, URL, public configuration or screenshot. The dedicated profile does not use a generic remote connector's OAuth configuration; using the generic URL would expose the wrong tool set.

## 4. Free check, then one deliberate generation

Read the connected server's tool list. It must contain the five `gpt_image_*` tools above and exclude general chat, audio, embeddings, DALL-E and Nano Banana. Call `gpt_image_list_models` with empty arguments; it reads static metadata without submitting generation. This proves loading, not the downstream credential, model availability or account balance.

Only after choosing an explicit GPT Image model and approving its [current price](https://platform.acedata.cloud/models?utm_source=glama&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_glama_first_run_price), call `gpt_image_generate` once with your prompt and selected model. Editing uses `gpt_image_edit` with the schema's ordered image URL list. Do not enable automatic paid retries. No paid generation was performed for this guide.

## 5. Query the original task and inspect the final image

Save the returned `task_id`. Call `gpt_image_get_task` with that same `id` until terminal success or failure; `gpt_image_list_tasks` looks up tasks using its advertised filter fields; use `gpt_image_get_task` for the original ID. A pending task, preview URL, accepted request or green client step is not a finished image. On terminal success, inspect the returned final media in the task response. On failure, stop polling and preserve its safe task/trace ID and error before considering a fresh submission. Never repeat generation merely to poll.

## Troubleshooting

| Symptom | Action |
|---|---|
| Dedicated entry missing in Glama | Search the exact profile name and check the official Registry. Downstream ingestion/claim is a separate review; do not call the generic OpenAI record a dedicated listing. |
| Unexpected chat/audio tools | Preserve `--profile gpt-image`; remove a mistaken generic remote configuration. |
| Unknown profile flag | Check the installed package version against the public manifest; an old package may predate the profile. |
| 401 / 403 | Check the raw application Token, model/API access, expiration, limits and balance. Do not bypass a moderation/access denial with a new key. |
| No model supplied | Choose a GPT Image model explicitly after reviewing price; there is no hidden fallback. |
| Pending / missing image | Query the original ID. Do not regenerate for progress. |
| 429 / timeout / failure | Reduce requests and inspect the original task; no automatic paid retry. |

[API reference](https://platform.acedata.cloud/documents/openai?utm_source=glama&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_glama_api_docs) · [Source/support](https://github.com/AceDataCloud/OpenAIMCP/issues).

## 中文操作指南

1. 搜索 Glama 的 **GPT Image** 并核对作者 AceDataCloud、独立五个 `gpt_image_*` 工具和 `--profile gpt-image` 参数。官方 MCP Registry 已有独立配置，不等于 Glama 已导入；截至2026-10-19普通 Glama 搜索、安装和授权仍未完成验收。现有 OpenAIMCP 页面是通用服务，不能冒充独立影像入口。
2. [注册或登录 Ace](https://platform.acedata.cloud/?utm_source=glama&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_glama_signup_zh) → [Applications／我的应用](https://platform.acedata.cloud/console/applications?utm_source=glama&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_glama_api_key_zh) → **General application／通用应用**。缺少时先初始化；核对模型/API权限、有效期、用量、余额和当前价格。
3. 用图中①复制已有Key，或② **Manage Keys → Create**建立专用Token。API限制要同时允许所需图片操作和`/openai/tasks`。图片已打码，原图Dify示例名不要求照抄；不要用平台管理Token代替应用API Token。
4. 包配置必须保留上方stdio命令的`--profile gpt-image`，原始Token放在私密`ACEDATACLOUD_API_TOKEN`环境变量中，不加Bearer。没有独立GPT Image远程URL；不能用genericOpenAI远程地址代替。Glama托管包的具体参数/密钥表单尚待真实登录核验，不虚构按钮或部署成功。
5. 先检查五工具并调用免费`gpt_image_list_models`；确认实际价格和预算后才提交一次生成/编辑，保存任务ID，之后只查同一ID到终态再展示最终图片。未跑收费示例，没有Glama终态、媒体或账单成功截图。

图源：真实Glama Suno入口图2026-10-17；Ace应用Key图来自固定SunoDify提交，2026-10-18核验、未重画。两者只作对应步骤参考，不证明GPT Image已在Glama上线。
