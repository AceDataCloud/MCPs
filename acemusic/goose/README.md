# ACE Music for goose

Install with `goose plugin install https://github.com/AceDataCloud/AceMusicMCP.git` after the standalone repository contains `.goose-plugin/plugin.json`, or install the checked-out ACE Music plugin directory from source. The plugin loads the pinned MCP with `uvx` and the bundled ACE Music Skill. Store your [application key](https://platform.acedata.cloud/console/applications?utm_source=opensource&utm_medium=referral&utm_campaign=evergreen) in the private `ACEDATACLOUD_API_TOKEN` environment variable before starting goose. Start a new session and ask it to list ACE Music models. To resume a song, pass the original task ID to `acemusic_get_task`.

[中文](README_zh_Hans.md) · [goose plugins](https://goose-docs.ai/docs/guides/context-engineering/plugins/#install-a-plugin)
