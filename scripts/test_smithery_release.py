"""Regression coverage for non-TTY publishing and authenticated terminal status."""

import json
import unittest

from scripts.sync_smithery_release import SOURCE, targets
from shared.smithery_release import accepted_release, wait_for_release

RELEASE_ID = "7d7ef38a-1838-4a48-a048-a3f6930a4229"
NAME = "acedatacloud-mcp/mcp-suno"


class SmitheryReleaseTest(unittest.TestCase):
    def test_receipt_after_cli_progress_lines(self):
        receipt = {
            "deploymentId": RELEASE_ID,
            "qualifiedName": NAME,
            "status": "PENDING",
        }
        self.assertEqual(
            accepted_release("Release accepted\n" + json.dumps(receipt), NAME),
            RELEASE_ID,
        )

    def test_receipt_without_id_or_with_wrong_server_is_rejected(self):
        for log in [
            "Publish failed",
            json.dumps({"deploymentId": RELEASE_ID, "qualifiedName": "other"}),
        ]:
            with self.subTest(log=log), self.assertRaises(ValueError):
                accepted_release(log, NAME)

    def test_pending_does_not_finish_before_the_same_release_succeeds(self):
        states = iter(["QUEUED", "WORKING", "SUCCESS"])
        calls = []

        def fetch(timeout):
            calls.append(timeout)
            return {"id": RELEASE_ID, "status": next(states)}

        result = wait_for_release(RELEASE_ID, fetch, sleep=lambda _: None)
        self.assertEqual(result["status"], "SUCCESS")
        self.assertEqual(len(calls), 3)

    def test_failure_auth_and_unknown_status_never_pass(self):
        for status in [
            "FAILURE",
            "FAILURE_SCAN",
            "AUTH_REQUIRED",
            "AUTH_TIMEOUT",
            "CANCELLED",
            "INTERNAL_ERROR",
            "UNKNOWN",
            None,
        ]:
            with self.subTest(status=status), self.assertRaises(RuntimeError):
                wait_for_release(
                    RELEASE_ID,
                    lambda _, status=status: {"id": RELEASE_ID, "status": status},
                )

    def test_an_older_successful_release_does_not_pass(self):
        with self.assertRaises(ValueError):
            wait_for_release(RELEASE_ID, lambda _: {"id": "older", "status": "SUCCESS"})

    def test_pending_times_out_without_republishing(self):
        ticks = iter([0, 0, 0, 1, 2])
        with self.assertRaises(TimeoutError):
            wait_for_release(
                RELEASE_ID,
                lambda _: {"id": RELEASE_ID, "status": "PENDING"},
                timeout=1,
                clock=lambda: next(ticks),
                sleep=lambda _: None,
            )

    def test_distribution_copies_and_workflows_use_the_verifier(self):
        paths = list(targets())
        self.assertGreater(len(paths), 0)
        for target in paths:
            with self.subTest(path=target):
                self.assertEqual(target.read_text(), SOURCE.read_text())
                workflow = (target.parent.parent / "workflows/publish.yml").read_text()
                section = workflow.split("  publish-smithery:\n", 1)[1].split("\n  publish-", 1)[0]
                self.assertNotIn("|| echo", section)
                self.assertIn("set -euo pipefail", section)
                self.assertIn("python3 .github/scripts/verify_smithery_release.py", section)


if __name__ == "__main__":
    unittest.main()
