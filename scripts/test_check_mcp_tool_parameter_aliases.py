#!/usr/bin/env python3
"""Self-tests for the MCP tool parameter alias guard."""

from __future__ import annotations

import ast
import unittest

from check_mcp_tool_parameter_aliases import (
    field_aliases,
    imported_field_names,
    parameter_expressions,
    type_aliases,
)


def find_aliases(source: str) -> list[tuple[int, str]]:
    tree = ast.parse(source)
    field_names, pydantic_names = imported_field_names(tree)
    aliases = type_aliases(tree)
    function = next(
        node for node in tree.body if isinstance(node, ast.AsyncFunctionDef)
    )
    found: list[tuple[int, str]] = []
    for parameter, default in parameter_expressions(function):
        for expression in (parameter.annotation, default):
            found.extend(
                field_aliases(
                    expression,
                    field_names=field_names,
                    pydantic_names=pydantic_names,
                    aliases=aliases,
                )
            )
    return found


class AliasGuardTests(unittest.TestCase):
    def test_finds_inline_field_alias(self) -> None:
        source = """
from typing import Annotated
from pydantic import Field

async def tool(async_: Annotated[bool, Field(alias="async")]) -> None:
    pass
"""
        self.assertEqual(find_aliases(source)[0][1], "'async'")

    def test_finds_default_field_alias(self) -> None:
        source = """
from pydantic import Field

async def tool(async_: bool = Field(default=False, alias="async")) -> None:
    pass
"""
        self.assertEqual(find_aliases(source)[0][1], "'async'")

    def test_finds_reusable_annotation_with_renamed_field(self) -> None:
        source = """
from typing import Annotated
from pydantic import Field as PydanticField

AsyncOption = Annotated[bool, PydanticField(alias="async")]

async def tool(async_: AsyncOption = False) -> None:
    pass
"""
        self.assertEqual(find_aliases(source)[0][1], "'async'")

    def test_allows_validation_alias(self) -> None:
        source = """
from typing import Annotated
import pydantic as pd

async def tool(async_: Annotated[bool, pd.Field(validation_alias="async")]) -> None:
    pass
"""
        self.assertEqual(find_aliases(source), [])


if __name__ == "__main__":
    unittest.main()
