# Copilot Sync Instructions for AceDataCloud MCPs

## Repository Structure

This is a monorepo with one MCP server per subdirectory (e.g., `suno/`, `luma/`, `flux/`).
Each subdirectory contains a standalone Python MCP server package.

## Source of Truth

The **AceDataCloud/Docs** repo is the source of truth:

- `openapi/<service>.json` — OpenAPI specs for each service
- `mcp/<service>.md` — MCP-specific documentation (optional reference)

## What to Sync

When the Docs repo changes, compare the OpenAPI specs against the MCP server code and update:

1. **Model/provider enums** — ensure all models listed in the OpenAPI spec are available
2. **Tool parameters** — match request body schemas from OpenAPI specs
3. **Endpoint paths** — verify API paths match the OpenAPI `paths` section
4. **Response schemas** — ensure tool return types match OpenAPI response schemas

## Rules

- Do NOT change the MCP server architecture or framework patterns
- Do NOT modify CI/CD workflows or sync.yaml
- Keep backward compatibility: add new models/params, don't remove existing ones unless the API removed them
- Each subdirectory is independent — only update directories for changed services
- Run `ruff check .` in affected subdirectories to verify linting passes
