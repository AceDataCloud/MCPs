# OpenAIMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-openai -->

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for OpenAI API access using [AceDataCloud](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_readme_platform).

Interact with OpenAI models for chat completions, image generation, text embeddings, and more — directly from Claude, VS Code, or any MCP-compatible client.

The AceDataCloud distribution is `mcp-openai-pro`. The unrelated
`mcp-openai` package on PyPI is not maintained by AceDataCloud. Update existing
`uvx` configurations to the new package name; the hosted MCP URL is unchanged.

## Features

- **Chat Completions** — Access GPT-4, GPT-4o, GPT-5, o1, o3, o4-mini, and many more models
- **Responses API** — Extended model variant support including dated releases and search-preview models
- **Image Generation** — Create images with gpt-image-1, gpt-image-2, GPT Image 2.5 Flare/Sunburst standard or official variants, dall-e-3, and nano-banana models
- **Image Editing** — Modify existing images with AI
- **Text Embeddings** — Generate vector representations with text-embedding-3 models
- **Audio** — Convert text to speech and transcribe audio with whisper-1 or gpt-transcribe

## Connect: hosted OAuth, API token, or local stdio

The hosted endpoint is `https://openai.mcp.acedata.cloud/mcp`. Choose one route for the MCP client:

| Route | When to use it | Credential setup |
|---|---|---|
| Hosted OAuth | The client supports remote MCP OAuth | Add only the URL, then sign in to AceDataCloud and approve access. No token needs to be pasted into client configuration. |
| Hosted API token | The client cannot finish OAuth, or you need an explicit integration credential | Send an AceDataCloud API token in the `Authorization: Bearer …` header. Keep it in a local secret store or environment variable. |
| Local stdio | The client runs a local MCP process | Install `mcp-openai-pro` and pass `ACEDATACLOUD_API_TOKEN` to that process. It still calls the AceDataCloud API. |

The hosted service advertises OAuth metadata and Dynamic Client Registration (DCR). **DCR registers the client application; it is not an API key.** OAuth signs you in and the client sends the resulting Bearer token; it may reuse or create an API credential for the account. Browser sign-in still requires an AceDataCloud account. The hosted service can be metered: review [current service documentation](https://platform.acedata.cloud/documents/openai?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_readme_quick_start) and displayed pricing before a real operation. Do not configure both an OAuth login and a fixed `Authorization` header for the same server.

### Hosted OAuth examples

- **Claude and Claude Desktop chat:** Add a remote custom connector in `Customize → Connectors → Add custom connector`, enter `https://openai.mcp.acedata.cloud/mcp`, select sign-in, and choose **Register automatically** if Claude asks how to register its OAuth client. Complete consent. Claude Desktop's local `claude_desktop_config.json` is a separate setup. [Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp).
- **Claude Code:** `claude mcp add --transport http --scope user openai https://openai.mcp.acedata.cloud/mcp`, then `claude mcp login openai`. Check `/mcp`. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp).
- **Cursor:** Add a remote server with only `https://openai.mcp.acedata.cloud/mcp`. For a project, merge the entry below into `<project>/.cursor/mcp.json`; for personal use, use `~/.cursor/mcp.json`. [Cursor MCP guide](https://cursor.com/docs/mcp).
- **VS Code / Copilot:** Run **MCP: Add Server**, select HTTP, enter `https://openai.mcp.acedata.cloud/mcp`, then finish the browser sign-in. New portable workspace configs use `<project>/.mcp.json`; the VS Code-specific format below uses `<project>/.vscode/mcp.json` or the user profile. Check **MCP: List Servers**. [VS Code MCP setup](https://code.visualstudio.com/docs/agent-customization/mcp-servers).
- **Codex:** `codex mcp add openai --url https://openai.mcp.acedata.cloud/mcp`, then `codex mcp login openai`. Its user settings are in `~/.codex/config.toml`. [Official Codex MCP guide](https://developers.openai.com/codex/mcp/).

Cursor project config (OAuth):

```json
{
  "mcpServers": {
    "openai": {"url": "https://openai.mcp.acedata.cloud/mcp"}
  }
}
```

VS Code-specific workspace config (OAuth):

```json
{
  "servers": {
    "openai": {"type": "http", "url": "https://openai.mcp.acedata.cloud/mcp"}
  }
}
```

### Hosted API token

Sign in at [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_readme_platform), open the [service page](https://platform.acedata.cloud/documents/openai?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_readme_quick_start), and obtain an API credential. A fixed Bearer header is useful when your client lacks OAuth; an invalid header does not fall back to OAuth in Claude Code. The header value is sensitive, so keep it out of committed files and screenshots.

For Claude Code, the shell expands the token when you add the server; treat the saved user MCP config as a secret:

```bash
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
claude mcp add --transport http --scope user openai https://openai.mcp.acedata.cloud/mcp \
  --header "Authorization: Bearer $ACEDATACLOUD_API_TOKEN"
```

For a Claude Code project config, put a variable reference in `<project>/.mcp.json` and set that variable in the environment that launches Claude Code:

```json
{
  "mcpServers": {
    "openai": {
      "type": "http",
      "url": "https://openai.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

Cursor uses a different environment-variable syntax in `~/.cursor/mcp.json` or an uncommitted project config:

```json
{
  "mcpServers": {
    "openai": {
      "url": "https://openai.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${env:ACEDATACLOUD_API_TOKEN}"}
    }
  }
}
```

In VS Code, run **MCP: Open User Configuration** and merge this server plus its masked input; `${input:...}` is for VS Code's user/workspace format and is not portable to the Agent Host `.mcp.json` format:

```json
{
  "inputs": [
    {"id": "acedata-openai-token", "type": "promptString", "description": "AceDataCloud API token", "password": true}
  ],
  "servers": {
    "openai": {
      "type": "http",
      "url": "https://openai.mcp.acedata.cloud/mcp",
      "headers": {"Authorization": "Bearer ${input:acedata-openai-token}"}
    }
  }
}
```

For **Cline**, use its MCP configuration UI or CLI file `~/.cline/data/settings/cline_mcp_settings.json`; its remote transport value is `streamableHttp`. For **JetBrains AI Assistant**, add a remote URL from **Settings → Tools → AI Assistant → Model Context Protocol (MCP)**. For **Zed**, use a `context_servers` entry with the URL only for OAuth or add a local Bearer header. These clients have different configuration schemas; follow their current UI rather than copying another client's JSON. [Cline](https://docs.cline.bot/mcp/mcp-overview) · [JetBrains](https://www.jetbrains.com/help/ai-assistant/mcp.html) · [Zed](https://zed.dev/docs/ai/mcp).

### Local stdio

Install the package and give the local process an API token:

```bash
python -m pip install mcp-openai-pro
export ACEDATACLOUD_API_TOKEN='YOUR_API_TOKEN'
mcp-openai-pro
```

For Claude Desktop local MCP, merge this entry into the file opened by its developer settings (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS). `uvx` requires [uv](https://docs.astral.sh/uv/) on `PATH`:

```json
{
  "mcpServers": {
    "openai": {
      "command": "uvx",
      "args": ["mcp-openai-pro"],
      "env": {"ACEDATACLOUD_API_TOKEN": "YOUR_API_TOKEN"}
    }
  }
}
```

Keep this user-level file private. Self-hosted HTTP uses `mcp-openai-pro --transport http --port 8000`; expose it only with suitable network and TLS controls. Local execution still calls the AceDataCloud API.

### Check before using the service

1. `https://openai.mcp.acedata.cloud/health` returning `{"status":"ok"}` checks endpoint reachability only.
2. Confirm that the MCP client loads tools. `openai_get_usage_guide` is a reference tool; it does not verify downstream API access or balance.
3. If you need a full API check, call `openai_generate_image` with your own valid input after reviewing [current service documentation](https://platform.acedata.cloud/documents/openai?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_readme_quick_start) and displayed pricing. If the result contains a task ID, call `openai_get_task` on that same ID until terminal success or failure. Do not resubmit the operation just to check progress.

For **401**, check which auth route the client used and whether the token or OAuth session is valid. A **403** may mean an account permission or content moderation failure; read the returned error. Insufficient balance and downstream service failures need their own diagnosis. A listed tool or submitted task does not prove a successful result.

## Available Tools

| Tool | Description |
|------|-------------|
| `openai_chat_completion` | Create chat completions using OpenAI models |
| `openai_create_response` | Create responses using the Responses API |
| `openai_generate_image` | Generate images from text descriptions |
| `openai_edit_image` | Edit existing images with AI |
| `openai_create_embedding` | Create text embedding vectors |
| `openai_text_to_speech` | Convert text to spoken audio |
| `openai_transcribe_audio` | Transcribe audio from a URL |
| `openai_list_chat_models` | List available chat/completion models |
| `openai_list_image_models` | List available image models |
| `openai_list_embedding_models` | List available embedding models |
| `openai_get_usage_guide` | Get comprehensive usage guide |

## Supported Models

### Chat Completion Models
- **GPT-5 Series**: gpt-5.5, gpt-5.5-pro, gpt-5.4, gpt-5.4-pro, gpt-5.2, gpt-5.1, gpt-5, gpt-5-mini, gpt-5-nano
- **GPT-4 Series**: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, gpt-4o, gpt-4o-mini, gpt-4
- **Reasoning**: o4-mini, o3, o3-mini, o3-pro, o1, o1-mini, o1-pro

### Image Models
- gpt-image-1, gpt-image-1.5, gpt-image-2, gpt-image-2:official, gpt-image-2.5-flare, gpt-image-2.5-flare:official, gpt-image-2.5-sunburst, gpt-image-2.5-sunburst:official, dall-e-3, dall-e-2, nano-banana, nano-banana-2, nano-banana-pro
- GPT Image `:official` variants settle from actual text-input, image-input, and image-output tokens.

### Embedding Models
- text-embedding-3-small, text-embedding-3-large
- `text-embedding-ada-002` is retired. Re-embed documents and rebuild existing indexes
  when migrating; do not mix old-model vectors with text-embedding-3 vectors.

### Audio Transcription Models
- whisper-1, gpt-transcribe

## Usage Examples

### Chat Completion

```
openai_chat_completion(
    messages=[{"role": "user", "content": "Explain quantum computing in simple terms"}],
    model="gpt-4.1"
)
```

### Image Generation

```
openai_generate_image(
    prompt="A serene Japanese garden with cherry blossoms at sunset, photorealistic",
    model="gpt-image-1",
    size="1024x1024"
)
```

### Text Embeddings

```
openai_create_embedding(
    input="The quick brown fox jumps over the lazy dog",
    model="text-embedding-3-small"
)
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `ACEDATACLOUD_API_TOKEN` | API token (required) | — |
| `ACEDATACLOUD_API_BASE_URL` | API base URL | `https://api.acedata.cloud` |
| `OPENAI_REQUEST_TIMEOUT` | Request timeout in seconds | `60` |
| `MCP_SERVER_NAME` | MCP server name | `openai` |
| `LOG_LEVEL` | Logging level | `INFO` |

## Development

```bash
# Install dependencies
pip install -e ".[dev,test]"

# Run tests
pytest

# Run linter
ruff check .
```

## API Reference

- [AceDataCloud Platform](https://platform.acedata.cloud?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_readme_platform)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## Documentation

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/openai?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=openai_mcp_readme_quick_start)

## License

MIT
