# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-28

### Added

- Initial release of the AceDataCloud Platform management MCP server.
- Read tools: `platform_get_balance`, `platform_list_applications`,
  `platform_list_services`, `platform_list_usage`, `platform_usage_summary`,
  `platform_list_credentials`, `platform_list_orders`,
  `platform_list_platform_tokens`, `platform_list_models`,
  `platform_list_announcements`.
- Write tools (gated by `confirm=true`): `platform_create_credential`,
  `platform_delete_credential`, `platform_create_order`, `platform_pay_order`,
  `platform_create_platform_token`, `platform_delete_platform_token`.
- Admin tool (superuser): `platform_create_announcement`.
- Informational tool `platform_get_usage_guide` and the `platform_guide` prompt.
- Secret masking for token/password fields in read output.
- Bearer-token authentication; stdio and HTTP transport modes.
- Docker support.
