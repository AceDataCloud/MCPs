# Changelog

## [2026.5.10.0] - 2026-05-10

### Added
- `aichat_create_conversation_v2` tool using the `/aichat2/conversations` endpoint
- `AiChatV2Model` type with 83 models including Claude, Gemini, Grok-4, and Kimi
- Support for Anthropic Claude (claude-opus-4-7, claude-sonnet-4-6, etc.)
- Support for Google Gemini (gemini-3.1-pro, gemini-2.5-flash-lite, etc.)
- Support for xAI Grok-4 (grok-4, grok-4-1-fast, etc.)
- Support for Kimi (kimi-k2.5, kimi-k2-thinking, etc.)
- Updated `aichat_list_models` to include v2 endpoint models
- Updated `aichat_get_usage_guide` with v2 tool documentation

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
