"""Regression coverage for non-TTY publishing and authenticated terminal status."""

import contextlib
import io
import json
import os
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from scripts.sync_smithery_release import SOURCE, targets
from shared.smithery_release import (
    USER_AGENT,
    ReleasePendingTimeout,
    accepted_release,
    main,
    read_release,
    safe_failure_reason,
    wait_for_release,
)

RELEASE_ID = "7d7ef38a-1838-4a48-a048-a3f6930a4229"
NAME = "acedatacloud-mcp/mcp-suno"


class SmitheryReleaseTest(unittest.TestCase):
    def test_api_reader_identifies_client_and_requests_json(self):
        response = io.BytesIO(json.dumps({"id": RELEASE_ID, "status": "SUCCESS"}).encode())
        with patch(
            "shared.smithery_release.urllib.request.urlopen", return_value=response
        ) as open_:
            result = read_release("https://api.smithery.ai/existing-release", "test-secret", 7)
        request = open_.call_args.args[0]
        self.assertEqual(request.get_header("User-agent"), USER_AGENT)
        self.assertEqual(request.get_header("Accept"), "application/json")
        self.assertEqual(request.get_header("Authorization"), "Bearer test-secret")
        self.assertEqual(open_.call_args.kwargs["timeout"], 7)
        self.assertEqual(result["id"], RELEASE_ID)

    def test_safe_http_diagnostics_do_not_echo_body_url_or_reason(self):
        secret = "must-not-appear"
        error = urllib.error.HTTPError(
            "https://upstream.invalid/?token=" + secret,
            403,
            secret,
            {},
            io.BytesIO(secret.encode()),
        )
        self.assertEqual(safe_failure_reason(error), "Release API returned HTTP 403")
        for error in [urllib.error.URLError(secret), ValueError(secret), RuntimeError(secret)]:
            self.assertNotIn(secret, safe_failure_reason(error))
        self.assertIn("still pending", safe_failure_reason(ReleasePendingTimeout(secret)))
        self.assertNotIn(secret, safe_failure_reason(ReleasePendingTimeout(secret)))

    def test_full_script_distinguishes_http_failure_from_scan_authentication(self):
        with tempfile.TemporaryDirectory() as folder:
            receipt = Path(folder) / "receipt.log"
            receipt.write_text(json.dumps({"deploymentId": RELEASE_ID, "qualifiedName": NAME}))
            for failure, expected in [
                (
                    urllib.error.HTTPError("https://hidden.invalid", 403, "hidden", {}, None),
                    "HTTP 403",
                ),
                (None, "AUTH_REQUIRED"),
            ]:
                with self.subTest(expected=expected):
                    options = (
                        {"side_effect": failure}
                        if failure
                        else {"return_value": {"id": RELEASE_ID, "status": "AUTH_REQUIRED"}}
                    )
                    with (
                        patch.dict(os.environ, {"SMITHERY_API_KEY": "test-secret"}),
                        patch("sys.argv", ["verify", NAME, str(receipt)]),
                        patch("shared.smithery_release.read_release", **options),
                        contextlib.redirect_stdout(io.StringIO()),
                        self.assertRaisesRegex(RuntimeError, expected) as raised,
                    ):
                        main()
                    self.assertNotIn("test-secret", str(raised.exception))
                    self.assertNotIn("hidden.invalid", str(raised.exception))

    def test_untrusted_status_is_not_logged_and_never_passes(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), self.assertRaisesRegex(RuntimeError, "UNKNOWN"):
            wait_for_release(
                RELEASE_ID, lambda _: {"id": RELEASE_ID, "status": "secret-value-from-upstream"}
            )
        self.assertNotIn("secret-value", output.getvalue())

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
