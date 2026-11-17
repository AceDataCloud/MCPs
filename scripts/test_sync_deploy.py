"""Deploy is a complete render followed by one apply, with no cluster-side repair."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.sync_deploy import ROOT, hosted_services, sync


class OrdinaryDeployTests(unittest.TestCase):
    def test_generated_sources_are_current(self):
        self.assertEqual(sync(check=True), [])
        for alias in hosted_services():
            with self.subTest(alias=alias):
                self.assertFalse((ROOT / alias / "deploy/oauth-state.sh").exists())
                workflow = yaml.safe_load(
                    (ROOT / alias / ".github/workflows/deploy.yaml").read_text()
                )
                self.assertEqual(workflow["concurrency"]["queue"], "max")
                steps = workflow["jobs"]["run"]["steps"]
                self.assertEqual(steps[0]["with"]["ref"], "main")
                self.assertTrue(any("pytest" in step.get("run", "") for step in steps))

    def test_apply_is_cwd_independent_and_propagates_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            deploy = root / "deploy"
            shutil.copytree(ROOT / "suno/deploy", deploy)
            binary = root / "bin"
            binary.mkdir()
            calls = root / "calls"
            (binary / "kubectl").write_text(
                '#!/bin/sh\nprintf "%s\\n" "$*" >> "$CALLS"\nexit "${APPLY_EXIT:-0}"\n'
            )
            (binary / "kubectl").chmod(0o755)
            env = {
                **os.environ,
                "PATH": f"{binary}:{os.environ['PATH']}",
                "CALLS": str(calls),
                "KUBE_CONTEXT": "reviewed",
                "BUILD_NUMBER": "123-1",
            }
            command = ["sh", str(deploy / "run.sh")]
            result = subprocess.run(
                command, cwd=root, env=env, check=False, capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--context reviewed apply -f", calls.read_text())
            self.assertEqual(len(calls.read_text().splitlines()), 1)
            self.assertEqual(result.stdout.strip(), "applied")
            result = subprocess.run(
                command,
                env={**env, "APPLY_EXIT": "17"},
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 17)
            self.assertNotIn("applied", result.stdout)
            calls.unlink()
            (deploy / "production/service.yaml").unlink()
            result = subprocess.run(
                command, env=env, check=False, capture_output=True, text=True
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(
                calls.exists(), "All resources must render before any apply"
            )

    def test_invalid_or_mutable_tags_fail_before_apply(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            deploy = root / "deploy"
            shutil.copytree(ROOT / "suno/deploy", deploy)
            binary = root / "bin"
            binary.mkdir()
            calls = root / "calls"
            (binary / "kubectl").write_text('#!/bin/sh\ntouch "$CALLS"\n')
            (binary / "kubectl").chmod(0o755)
            env = {
                **os.environ,
                "PATH": f"{binary}:{os.environ['PATH']}",
                "CALLS": str(calls),
                "KUBE_CONTEXT": "reviewed",
            }
            for version in ("", "latest", ".bad", "-bad", "bad;command", "a" * 129):
                with self.subTest(version=version):
                    result = subprocess.run(
                        ["sh", str(deploy / "run.sh")],
                        env={**env, "BUILD_NUMBER": version},
                        capture_output=True,
                        text=True,
                        check=False,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(calls.exists())
