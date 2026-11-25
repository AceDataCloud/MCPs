# ACE Music MCP 中文指南

在支持 MCP 的客户端添加远程 Streamable HTTP 服务器 `https://acemusic.mcp.acedata.cloud/mcp`。使用客户端的 OAuth 登录，或在私有设置中配置 `Authorization: Bearer <应用密钥>`。[申请密钥](https://platform.acedata.cloud/console/applications) · [VS Code 专用扩展](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-acemusic)

本地 stdio 模式使用命令 `uvx`，参数为 `mcp-acemusic`，在客户端的私有环境中设置 `ACEDATACLOUD_API_TOKEN`。连接后先调用 `acemusic_list_models` 或 `acemusic_get_capabilities`。这些操作可以检查连接，无须创建歌曲。

创作歌曲时可提供提示词，或填写自定义歌词、风格和标题。导入参考 MP3、翻唱、两首参考融合及歌词创作分别有对应工具。提交成功后保存任务 ID，用 `acemusic_get_task` 查询到终态。翻唱和融合的参考使用个人音轨 ID；查询进度使用任务 ID。遇到部分失败时，以任务返回的状态和可用音轨为准。

[全部生态入口](../ECOSYSTEM.md) · [API 与 OpenAPI](https://github.com/AceDataCloud/ACEMusicAPI) · [中文 API 指南](https://docs.acedata.cloud/zh-Hans/guides/acemusic/acemusic_audios.md)
