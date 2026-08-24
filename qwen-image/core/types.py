"""Type definitions for Qwen Image MCP server."""

from typing import Literal

QwenImageModel = Literal["qwen-image-3.0", "qwen-image-3.0-pro"]
PromptExtendMode = Literal["direct", "agent"]
TaskAction = Literal["retrieve", "retrieve_batch"]
DEFAULT_MODEL: QwenImageModel = "qwen-image-3.0"
