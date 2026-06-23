"""Runnable code-example tool — generated from the OpenAPI spec."""

import json
from typing import Any

from core.client import client
from core.config import settings
from core.exceptions import DocsError
from core.server import mcp

PUBLIC_STAGES = ["Beta", "Production"]


def _example_body(definition: dict, path: str, method: str) -> dict:
    """Best-effort example request body from an OpenAPI operation schema."""
    try:
        op = definition["paths"][path][method.lower()]
        content = op["requestBody"]["content"]["application/json"]
        schema = content.get("schema", {})
        if "example" in content:
            return content["example"]
        if "example" in schema:
            return schema["example"]
        body: dict[str, Any] = {}
        for name, prop in (schema.get("properties") or {}).items():
            if "example" in prop:
                body[name] = prop["example"]
            elif prop.get("default") is not None:
                body[name] = prop["default"]
            elif prop.get("enum"):
                body[name] = prop["enum"][0]
            elif name in (schema.get("required") or []):
                body[name] = f"<{name}>"
        return body
    except Exception:  # noqa: BLE001 - schema shape varies; fall back to empty body
        return {}


def _snippets(method: str, url: str, body: dict) -> dict[str, str]:
    body_json = json.dumps(body, ensure_ascii=False, indent=2)
    curl = (
        f"curl -X {method.upper()} '{url}' \\\n"
        f"  -H 'Authorization: Bearer YOUR_API_TOKEN' \\\n"
        f"  -H 'Content-Type: application/json' \\\n"
        f"  -d '{json.dumps(body, ensure_ascii=False)}'"
    )
    python = (
        "import requests\n\n"
        f'url = "{url}"\n'
        'headers = {"Authorization": "Bearer YOUR_API_TOKEN", "Content-Type": "application/json"}\n'
        f"payload = {body_json}\n"
        f"resp = requests.{method.lower()}(url, headers=headers, json=payload)\n"
        "print(resp.json())"
    )
    js = (
        f'const resp = await fetch("{url}", {{\n'
        f'  method: "{method.upper()}",\n'
        '  headers: { "Authorization": "Bearer YOUR_API_TOKEN", "Content-Type": "application/json" },\n'
        f"  body: JSON.stringify({json.dumps(body, ensure_ascii=False)})\n"
        "});\nconsole.log(await resp.json());"
    )
    return {"curl": curl, "python": python, "javascript": js}


@mcp.tool()
async def acedatacloud_get_code_example(api_path: str, lang: str = "all") -> str:
    """Generate a runnable code snippet for calling an AceData Cloud API.

    Args:
        api_path: The API path, e.g. "/suno/audios" or "/serp/google".
        lang: One of curl, python, javascript, or all (default all).
    """
    try:
        apis = await client.list_apis(path=api_path, stages=PUBLIC_STAGES)
        # Match path + public stage client-side so we never build an example for
        # the wrong API or a non-public stage if a backend filter isn't applied.
        api = next(
            (
                a
                for a in apis
                if isinstance(a, dict)
                and a.get("definition")
                and a.get("stage") in PUBLIC_STAGES
                and api_path in (a.get("path"), a.get("path2"))
            ),
            None,
        )
        if not api:
            return f"No public API with an OpenAPI spec found for path {api_path}."
        definition = api["definition"]
        method = (api.get("method") or "POST").upper()
        url = f"{settings.api_base_url}{api.get('path') or api_path}"
        body = _example_body(definition, api.get("path") or api_path, method)
        snippets = _snippets(method, url, body)
        if lang != "all" and lang in snippets:
            return snippets[lang]
        return json.dumps(snippets, ensure_ascii=False, indent=2)
    except DocsError as e:
        return f"Failed to build example: {e.message}"
