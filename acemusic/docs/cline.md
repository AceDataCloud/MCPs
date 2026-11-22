# ACE Music in Cline

Add the hosted server from Cline's MCP settings or CLI:

```sh
cline mcp add ace-music https://acemusic.mcp.acedata.cloud/mcp --transport http --yes
```

Complete the client's OAuth sign-in, or configure a private Bearer header with an [application key](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_cline_api_key). List available tools and run `acemusic_list_models` for a free check. Keep the original task ID when requesting songs.

## 中文

在 Cline 的 MCP 设置添加上面的 HTTPS 地址并登录。先查询模型确认连接；创建歌曲后使用原任务 ID 查询结果。
