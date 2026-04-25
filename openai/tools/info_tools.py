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
| nano-banana      | Nano Banana - fast, efficient generation          |
| nano-banana-2    | Nano Banana 2 - improved version                  |
| nano-banana-pro  | Nano Banana Pro - highest quality                 |

## Supported Sizes
| Size        | Aspect Ratio    | Notes                        |
|-------------|-----------------|------------------------------|
| 1024x1024   | 1:1 (Square)    | Default, works with all      |
| 1792x1024   | ~16:9 (Wide)    | Landscape                    |
| 1024x1792   | ~9:16 (Tall)    | Portrait                     |
| 1536x1024   | 3:2             | Wide format                  |
| 1024x1536   | 2:3             | Tall format                  |
| 256x256     | 1:1             | Small, legacy                |
| 512x512     | 1:1             | Medium, legacy               |
| auto        | Varies          | Model chooses                |

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

## Best Practices

1. **Model selection**: Use gpt-4.1 for general tasks, o4-mini for complex reasoning
2. **Temperature**: Lower (0.1-0.3) for factual tasks, higher (0.7-1.0) for creative tasks
3. **Tokens**: Set max_tokens when you need predictable response lengths
4. **Images**: Use 1024x1024 for general images, larger for detail-rich content
5. **Embeddings**: text-embedding-3-small is cost-efficient for most use cases
"""
