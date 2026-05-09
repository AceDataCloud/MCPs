"""Informational tools for OpenAI API."""

from core.server import mcp


@mcp.tool()
async def openai_list_chat_models() -> str:
    """List all available chat completion models.

    Shows all models available for the chat completions and responses endpoints,
    including GPT-4, GPT-4o, GPT-5, and o-series models.

    Returns:
        Table of all chat models with descriptions.
    """
    # Last updated: 2026-04-25
    return """Available OpenAI Chat Completion Models:

## GPT-5 Series
| Model         | Description                              |
|---------------|------------------------------------------|
| gpt-5.5       | Latest GPT-5.5 model                     |
| gpt-5.5-pro   | GPT-5.5 Pro variant                      |
| gpt-5.4       | GPT-5.4 model                            |
| gpt-5.4-pro   | GPT-5.4 Pro variant                      |
| gpt-5.2       | GPT-5.2 model                            |
| gpt-5.1       | GPT-5.1 model                            |
| gpt-5.1-all   | GPT-5.1 all-access variant               |
| gpt-5         | GPT-5 standard                           |
| gpt-5-mini    | GPT-5 Mini - cost efficient              |
| gpt-5-nano    | GPT-5 Nano - ultra cost efficient        |

## GPT-4 Series
| Model              | Description                         |
|--------------------|-------------------------------------|
| gpt-4.1            | GPT-4.1 (recommended default)       |
| gpt-4.1-mini       | GPT-4.1 Mini - cost efficient       |
| gpt-4.1-nano       | GPT-4.1 Nano - ultra cost efficient |
| gpt-4o             | GPT-4o multimodal                   |
| gpt-4o-2024-05-13  | GPT-4o dated variant                |
| gpt-4o-all         | GPT-4o all-access                   |
| gpt-4o-image       | GPT-4o with image capabilities      |
| gpt-4o-mini        | GPT-4o Mini                         |
| gpt-4              | GPT-4 standard                      |
| gpt-35-turbo-16k   | GPT-3.5 Turbo 16K                   |

## Reasoning (o-series)
| Model    | Description                               |
|----------|-------------------------------------------|
| o4-mini  | o4 Mini - fast reasoning                  |
| o3       | o3 - advanced reasoning                   |
| o3-mini  | o3 Mini                                   |
| o3-pro   | o3 Pro                                    |
| o1       | o1 - original reasoning model             |
| o1-mini  | o1 Mini                                   |
| o1-pro   | o1 Pro                                    |
"""


@mcp.tool()
async def openai_list_image_models() -> str:
    """List all available image generation and editing models.

    Shows all models available for the images/generations and images/edits endpoints.

    Returns:
        Table of all image models with descriptions.
    """
    # Last updated: 2026-04-25
    return """Available OpenAI Image Models:

| Model            | Description                                        |
|------------------|----------------------------------------------------|
| gpt-image-1      | GPT Image 1 - versatile image generation (default)|
| gpt-image-1.5    | GPT Image 1.5 - improved quality                  |
| gpt-image-2      | GPT Image 2 - latest GPT image model              |
| dall-e-3         | DALL-E 3 - high quality artistic generation       |
| dall-e-2         | DALL-E 2 - legacy image generation                |
| nano-banana      | Nano Banana - fast, efficient generation          |
| nano-banana-2    | Nano Banana 2 - improved version                  |
| nano-banana-pro  | Nano Banana Pro - highest quality                 |

## Supported Sizes
| Size        | Aspect Ratio    | Notes                        |
|-------------|-----------------|------------------------------|
| 1024x1024   | 1:1 (Square)    | Default, 1K tier             |
| 1792x1024   | ~16:9 (Wide)    | Landscape, 1K tier           |
| 1024x1792   | ~9:16 (Tall)    | Portrait, 1K tier            |
| 1536x1024   | 3:2             | Wide format, 1K tier         |
| 1024x1536   | 2:3             | Tall format, 1K tier         |
| 2048x2048   | 1:1             | 2K Square, 1.5× rate         |
| 2048x1536   | 4:3             | 2K Wide, 1.5× rate           |
| 1536x2048   | 3:4             | 2K Tall, 1.5× rate           |
| 2048x1152   | 16:9            | 2K Landscape, 1.5× rate      |
| 1152x2048   | 9:16            | 2K Portrait, 1.5× rate       |
| 2880x2880   | 1:1             | 4K Square, 1.5× rate         |
| 3264x2448   | 4:3             | 4K Wide, 1.5× rate           |
| 2448x3264   | 3:4             | 4K Tall, 1.5× rate           |
| 3840x2160   | 16:9            | 4K Landscape, 1.5× rate      |
| 2160x3840   | 9:16            | 4K Portrait, 1.5× rate       |
| 256x256     | 1:1             | Small, legacy (dall-e-2)     |
| 512x512     | 1:1             | Medium, legacy (dall-e-2)    |
| auto        | Varies          | Model chooses                |
| WIDTHxHEIGHT | Custom         | gpt-image-2: any valid dims  |

**gpt-image-2 custom dimensions**: multiples of 16, longer side ≤ 3840, total pixels ≤ 8,294,400.

## Quality Options
| Quality   | Description                                    |
|-----------|------------------------------------------------|
| auto      | Model chooses quality (default)                |
| high      | Maximum quality                                |
| medium    | Balanced quality/speed                         |
| low       | Faster, lower quality                          |
| hd        | High detail (dall-e-3 only)                    |
| standard  | Standard detail (dall-e-3 only)                |
"""


@mcp.tool()
async def openai_list_embedding_models() -> str:
    """List all available text embedding models.

    Shows all models available for the embeddings endpoint.

    Returns:
        Table of all embedding models with descriptions.
    """
    # Last updated: 2026-04-25
    return """Available OpenAI Embedding Models:

| Model                    | Dimensions | Description                              |
|--------------------------|------------|------------------------------------------|
| text-embedding-3-small   | 1536       | Cost-efficient, good quality (default)   |
| text-embedding-3-large   | 3072       | Higher quality, larger vectors           |
| text-embedding-ada-002   | 1536       | Legacy model, widely supported           |

## Notes
- text-embedding-3 models support custom dimensions via the `dimensions` parameter
- text-embedding-ada-002 does not support custom dimensions
- Larger dimensions provide better quality but cost more

## Use Cases
- Semantic search and retrieval
- Text similarity and clustering
- Classification tasks
- Recommendation systems
"""


@mcp.tool()
async def openai_get_usage_guide() -> str:
    """Get a comprehensive guide for using the OpenAI tools.

    Provides detailed information on how to use all available OpenAI tools
    effectively, including examples and best practices.

    Returns:
        Complete usage guide for OpenAI tools.
    """
    # Last updated: 2026-04-25
    return """# OpenAI Tools Usage Guide

## Available Tools

### Chat Completion
**openai_chat_completion** - Generate text responses from a conversation
- messages: Conversation history (required)
- model: GPT model to use (default: gpt-4.1)
- max_tokens: Response length limit
- temperature: Creativity level (0-2, default: 1)
- n: Number of responses to generate

### Responses API
**openai_create_response** - Alternative completion API with more model variants
- input: Conversation messages (required)
- model: Model to use (default: gpt-4.1)
- background: Run in background mode

### Image Generation
**openai_generate_image** - Create images from text descriptions
- prompt: Image description (required)
- model: Image model (default: gpt-image-1)
- size: Image dimensions (default: 1024x1024)
- quality: Output quality (default: auto)
- n: Number of images (1-10)
- style: vivid or natural (dall-e-3)

### Image Editing
**openai_edit_image** - Modify existing images
- image: Reference image URL (required)
- prompt: Edit description (required)
- model: Image model (default: gpt-image-1)
- input_fidelity: How closely to follow reference

### Text Embeddings
**openai_create_embedding** - Convert text to vector representations
- input: Text to embed (required)
- model: Embedding model (default: text-embedding-3-small)
- dimensions: Custom output dimensions (optional)

### Task Retrieval
**openai_get_task** - Retrieve a single async image task
- id: Task ID returned by the original image request
- trace_id: Custom trace ID supplied on the original request
- At least one of 'id' or 'trace_id' must be provided

**openai_list_tasks** - List async image tasks (batch)
- ids: List of task IDs
- trace_ids: List of custom trace IDs
- application_id: List all tasks for an application
- user_id: List all tasks for an end user
- type: Filter by type ('images', 'images_generations', or 'images_edits')
- offset / limit: Pagination (default: 0 / 12)
- created_at_min / created_at_max: Unix timestamp range filter

### Information Tools
- **openai_list_chat_models** - List chat/completion models
- **openai_list_image_models** - List image generation models
- **openai_list_embedding_models** - List embedding models
- **openai_get_usage_guide** - This guide

## Example Usage

### Basic Chat
```
openai_chat_completion(
    messages=[{"role": "user", "content": "What is machine learning?"}]
)
```

### Chat with System Prompt
```
openai_chat_completion(
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python hello world"}
    ],
    model="gpt-4.1"
)
```

### Generate Image
```
openai_generate_image(
    prompt="A futuristic city with flying cars at sunset, photorealistic",
    model="gpt-image-1",
    size="1792x1024"
)
```

### Edit Image
```
openai_edit_image(
    image="https://example.com/photo.jpg",
    prompt="Add a rainbow in the sky",
    model="gpt-image-1"
)
```

### Create Embeddings
```
openai_create_embedding(
    input="The quick brown fox jumps over the lazy dog",
    model="text-embedding-3-small"
)
```

### Retrieve Async Task
```
# Generate an image with a callback URL and a custom trace_id
openai_generate_image(
    prompt="A watercolor cat on a desk",
    model="gpt-image-1",
    callback_url="https://webhook.site/your-uuid",
    trace_id="my-custom-trace-001"
)
# The task is persisted server-side; poll for the result later
openai_get_task(trace_id="my-custom-trace-001")
```

## Best Practices

1. **Model selection**: Use gpt-4.1 for general tasks, o4-mini for complex reasoning
2. **Temperature**: Lower (0.1-0.3) for factual tasks, higher (0.7-1.0) for creative tasks
3. **Tokens**: Set max_tokens when you need predictable response lengths
4. **Images**: Use 1024x1024 for general images, larger for detail-rich content
5. **Embeddings**: text-embedding-3-small is cost-efficient for most use cases
"""
