# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-28

### Added

- Initial release of the unified AceDataCloud MCP server (`mcp-acedatacloud`).
- **Public catalog & docs tools** (no token): `acedatacloud_list_services`,
  `acedatacloud_get_service`, `acedatacloud_list_apis`, `acedatacloud_get_api_spec`,
  `acedatacloud_get_pricing`, `acedatacloud_search_docs`, `acedatacloud_list_docs`,
  `acedatacloud_get_doc`, `acedatacloud_list_models`, `acedatacloud_get_model`,
  `acedatacloud_list_datasets`, `acedatacloud_list_integrations`. Consolidates the
  former public docs MCP (`docs.mcp.acedata.cloud`).
- **Account-management read tools** (platform token): `acedatacloud_get_balance`,
  `acedatacloud_list_applications`, `acedatacloud_list_usage`,
  `acedatacloud_usage_summary`, `acedatacloud_list_credentials`,
  `acedatacloud_list_orders`, `acedatacloud_list_platform_tokens`,
  `acedatacloud_list_distributions`, `acedatacloud_list_announcements`.
- **Write tools** (gated by `confirm=true`): `acedatacloud_create_credential`,
  `acedatacloud_delete_credential`, `acedatacloud_create_order`,
  `acedatacloud_pay_order`, `acedatacloud_create_platform_token`,
  `acedatacloud_delete_platform_token`; admin `acedatacloud_create_announcement`.
- Informational tool `acedatacloud_get_usage_guide` + the `acedatacloud_guide` prompt.
- Token is **optional**: catalog/docs tools work without it; account tools require it.
- Secret masking for token/password/pay_url fields in read output.
- stdio and HTTP transport modes (HTTP injects a per-request bearer token).
- Docker support.
