"""Voice cloning tools for Digital Human."""

import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import DigitalHumanAPIError, DigitalHumanAuthError
from core.server import mcp
from core.types import DEFAULT_VOICE_LANGUAGE, DigitalHumanVoiceLanguage
from core.utils import format_voice_result


@mcp.tool()
async def digitalhuman_clone_voice(
    audio_url: Annotated[
        str,
        Field(description="Public URL of a clean 10-20 second voice sample.", min_length=1),
    ],
    lang: Annotated[
        DigitalHumanVoiceLanguage,
        Field(description="Language of the reference audio: zh or en."),
    ] = DEFAULT_VOICE_LANGUAGE,
    name: Annotated[
        str | None,
        Field(description="Optional label for the cloned voice."),
    ] = None,
    async_: Annotated[
        bool | None,
        Field(alias="async", description="Whether to return immediately with a task_id."),
    ] = None,
) -> str:
    """Clone a voice for later Digital Human TTS use."""
    payload = {
        "audio_url": audio_url,
        "lang": lang,
        "name": name,
        "async": async_,
    }
    try:
        return format_voice_result(await client.clone_voice(payload))
    except DigitalHumanAuthError as exc:
        return json.dumps({"error": "Authentication Error", "message": exc.message})
    except DigitalHumanAPIError as exc:
        return json.dumps({"error": "API Error", "message": exc.message})
    except Exception as exc:
        return json.dumps({"error": "Error cloning voice", "message": str(exc)})
