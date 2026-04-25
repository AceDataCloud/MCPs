"""Prompts module for MCP OpenAI server."""

from core.server import mcp


@mcp.prompt()
def openai_usage_guide() -> str:
    """Guide for using OpenAI tools."""
    return """Use openai_chat_completion for conversational AI, openai_embeddings for text embeddings,
openai_image_generate for image generation, openai_responses for the responses API,
and openai_image_edit for image editing. Call openai_list_models to see available models."""


__all__: list[str] = []
