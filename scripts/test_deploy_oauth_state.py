"""Check that hosted OAuth deploys preserve their per-service state key."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class DeployOAuthStateTests(unittest.TestCase):
    def test_creates_key_once_and_refuses_silent_rotation(self):
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            (work / "deploy/production").mkdir(parents=True)
            (work / "deploy/production/deployment.yaml").write_text(
                "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: mcp-test\n"
            )
            (work / "deploy/oauth-state.sh").write_bytes(
                (ROOT / "shared/deploy_oauth_state.sh").read_bytes()
            )
            fake_bin = work / "bin"
            fake_bin.mkdir()
            kubectl = fake_bin / "kubectl"
            kubectl.write_text(
                """#!/usr/bin/env python3
import json, os, sys
from pathlib import Path
path = Path(os.environ['FAKE_OAUTH_STATE_PATH'])
state = json.loads(path.read_text())
args = sys.argv[1:]
if args[:2] == ['-n', 'acedatacloud']:
    args = args[2:]
if args[:2] == ['get', 'secret']:
    if not state['secret']:
        sys.exit(1)
    if '-o' in args:
        print('yes')
elif args[:2] == ['get', 'deployment']:
    print('true' if state['marker'] else '')
elif args[:2] == ['create', 'secret']:
    state['secret'] = True
    state['creations'] += 1
elif args[:2] == ['rollout', 'status']:
    state['rollouts'] += 1
elif args[:2] == ['annotate', 'deployment']:
    state['marker'] = True
else:
    sys.exit(2)
path.write_text(json.dumps(state))
"""
            )
            kubectl.chmod(0o755)
            openssl = fake_bin / "openssl"
            openssl.write_text("#!/bin/sh\nprintf '%064d\\n' 0\n")
            openssl.chmod(0o755)
            state_path = work / "state.json"
            state_path.write_text(
                json.dumps(
                    {"secret": False, "marker": False, "creations": 0, "rollouts": 0}
                )
            )
            env = {
                **os.environ,
                "PATH": f"{fake_bin}:{os.environ['PATH']}",
                "FAKE_OAUTH_STATE_PATH": str(state_path),
            }
            command = [
                "sh",
                "-c",
                ". ./deploy/oauth-state.sh; mark_oauth_key_initialized",
            ]

            first = subprocess.run(
                command, cwd=work, env=env, capture_output=True, text=True, check=False
            )
            self.assertEqual(first.returncode, 0, first.stderr)
            second = subprocess.run(
                command, cwd=work, env=env, capture_output=True, text=True, check=False
            )
            self.assertEqual(second.returncode, 0, second.stderr)
            state = json.loads(state_path.read_text())
            self.assertEqual(state["creations"], 1)
            self.assertEqual(state["rollouts"], 2)

            state["secret"] = False
            state_path.write_text(json.dumps(state))
            missing = subprocess.run(
                command, cwd=work, env=env, capture_output=True, text=True, check=False
            )
            self.assertNotEqual(missing.returncode, 0)
            self.assertIn("restore mcp-test-oauth-state", missing.stderr)
            self.assertEqual(json.loads(state_path.read_text())["creations"], 1)


if __name__ == "__main__":
    unittest.main()
