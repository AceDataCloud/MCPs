<!-- Generated from PlatformBackend; edit the backend source. -->
# API reference

These are the public HTTP API contracts. Native MCP tools and CLI commands are described in the package README.

## GLM

| Method | Endpoint | Request fields |
| --- | --- | --- |
| POST | `/glm/chat/completions` | `n`, `model`, `stream`, `messages`, `max_tokens`, `temperature`, `response_format`, `top_p`, `frequency_penalty`, `presence_penalty`, `seed`, `stop`, `max_completion_tokens`, `logprobs`, `top_logprobs`, `stream_options`, `parallel_tool_calls`, `user`, `reasoning_effort`, `service_tier`, `store`, `metadata`, `logit_bias`, `modalities`, `audio`, `prediction`, `web_search_options`, `tools`, `tool_choice` |

Full schema: [glm.json](openapi/glm.json).

### Guides

- [development_glm_chat_completions.md](guides/development_glm_chat_completions.md)

Source: [PlatformBackend@945664eca88d](https://github.com/AceDataCloud/PlatformBackend/tree/945664eca88d16d21159d3739f874c830c046005).
