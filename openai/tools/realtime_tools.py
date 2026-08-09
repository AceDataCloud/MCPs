"""Realtime API helper tools for OpenAI."""

import json
from typing import Annotated

from pydantic import Field

from core.config import settings
from core.server import mcp
from core.types import DEFAULT_REALTIME_MODEL, RealtimeModel


@mcp.tool()
async def openai_get_realtime_connection_info(
    model: Annotated[
        RealtimeModel,
        Field(
            description=(
                "Realtime model to use. Options: 'gpt-realtime' (default) "
                "or 'gpt-realtime-2'."
            )
        ),
    ] = DEFAULT_REALTIME_MODEL,
) -> str:
    """Get connection details for the OpenAI Realtime WebSocket endpoint.

    Returns the AceDataCloud Realtime API WebSocket URL and model parameter.
    Clients should connect with an Authorization bearer token (or browser
    subprotocol token) and exchange OpenAI Realtime JSON events.
    """
    base_url = settings.api_base_url.rstrip("/")
    ws_base_url = base_url.replace("https://", "wss://", 1).replace("http://", "ws://", 1)
    return json.dumps(
        {
            "url": f"{ws_base_url}/v1/realtime?model={model}",
            "model": model,
            "audio_format": "pcm16 @ 24kHz mono",
            "events": [
                "session.update",
                "input_audio_buffer.append",
                "response.create",
                "response.output_audio.delta",
                "response.done",
            ],
        },
        ensure_ascii=False,
        indent=2,
    )
