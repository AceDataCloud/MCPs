# GPT Image by Ace Data Cloud：中文安装与首用指南

[English](https://github.com/AceDataCloud/OpenAIMCP/blob/main/GPT_IMAGE.md)

本集成由 **Ace Data Cloud** 提供，基于现有 OpenAIMCP 包中的独立 GPT Image 配置。它只暴露生成、编辑、同任务查询、批量任务查询和本地模型说明五个工具；不包括聊天、音频、嵌入、DALL-E 或 Nano Banana，也不是 OpenAI 官方出品或背书。

更新日期：2026-10-18。独立配置已在本地源码和构建包中通过协议检查，但 [PR #983](https://github.com/AceDataCloud/MCPs/pull/983) 尚未合并，**新配置尚未公开发包或在 Registry 收录**。不要把旧线上 `mcp-openai-pro` 包或本地导入当成新的公开目录安装成功。

## 1. 官方安装入口与当前候选状态

候选条目为 [io.github.AceDataCloud/mcp-gpt-image](https://registry.modelcontextprotocol.io/?q=io.github.AceDataCloud%2Fmcp-gpt-image)。目前搜 `gpt-image` 没有 Ace 的独立条目；它仍需要源码合并、镜像同步、匹配包发行及官方元数据发布。官方目录按名称搜索，改通用 OpenAI 的描述不能补这个缺口。

发布后，在支持 MCP Registry 的客户端从该条目导入 **Packages**。目录会使用原有 `mcp-openai-pro` 包以及 **`--profile gpt-image`** 参数。若客户端忽略这个参数，就会变成通用 OpenAI 工具集，应停止并检查配置；不能当作正确安装。

本配置没有独立远程 URL。`https://openai.mcp.acedata.cloud/mcp` 是通用 OpenAI 远程服务，不是这个五工具配置。Registry 本身是目录，没有统一聊天、Token 填写或运行按钮；具体安装界面由客户端提供。

## 2. 注册/登录 Ace 并复制或创建专用 Token

1. 打开 [Ace Data Cloud → Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_readme_api_key)，注册或登录。
2. 进入 **General application**；尚未创建时选 **Initialize General Application**。复制应用卡片的 API Key，或打开 **Keys / Manage Keys → Create** 新建单独命名的集成凭据，例如 `GPT Image MCP`。
3. 核对过期时间、使用额度限制与 Allowed APIs。如果启用接口限制，允许本次图像生成/编辑及 `/openai/tasks` 查询；查询权限不授予生成权限。
4. 查看当前服务/模型权限、余额和[当前价格](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=gpt_image_mcp_readme_pricing)。不要从旧教程推断免费额度或价格，也不要把 `platform-...` 账户管理 Token 当成生成 Key。

![真实 Ace 应用 Key 界面，敏感内容已遮挡](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![真实 Ace 创建 Key 界面，可设置过期、额度和接口范围](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

原图来自固定版本 SunoDify 教程，图片仓库更新日期 **2026-10-09 Asia/Shanghai**，不是本次新建凭据实拍。创建框保留历史名称 `Dify tutorial`；这里只解释同一 Ace 平台流程，不伪称已经创建 GPT Image Key。密钥内容已遮挡；任何新截图也必须遮住 Key。

## 3. 客户端中的填写位置

目录支持客户端应读取 manifest 的包、版本、参数和环境变量。手动配置客户端只作为兼容路径，以下应写在其用户级 MCP 配置，不写进聊天正文：

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

仅在匹配新配置的包真实发布后使用；安装准确版本应以公开条目为准。将原始 Token 填进 `ACEDATACLOUD_API_TOKEN`，不加 `Bearer `。优先客户端安全凭据存储；用户级配置若含 Key 就是秘密，不能共享或提交。需要 `uv` 在 PATH 中，以及满足包要求的 Python。

该配置的客户端目录安装/填写 UI 还没有真实验收截图，本文不以假界面或旧客户端原图代替。当前只有本地协议执行证据，不能据此声称所有普通用户安装成功。

## 4. 先读取模型信息，再决定收费调用

连接后确认恰好五个工具：

- `gpt_image_generate`
- `gpt_image_edit`
- `gpt_image_get_task`
- `gpt_image_list_tasks`
- `gpt_image_list_models`

首先调用 `gpt_image_list_models`；它读取本地信息，不发起生成。正式生成前，用户必须明确选择当前允许的 GPT Image 模型，并确认价格/余额/预算。生成参数例子（**仅说明，不代表已经提交**）：

```json
{"prompt":"说明你希望得到的图片","model":"gpt-image-2","async":true}
```

编辑调用 `gpt_image_edit`，在 `image` 填按顺序排列的 URL 数组，保持基础图/参考图顺序。不要用未批准模型或自动fallback；此配置不改价格。本文更新没有发起付费生成，模拟测试不构成真实媒体或账单证据。

## 5. 用原任务 ID 等待终态和读取图片

保存生成或编辑响应的 `task_id`，调用 `gpt_image_get_task` 时填入参数 **`id`**（注意这与四个其他媒体服务的 `task_id` 参数不同）：

```json
{"id":"ORIGINAL_TASK_ID"}
```

继续查同一 ID，直到出现成功/失败终态。`pending`、空媒体或客户端绿色执行提示都不是完成；读取返回 `response` 中的媒体或错误，确认 URL 可访问。不要为了“刷新”重跑生成，否则可能创建新任务并收费。已有合法成功任务也只查询同一 ID。

尚无本配置从官方目录安装→收费提交→终态图片→唯一 Credits 账单的完整实测，因此不展示别的宿主结果图充数，不声称已带来注册或营收。

## 6. 常见问题

| 现象 | 排查 |
|---|---|
| 官方目录搜不到 Ace GPT Image | 新条目仍是候选，等匹配包与元数据正式发布；不要把手动导入当官方收录。 |
| `--profile` 不认识 | 旧包不含新配置，核实际安装版本与发布状态。 |
| 出现聊天/音频或15个通用工具 | 参数没生效或误连通用remote；应是五工具本地配置。 |
| 模型缺失/不支持 | 从 `gpt_image_list_models` 选受限枚举，明确填模型，核账户权限和当前价。 |
| 401/403 | 核原始Token、有效期、应用范围、生成/任务查询接口限制；不盲目新建Key。 |
| pending或无图 | 继续查原始 `id`，不要再发生成。 |
| 文件CDN下载失败 | 保留包版本和网络日志，不改TLS验证，不冒称正常安装已完成。 |
| 5xx/任务失败 | 带task/trace ID排错，不发Key；检查原任务再决定是否重试。 |

## 证据与来源

本指南使用真实打码平台Key原图；没有新客户端安装/调用结果截图。官方Schema允许独立包参数，但元数据校验通过不等于官方已发布或精选。当前受限配置的工具测试、本地wheel会话与CI只是实现验证。
