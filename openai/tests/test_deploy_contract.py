import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_apply_preserves_manifest_namespace_and_explicit_context(
    tmp_path: Path,
) -> None:
    binary = tmp_path / "bin"
    binary.mkdir()
    capture = tmp_path / "applied.json"
    kubectl = binary / "kubectl"
    kubectl.write_text(
        "#!/usr/bin/env python3\nimport json,os,sys\nfrom pathlib import Path\n"
        "resources = {p.name:p.read_text() for p in Path(sys.argv[-1]).glob('*.yaml')}\n"
        "Path(os.environ['CAPTURE']).write_text(json.dumps({'args':sys.argv[1:], 'resources':resources}))\n"
    )
    kubectl.chmod(0o755)
    env = {
        **os.environ,
        "PATH": f"{binary}:{os.environ['PATH']}",
        "CAPTURE": str(capture),
        "KUBE_CONTEXT": "reviewed",
        "BUILD_NUMBER": "123-1",
    }
    result = subprocess.run(
        ["sh", str(ROOT / "deploy/run.sh")],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    applied = json.loads(capture.read_text())
    assert applied["args"][:4] == ["--context", "reviewed", "apply", "-f"]
    assert set(applied["resources"]) == {
        "deployment.yaml",
        "service.yaml",
        "ingress.yaml",
    }
    assert all("namespace: acedatacloud" in text for text in applied["resources"].values())
    assert "ghcr.io/acedatacloud/mcp-openai:123-1" in applied["resources"]["deployment.yaml"]
    assert result.stdout.strip() == "applied"
