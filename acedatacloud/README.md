# AceDataCloudMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-acedatacloud -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-acedatacloud.svg)](https://pypi.org/project/mcp-acedatacloud/)
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
| `acedatacloud_get_balance` | Remaining credits per subscription, plus a total. |
| `acedatacloud_list_applications` | Your subscriptions with balance/spend. |
| `acedatacloud_list_services` | List or search available services. |
| `acedatacloud_list_usage` | Recent API call records (status, latency, credits). |
| `acedatacloud_usage_summary` | Spend aggregated by API over N days. |
| `acedatacloud_list_credentials` | Your API keys (token values masked). |
| `acedatacloud_list_orders` | Recharge orders. |
| `acedatacloud_list_platform_tokens` | Platform tokens (masked). |
| `acedatacloud_list_models` | Available chat models. |
| `acedatacloud_list_announcements` | Published announcements. |
| `acedatacloud_list_distributions` | Your referral/affiliate status + commission history. |

### Catalog & Docs (public — no token needed)

| Tool | Description |
|------|-------------|
| `acedatacloud_get_service` | One service's detail (type, unit, free_amount, cost), by alias or id. |
| `acedatacloud_get_pricing` | A service's billing unit, free_amount and display pricing. |
| `acedatacloud_list_apis` | API endpoints, optionally scoped to one service (path, method, cost). |
| `acedatacloud_get_api_spec` | One API's OpenAPI `definition` + cost, by path. |
| `acedatacloud_list_datasets` | Downloadable datasets (price, download/preview URLs). |
| `acedatacloud_list_integrations` | Third-party integrations. |
| `acedatacloud_search_docs` | Full-text search the documentation (alias/title/snippet/url). |
| `acedatacloud_list_docs` | Browse documentation pages. |
| `acedatacloud_get_doc` | Fetch one doc's full content by UUID. |
| `acedatacloud_list_model_catalog` | Rich model catalog (provider, modality, credit pricing). |
| `acedatacloud_get_model` | Look up a model's pricing & capabilities by id/name. |

### Write (require `confirm=true`)

| Tool | Description |
|------|-------------|
| `acedatacloud_create_credential` | Create an API key on an application. |
| `acedatacloud_delete_credential` | Revoke an API key. |
| `acedatacloud_create_order` | Create a recharge order. |
| `acedatacloud_pay_order` | Create a payment session and return `pay_url`. |
| `acedatacloud_create_platform_token` | Create a new platform token. |
| `acedatacloud_delete_platform_token` | Revoke a platform token. |

### Admin (superuser token)

| Tool | Description |
|------|-------------|
| `acedatacloud_create_announcement` | Publish a platform announcement (`confirm=true`). |

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
pip install mcp-acedatacloud
```

### 3. Configure your client

**Claude Desktop / VS Code (stdio):**

```json
{
  "mcpServers": {
    "acedatacloud": {
      "command": "mcp-acedatacloud",
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
    "acedatacloud": {
      "url": "https://mcp.acedata.cloud/mcp",
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
mcp-acedatacloud --transport http --port 8000
```

## Notes

- Amounts (`remaining_amount`, `used_amount`, totals) are in **Credits**, not USD.
- Newly created credential/platform tokens are returned in full **only once** —
  store them immediately.
- Credential rotation = delete + recreate (no in-place rotate endpoint).
- Announcement tools require a **superuser** token.

## License

MIT — see [LICENSE](LICENSE).
