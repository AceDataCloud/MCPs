"""Prompt templates module for MCP GLM server."""

# Import all prompts to register them with the MCP server
from prompts import glm_prompts  # noqa: F401

__all__ = [
    "glm_prompts",
]
