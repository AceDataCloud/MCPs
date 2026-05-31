# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org/).

## [Unreleased]

## [2026.4.5.0] - 2026-04-05

### Added

- Initial release of the MCP Fish Audio Server.
- Text-to-speech tools backed by the AceDataCloud Fish Audio API:
  - `fish_generate_audio` — submit a TTS job (text, model, reference voice).
  - `fish_get_task` — query the status of a single TTS task.
  - `fish_get_tasks_batch` — query multiple TTS tasks in one call.
  - `fish_list_models` — list available Fish Audio voice models.
  - `fish_get_model` — get metadata for a single voice model.
  - `fish_get_usage_guide` — concise client-side usage guide.
- Two MCP prompts: `fish_guide`, `fish_workflow_examples`.
- stdio and Streamable HTTP transports.
- OAuth 2.1 (PKCE) support for hosted Claude.ai deployment.
- Bearer-token authentication for direct HTTP access.
- JetBrains AI Assistant plugin scaffold and VS Code extension scaffold.
- GitHub Actions pipeline for PyPI / GitHub Release / MCP Registry / Smithery /
  VS Code Marketplace / JetBrains Marketplace / Docker Hub publication.

[Unreleased]: https://github.com/AceDataCloud/FishMCP/compare/v2026.4.5.0...HEAD
[2026.4.5.0]: https://github.com/AceDataCloud/FishMCP/releases/tag/v2026.4.5.0
