"""Type definitions for GLM MCP server."""

from typing import Literal

# GLM model options
GlmModel = Literal[
    "glm-5.1",
    "glm-4.7",
    "glm-4.6",
    "glm-3-turbo",
]

# Reasoning effort options
ReasoningEffort = Literal["minimal", "low", "medium", "high"]

# Service tier options
ServiceTier = Literal["auto", "default", "flex", "scale", "priority"]

# Default values
DEFAULT_MODEL: GlmModel = "glm-4.7"
