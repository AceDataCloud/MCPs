# Use Ace Data Cloud tools in Zed

Connect Zed Agent to the media and search tools you need for a project. For example, look up an existing music or video task to recover a published asset URL, or use Google Search to gather sources for a design note.

| | Service | Settings key | Tools |
| --- | --- | --- | --- |
| <img src="https://cdn.acedata.cloud/acemusic-icon-52deddfc87b9.png" width="28" alt=""> | ACE Music | `ace-music` | Music generation and recovery of earlier tasks. |
| <img src="https://cdn.acedata.cloud/l3ffw7.jpg" width="28" alt=""> | Suno | `ace-suno` | Music generation and audio task lookup. |
| <img src="https://cdn.acedata.cloud/859plc.jpg" width="28" alt=""> | Nano Banana | `ace-nano-banana` | Image generation and editing. |
| <img src="https://raw.githubusercontent.com/AceDataCloud/GPTImageDify/main/_assets/icon.png" width="28" alt=""> | GPT Image | `ace-gpt-image` | Image generation and editing. The hosted OpenAI server also exposes its other tools. |
| <img src="https://cdn.acedata.cloud/9egrbn.png" width="28" alt=""> | Seedream | `ace-seedream` | Image editing and generation. |
| <img src="https://cdn.acedata.cloud/9q90dl.png" width="28" alt=""> | Seedance | `ace-seedance` | Video generation and task lookup. |
| <img src="https://cdn.acedata.cloud/8nxyy9.jpg" width="28" alt=""> | Veo | `ace-veo` | Video generation and task lookup. |
| <img src="https://cdn.acedata.cloud/27e11e555d.png" width="28" alt=""> | Google Search | `ace-google-search` | Search and structured results. |

## Connect a hosted server

1. Open **Settings → AI → MCP Servers** in Zed. Choose **Add Server → Add Remote Server**.
2. Copy the `url` for the service you want from [the hosted examples](remote.settings.json). Give it the corresponding settings key. You can also merge that one entry into `context_servers` in your existing Zed settings.
3. Follow the service's OAuth prompt. If you already have an application key for that service, you can instead supply `Authorization` with the value `Bearer YOUR_SERVICE_KEY` in the remote server's headers. Keep keys in your personal settings.
4. Check for the **Server is active** indicator and inspect the server's tools. Use an existing task ID with a task lookup tool to retrieve an earlier result. Starting a generation or running a search requires the matching application and may spend credits.

The hosted OpenAI endpoint exposes its full tool list. For a toolset restricted to GPT Image, use the local profile below.

## Run a published package locally

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and copy the entry for one service from [the local examples](local.settings.json) into your Zed `context_servers`. Set `ACEDATACLOUD_API_TOKEN` in the environment used to launch Zed, or add it to the selected server's `env` object in your personal settings. Use a key that has access to that service. `ace-gpt-image` starts the published OpenAI package with `--profile gpt-image`, exposing only the image tools. If `uvx` is not on Zed's PATH, use its absolute path for `command`.

[Manage service applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Service pricing](https://platform.acedata.cloud/models?utm_source=github&utm_medium=referral&utm_campaign=evergreen) · [Zed MCP settings](https://zed.dev/docs/ai/mcp#as-custom-servers)
