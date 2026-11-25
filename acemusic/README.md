# ACE Music MCP

[![ACE Music MCP on Glama](https://glama.ai/mcp/servers/AceDataCloud/AceMusicMCP/badges/score.svg)](https://glama.ai/mcp/servers/AceDataCloud/AceMusicMCP)

[中文安装指南](https://github.com/AceDataCloud/AceMusicMCP/blob/main/readme/README_zh_Hans.md) · [Ecosystem directory](https://github.com/AceDataCloud/AceMusicMCP/blob/main/ECOSYSTEM.md) · [Glama](https://github.com/AceDataCloud/AceMusicMCP/blob/main/readme/GLAMA.md)

Create songs from an idea or custom lyrics, import reference audio, cover a track, blend two tracks, and retrieve the original task through Ace Data Cloud.

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/mcp-acemusic?utm_source=github&utm_medium=referral&utm_campaign=evergreen)

## Connect to ACE Music

- **VS Code** installs the [ACE Music extension](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-acemusic), which registers the hosted server.
- **Remote MCP clients** use the Streamable HTTP URL `https://acemusic.mcp.acedata.cloud/mcp`. Choose the client's OAuth sign-in flow or configure a Bearer application API key in its private credential settings. The [server card](https://acemusic.mcp.acedata.cloud/.well-known/mcp/server-card.json) lists the available tools.
- **Local stdio clients** launch the [published Python package](https://pypi.org/project/mcp-acemusic/) with command `uvx` and argument `mcp-acemusic`. Supply `ACEDATACLOUD_API_TOKEN` through the client's private environment settings.

Get an application API key in [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen). A general application with ACE Music access or a dedicated ACE Music application can run the tools. For a first read-only check, list the models or retrieve an existing task. To add the companion instructions to an agent, install the [ACE Music Skill](https://skills.sh/acedatacloud/skills/ace-music).

## Other integrations

[REST API, OpenAPI and examples](https://github.com/AceDataCloud/ACEMusicAPI) · [CLI](https://github.com/AceDataCloud/AceMusicCli) · [Python, TypeScript and Go SDKs](https://github.com/AceDataCloud/SDK) · [n8n community node](https://github.com/AceDataCloud/ACEMusicN8N)

[goose plugin](https://github.com/AceDataCloud/AceMusicMCP/blob/main/goose/README.md) · [Cline](https://github.com/AceDataCloud/AceMusicMCP/blob/main/docs/cline.md) · [Kilo Code](https://github.com/AceDataCloud/AceMusicMCP/blob/main/kilo/README.md) · [LobeHub](https://github.com/AceDataCloud/AceMusicMCP/blob/main/lobehub/README.md)

## Tools

| Tool | Purpose |
| --- | --- |
| `acemusic_generate_music` | One paid idea-to-song submission |
| `acemusic_generate_custom_music` | One paid submission with lyrics, style and title |
| `acemusic_upload_audio` | Separate priced single-track import from a public HTTPS MP3 URL |
| `acemusic_cover_audio` | One paid cover submission using an owned platform audio ID |
| `acemusic_mashup_audio` | One paid submission using exactly two compatible owned platform audio IDs |
| `acemusic_generate_lyrics` | Separately priced title/lyrics assistant |
| `acemusic_get_task` | Free authenticated lookup of the original task |
| `acemusic_get_tasks_batch` | Query up to 50 original tasks |
| `acemusic_list_tasks` | Paginated caller history |
| `acemusic_list_models` | Local model discovery |
| `acemusic_get_capabilities` | Supported workflows and recovery boundaries |

Models: `acemusic-v1.1` (default), `acemusic-v1`. A music task targets two MP3 candidates. Use lyrics section markers such as `[Verse]` and `[Chorus]`; the platform request field is `lyric`, not `lyrics`.

Save `task_id` immediately. Poll the same task every 10 seconds, inspecting its persisted `response` and group state. Partial failure is terminal and may include one playable candidate. A nonempty URL or a task ID alone does not mean full success. A client timeout must preserve the task identity for recovery rather than triggering another paid generation. If submission times out before a task ID arrives, reconcile the original request.

Cover and mashup require `acemusic-v1.1`, supplied lyrics/style and compatible caller-owned platform audio IDs. `audio_influence` accepts 1–100 (default 60); title is optional for these actions. Upload is explicit and separately priced, with one delivered track. It accepts a public HTTPS MP3 URL and an optional owned audio ID anchor; it never creates a cover implicitly. Continuation, stems, voice cloning, WAV, MIDI and video export remain unsupported. Check [current pricing](https://platform.acedata.cloud/services/024e09b4-52cf-5e98-a91a-efedf43104c4?utm_source=github&utm_medium=referral&utm_campaign=evergreen) before submitting; task lookup is free and still requires authorization.

## Development and deployment

Run `ruff check .`, `ruff format --check .`, `mypy core tools main.py`, `pytest`, and `python -m build`. Tests mock HTTP and do not spend account credit.

`deploy/production` targets the shared `nginx-router` ingress. Provision `mcp-acemusic-oauth-state` with `state_key`, the shared OAuth Redis secret, DNS/TLS and package/image publication before enabling the hosted entry. `deploy/run.sh` uses the repository's normal release mechanism.

<!-- mcp-name: io.github.AceDataCloud/mcp-acemusic -->


The official ACE Music icon comes from the immutable CDN URL and SHA256 in
`brand-assets.json`. VS Code and JetBrains builds download and verify that asset
before packaging; generated icon files are ignored and are not source assets.
