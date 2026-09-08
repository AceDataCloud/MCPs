#!/usr/bin/env python3
from __future__ import annotations

import unittest

from mcp_catalog import acquisition_target


class AcquisitionTargetTest(unittest.TestCase):
    def test_active_entry_gets_stable_campaign(self) -> None:
        self.assertEqual(
            acquisition_target("suno", {"status": "active"}),
            "https://platform.acedata.cloud/?utm_source=github&utm_medium=repo&utm_campaign=mcp-suno",
        )

    def test_retired_entry_has_no_acquisition_target(self) -> None:
        self.assertIsNone(acquisition_target("sora", {"status": "retired"}))

    def test_invalid_status_and_alias_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            acquisition_target("suno", {"status": "draft"})
        with self.assertRaises(ValueError):
            acquisition_target("Suno MCP", {"status": "active"})


if __name__ == "__main__":
    unittest.main()
