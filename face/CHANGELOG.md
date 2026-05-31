# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Calendar Versioning](https://calver.org/).

## [Unreleased]

### Added

- Initial release of MCP Face Transform Server.
- Seven face tools wrapping the AceDataCloud Face Transform API:
  - `face_detect_keypoints` — `POST /face/analyze` (90+ keypoints per face)
  - `face_beautify` — `POST /face/beautify`
  - `face_change_age` — `POST /face/change-age`
  - `face_change_gender` — `POST /face/change-gender`
  - `face_swap` — `POST /face/swap` (optional async `callback_url`)
  - `face_cartoonize` — `POST /face/cartoon`
  - `face_detect_liveness` — `POST /face/detect-live`
  - `face_get_usage_guide` — concise tool reference
- Two MCP prompts: `face_guide`, `face_workflow_examples`.
- stdio and Streamable HTTP transports.
- OAuth 2.1 (PKCE) support for hosted Claude.ai deployment.
- Bearer-token authentication for direct HTTP access.
- JetBrains AI Assistant plugin scaffold and VS Code extension scaffold.
- GitHub Actions pipeline for PyPI / GitHub Release / MCP Registry / Smithery /
  VS Code Marketplace / JetBrains Marketplace / Docker Hub publication.
