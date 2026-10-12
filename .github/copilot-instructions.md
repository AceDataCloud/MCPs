# Copilot Sync Instructions for AceDataCloud MCPs

## Repository Structure

This is a monorepo with one MCP server per subdirectory (e.g., `suno/`, `luma/`, `flux/`).
Each subdirectory contains a standalone Python MCP server package.

## Source of Truth

**AceDataCloud/PlatformBackend** is the contract source of truth. Use the exact
commit and allowed package directories in the sync issue. Compile and verify
its bundle with `scripts/ecosystem_contracts.py`; the consumer's
`scripts/platform_contract.py` resolves service aliases to package directories.
Docs is a published reference, not a second contract input.

## What to Sync

When a PlatformBackend contract changes, compare its compiled OpenAPI against the MCP server code and update:

1. **Model/provider enums** — ensure all models listed in the OpenAPI spec are available
2. **Tool parameters** — match request body schemas from OpenAPI specs
3. **Endpoint paths** — verify API paths match the OpenAPI `paths` section
4. **Response schemas** — ensure tool return types match OpenAPI response schemas

## Rules

- Do NOT change the MCP server architecture or framework patterns
- Do NOT modify CI/CD workflows or sync.yaml
- Keep backward compatibility: add new models/params, don't remove existing ones unless the API removed them
- Each subdirectory is independent — only update directories for changed services
- When a public MCP parameter needs a different Python name, use `Field(validation_alias="<public-name>")`; never use `Field(alias=...)` on an `@mcp.tool` parameter because FastMCP dispatches the alias as an invalid Python keyword
- Add an `mcp.call_tool(...)` test for every new or changed public-to-Python parameter mapping
- Run `ruff check .` in affected subdirectories to verify linting passes
- OAuth files marked `Generated from shared/oauth.py` are distribution artifacts. Edit `shared/oauth.py` and run `python3 scripts/sync_oauth.py`; commit all generated changes together. The explicitly classified local OAuth variants are not generated.
