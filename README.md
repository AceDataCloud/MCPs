# AceDataCloud MCPs

Monorepo for all AceDataCloud MCP (Model Context Protocol) servers.

## Servers

| Directory | Standalone Repo | Description |
|---|---|---|
| `luma/` | [LumaMCP](https://github.com/AceDataCloud/LumaMCP) | AI video generation (Luma Dream Machine) |
| `suno/` | [SunoMCP](https://github.com/AceDataCloud/SunoMCP) | AI music generation |
| `midjourney/` | [MidjourneyMCP](https://github.com/AceDataCloud/MidjourneyMCP) | AI image generation |
| `flux/` | [FluxMCP](https://github.com/AceDataCloud/FluxMCP) | AI image generation (Flux models) |
| `sora/` | [SoraMCP](https://github.com/AceDataCloud/SoraMCP) | AI video generation (OpenAI Sora) |
| `veo/` | [VeoMCP](https://github.com/AceDataCloud/VeoMCP) | AI video generation (Google Veo) |
| `serp/` | [SerpMCP](https://github.com/AceDataCloud/SerpMCP) | Web search |
| `nanobanana/` | [NanoBananaMCP](https://github.com/AceDataCloud/NanoBananaMCP) | AI image generation (Gemini-based) |
| `seedance/` | [SeedanceMCP](https://github.com/AceDataCloud/SeedanceMCP) | AI video generation (Seedance) |
| `seedream/` | [SeedreamMCP](https://github.com/AceDataCloud/SeedreamMCP) | AI image generation (Seedream) |
| `shorturl/` | [ShortURLMCP](https://github.com/AceDataCloud/ShortURLMCP) | URL shortener |

## How It Works

This is the source-of-truth monorepo. Changes pushed to `main` are automatically synced to the standalone repos via GitHub Actions.

The mapping between subdirectories and standalone repos is defined in [`sync.yaml`](sync.yaml).

**Do not edit standalone repos directly** — all changes should be made here.
