# AceDataCloud MCPs

Monorepo for all AceDataCloud MCP (Model Context Protocol) servers.

## Servers

| Directory | Standalone Repo | PyPI Package | Category |
|---|---|---|---|
| `flux/` | [FluxMCP](https://github.com/AceDataCloud/FluxMCP) | [mcp-flux-pro](https://pypi.org/project/mcp-flux-pro/) | Image |
| `hailuo/` | [HailuoMCP](https://github.com/AceDataCloud/HailuoMCP) | [mcp-hailuo](https://pypi.org/project/mcp-hailuo/) | Video |
| `kling/` | [KlingMCP](https://github.com/AceDataCloud/KlingMCP) | [mcp-kling](https://pypi.org/project/mcp-kling/) | Video |
| `luma/` | [LumaMCP](https://github.com/AceDataCloud/LumaMCP) | [mcp-luma](https://pypi.org/project/mcp-luma/) | Video |
| `midjourney/` | [MidjourneyMCP](https://github.com/AceDataCloud/MidjourneyMCP) | [mcp-midjourney](https://pypi.org/project/mcp-midjourney/) | Image |
| `nanobanana/` | [NanoBananaMCP](https://github.com/AceDataCloud/NanoBananaMCP) | [mcp-nanobanana-pro](https://pypi.org/project/mcp-nanobanana-pro/) | Image |
| `producer/` | [ProducerMCP](https://github.com/AceDataCloud/ProducerMCP) | [mcp-producer](https://pypi.org/project/mcp-producer/) | Music |
| `seedance/` | [SeedanceMCP](https://github.com/AceDataCloud/SeedanceMCP) | [mcp-seedance](https://pypi.org/project/mcp-seedance/) | Video |
| `seedream/` | [SeedreamMCP](https://github.com/AceDataCloud/SeedreamMCP) | [mcp-seedream-pro](https://pypi.org/project/mcp-seedream-pro/) | Image |
| `serp/` | [SerpMCP](https://github.com/AceDataCloud/SerpMCP) | [mcp-serp](https://pypi.org/project/mcp-serp/) | Search |
| `shorturl/` | [ShortURLMCP](https://github.com/AceDataCloud/ShortURLMCP) | [mcp-shorturl](https://pypi.org/project/mcp-shorturl/) | Utility |
| `sora/` | [SoraMCP](https://github.com/AceDataCloud/SoraMCP) | [mcp-sora](https://pypi.org/project/mcp-sora/) | Video |
| `suno/` | [SunoMCP](https://github.com/AceDataCloud/SunoMCP) | [mcp-suno](https://pypi.org/project/mcp-suno/) | Music |
| `veo/` | [VeoMCP](https://github.com/AceDataCloud/VeoMCP) | [mcp-veo](https://pypi.org/project/mcp-veo/) | Video |
| `wan/` | [WanMCP](https://github.com/AceDataCloud/WanMCP) | [mcp-wan](https://pypi.org/project/mcp-wan/) | Video |

## Publishing

Each MCP is published to multiple channels automatically on every push to `main`:

| Channel | Status |
|---|---|
| [PyPI](https://pypi.org/) | All 15 servers published |
| [VS Code Marketplace](https://marketplace.visualstudio.com/) | All 15 extensions published |
| [JetBrains Marketplace](https://plugins.jetbrains.com/) | All 15 plugins published |
| [Smithery](https://smithery.ai/) | All 15 servers published |
| [MCP Registry](https://registry.modelcontextprotocol.io/) | All 15 servers published |

Versioning uses **CalVer** (`YYYY.M.D.BUILD`), auto-generated at publish time.

## How It Works

### Sync Pipeline

```
AceDataCloud/Docs (OpenAPI specs)
     │  push to main
     ▼
dispatch-on-push.yml ──► docs-updated event
     │
     ▼
MCPs/sync-from-docs.yml ──► creates issue for Copilot
     │                       Copilot compares specs, opens PR
     ▼                       PR auto-merged
MCPs/sync-to-repos.yml ──► pushes to 15 standalone repos
     │
     ▼
<Repo>/publish.yml ──► PyPI, VS Code, JetBrains, Smithery, MCP Registry
```

### Rules

- This monorepo is the **source of truth**. Do not edit standalone repos directly.
- The mapping between subdirectories and standalone repos is defined in [`sync.yaml`](sync.yaml).
- CI runs lint (`ruff`) and tests (`pytest`, Python 3.10/3.11/3.12) on every push and PR.

## Development

```bash
cd <server>/
pip install -e ".[dev]"
pytest --cov=core --cov=tools
ruff check .
```
