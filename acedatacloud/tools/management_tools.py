"""Register typed tools for each fixed operation in the management contract."""

import base64
import inspect
from typing import Annotated, Any, Literal
from urllib.parse import quote

from pydantic import BaseModel, ConfigDict, Field, create_model

from contracts.management_surface import SURFACE_TOOLS
from core.client import client, get_request_subject
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json
from tools.blog_tools import Category


def _type(schema: dict[str, Any], name: str) -> Any:
    choices = schema.get("enum")
    if choices and all(isinstance(value, str | int | float | bool) for value in choices):
        kind: Any = Literal[tuple(choices)]  # type: ignore[valid-type]
    elif schema.get("type") == "object" and schema.get("properties"):
        kind = _model(schema, name)
    elif schema.get("type") == "array":
        kind = list[_type(schema.get("items", {}), name + "Item")]  # type: ignore[misc]
    else:
        kind = {"integer": int, "number": float, "boolean": bool, "object": dict[str, Any]}.get(
            str(schema.get("type", "unknown")), Any
        )
    constraints: dict[str, Any] = {"description": schema.get("description", name)}
    for key, value in [
        ("minLength", "min_length"),
        ("maxLength", "max_length"),
        ("minItems", "min_length"),
        ("maxItems", "max_length"),
    ]:
        if key in schema:
            constraints[value] = schema[key]
    if kind in (int, float):
        for key, value in [("minimum", "ge"), ("maximum", "le")]:
            if key in schema:
                constraints[value] = int(schema[key]) if kind is int else float(schema[key])
    if schema.get("nullable"):
        kind = kind | None
    return Annotated[kind, Field(**constraints)]


def _model(schema: dict[str, Any], name: str) -> type[BaseModel]:
    required = set(schema.get("required", []))
    fields: dict[str, Any] = {}
    for key, value in schema.get("properties", {}).items():
        kind = _type(value, name + "_" + key)
        fields[key] = (kind if key in required else kind | None, ... if key in required else None)
    return create_model(name, __config__=ConfigDict(extra="forbid"), **fields)


def _plain(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", exclude_unset=True)
    if isinstance(value, list):
        return [_plain(item) for item in value]
    if isinstance(value, dict):
        return {key: _plain(item) for key, item in value.items()}
    return value


def build_tool(spec: dict[str, Any]) -> Any:
    """Build one native tool with a fixed method/path and validated request fields."""
    parameters: list[inspect.Parameter] = []
    names: set[str] = set()
    body_names: dict[str, str] = {}
    query_names: dict[str, str] = {}
    for key in spec["path_parameters"]:
        parameters.append(inspect.Parameter(key, inspect.Parameter.KEYWORD_ONLY, annotation=str))
        names.add(key)
    for schema_name, mapping in [("body_schema", body_names), ("query_schema", query_names)]:
        schema = spec[schema_name]
        required = set(schema.get("required", []))
        for key, value in schema.get("properties", {}).items():
            argument = (
                key
                if key not in names and key != "confirm"
                else schema_name.split("_")[0] + "_" + key
            )
            names.add(argument)
            mapping[key] = argument
            kind = (
                Category
                if key == "category"
                and spec["path"] in {"/blogs/", "/blogs/admin/", "/blogs/admin/{id}/"}
                else _type(value, spec["name"] + "_" + argument)
            )
            parameters.append(
                inspect.Parameter(
                    argument,
                    inspect.Parameter.KEYWORD_ONLY,
                    annotation=kind if key in required else kind | None,
                    default=inspect.Parameter.empty if key in required else None,
                )
            )
    if spec["confirm"]:
        parameters.append(
            inspect.Parameter(
                "confirm", inspect.Parameter.KEYWORD_ONLY, annotation=bool, default=False
            )
        )

    async def invoke(**kwargs: Any) -> str:
        # Preview before touching even the authentication/identity endpoint.
        body = {
            key: _plain(kwargs[arg])
            for key, arg in body_names.items()
            if kwargs.get(arg) is not None
        }
        query = {
            key: _plain(kwargs[arg])
            for key, arg in query_names.items()
            if kwargs.get(arg) is not None
        }
        target = {
            "path": {key: kwargs[key] for key in spec["path_parameters"]},
            "body": body,
            "query": query,
        }
        if spec["confirm"] and not kwargs.get("confirm", False):
            return confirmation_required(spec["method"] + " " + spec["path"], target)
        endpoint = spec["path"]
        for key in spec["path_parameters"]:
            value = str(kwargs[key])
            if any(part in {".", ".."} for part in value.split("/")):
                return error_json(
                    "validation_error", "Path identifiers cannot contain traversal segments"
                )
            endpoint = endpoint.replace("{" + key + "}", quote(value, safe=""))
        try:
            owner_collections = {
                "/applications/": "applications:read:any",
                "/credentials/": "credentials:write:any",
                "/orders/": "orders:read:any",
                "/platform-tokens/": None,
                "/usage/apis/": "usage:read:any",
                "/usage/proxies/": "usage:read:any",
                "/coin-infos/": None,
                "/distribution-statuses/": "distribution:read:any",
            }
            if spec["method"] == "GET" and spec["path"] in owner_collections:
                subject = await get_request_subject()
                granted = set(subject.get("permissions", []))
                # An unrelated administrative grant must never broaden this query.
                cross_account = owner_collections[spec["path"]]
                if not cross_account or cross_account not in granted:
                    owner_id = str(subject["id"])
                    requested_users = query.get("user_id")
                    if requested_users is not None and any(
                        user_id != owner_id
                        for user_id in (
                            requested_users
                            if isinstance(requested_users, list)
                            else [requested_users]
                        )
                    ):
                        return error_json(
                            "permission_denied",
                            "A cross-account query requires the matching account permission",
                        )
                    query["user_id"] = owner_id
            if spec.get("encoding") == "multipart":
                try:
                    content = base64.b64decode(body["content_base64"], validate=True)
                except (ValueError, KeyError):
                    return error_json(
                        "validation_error", "content_base64 must contain valid base64"
                    )
                result = await client.upload_file(
                    endpoint,
                    body["filename"],
                    content,
                    body.get("content_type") or "application/octet-stream",
                    fields={
                        key: value
                        for key, value in body.items()
                        if key not in {"filename", "content_base64", "content_type"}
                    },
                )
            else:
                result = await client.request_payload(
                    spec["method"],
                    endpoint,
                    params=query,
                    json_body=body if spec["method"] != "GET" else None,
                    auth_required=spec["authentication"] != "public",
                    display_endpoint=spec["path"],
                )
            return dumps(result, disclose=set(spec.get("disclose", [])))
        except PlatformError as error:
            return error_json(error.code, error.message)

    invoke.__name__ = spec["name"]
    permissions = ", ".join(spec["required_permissions"]) or spec["authentication"]
    invoke.__doc__ = spec["description"] + "\nRequired permissions: " + permissions
    invoke.__signature__ = inspect.Signature(parameters, return_annotation=str)  # type: ignore[attr-defined]
    return invoke


REGISTERED_TOOLS = {spec["name"]: build_tool(spec) for spec in SURFACE_TOOLS}
for function in REGISTERED_TOOLS.values():
    mcp.add_tool(function)
