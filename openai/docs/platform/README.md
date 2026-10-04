<!-- Generated from PlatformBackend; edit the backend source. -->
# API reference

These are the public HTTP API contracts. Native MCP tools and CLI commands are described in the package README.

## OpenAI generation

| Method | Endpoint | Request fields |
| --- | --- | --- |
| POST | `/openai/chat/completions` | `n`, `model`, `stream`, `messages`, `max_tokens`, `temperature`, `response_format`, `tools`, `tool_choice`, `top_p`, `frequency_penalty`, `presence_penalty`, `seed`, `stop`, `max_completion_tokens`, `logprobs`, `top_logprobs`, `stream_options`, `parallel_tool_calls`, `user`, `reasoning_effort`, `service_tier`, `store`, `metadata`, `logit_bias`, `modalities`, `audio`, `prediction`, `web_search_options` |
| POST | `/openai/embeddings` | `model`, `input`, `encoding_format`, `dimensions` |
| POST | `/openai/images/generations` | `prompt`, `background`, `model`, `moderation`, `n`, `output_compression`, `output_format`, `partial_images`, `size`, `quality`, `response_format`, `style`, `callback_url`, `async` |
| POST | `/openai/responses` | `n`, `model`, `background`, `stream`, `input`, `tools`, `max_tokens`, `temperature`, `response_format`, `tool_choice`, `parallel_tool_calls`, `include`, `reasoning`, `text`, `max_output_tokens`, `store`, `stream_options` |
| POST | `/openai/images/edits` | `image`, `prompt`, `model`, `n`, `background`, `input_fidelity`, `output_format`, `output_compression`, `quality`, `size`, `response_format`, `callback_url`, `async` |
| POST | `/v1/audio/speech` | `model`, `input`, `voice`, `response_format`, `speed` |
| POST | `/v1/audio/transcriptions` | See OpenAPI |
| POST | `/openai/tasks` | `action`, `id`, `trace_id`, `ids`, `trace_ids`, `application_id`, `user_id`, `type`, `offset`, `limit`, `created_at_min`, `created_at_max`, `count_mode` |

Full schema: [openai.json](openapi/openai.json).

### Guides

- [development_openai_audio_speech.md](guides/development_openai_audio_speech.md)
- [development_openai_audio_transcriptions.md](guides/development_openai_audio_transcriptions.md)
- [development_openai_chat_completions.md](guides/development_openai_chat_completions.md)
- [development_openai_embeddings.md](guides/development_openai_embeddings.md)
- [development_openai_images_edits.md](guides/development_openai_images_edits.md)
- [development_openai_images_generations.md](guides/development_openai_images_generations.md)
- [development_openai_responses.md](guides/development_openai_responses.md)
- [development_openai_tasks.md](guides/development_openai_tasks.md)

Source: [PlatformBackend@945664eca88d](https://github.com/AceDataCloud/PlatformBackend/tree/945664eca88d16d21159d3739f874c830c046005).
