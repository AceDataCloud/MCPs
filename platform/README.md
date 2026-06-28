# PlatformMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-acedata-platform -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-acedata-platform.svg)](https://pypi.org/project/mcp-acedata-platform/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for
**managing your [AceDataCloud](https://platform.acedata.cloud) account** through
the [platform management API](https://platform.acedata.cloud/documents/platform-token).

Check your balance, look up usage and spend, manage API keys, list services,
create and pay recharge orders, manage platform tokens, list models, and (for
admins) publish announcements — directly from Claude, VS Code, or any
MCP-compatible client.

> This is the **management / console** API (`platform.acedata.cloud`) — different
> from the data-generation MCP servers (Suno, Midjourney, …) that call
> `api.acedata.cloud`.

## Tool Reference

### Read (always safe)

| Tool | Description |
|------|-------------|
| `platform_get_balance` | Remaining credits per subscription, plus a total. |
| `platform_list_applications` | Your subscriptions with balance/spend. |
| `platform_list_services` | List or search available services. |
| `platform_list_usage` | Recent API call records (status, latency, credits). |
| `platform_usage_summary` | Spend aggregated by API over N days. |
| `platform_list_credentials` | Your API keys (token values masked). |
| `platform_list_orders` | Recharge orders. |
| `platform_list_platform_tokens` | Platform tokens (masked). |
| `platform_list_models` | Available chat models. |
| `platform_list_announcements` | Published announcements. |

### Write (require `confirm=true`)

| Tool | Description |
|------|-------------|
| `platform_create_credential` | Create an API key on an application. |
| `platform_delete_credential` | Revoke an API key. |
| `platform_create_order` | Create a recharge order. |
| `platform_pay_order` | Create a payment session and return `pay_url`. |
| `platform_create_platform_token` | Create a new platform token. |
| `platform_delete_platform_token` | Revoke a platform token. |

### Admin (superuser token)

| Tool | Description |
|------|-------------|
| `platform_create_announcement` | Publish a platform announcement (`confirm=true`). |

Calling a write/admin tool **without** `confirm=true` returns a dry-run preview
and changes nothing.

## Quick Start

### 1. Get a platform token

Create one at [platform.acedata.cloud/console/platform-tokens](https://platform.acedata.cloud/console/platform-tokens).
It starts with `platform-` and never expires.

> Use a **platform token**, not the per-service `api.acedata.cloud` token — the
> latter returns 401 against the management API.

### 2. Install

```bash
pip install mcp-acedata-platform
```

### 3. Configure your client

**Claude Desktop / VS Code (stdio):**

```json
{
  "mcpServers": {
    "acedata-platform": {
      "command": "mcp-acedata-platform",
      "env": {
        "ACEDATACLOUD_PLATFORM_TOKEN": "platform-v1-xxxxxxxx"
      }
    }
  }
}
```

**Hosted (HTTP) — token per request:**

```json
{
  "mcpServers": {
    "acedata-platform": {
      "url": "https://platform.mcp.acedata.cloud/mcp",
      "headers": { "Authorization": "Bearer platform-v1-xxxxxxxx" }
    }
  }
}
```

## Example prompts

- "How many credits do I have left?"
- "What did I spend on Suno in the last 7 days?"
- "List my API keys and show which ones have a spend cap."
- "Create a new API key on application `<id>` named ci." → previews, then run with confirm.
- "Top up application `<id>` with package `<id>` and give me the Stripe pay link."

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ACEDATACLOUD_PLATFORM_TOKEN` | — | **Required.** Platform token. |
| `PLATFORM_API_BASE_URL` | `https://platform.acedata.cloud` | Management API base. |
| `PLATFORM_REQUEST_TIMEOUT` | `30` | Request timeout (seconds). |
| `LOG_LEVEL` | `INFO` | Logging level. |

## Development

```bash
pip install -e ".[dev,test,http]"
pytest -m "not integration"      # unit tests
ruff check .                      # lint
mypy core tools                   # type-check
mcp-acedata-platform --transport http --port 8000
```

## Notes

- Amounts (`remaining_amount`, `used_amount`, totals) are in **Credits**, not USD.
- Newly created credential/platform tokens are returned in full **only once** —
  store them immediately.
- Credential rotation = delete + recreate (no in-place rotate endpoint).
- Announcement tools require a **superuser** token.

## License

MIT — see [LICENSE](LICENSE).
