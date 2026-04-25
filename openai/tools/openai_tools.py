"""OpenAI API tools for chat completions, embeddings, image generation, responses, and image editing."""

from __future__ import annotations

import json
from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client
from core.exceptions import OpenaiAPIError, OpenaiAuthError
from core.server import mcp

ChatCompletionModel = Literal[
    "gpt-5.5",
    "gpt-5.5-pro",
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

EmbeddingModel = Literal[
    "text-embedding-3-small",
    "text-embedding-3-large",
    "text-embedding-ada-002",
]

ImageModel = Literal[
    "dall-e-3",
    "gpt-image-1",
    "gpt-image-1.5",
    "gpt-image-2",
    "nano-banana",
    "nano-banana-2",
    "nano-banana-pro",
]

ResponsesModel = Literal[
    "gpt-5.5",
    "gpt-5.5-pro",
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


@mcp.tool()
async def openai_chat_completion(
    model: Annotated[
        ChatCompletionModel,
        Field(description="The model to use for chat completion. Default is 'gpt-4o'."),
    ] = "gpt-4o",
    messages: Annotated[
        list[dict[str, Any]],
        Field(
            description="List of message objects. Each message must have 'role' (system/user/assistant) and 'content' (string) fields."
        ),
    ] = None,  # type: ignore[assignment]
    n: Annotated[
        int | None,
        Field(description="Number of completions to generate. Default is 1."),
    ] = None,
    stream: Annotated[
        bool | None,
        Field(description="Whether to stream the response. Default is false."),
    ] = None,
    max_tokens: Annotated[
        int | None,
        Field(description="Maximum number of tokens to generate."),
    ] = None,
    temperature: Annotated[
        float | None,
        Field(description="Sampling temperature between 0 and 2. Higher values produce more random output."),
    ] = None,
    response_format: Annotated[
        dict[str, Any] | None,
        Field(description="Format of the response, e.g. {'type': 'json_object'} for JSON output."),
    ] = None,
    tools: Annotated[
        list[dict[str, Any]] | None,
        Field(description="List of tools (functions) the model may call."),
    ] = None,
    tool_choice: Annotated[
        str | dict[str, Any] | None,
        Field(description="Controls which tool is called. Can be 'none', 'auto', or a specific tool."),
    ] = None,
) -> str:
    """Perform a chat completion using the OpenAI API.

    Creates a completion for the provided messages using the specified model.

    Args:
        model: The model to use for chat completion.
        messages: List of message objects with 'role' and 'content'.
        n: Number of completions to generate.
        stream: Whether to stream the response.
        max_tokens: Maximum number of tokens to generate.
        temperature: Sampling temperature between 0 and 2.
        response_format: Format of the response.
        tools: List of tools the model may call.
        tool_choice: Controls which tool is called.

    Returns:
        JSON string containing the chat completion response.

    Example:
        openai_chat_completion(
            model="gpt-4o",
            messages=[{"role": "user", "content": "Hello!"}]
        )
    """
    try:
        payload: dict[str, Any] = {"model": model}

        if messages is not None:
            payload["messages"] = messages
        else:
            payload["messages"] = []

        if n is not None:
            payload["n"] = n
        if stream is not None:
            payload["stream"] = stream
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if response_format is not None:
            payload["response_format"] = response_format
        if tools is not None:
            payload["tools"] = tools
        if tool_choice is not None:
            payload["tool_choice"] = tool_choice

        result = await client.chat_completion(**payload)

        if not result:
            return json.dumps({"error": "No response from chat completion API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenaiAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenaiAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error performing chat completion", "message": str(e)})


@mcp.tool()
async def openai_embeddings(
    model: Annotated[
        EmbeddingModel,
        Field(description="The model to use for embeddings. Default is 'text-embedding-3-small'."),
    ] = "text-embedding-3-small",
    input: Annotated[
        str | list[str],
        Field(description="The text(s) to embed. Can be a single string or list of strings."),
    ] = "",
    encoding_format: Annotated[
        Literal["float", "base64"] | None,
        Field(description="The format of the embeddings. Options: 'float' (default) or 'base64'."),
    ] = None,
    dimensions: Annotated[
        int | None,
        Field(description="Number of dimensions for the output embeddings (only supported by text-embedding-3 models)."),
    ] = None,
) -> str:
    """Create embeddings for input text using the OpenAI embeddings API.

    Args:
        model: The model to use for embeddings.
        input: The text(s) to embed.
        encoding_format: The format of the embeddings ('float' or 'base64').
        dimensions: Number of dimensions for the output embeddings.

    Returns:
        JSON string containing the embeddings response.

    Example:
        openai_embeddings(model="text-embedding-3-small", input="Hello world")
    """
    try:
        payload: dict[str, Any] = {"model": model, "input": input}

        if encoding_format is not None:
            payload["encoding_format"] = encoding_format
        if dimensions is not None:
            payload["dimensions"] = dimensions

        result = await client.embeddings(**payload)

        if not result:
            return json.dumps({"error": "No response from embeddings API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenaiAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenaiAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error creating embeddings", "message": str(e)})


@mcp.tool()
async def openai_image_generate(
    prompt: Annotated[
        str,
        Field(description="A text description of the desired image(s). Required."),
    ],
    model: Annotated[
        ImageModel,
        Field(description="The model to use for image generation. Default is 'gpt-image-1'."),
    ] = "gpt-image-1",
    n: Annotated[
        int | None,
        Field(description="Number of images to generate (default: 1)."),
    ] = None,
    size: Annotated[
        str | None,
        Field(description="Size of the generated image. Options: '256x256', '512x512', '1024x1024', '1792x1024', '1024x1792'."),
    ] = None,
    quality: Annotated[
        str | None,
        Field(description="Quality of the image. Options: 'standard', 'hd', 'low', 'medium', 'high', 'auto'."),
    ] = None,
    style: Annotated[
        Literal["vivid", "natural"] | None,
        Field(description="Style of the image. Options: 'vivid' (hyper-real) or 'natural' (more natural)."),
    ] = None,
    background: Annotated[
        Literal["transparent", "opaque", "auto"] | None,
        Field(description="Background type. Options: 'transparent', 'opaque', 'auto'."),
    ] = None,
    moderation: Annotated[
        str | None,
        Field(description="Moderation level for the image content."),
    ] = None,
    output_format: Annotated[
        Literal["png", "jpeg", "webp"] | None,
        Field(description="Output image format. Options: 'png', 'jpeg', 'webp'."),
    ] = None,
    output_compression: Annotated[
        int | None,
        Field(description="Compression level for jpeg/webp output (0-100)."),
    ] = None,
    response_format: Annotated[
        Literal["url", "b64_json"] | None,
        Field(description="Format of the response. Options: 'url' or 'b64_json'."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="URL to receive async callback when image generation is complete."),
    ] = None,
) -> str:
    """Generate images from a text prompt using the OpenAI image generation API.

    Args:
        prompt: A text description of the desired image(s).
        model: The model to use for image generation.
        n: Number of images to generate.
        size: Size of the generated image.
        quality: Quality of the image.
        style: Style of the image ('vivid' or 'natural').
        background: Background type.
        moderation: Moderation level.
        output_format: Output image format.
        output_compression: Compression level for jpeg/webp.
        response_format: Format of the response ('url' or 'b64_json').
        callback_url: URL for async callback.

    Returns:
        JSON string containing the image generation response.

    Example:
        openai_image_generate(prompt="A beautiful sunset over the ocean", model="gpt-image-1")
    """
    try:
        payload: dict[str, Any] = {"prompt": prompt, "model": model}

        if n is not None:
            payload["n"] = n
        if size is not None:
            payload["size"] = size
        if quality is not None:
            payload["quality"] = quality
        if style is not None:
            payload["style"] = style
        if background is not None:
            payload["background"] = background
        if moderation is not None:
            payload["moderation"] = moderation
        if output_format is not None:
            payload["output_format"] = output_format
        if output_compression is not None:
            payload["output_compression"] = output_compression
        if response_format is not None:
            payload["response_format"] = response_format
        if callback_url is not None:
            payload["callback_url"] = callback_url

        result = await client.image_generate(**payload)

        if not result:
            return json.dumps({"error": "No response from image generation API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenaiAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenaiAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error generating image", "message": str(e)})


@mcp.tool()
async def openai_responses(
    model: Annotated[
        ResponsesModel,
        Field(description="The model to use for the responses API. Default is 'gpt-4o'."),
    ] = "gpt-4o",
    input: Annotated[
        str | list[dict[str, Any]],
        Field(description="Input text or list of input items for the model."),
    ] = "",
    n: Annotated[
        int | None,
        Field(description="Number of responses to generate. Default is 1."),
    ] = None,
    stream: Annotated[
        bool | None,
        Field(description="Whether to stream the response. Default is false."),
    ] = None,
    max_tokens: Annotated[
        int | None,
        Field(description="Maximum number of output tokens to generate."),
    ] = None,
    temperature: Annotated[
        float | None,
        Field(description="Sampling temperature between 0 and 2."),
    ] = None,
    response_format: Annotated[
        dict[str, Any] | None,
        Field(description="Format of the response, e.g. {'type': 'json_object'}."),
    ] = None,
    tools: Annotated[
        list[dict[str, Any]] | None,
        Field(description="List of tools the model may use."),
    ] = None,
    background: Annotated[
        bool | None,
        Field(description="Whether to run the response in the background."),
    ] = None,
) -> str:
    """Create a response using the OpenAI responses API.

    Args:
        model: The model to use for the responses API.
        input: Input text or list of input items.
        n: Number of responses to generate.
        stream: Whether to stream the response.
        max_tokens: Maximum number of output tokens.
        temperature: Sampling temperature between 0 and 2.
        response_format: Format of the response.
        tools: List of tools the model may use.
        background: Whether to run in the background.

    Returns:
        JSON string containing the responses API response.

    Example:
        openai_responses(model="gpt-4o", input="Tell me about the solar system.")
    """
    try:
        payload: dict[str, Any] = {"model": model, "input": input}

        if n is not None:
            payload["n"] = n
        if stream is not None:
            payload["stream"] = stream
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if temperature is not None:
            payload["temperature"] = temperature
        if response_format is not None:
            payload["response_format"] = response_format
        if tools is not None:
            payload["tools"] = tools
        if background is not None:
            payload["background"] = background

        result = await client.responses(**payload)

        if not result:
            return json.dumps({"error": "No response from responses API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenaiAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenaiAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error calling responses API", "message": str(e)})


@mcp.tool()
async def openai_image_edit(
    image: Annotated[
        str,
        Field(description="URL or base64-encoded image to edit. Required."),
    ],
    prompt: Annotated[
        str,
        Field(description="A text description of the desired edits. Required."),
    ],
    model: Annotated[
        ImageModel,
        Field(description="The model to use for image editing. Default is 'gpt-image-1'."),
    ] = "gpt-image-1",
    n: Annotated[
        int | None,
        Field(description="Number of edited images to generate (default: 1)."),
    ] = None,
    size: Annotated[
        str | None,
        Field(description="Size of the output image. Options: '256x256', '512x512', '1024x1024'."),
    ] = None,
    quality: Annotated[
        str | None,
        Field(description="Quality of the image. Options: 'standard', 'hd', 'low', 'medium', 'high', 'auto'."),
    ] = None,
    background: Annotated[
        Literal["transparent", "opaque", "auto"] | None,
        Field(description="Background type. Options: 'transparent', 'opaque', 'auto'."),
    ] = None,
    input_fidelity: Annotated[
        str | None,
        Field(description="How closely the output follows the input image. Options: 'low', 'high'."),
    ] = None,
    output_format: Annotated[
        Literal["png", "jpeg", "webp"] | None,
        Field(description="Output image format. Options: 'png', 'jpeg', 'webp'."),
    ] = None,
    output_compression: Annotated[
        int | None,
        Field(description="Compression level for jpeg/webp output (0-100)."),
    ] = None,
    response_format: Annotated[
        Literal["url", "b64_json"] | None,
        Field(description="Format of the response. Options: 'url' or 'b64_json'."),
    ] = None,
    callback_url: Annotated[
        str | None,
        Field(description="URL to receive async callback when image editing is complete."),
    ] = None,
) -> str:
    """Edit an existing image using the OpenAI image editing API.

    Args:
        image: URL or base64-encoded image to edit.
        prompt: A text description of the desired edits.
        model: The model to use for image editing.
        n: Number of edited images to generate.
        size: Size of the output image.
        quality: Quality of the image.
        background: Background type.
        input_fidelity: How closely the output follows the input image.
        output_format: Output image format.
        output_compression: Compression level for jpeg/webp.
        response_format: Format of the response ('url' or 'b64_json').
        callback_url: URL for async callback.

    Returns:
        JSON string containing the image editing response.

    Example:
        openai_image_edit(image="https://example.com/image.png", prompt="Add a sunset background")
    """
    try:
        payload: dict[str, Any] = {"image": image, "prompt": prompt, "model": model}

        if n is not None:
            payload["n"] = n
        if size is not None:
            payload["size"] = size
        if quality is not None:
            payload["quality"] = quality
        if background is not None:
            payload["background"] = background
        if input_fidelity is not None:
            payload["input_fidelity"] = input_fidelity
        if output_format is not None:
            payload["output_format"] = output_format
        if output_compression is not None:
            payload["output_compression"] = output_compression
        if response_format is not None:
            payload["response_format"] = response_format
        if callback_url is not None:
            payload["callback_url"] = callback_url

        result = await client.image_edit(**payload)

        if not result:
            return json.dumps({"error": "No response from image editing API."})

        return json.dumps(result, ensure_ascii=False, indent=2)

    except OpenaiAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except OpenaiAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error editing image", "message": str(e)})
