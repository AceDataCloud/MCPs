import argparse
import ast
import importlib
import inspect
import json
import os
import sys
import textwrap
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--backend", type=Path, required=True)
parser.add_argument("--output", type=Path, required=True)
args = parser.parse_args()
root = args.backend.resolve()
os.chdir(root)
sys.path.insert(0, str(root))
os.environ.pop("TENCENT_SSM_SECRET_NAME", None)
for node in ast.walk(ast.parse((root / "core/settings.py").read_text())):
    if (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and isinstance(node.func.value, ast.Name)
        and node.func.value.id == "env"
        and node.args
        and isinstance(node.args[0], ast.Constant)
    ):
        name = node.args[0].value
        if len(node.args) == 1 and not any(k.arg == "default" for k in node.keywords):
            os.environ.setdefault(
                name,
                "0"
                if node.func.attr in ("int", "float")
                else "false"
                if node.func.attr == "bool"
                else "test",
            )
from environs import Env

Env.read_env = lambda *_args, **_kwargs: None
os.environ["DJANGO_SETTINGS_MODULE"] = "core.settings"
os.environ["APP_ENV"] = "test"
from loguru import logger

logger.remove()
import django

django.setup()
import contextlib
from types import SimpleNamespace

from django.urls import URLResolver, get_resolver
from rest_framework.request import Request
from rest_framework.schemas.openapi import AutoSchema
from rest_framework.test import APIRequestFactory

rows = []


def shape(value):
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    if isinstance(value, list):
        return {"type": "array", "items": {"type": "string"}}
    if isinstance(value, dict):
        return {"type": "object"}
    return {"type": "string"}


def source_inputs(view, method):
    handler = inspect.unwrap(getattr(view, view.action or method, None))
    for cell in getattr(handler, "__closure__", None) or []:
        if (
            inspect.isfunction(cell.cell_contents)
            and cell.cell_contents.__name__ == view.__class__.__name__
        ):
            handler = inspect.unwrap(cell.cell_contents)
    try:
        source = textwrap.dedent(inspect.getsource(handler))
        module = importlib.import_module(view.__class__.__module__)
        if method == "get":
            for extra in ("get_queryset", "get_serializer_context"):
                function = getattr(view, extra, None)
                if function is not None:
                    with contextlib.suppress(OSError, TypeError):
                        source += "\n" + textwrap.dedent(
                            inspect.getsource(inspect.unwrap(function))
                        )
        tree = ast.parse(source)
        for node in list(ast.walk(tree)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                function = getattr(module, node.func.id, None)
                if inspect.isfunction(function) and function.__module__ == module.__name__:
                    with contextlib.suppress(OSError, TypeError):
                        source += "\n" + textwrap.dedent(
                            inspect.getsource(inspect.unwrap(function))
                        )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "self"
                and node.func.attr.startswith("_")
            ):
                nested = getattr(view, node.func.attr, None)
                if nested is not None:
                    with contextlib.suppress(OSError, TypeError):
                        source += "\n" + textwrap.dedent(inspect.getsource(inspect.unwrap(nested)))
        tree = ast.parse(source)
    except (OSError, TypeError):
        return {}, {}, [], False
    body = {}
    query = {}
    actions = set()
    serializer = None
    module = importlib.import_module(view.__class__.__module__)
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id.endswith("Serializer")
            and any(k.arg == "data" for k in node.keywords)
        ):
            candidate = getattr(module, node.func.id, None)
            if candidate is None:
                for imported in ast.walk(tree):
                    if isinstance(imported, ast.ImportFrom) and any(
                        a.name == node.func.id for a in imported.names
                    ):
                        with contextlib.suppress(ImportError, AttributeError):
                            candidate = getattr(
                                importlib.import_module(imported.module), node.func.id
                            )
            if candidate:
                with contextlib.suppress(Exception):
                    serializer = AutoSchema().map_serializer(candidate())
        if (
            isinstance(node, ast.Compare)
            and isinstance(node.left, ast.Name)
            and node.left.id in {"action", "action_name"}
        ):
            for c in node.comparators:
                if isinstance(c, ast.Constant) and isinstance(c.value, str):
                    actions.add(c.value)
                elif isinstance(c, ast.Set | ast.List | ast.Tuple):
                    actions.update(
                        n.value
                        for n in c.elts
                        if isinstance(n, ast.Constant) and isinstance(n.value, str)
                    )
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr in {"get", "getlist"}
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            target = ast.unparse(node.func.value)
            key = node.args[0].value
            if key in {"HTTP_AUTHORIZATION"}:
                continue
            destination = (
                query
                if target.endswith((".query_params", ".GET"))
                or target in {"params", "query_params"}
                else body
                if target.endswith(".data") or target in {"data", "payload", "body"}
                else None
            )
            if destination is not None:
                default = (
                    node.args[1].value
                    if len(node.args) > 1 and isinstance(node.args[1], ast.Constant)
                    else None
                )
                field = shape(default) if default is not None else {}
                if node.func.attr == "getlist":
                    field = {"type": "array", "items": {"type": "string"}}
                if (
                    key
                    in {
                        "metadata",
                        "context",
                        "audience_rule",
                        "guardrail_thresholds",
                        "config",
                        "configuration",
                        "custom_package",
                        "filters",
                        "answers",
                        "snapshot",
                        "settings",
                    }
                    and default is None
                ):
                    field = {"type": "object"}
                if key in {
                    "ids",
                    "user_ids",
                    "application_ids",
                    "package_ids",
                    "recipient_ids",
                    "selected_user_ids",
                    "models",
                    "tags",
                }:
                    field = {"type": "array", "items": {"type": "string"}}
                if key.startswith(("is_", "allow_")) or key in {
                    "enabled",
                    "disabled",
                    "visible",
                    "public",
                    "sending_enabled",
                    "sponsor",
                }:
                    field = {"type": "boolean"}
                destination[key] = field
    mapping = getattr(view, "required_permissions", {})
    if view.action is None:
        actions.update(
            k
            for k in mapping
            if k not in {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
        )
    unsupported = False
    if method in {"post", "put", "patch", "delete"} and view.action in {
        None,
        "create",
        "update",
        "partial_update",
        "destroy",
    }:
        target = getattr(
            view,
            "create" if method == "post" else "destroy" if method == "delete" else "update",
            None,
        )
        try:
            src = inspect.getsource(target)
            unsupported = "raise MethodNotAllowed" in src and len(src.splitlines()) <= 5
        except (OSError, TypeError):
            pass
    return (
        serializer or ({"type": "object", "properties": body} if body else None),
        query,
        sorted(actions),
        unsupported,
    )


def walk(patterns, prefix=""):
    for pattern in patterns:
        path = prefix + str(pattern.pattern)
        if isinstance(pattern, URLResolver):
            walk(pattern.url_patterns, path)
            continue
        callback = pattern.callback
        cls = getattr(callback, "cls", None)
        if cls is None:
            rows.append({"path": path, "function": callback.__name__, "methods": []})
            continue
        view = cls(**getattr(callback, "initkwargs", {}))
        view.kwargs = {}
        view.format_kwarg = None
        actions = getattr(callback, "actions", {})
        for method in ["get", "post", "put", "patch", "delete"]:
            if actions and method not in actions:
                continue
            if not actions and not hasattr(view, method):
                continue
            if method not in view.http_method_names:
                continue
            view.action = actions.get(method)
            view.request = Request(APIRequestFactory().generic(method.upper(), "/api/v1/" + path))
            view.request.user = SimpleNamespace(
                id="test", is_authenticated=True, is_superuser=True, permissions=[]
            )
            scope = getattr(view, "required_permission", None)
            mapping = (
                getattr(view, "required_permissions", None)
                or getattr(view, "required_scopes", None)
                or {}
            )
            scope = mapping.get(view.action, mapping.get(method.upper(), scope))
            schema = AutoSchema()
            schema._view = view
            request_schema = None
            error = None
            if method != "get":
                try:
                    serializer = view.get_serializer()
                    request_schema = schema.map_serializer(serializer)
                except Exception as exc:
                    error = type(exc).__name__ + ": " + str(exc)[:160]
            custom_body, queries, action_choices, unsupported = source_inputs(view, method)
            if custom_body is not None:
                request_schema = custom_body
                error = None
            rows.append(
                {
                    "path": path,
                    "queries": queries,
                    "action_choices": action_choices,
                    "unsupported": unsupported,
                    "method": method.upper(),
                    "class": cls.__name__,
                    "module": cls.__module__,
                    "action": view.action,
                    "scope": scope,
                    "permissions": [type(p).__name__ for p in view.get_permissions()],
                    "body": request_schema,
                    "schema_error": error,
                    "filters": getattr(view, "filterset_fields", None),
                    "ordering": getattr(view, "ordering_fields", None),
                }
            )


walk(get_resolver("app.urls").url_patterns)
args.output.write_text(json.dumps(rows, indent=2, default=str) + "\n")
print("Resolved operations:", len(rows))
print("Body schemas:", sum(bool(r.get("body")) for r in rows))
