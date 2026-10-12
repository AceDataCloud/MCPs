from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_rollout_uses_manifest_namespace() -> None:
    script = (ROOT / "deploy/run.sh").read_text()
    deployment = (ROOT / "deploy/production/deployment.yaml").read_text()

    assert 'NAMESPACE=$(awk \'$1 == "namespace:"' in script
    assert 'kubectl rollout status "deployment/$DEPLOYMENT_NAME" --namespace "$NAMESPACE"' in script
    assert "namespace: acedatacloud" in deployment
