<!-- Generated from PlatformBackend; edit the backend source. -->
# API reference

These are the public HTTP API contracts. Native MCP tools and CLI commands are described in the package README.

## Grok

| Method | Endpoint | Request fields |
| --- | --- | --- |
| POST | `/grok/chat/completions` | `n`, `model`, `stream`, `messages`, `max_tokens`, `temperature`, `top_p`, `frequency_penalty`, `presence_penalty`, `seed`, `stop`, `max_completion_tokens`, `logprobs`, `top_logprobs`, `stream_options`, `parallel_tool_calls`, `user`, `reasoning_effort`, `service_tier`, `store`, `metadata`, `logit_bias`, `modalities`, `audio`, `prediction`, `web_search_options`, `tools`, `tool_choice`, `response_format` |
| POST | `/grok/videos` | `prompt`, `model`, `image_url`, `reference_image_urls`, `aspect_ratio`, `resolution`, `duration`, `callback_url`, `async` |
| POST | `/grok/tasks` | `id`, `ids`, `action` |

Full schema: [grok.json](openapi/grok.json).

### Guides

- [development_grok_chat_completions.md](guides/development_grok_chat_completions.md)
- [development_grok_tasks.md](guides/development_grok_tasks.md)
- [development_grok_videos.md](guides/development_grok_videos.md)

Source: [PlatformBackend@945664eca88d](https://github.com/AceDataCloud/PlatformBackend/tree/945664eca88d16d21159d3739f874c830c046005).
