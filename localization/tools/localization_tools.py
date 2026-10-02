"""Localization translation tools."""

import json
from typing import Annotated

from pydantic import Field

from core.client import (
    LocalizationExtension,
    LocalizationInput,
    LocalizationLocale,
    LocalizationModel,
    client,
)
from core.exceptions import LocalizationAPIError, LocalizationAuthError
from core.server import mcp


@mcp.tool()
async def localization_translate(
    input: Annotated[
        LocalizationInput,
        Field(description="Markdown string or JSON object to translate."),
    ],
    locale: Annotated[
        LocalizationLocale,
        Field(description="Target locale for the translated output."),
    ],
    extension: Annotated[
        LocalizationExtension,
        Field(description="Input/output format. Use 'md' for Markdown strings and 'json' for JSON objects."),
    ],
    model: Annotated[
        LocalizationModel | None,
        Field(description="Optional translation model to use."),
    ] = None,
) -> str:
    """Translate Markdown or JSON localization input to a target locale."""
    if extension == "md" and not isinstance(input, str):
        return json.dumps(
            {"error": "Validation Error", "message": "input must be a string when extension is md"}
        )
    if extension == "json" and not isinstance(input, dict):
        return json.dumps(
            {"error": "Validation Error", "message": "input must be an object when extension is json"}
        )

    try:
        result = await client.translate(
            input=input,
            locale=locale,
            extension=extension,
            model=model,
        )
        return json.dumps(result, ensure_ascii=False, indent=2)
    except LocalizationAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except LocalizationAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error translating localization input", "message": str(e)})
