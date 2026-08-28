#!/usr/bin/env python3
"""Require zero-downtime rollout and verified deployment scripts for every MCP."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    deployments = sorted(ROOT.glob("*/deploy/production/deployment.yaml"))
    if len(deployments) != 27:
        raise SystemExit(f"expected 27 MCP deployments, found {len(deployments)}")
    for deployment in deployments:
        service = deployment.parts[-4]
        manifest = deployment.read_text()
        if "maxSurge: 1" not in manifest or "maxUnavailable: 0" not in manifest:
            raise SystemExit(f"{service}: deployment must keep the old replica available")
        run = ROOT / service / "deploy/run.sh"
        source = run.read_text()
        required = ("set -eu", "kubectl apply", "kubectl -n acedatacloud rollout status", "--timeout=15m")
        if any(item not in source for item in required):
            raise SystemExit(f"{service}: deploy script does not verify rollout")
        if "|| true" in source:
            raise SystemExit(f"{service}: deploy script swallows a release failure")
    print(f"verified {len(deployments)} zero-downtime MCP deployments")


if __name__ == "__main__":
    main()
