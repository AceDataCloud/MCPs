#!/usr/bin/env python3
"""Reject Pydantic aliases that break FastMCP tool dispatch."""

from __future__ import annotations

import ast
import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(os.environ.get("MCP_ROOT", Path(__file__).resolve().parents[1])).resolve()


@dataclass(frozen=True)
class Violation:
    path: Path
    line: int
    tool: str
    parameter: str
    alias: str


def is_tool_decorator(node: ast.expr) -> bool:
    if isinstance(node, ast.Call):
        node = node.func
    return (
        isinstance(node, ast.Attribute)
        and node.attr == "tool"
        and isinstance(node.value, ast.Name)
        and node.value.id == "mcp"
    )


def imported_field_names(tree: ast.Module) -> tuple[set[str], set[str]]:
    field_names: set[str] = set()
    pydantic_names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.ImportFrom) and node.module in {
            "pydantic",
            "pydantic.fields",
        }:
            field_names.update(
                imported.asname or imported.name
                for imported in node.names
                if imported.name == "Field"
            )
        elif isinstance(node, ast.Import):
            pydantic_names.update(
                imported.asname or imported.name
                for imported in node.names
                if imported.name == "pydantic"
            )
    return field_names, pydantic_names


def type_aliases(tree: ast.Module) -> dict[str, ast.expr]:
    aliases: dict[str, ast.expr] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name):
                aliases[target.id] = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            if node.value is not None:
                aliases[node.target.id] = node.value
    return aliases


def field_aliases(
    expression: ast.expr | None,
    *,
    field_names: set[str],
    pydantic_names: set[str],
    aliases: dict[str, ast.expr],
    resolving: frozenset[str] = frozenset(),
) -> list[tuple[int, str]]:
    if expression is None:
        return []
    if isinstance(expression, ast.Name) and expression.id in aliases:
        if expression.id in resolving:
            return []
        return field_aliases(
            aliases[expression.id],
            field_names=field_names,
            pydantic_names=pydantic_names,
            aliases=aliases,
            resolving=resolving | {expression.id},
        )

    found: list[tuple[int, str]] = []
    for node in ast.walk(expression):
        if not isinstance(node, ast.Call):
            continue
        is_field = isinstance(node.func, ast.Name) and node.func.id in field_names
        is_qualified_field = (
            isinstance(node.func, ast.Attribute)
            and node.func.attr == "Field"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id in pydantic_names
        )
        if not (is_field or is_qualified_field):
            continue
        for keyword in node.keywords:
            if keyword.arg != "alias":
                continue
            value = (
                repr(keyword.value.value)
                if isinstance(keyword.value, ast.Constant)
                else ast.unparse(keyword.value)
            )
            found.append((keyword.value.lineno, value))
    return found


def parameter_expressions(
    node: ast.FunctionDef | ast.AsyncFunctionDef,
) -> list[tuple[ast.arg, ast.expr | None]]:
    positional = [*node.args.posonlyargs, *node.args.args]
    positional_defaults: list[ast.expr | None] = [None] * (
        len(positional) - len(node.args.defaults)
    ) + list(node.args.defaults)
    parameters = list(zip(positional, positional_defaults, strict=True))
    parameters.extend(zip(node.args.kwonlyargs, node.args.kw_defaults, strict=True))
    if node.args.vararg is not None:
        parameters.append((node.args.vararg, None))
    if node.args.kwarg is not None:
        parameters.append((node.args.kwarg, None))
    return parameters


def main() -> None:
    package_count = sum(1 for _ in ROOT.glob("*/pyproject.toml"))
    violations: list[Violation] = []
    tool_count = 0

    for path in sorted(ROOT.glob("*/tools/**/*.py")):
        tree = ast.parse(path.read_text(), filename=str(path))
        field_names, pydantic_names = imported_field_names(tree)
        aliases = type_aliases(tree)
        for node in ast.walk(tree):
            if not isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                continue
            if not any(
                is_tool_decorator(decorator) for decorator in node.decorator_list
            ):
                continue
            tool_count += 1
            for parameter, default in parameter_expressions(node):
                for expression in (parameter.annotation, default):
                    for line, alias in field_aliases(
                        expression,
                        field_names=field_names,
                        pydantic_names=pydantic_names,
                        aliases=aliases,
                    ):
                        violations.append(
                            Violation(
                                path=path.relative_to(ROOT),
                                line=line,
                                tool=node.name,
                                parameter=parameter.arg,
                                alias=alias,
                            )
                        )

    if tool_count == 0:
        raise SystemExit("MCP tool alias check found no @mcp.tool functions")
    if violations:
        details = "\n".join(
            f"- {item.path}:{item.line}: {item.tool} parameter {item.parameter!r} "
            f"uses alias={item.alias}; use validation_alias={item.alias}"
            for item in violations
        )
        raise SystemExit(f"Unsafe MCP tool parameter aliases:\n{details}")

    print(f"MCP tool aliases OK: {tool_count} tools across {package_count} packages")


if __name__ == "__main__":
    main()
