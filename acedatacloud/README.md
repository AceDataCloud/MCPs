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

<!-- BEGIN GENERATED TOOL REFERENCE -->
## Tool Reference

### Account reads

| Tool | Description |
|------|-------------|
| `acedatacloud_export_orders` | Export bounded order CSV. |
| `acedatacloud_export_usage` | Export bounded usage CSV. |
| `acedatacloud_get_application` | Get one application and service details. |
| `acedatacloud_get_auto_recharge` | Get auto recharge. |
| `acedatacloud_get_balance` | Summarize remaining Credits. |
| `acedatacloud_get_credential` | Get one credential with secrets masked. |
| `acedatacloud_get_deployment_events` | Get deployment scheduling events. |
| `acedatacloud_get_deployment_logs` | Get bounded deployment logs. |
| `acedatacloud_get_deployment_status` | Get live deployment status. |
| `acedatacloud_get_invoice` | Get one invoice. |
| `acedatacloud_get_invoice_download` | Get a signed invoice URL. |
| `acedatacloud_get_order` | Get one order. |
| `acedatacloud_get_order_invoice` | Get an order's active invoice. |
| `acedatacloud_get_order_summary` | Summarize caller orders. |
| `acedatacloud_get_proxy_usage` | Get proxy usage detail. |
| `acedatacloud_get_usage` | Get API usage detail. |
| `acedatacloud_get_user_info` | Current authenticated account profile. |
| `acedatacloud_list_applications` | List account subscriptions. |
| `acedatacloud_list_auto_recharges` | List auto-recharge configs. |
| `acedatacloud_list_billing_profiles` | List billing profiles. |
| `acedatacloud_list_credentials` | List API credentials with secrets masked. |
| `acedatacloud_list_distributions` | Get referral status. |
| `acedatacloud_list_invoices` | List invoices. |
| `acedatacloud_list_models` | List OpenAI-compatible chat models. |
| `acedatacloud_list_orders` | List recharge orders. |
| `acedatacloud_list_platform_tokens` | List management tokens with values masked. |
| `acedatacloud_list_proxy_usage` | List proxy usage. |
| `acedatacloud_list_usage` | List recent API usage records. |
| `acedatacloud_list_usage_status_codes` | List usage status codes. |
| `acedatacloud_preview_invoice` | Preview invoice amount. |
| `acedatacloud_quote_auto_recharge` | Quote auto recharge. |
| `acedatacloud_usage_summary` | Aggregate API spend by API. |

### Catalog & docs

| Tool | Description |
|------|-------------|
| `acedatacloud_get_api_spec` | Get one API's OpenAPI definition by path. |
| `acedatacloud_get_doc` | Fetch one documentation page by UUID. |
| `acedatacloud_get_model` | Find models by ID or name. |
| `acedatacloud_get_pricing` | Get one service's display pricing. |
| `acedatacloud_get_service` | Get one service by UUID or alias. |
| `acedatacloud_list_announcements` | List published announcements. |
| `acedatacloud_list_apis` | List API endpoints and billing metadata. |
| `acedatacloud_list_datasets` | List downloadable datasets. |
| `acedatacloud_list_docs` | Browse documentation pages. |
| `acedatacloud_list_integrations` | List platform integrations. |
| `acedatacloud_list_model_catalog` | List rich model metadata and pricing. |
| `acedatacloud_list_services` | List or search available services. |
| `acedatacloud_search_docs` | Search public documentation. |

### Writes

| Tool | Description |
|------|-------------|
| `acedatacloud_apply_invoice` | Apply for an invoice. |
| `acedatacloud_cancel_invoice` | Cancel an invoice. |
| `acedatacloud_confirm_auto_recharge_setup` | Confirm saved card setup. |
| `acedatacloud_control_deployment` | Start a stopped deployment. |
| `acedatacloud_create_application` | Create an application subscription. |
| `acedatacloud_create_auto_recharge` | Create auto recharge. |
| `acedatacloud_create_credential` | Create an API credential. |
| `acedatacloud_create_order` | Create a recharge order. |
| `acedatacloud_create_platform_token` | Create a management token. |
| `acedatacloud_delete_auto_recharge` | Delete auto recharge. |
| `acedatacloud_delete_credential` | Revoke an API credential. |
| `acedatacloud_delete_platform_token` | Revoke a management token. |
| `acedatacloud_deploy_application` | Start or redeploy an application workload. |
| `acedatacloud_disable_auto_recharge` | Disable auto recharge. |
| `acedatacloud_pay_order` | Create an order payment session. |
| `acedatacloud_refresh_order` | Refresh payment state. |
| `acedatacloud_rotate_credential` | Rotate and disclose a credential secret once. |
| `acedatacloud_save_deployment_config` | Save a deployment configuration draft. |
| `acedatacloud_setup_auto_recharge` | Create card setup state. |
| `acedatacloud_teardown_deployment` | Destroy a workload and delete its application. |
| `acedatacloud_update_application_balance_policy` | Update global-balance fallback policy. |
| `acedatacloud_update_auto_recharge` | Update auto recharge. |
| `acedatacloud_update_credential` | Update credential limits and API scope. |
| `acedatacloud_verify_apple_order` | Verify and fulfill Apple IAP. |

### Admin

| Tool | Description |
|------|-------------|
| `acedatacloud_create_announcement` | Publish a platform announcement. |

Calling a write/admin tool **without** `confirm=true` returns a redacted
dry-run preview and performs no HTTP request.

<!-- END GENERATED TOOL REFERENCE -->

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
