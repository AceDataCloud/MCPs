# ACE Music MCP

Create songs from an idea or custom lyrics, generate lyrics, and retrieve the original task through Ace Data Cloud.

<!-- canonical-documentation -->
[Documentation](https://platform.acedata.cloud/documents/mcp-acemusic?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_mcp_readme_quick_start)

This new service package is prepared for release alongside the ACE Music API. Package publication, hosted deployment and real generation are separate release checks; source code does not confirm their availability.

## Configure a credential

Get an application API key at [Applications](https://platform.acedata.cloud/console/applications?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_mcp_readme_api_key). Use a general application with ACE Music access or an ACE Music application; check balance, expiration and allowed APIs. Store the raw key in `ACEDATACLOUD_API_TOKEN`, never in a prompt or commit. Account management tokens do not replace generation API keys.

```bash
export ACEDATACLOUD_API_TOKEN="your-api-key"
# After the package is published:
uvx mcp-acemusic
```

For source development: `pip install -e ".[dev,test]"`, then `mcp-acemusic`.

The hosted target after deployment is `https://acemusic.mcp.acedata.cloud/mcp`. Configure a Bearer API key in the client or use its OAuth connection flow when registration is enabled. The deployer must sync ACE Music's own AuthBackend OAuth seed and provision its state secret; credentials from another service must not be reused.

## Tools

| Tool | Purpose |
| --- | --- |
| `acemusic_generate_music` | One paid idea-to-song submission |
| `acemusic_generate_custom_music` | One paid submission with lyrics, style and title |
| `acemusic_generate_lyrics` | Separately priced title/lyrics assistant |
| `acemusic_get_task` | Free authenticated lookup of the original task |
| `acemusic_get_tasks_batch` | Query up to 50 original tasks |
| `acemusic_list_tasks` | Paginated caller history |
| `acemusic_list_models` | Local model discovery |
| `acemusic_get_capabilities` | Supported workflows and recovery boundaries |

Models: `acemusic-v1.1` (default), `acemusic-v1`. A music task targets two MP3 candidates. Use lyrics section markers such as `[Verse]` and `[Chorus]`; the platform request field is `lyric`, not `lyrics`.

Save `task_id` immediately. Poll the same task every 10 seconds, inspecting its persisted `response` and group state. Partial failure is terminal and may include one playable candidate. A nonempty URL or a task ID alone does not mean full success. A client timeout must preserve the task identity for recovery rather than triggering another paid generation. If submission times out before a task ID arrives, reconcile the original request.

The package does not promise upload, cover, extend, stems, voice cloning, WAV, MIDI or video export. Check [current pricing](https://platform.acedata.cloud/services/024e09b4-52cf-5e98-a91a-efedf43104c4?utm_source=github&utm_medium=referral&utm_campaign=evergreen&utm_content=acemusic_mcp_readme_services_024e09b4-52cf-5e98-a91a-efedf43104c4) before submitting; task lookup is free and still requires authorization.

## Development and deployment

Run `ruff check .`, `ruff format --check .`, `mypy core tools main.py`, `pytest`, and `python -m build`. Tests mock HTTP and do not spend account credit.

`deploy/production` targets the shared `nginx-router` ingress. Provision `mcp-acemusic-oauth-state` with `state_key`, the shared OAuth Redis secret, DNS/TLS and package/image publication before enabling the hosted entry. `deploy/run.sh` uses the repository's normal release mechanism.

<!-- mcp-name: io.github.AceDataCloud/mcp-acemusic -->


The official ACE Music icon comes from the immutable CDN URL and SHA256 in
`brand-assets.json`. VS Code and JetBrains builds download and verify that asset
before packaging; generated icon files are ignored and are not source assets.
