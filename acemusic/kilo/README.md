# ACE Music in Kilo Code

In the MCP settings add a remote Streamable HTTP server at `https://acemusic.mcp.acedata.cloud/mcp`. Use the client sign-in flow or supply a private Bearer header with your [application key](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_kilo_api_key). A local alternative uses command `uvx`, arguments `--from mcp-acemusic==2026.11.18.0 mcp-acemusic`, and private environment variable `ACEDATACLOUD_API_TOKEN`. Start with `acemusic_list_models`. [中文](README_zh_Hans.md)
