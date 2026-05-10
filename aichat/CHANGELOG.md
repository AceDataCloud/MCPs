# Changelog

## [2026.5.10.0] - 2026-05-10

### Added
- `aichat_create_conversation_v2` tool for AI dialogue via the v2 API endpoint (`/aichat2/conversations`)
- `AiChatV2Model` type with 83 models including Claude, Gemini, Grok-4, Kimi, and more
- v2 model listing in `aichat_list_models` and `aichat_get_usage_guide`
- Updated prompts to guide model selection between v1 and v2

## [2026.4.25.0] - 2026-04-25

### Added
- Initial release of MCP AiChat server
- `aichat_create_conversation` tool for AI dialogue with all supported models
- `aichat_list_models` tool to list available models
- `aichat_get_usage_guide` tool for usage documentation
- Support for GPT-4/5, o-series, DeepSeek, Grok, and GLM models
- Multi-turn conversation support via conversation_id
- HTTP and stdio transport modes
- OAuth 2.1 support for remote deployments
