# AceDataCloudMCP

<!-- mcp-name: io.github.AceDataCloud/mcp-acedatacloud -->

[![PyPI version](https://img.shields.io/pypi/v/mcp-acedatacloud.svg)](https://pypi.org/project/mcp-acedatacloud/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io)

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server for the
whole **[AceDataCloud](https://platform.acedata.cloud) platform**: browse the
public **catalog & docs** (services, APIs, OpenAPI specs, pricing, models,
documentation — no token), and **manage your account** (balance, usage, API keys,
orders, referral earnings — with a platform token).

Two tiers in one server:

- **Public (no token):** search docs, browse services/APIs/specs, check pricing and models.
- **Account (platform token):** balance, usage/spend, API keys, orders, platform tokens, distributions, announcements.

> Consolidates the former public **docs** MCP (`docs.mcp.acedata.cloud`) into this
> single server. It is the **management / console** side (`platform.acedata.cloud`)
> — different from the data-generation MCP servers (Suno, Midjourney, …) that call
> `api.acedata.cloud`.

## Tool Reference

### Catalog & docs — public, no token required

| Tool | Description |
|------|-------------|
| `acedatacloud_list_services` | List / search the service catalog. |
| `acedatacloud_get_service` | One service's detail: its APIs + pricing packages. |
| `acedatacloud_list_apis` | Public API endpoints, optionally per service. |
| `acedatacloud_get_api_spec` | OpenAPI spec for an API (by path or service). |
| `acedatacloud_get_pricing` | Display pricing (unit, free quota, cost rules). |
| `acedatacloud_search_docs` | Search the documentation by keyword/question. |
| `acedatacloud_list_docs` | Browse documentation pages. |
| `acedatacloud_get_doc` | Read a full documentation page. |
| `acedatacloud_list_models` | Model catalog (all modalities) + credit pricing. |
| `acedatacloud_get_model` | One model's detail + pricing. |
| `acedatacloud_list_datasets` / `acedatacloud_list_integrations` | Catalog extras. |

### Account — read (needs a platform token)

| Tool | Description |
|------|-------------|
| `acedatacloud_get_balance` | Remaining credits per subscription, plus a total. |
| `acedatacloud_list_applications` | Your subscriptions with balance/spend. |
| `acedatacloud_list_usage` | Recent API call records (status, latency, credits). |
| `acedatacloud_usage_summary` | Spend aggregated by API over N days. |
| `acedatacloud_list_credentials` | Your API keys (token values masked). |
| `acedatacloud_list_orders` | Recharge orders. |
| `acedatacloud_list_platform_tokens` | Platform tokens (masked). |
| `acedatacloud_list_distributions` | Referral / affiliate status + commissions. |
| `acedatacloud_list_announcements` | Published announcements. |

### Account — write (require `confirm=true`)

| Tool | Description |
|------|-------------|
| `acedatacloud_create_credential` / `acedatacloud_delete_credential` | Create / revoke an API key. |
| `acedatacloud_create_order` | Create a recharge order. |
| `acedatacloud_pay_order` | Create a payment session and return `pay_url`. |
| `acedatacloud_create_platform_token` / `acedatacloud_delete_platform_token` | Create / revoke a platform token. |
| `acedatacloud_create_announcement` | Publish an announcement (superuser). |

Calling a write/admin tool **without** `confirm=true` returns a dry-run preview
and changes nothing. The catalog & docs tools work **without any token**; account
tools need `ACEDATACLOUD_PLATFORM_TOKEN`.

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
      "url": "https://acedatacloud.mcp.acedata.cloud/mcp",
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
