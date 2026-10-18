# goose 的 Suno by Ace Data Cloud 插件

这是 **Ace Data Cloud 维护的 Suno 独立集成**，不是 Suno 品牌官方插件，也未内置于 goose。底层复用公开 `mcp-suno==2026.10.12.1`；不会安装其它媒体服务。默认分支尚未同步本 PR 前，以下安装入口是待发布候选，不能宣称已上线。

## 1. 安装

需要 goose 1.55.0+、Python 与 uv。使用 [goose 官方原生插件命令](https://goose-docs.ai/docs/guides/context-engineering/plugins/#install-a-plugin)：

```sh
goose plugin install https://github.com/AceDataCloud/SunoMCP.git
```

新会话自动加载 MCP 和 `suno-by-acedatacloud:suno-music` 工作流，省去手写 MCP 地址/JSON。不要同时保留同服务的重复手动配置。

## 2. 获取服务 Token

先[注册或登录 Ace → Applications](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_goose_api_key)，打开 **General application**；没有通用应用时先初始化。检查 Suno 权限、余额和[当前价格](https://platform.acedata.cloud/models?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=suno_goose_pricing)。复制卡片 API Key，或 **Manage Keys → Create** 创建专用 `goose Suno` Key。限制 Allowed APIs 时需同时放行 `/suno/audios, /suno/tasks` 等本次流程会用的接口。

![真实 Ace 页面：复制已有 Key 或管理 Key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/get-api-key-en.png)

![真实 Ace 页面：创建专用 Key](https://raw.githubusercontent.com/AceDataCloud/SunoDify/8d3d03570e73324220f111f7fe343da0792a8071/_assets/tutorial/create-api-key-en.png)

图片来自 SunoDify 固定提交 `8d3d035` 的已脱敏真实教程，2026-10-18 引用，展示共同账户界面，不是本插件生成证据。复制原始 Token 字符串，不加 `Bearer `；`platform-...` 管理 Token 不适用。不要在聊天、共享配置、截图或 Git 中写真实凭据。

## 3. 在 goose 中使用

在启动 goose 的进程环境设置 `ACEDATACLOUD_API_TOKEN`，然后重启/新建会话。可在 Bash 终端安全输入：

```sh
read -r -s -p 'Ace service API Token: ' ACEDATACLOUD_API_TOKEN
printf '\n'
export ACEDATACLOUD_API_TOKEN
goose session
```

已经启动的桌面进程不会自动继承后开的终端变量；本插件不虚构 Key 输入弹窗。先只调用 `suno_list_models` 做免费静态参考检查。

![goose 官方原始工具列表参考](https://raw.githubusercontent.com/aaif-goose/goose/cd643d2126fffab4c6a6186905211ba868d6a657/documentation/docs/assets/guides/custom-extension-tools.png)

这张是官方文档的 wiki/developer 示例，不是 Ace 实测；原拍摄日期/客户端版本未标注，引用的是 1.54.0 文档快照。

明确需要且授权费用后，使用 `suno_generate_music`, `suno_generate_custom_music` 生成/编辑，保存返回的 task ID，用 `suno_get_task` 查询同一个 ID 到成功/失败。pending、预览或工具卡片不代表完成；用真实返回媒体 URL 查看结果，不为轮询重复生成。Goose 聊天模型费用另计。

认证失败时核完整 Key、服务权限、过期、Allowed APIs；余额不足/限流保持错误含义。无工具时检查 uv/PyPI 网络、进程环境与新会话；不要更改全局索引或扩权来绕过问题。完整设置与限制见 [English guide](README.md)。
