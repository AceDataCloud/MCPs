"""Reusable Qwen Image workflow guidance."""

from core.server import mcp


@mcp.prompt()
def qwen_image_workflow() -> str:
    """Explain the Qwen Image generation and editing workflow."""
    return """Use qwen_image_generate for text-to-image and qwen_image_edit for one to three reference images. Use qwen-image-3.0 for throughput and value, or qwen-image-3.0-pro for complex layouts and detail. Keep the returned task_id and poll qwen_image_get_task every 15 seconds until terminal."""
