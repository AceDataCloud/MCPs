"""Task polling tools for the Image2Text API."""

import asyncio
import json
from typing import Annotated

from pydantic import Field

from core.client import client
from core.exceptions import Image2TextAPIError, Image2TextAuthError
from core.server import mcp


@mcp.tool()
async def image2text_get_task(task_id: Annotated[str, Field(description="Task ID returned by an async image2text request.")]) -> str:
    """Poll an async image2text task."""
    if not task_id:
        return json.dumps({"error": "Validation Error", "message": "task_id is required"})
    try:
        result = await client.get_task(task_id=task_id)
        if result.get("status") == "processing":
            await asyncio.sleep(3)
        return json.dumps(result, ensure_ascii=False, indent=2)
    except Image2TextAuthError as e:
        return json.dumps({"error": "Authentication Error", "message": e.message})
    except Image2TextAPIError as e:
        return json.dumps({"error": "API Error", "message": e.message})
    except Exception as e:
        return json.dumps({"error": "Error retrieving task", "message": str(e)})
