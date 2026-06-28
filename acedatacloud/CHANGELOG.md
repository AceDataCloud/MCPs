# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-06-28

### Added

- Public **catalog** tools (no token needed): `acedatacloud_get_service`,
  `acedatacloud_get_pricing`, `acedatacloud_list_apis`, `acedatacloud_get_api_spec`,
  `acedatacloud_list_datasets`, `acedatacloud_list_integrations`.
- Public **docs** tools: `acedatacloud_search_docs`, `acedatacloud_list_docs`,
  `acedatacloud_get_doc`.
- Public **model catalog** tools: `acedatacloud_list_model_catalog`, `acedatacloud_get_model`.
- Account tool: `acedatacloud_list_distributions` (referral status + commission history).
- Client now supports a public (no-token) request path via `get_public`; catalog/docs/model
  tools work with or without a platform token.

### Notes

- Catalog/docs lookups use list+filter (`services/?id=`, `apis/?path=`, `documents/?id=`)
  because the platform's detail routes are unreliable; `apis`/`services` collection filters
  that are ignored server-side are applied client-side.

## [0.1.0] - 2026-06-28

### Added

- Initial release of the AceDataCloud Platform management MCP server.
- Read tools: `acedatacloud_get_balance`, `acedatacloud_list_applications`,
  `acedatacloud_list_services`, `acedatacloud_list_usage`, `acedatacloud_usage_summary`,
  `acedatacloud_list_credentials`, `acedatacloud_list_orders`,
  `acedatacloud_list_platform_tokens`, `acedatacloud_list_models`,
  `acedatacloud_list_announcements`.
- Write tools (gated by `confirm=true`): `acedatacloud_create_credential`,
  `acedatacloud_delete_credential`, `acedatacloud_create_order`, `acedatacloud_pay_order`,
  `acedatacloud_create_platform_token`, `acedatacloud_delete_platform_token`.
- Admin tool (superuser): `acedatacloud_create_announcement`.
- Informational tool `acedatacloud_get_usage_guide` and the `acedatacloud_guide` prompt.
- Secret masking for token/password fields in read output.
- Bearer-token authentication; stdio and HTTP transport modes.
- Docker support.
