"""Type definitions for OpenAI MCP server."""

from typing import Literal

# Chat completion model options
ChatModel = Literal[
    "gpt-5.5",
    "gpt-5.5-pro",
    "gpt-5.4",
    "gpt-5.4-pro",
    "gpt-5.2",
    "gpt-5.1",
    "gpt-5.1-all",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4",
    "gpt-4.1",
    "gpt-4.1-mini",
    "gpt-4.1-nano",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-all",
    "gpt-4o-image",
    "gpt-4o-mini",
    "gpt-35-turbo-16k",
    "o1",
    "o1-mini",
    "o1-pro",
    "o3",
    "o3-mini",
    "o3-pro",
    "o4-mini",
]

# Responses API model options
ResponsesModel = Literal[
    "gpt-5.5",
    "gpt-5.5-pro",
    "gpt-5.4",
    "gpt-5.4-pro",
    "gpt-5.1",
    "gpt-5.1-all",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4",
    "gpt-4-all",
    "gpt-4-turbo",
    "gpt-4-turbo-preview",
    "gpt-4-vision-preview",
    "gpt-4.1",
    "gpt-4.1-2025-04-14",
    "gpt-4.1-mini",
    "gpt-4.1-mini-2025-04-14",
    "gpt-4.1-nano",
    "gpt-4.1-nano-2025-04-14",
    "gpt-4.5-preview",
    "gpt-4.5-preview-2025-02-27",
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-11-20",
    "gpt-4o-all",
    "gpt-4o-image",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-4o-mini-search-preview",
    "gpt-4o-mini-search-preview-2025-03-11",
    "gpt-4o-search-preview",
    "gpt-4o-search-preview-2025-03-11",
    "gpt-35-turbo-16k",
    "o1",
    "o1-2024-12-17",
    "o1-all",
    "o1-mini",
    "o1-mini-2024-09-12",
    "o1-mini-all",
    "o1-preview",
    "o1-preview-2024-09-12",
    "o1-preview-all",
    "o1-pro",
    "o1-pro-2025-03-19",
    "o1-pro-all",
    "o3",
    "o3-2025-04-16",
    "o3-all",
    "o3-mini",
    "o3-mini-2025-01-31",
    "o3-mini-2025-01-31-high",
    "o3-mini-2025-01-31-low",
    "o3-mini-2025-01-31-medium",
    "o3-mini-all",
    "o3-mini-high",
    "o3-mini-high-all",
    "o3-mini-low",
    "o3-mini-medium",
    "o3-pro",
    "o3-pro-2025-06-10",
    "o4-mini",
    "o4-mini-2025-04-16",
    "o4-mini-all",
    "o4-mini-high-all",
]

# Embedding model options
EmbeddingModel = Literal[
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
]

# Embedding encoding format options
EmbeddingEncodingFormat = Literal["float", "base64"]

# Image generation/edit model options
ImageModel = Literal[
    "dall-e-3",
    "gpt-image-1",
    "gpt-image-1.5",
    "gpt-image-2",
    "nano-banana",
    "nano-banana-2",
    "nano-banana-pro",
]

# Image size options
ImageSize = Literal[
    "1024x1024",
    "1792x1024",
    "1024x1792",
    "1536x1024",
    "1024x1536",
    "256x256",
    "512x512",
    "auto",
]

# Image edit size options
ImageEditSize = Literal[
    "1024x1024",
    "1536x1024",
    "1024x1536",
    "256x256",
    "512x512",
    "auto",
]

# Image quality options
ImageQuality = Literal["auto", "high", "medium", "low", "hd", "standard"]

# Image edit quality options
ImageEditQuality = Literal["auto", "high", "medium", "low", "standard"]

# Image output format options
ImageOutputFormat = Literal["png", "jpeg", "webp"]

# Image response format options
ImageResponseFormat = Literal["url", "b64_json"]

# Image style options (dall-e-3)
ImageStyle = Literal["vivid", "natural"]

# Image background options
ImageBackground = Literal["transparent", "opaque", "auto"]

# Image moderation options
ImageModeration = Literal["low", "auto"]

# Image input fidelity options
ImageInputFidelity = Literal["high", "low"]

# === Default values ===

DEFAULT_CHAT_MODEL: ChatModel = "gpt-4.1"
DEFAULT_RESPONSES_MODEL: ResponsesModel = "gpt-4.1"
DEFAULT_EMBEDDING_MODEL: EmbeddingModel = "text-embedding-3-small"
DEFAULT_IMAGE_MODEL: ImageModel = "gpt-image-1"
DEFAULT_IMAGE_SIZE: ImageSize = "1024x1024"
DEFAULT_IMAGE_QUALITY: ImageQuality = "auto"
DEFAULT_IMAGE_OUTPUT_FORMAT: ImageOutputFormat = "png"
DEFAULT_IMAGE_RESPONSE_FORMAT: ImageResponseFormat = "url"
DEFAULT_EMBEDDING_ENCODING_FORMAT: EmbeddingEncodingFormat = "float"
