"""Model information tools for Qwen Image 3."""

from core.server import mcp


@mcp.tool()
async def qwen_image_list_models() -> str:
    """List Qwen Image 3 models and their intended use."""
    return """| Model | Best for | Output |\n|---|---|---|\n| `qwen-image-3.0` | Fast, cost-effective production | 1K/2K |\n| `qwen-image-3.0-pro` | Complex layouts and fine detail | 1K/2K |"""
