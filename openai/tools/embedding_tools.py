"""Text embedding tools for OpenAI API."""

import json
from typing import Annotated, Any

from pydantic import Field

from core.client import client
from core.exceptions import OpenAIAPIError, OpenAIAuthError
from core.server import mcp
from core.types import (
    DEFAULT_EMBEDDING_ENCODING_FORMAT,
    DEFAULT_EMBEDDING_MODEL,
    EmbeddingEncodingFormat,
    EmbeddingModel,
)


@mcp.tool()
async def openai_create_embedding(
    input: Annotated[
        str,
        Field(
            description=(
                "Input text to embed. Can be a single string, an array of strings, "
                "or token arrays. The text to embed into a numerical vector representation."
            )
        ),
    ],
    model: Annotated[
        EmbeddingModel,
        Field(
            description=(
                "The embedding model to use. Options: 'text-embedding-3-small' (default, "
                "cost-efficient), 'text-embedding-3-large' (higher quality), "
                "'text-embedding-ada-002' (legacy)."
            )
        ),
    ] = DEFAULT_EMBEDDING_MODEL,
    encoding_format: Annotated[
        EmbeddingEncodingFormat,
        Field(
            description=(
                "The format of the returned embeddings. 'float' returns floating-point numbers "
                "(default), 'base64' returns base64-encoded data."
            )
        ),
    ] = DEFAULT_EMBEDDING_ENCODING_FORMAT,
    dimensions: Annotated[
        int | None,
        Field(
            description=(
                "Optional output embedding size. Supported by text-embedding-3 models. "
                "Reduces the embedding dimensions while maintaining quality."
            )
        ),
    ] = None,
) -> str:
    """Create text embeddings using OpenAI embedding models via AceDataCloud.

    Converts text into numerical vector representations that can be used for
    semantic search, text similarity, clustering, and other ML tasks.

    Use this when:
    - You need to compare semantic similarity between texts
    - You want to build a semantic search system
    - You need vector representations for machine learning

    Returns:
        JSON response containing the embedding vectors and usage information.
    """
    try:
        payload: dict[str, Any] = {
            "model": model,
            "input": input,
            "encoding_format": encoding_format,
        }

        if dimensions is not None:
            payload["dimensions"] = dimensions

        result = await client.embeddings(**payload)

        if not result:
            return json.dumps({"error": "No response received."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenAIAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenAIAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating embedding", "message": str(e)})
