#!/usr/bin/env python3
from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stdout
from datetime import date
from unittest.mock import MagicMock, patch

from scripts.registry_health import (
    Finding,
    NAMESPACE,
    OFFICIAL_META,
    Surface,
    classify,
    compare_surfaces,
    health_url,
    live_findings,
    load_registry,
    local_surfaces,
    main,
    registry_surfaces,
)


def registry_row(status="active", name=NAMESPACE + "one"):
    return {
        "server": {
            "name": name,
            "packages": [{"identifier": "pkg", "version": "2026.10.12.1"}],
            "remotes": [{"url": "https://one.example/mcp"}],
        },
        "_meta": {OFFICIAL_META: {"status": status, "isLatest": True}},
    }


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

    def test_deprecated_retired_entry_is_not_active_drift(self) -> None:
        retired = Surface(
            "one", NAMESPACE + "one", "pkg", "https://one.example/mcp", "retired"
        )
        registry = registry_surfaces({"servers": [registry_row("deprecated")]})
        self.assertEqual(compare_surfaces({retired.name: retired}, registry), [])

    def test_deprecated_active_entry_is_missing_active_distribution(self) -> None:
        active = Surface(
            "one", NAMESPACE + "one", "pkg", "https://one.example/mcp", "active"
        )
        registry = registry_surfaces({"servers": [registry_row("deprecated")]})
        self.assertEqual(
            compare_surfaces({active.name: active}, registry)[0].kind,
            "registry_missing",
        )

    def test_duplicate_latest_name_fails_instead_of_overwriting(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "duplicate latest"):
            registry_surfaces({"servers": [registry_row(), registry_row()]})

    def test_response_requires_official_latest_and_status(self) -> None:
        for metadata in ({}, {"status": "active", "isLatest": False}):
            row = registry_row()
            row["_meta"][OFFICIAL_META] = metadata
            with self.subTest(metadata=metadata), self.assertRaises(RuntimeError):
                registry_surfaces({"servers": [row]})

    def test_substring_namespace_neighbor_is_excluded(self) -> None:
        self.assertEqual(
            registry_surfaces(
                {"servers": [registry_row(name="io.github.AceDataCloudOther/one")]}
            ),
            {},
        )

    @patch("scripts.registry_health.load_json_url")
    def test_reads_all_pages_and_encodes_cursor(self, load) -> None:
        load.side_effect = [
            {"servers": [registry_row()], "metadata": {"nextCursor": "a+b"}},
            {"servers": [registry_row(name=NAMESPACE + "two")]},
        ]
        self.assertEqual(len(load_registry()["servers"]), 2)
        self.assertIn("cursor=a%2Bb", load.call_args.args[0])

    @patch("scripts.registry_health.load_json_url")
    def test_repeated_cursor_fails(self, load) -> None:
        load.return_value = {"metadata": {"nextCursor": "same"}}
        with self.assertRaisesRegex(RuntimeError, "repeated pagination"):
            load_registry()

    @patch("scripts.registry_health.urllib.request.urlopen")
    @patch("scripts.registry_health.load_json_url")
    def test_checks_advertised_package_version_and_rejects_yanked_files(
        self, load, urlopen
    ) -> None:
        active = Surface(
            "one", NAMESPACE + "one", "pkg", "https://one.example/mcp", "active"
        )
        registry = registry_surfaces({"servers": [registry_row()]})
        load.return_value = {"urls": [{"yanked": True}]}
        response = MagicMock()
        response.__enter__.return_value.status = 200
        urlopen.return_value = response
        findings = live_findings({active.name: active}, registry)
        load.assert_called_once_with("https://pypi.org/pypi/pkg/2026.10.12.1/json")
        self.assertEqual([finding.kind for finding in findings], ["pypi_unhealthy"])

    def test_current_local_manifest_contract_is_valid(self) -> None:
        surfaces = local_surfaces()
        self.assertTrue(surfaces)
        self.assertTrue(
            all(surface.name.startswith(NAMESPACE) for surface in surfaces.values())
        )

    @patch("scripts.registry_health.load_registry", side_effect=TimeoutError("timeout"))
    @patch("sys.argv", ["registry_health.py", "--skip-live"])
    def test_registry_outage_emits_failure_report_without_false_missing_entries(
        self, load
    ) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            self.assertEqual(main(), 1)
        report = json.loads(output.getvalue())
        self.assertFalse(report["registry_checked"])
        self.assertIsNone(report["registry_latest"])
        self.assertEqual(
            [row["kind"] for row in report["blocking"]], ["registry_unavailable"]
        )


if __name__ == "__main__":
    unittest.main()
