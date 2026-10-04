<!-- Generated from PlatformBackend; edit the backend source. -->
# API reference

These are the public HTTP API contracts. Native MCP tools and CLI commands are described in the package README.

## WebExtrator Web Render & Extract

| Method | Endpoint | Request fields |
| --- | --- | --- |
| POST | `/webextrator/extract` | `url`, `expected_type`, `enable_llm`, `wait_until`, `timeout`, `delay`, `wait_for_selector`, `block_resources`, `headers`, `user_agent`, `callback_url`, `async` |
| POST | `/webextrator/render` | `url`, `wait_until`, `timeout`, `delay`, `wait_for_selector`, `block_resources`, `headers`, `user_agent`, `callback_url`, `async` |
| POST | `/webextrator/tasks` | `action`, `id`, `trace_id`, `ids`, `trace_ids`, `offset`, `limit` |

Full schema: [webextrator.json](openapi/webextrator.json).

### Guides

- [development_webextrator_extract.md](guides/development_webextrator_extract.md)
- [development_webextrator_render.md](guides/development_webextrator_render.md)
- [development_webextrator_tasks.md](guides/development_webextrator_tasks.md)

Source: [PlatformBackend@945664eca88d](https://github.com/AceDataCloud/PlatformBackend/tree/945664eca88d16d21159d3739f874c830c046005).
