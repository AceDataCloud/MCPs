# Producer MCP

AI music with Producer (FUZZ) — songs, lyrics, covers, vocal/instrument swap, section replace.

[![VS Code Marketplace](https://img.shields.io/visual-studio-marketplace/v/acedatacloud.mcp-producer?label=VS%20Code)](https://marketplace.visualstudio.com/items?itemName=acedatacloud.mcp-producer) [![PyPI](https://img.shields.io/pypi/v/mcp-producer.svg?label=PyPI)](https://pypi.org/project/mcp-producer/) [![Hosted MCP](https://img.shields.io/badge/hosted-mcp-blue)](https://producer.mcp.acedata.cloud/mcp)

Music generation, lyric writing, song extension, covers, vocal/instrumental swap, section replace, and reference audio upload — using the Producer (FUZZ) models.

This extension registers the **producer** MCP server with VS Code so GitHub
Copilot and any other agent that speaks the [Model Context Protocol](https://modelcontextprotocol.io/)
can call it directly from chat.

---

## Quick Start

1. **Install this extension.** VS Code registers the `producer` MCP server automatically.
2. **Get an API key** from [Ace Data Cloud](https://platform.acedata.cloud/console/applications) (Applications → API Key). New accounts include free trial credit.
3. **Open Copilot Chat** in agent mode and ask for a music task — the extension prompts for the API key the first time and stores it in the OS keychain via VS Code's `SecretStorage`.

You can rotate or remove the API key any time from the command palette:

- **Producer MCP: Set Ace Data Cloud API Key**
- **Producer MCP: Clear Ace Data Cloud API Key**

> The default config talks to the **hosted streamable-HTTP endpoint** at
> `https://producer.mcp.acedata.cloud/mcp` — no Python, no `uvx`, no local install needed.

### Example prompts

- "Generate a Producer track: dreamy synthwave instrumental, 90 BPM, A minor."
- "Replace seconds 30–45 of song <id> with a guitar solo."

---

## Tool Reference

**18 tools** available via this server.

| Tool | Description |
| --- | --- |
| `producer_generate_music` | Generate AI music from a text prompt. |
| `producer_generate_custom_music` | Generate music with custom lyrics, title, and style. |
| `producer_extend_music` | Extend an existing song from a specific timestamp. |
| `producer_cover_music` | Create a cover/remix version in a different style. |
| `producer_variation_music` | Create a variation of an existing song. |
| `producer_swap_vocals` | Swap vocals between two songs. |
| `producer_swap_instrumentals` | Swap instrumentals between two songs. |
| `producer_replace_section` | Replace a specific time range with new content. |
| `producer_stems_music` | Separate a song into vocal and instrumental stems. |
| `producer_generate_lyrics` | Generate structured song lyrics from a prompt. |
| `producer_upload_audio` | Upload external audio for processing. |
| `producer_generate_video` | Generate a music video for a song. |
| `producer_generate_wav` | Get lossless WAV format of a song. |
| `producer_get_task` | Query the status of a generation task. |
| `producer_get_tasks_batch` | Query multiple generation tasks at once. |
| `producer_list_models` | List all available FUZZ models. |
| `producer_list_actions` | List all available actions and tools. |
| `producer_get_lyric_format_guide` | Get lyrics formatting guide. |

## Supported Models

`fuzz-1.0`, `fuzz-1.1`, `fuzz-1.5`, `fuzz-2.0`, `fuzz-2.5`, `fuzz-3.0`, `fuzz-3.5`, `fuzz-4.0`

## Pricing

From $0.05 per song. Free trial credit on sign-up. See full pricing at [https://docs.acedata.cloud](https://docs.acedata.cloud).

---

## Configuration

This extension implements the `mcpServerDefinitionProviders` contribution point
and registers a single hosted server with VS Code:

```text
Provider id : acedatacloud.producer
Server label: Producer MCP
Server URL  : https://producer.mcp.acedata.cloud/mcp
Transport   : Streamable HTTP
Auth        : Bearer API key from VS Code SecretStorage (or $ACEDATACLOUD_API_TOKEN)
```

You don't need to edit `mcp.json` — the extension handles registration and
token handling automatically. If you'd rather configure things by hand, the
sections below show equivalent `mcp.json` snippets you can use **instead of**
this extension.

### Alternative: manual `mcp.json` (hosted)

```jsonc
{
  "servers": {
    "producer": {
      "type": "http",
      "url": "https://producer.mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer ${input:acedatacloud_api_token}" }
    }
  },
  "inputs": [
    {
      "type": "promptString",
      "id": "acedatacloud_api_token",
    "description": "Ace Data Cloud API key",
      "password": true
    }
  ]
}
```

### Alternative: local stdio (no network roundtrip)

For offline dev, air-gapped environments, or pinning to a specific PyPI
version, install [`uv`](https://docs.astral.sh/uv/) and use:

```jsonc
{
  "servers": {
    "producer": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-producer"],
      "env": { "ACEDATACLOUD_API_TOKEN": "${input:acedatacloud_api_token}" }
    }
  }
}
```

`uvx` will download and run the latest [`mcp-producer`](https://pypi.org/project/mcp-producer/) on demand.

---

## Links

- **Hosted endpoint:** https://producer.mcp.acedata.cloud/mcp
- **PyPI package:** [`mcp-producer`](https://pypi.org/project/mcp-producer/)
- **Source repository:** https://github.com/AceDataCloud/ProducerMCP
- **Ace Data Cloud platform:** https://platform.acedata.cloud
- **MCP documentation:** https://docs.acedata.cloud

## License

MIT — see [LICENSE](LICENSE).
