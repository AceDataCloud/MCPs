#!/usr/bin/env python3
from __future__ import annotations

import unittest
from datetime import date

from registry_health import Finding, Surface, classify, compare_surfaces, health_url


class RegistryHealthTest(unittest.TestCase):
    def test_detects_missing_retired_and_contract_drift(self) -> None:
        local = {
            "active": Surface(
                "active", "active", "pkg-a", "https://a.example/mcp", "active"
            ),
            "retired": Surface(
                "retired", "retired", "pkg-r", "https://r.example/mcp", "retired"
            ),
            "changed": Surface(
                "changed", "changed", "pkg-local", "https://local.example/mcp", "active"
            ),
        }
        registry = {
            "retired": Surface(
                "", "retired", "pkg-r", "https://r.example/mcp", "active"
            ),
            "changed": Surface(
                "", "changed", "pkg-public", "https://public.example/mcp", "active"
            ),
            "orphan": Surface("", "orphan", "pkg-o", "https://o.example/mcp", "active"),
        }
        kinds = {finding.kind for finding in compare_surfaces(local, registry)}
        self.assertEqual(
            kinds,
            {
                "registry_missing",
                "retired_registry_active",
                "package_mismatch",
                "remote_mismatch",
                "local_missing",
            },
        )

    def test_exception_expires_and_then_blocks(self) -> None:
        findings = [
            Finding("registry_missing:one", "registry_missing", "one", "detail")
        ]
        exceptions = {
            "registry_missing:one": {
                "owner": "ecosystem",
                "expires_on": "2026-09-30",
                "action": "Resolve it.",
            }
        }
        _, blocking_before = classify(findings, exceptions, date(2026, 9, 9))
        _, blocking_after = classify(findings, exceptions, date(2026, 10, 1))
        self.assertEqual(blocking_before, [])
        self.assertEqual(len(blocking_after), 1)

    def test_health_url_uses_origin_only(self) -> None:
        self.assertEqual(
            health_url("https://suno.mcp.acedata.cloud/mcp"),
            "https://suno.mcp.acedata.cloud/health",
        )


if __name__ == "__main__":
    unittest.main()
