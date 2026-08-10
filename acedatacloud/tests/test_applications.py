"""Application and deployment tool contract tests."""

import json

import httpx
import pytest
import respx

from core.client import set_request_api_token
from tools.user.applications import (
    acedatacloud_control_deployment,
    acedatacloud_create_application,
    acedatacloud_deploy_application,
    acedatacloud_get_application,
    acedatacloud_get_deployment_events,
    acedatacloud_get_deployment_logs,
    acedatacloud_get_deployment_status,
    acedatacloud_list_applications,
    acedatacloud_save_deployment_config,
    acedatacloud_teardown_deployment,
    acedatacloud_update_application_balance_policy,
)

API = "https://platform.acedata.cloud/api/v1"
APP_ID = "11111111-1111-1111-1111-111111111111"


@respx.mock
@pytest.mark.asyncio
async def test_list_applications_sends_repeated_filters_and_subject():
    respx.get(f"{API}/platform-tokens/me/").mock(
        return_value=httpx.Response(200, json={"id": "user-1"})
    )
    route = respx.get(f"{API}/applications/").mock(
        return_value=httpx.Response(200, json={"count": 0, "items": []})
    )
    set_request_api_token("platform-token")
    try:
        await acedatacloud_list_applications(
            service_id=["svc-1", "svc-2"],
            application_type=["Usage", "Period"],
            scope=["Individual", "Global"],
            affiliation=["owner", "granted"],
            ordering="-created_at",
            limit=10,
            offset=20,
        )
    finally:
        set_request_api_token(None)

    params = route.calls[0].request.url.params
    assert params.get_list("service_id") == ["svc-1", "svc-2"]
    assert params.get_list("type") == ["Usage", "Period"]
    assert params.get_list("scope") == ["Individual", "Global"]
    assert params.get_list("affiliation") == ["owner", "granted"]
    assert params["user_id"] == "user-1"
    assert params["ordering"] == "-created_at"
    assert params["offset"] == "20"


@respx.mock
@pytest.mark.asyncio
async def test_create_application_confirmation_and_body():
    route = respx.post(f"{API}/applications/").mock(
        return_value=httpx.Response(201, json={"id": APP_ID})
    )
    preview = json.loads(
        await acedatacloud_create_application(
            service_id="svc-1", application_type="Period", confirm=False
        )
    )
    assert preview["status"] == "confirmation_required"
    assert route.call_count == 0

    result = json.loads(
        await acedatacloud_create_application(
            service_id="svc-1", application_type="Period", confirm=True
        )
    )
    assert result["id"] == APP_ID
    assert json.loads(route.calls[0].request.content) == {
        "service_id": "svc-1",
        "type": "Period",
        "scope": "Individual",
    }


@respx.mock
@pytest.mark.asyncio
async def test_application_reads_use_exact_routes():
    routes = {
        "detail": respx.get(f"{API}/applications/{APP_ID}").mock(
            return_value=httpx.Response(200, json={"id": APP_ID})
        ),
        "status": respx.get(f"{API}/applications/{APP_ID}/deployment-status/").mock(
            return_value=httpx.Response(200, json={"deployment": {"status": "ready"}})
        ),
        "logs": respx.get(f"{API}/applications/{APP_ID}/deployment-logs/").mock(
            return_value=httpx.Response(200, json={"logs": ["ready"]})
        ),
        "events": respx.get(f"{API}/applications/{APP_ID}/deployment-events/").mock(
            return_value=httpx.Response(200, json={"events": []})
        ),
    }
    await acedatacloud_get_application(APP_ID)
    await acedatacloud_get_deployment_status(APP_ID)
    await acedatacloud_get_deployment_logs(APP_ID, tail=500, since="5m", container="worker")
    await acedatacloud_get_deployment_events(APP_ID)

    assert all(route.call_count == 1 for route in routes.values())
    params = routes["logs"].calls[0].request.url.params
    assert dict(params) == {"tail": "500", "since": "5m", "container": "worker"}


@respx.mock
@pytest.mark.asyncio
async def test_application_mutations_use_exact_routes_and_bodies():
    policy = respx.post(f"{API}/applications/{APP_ID}/update-allow-consume-global/").mock(
        return_value=httpx.Response(200, json={"allow_consume_global": True})
    )
    save = respx.post(f"{API}/applications/{APP_ID}/deployment-save-config/").mock(
        return_value=httpx.Response(200, json={"status": "saved"})
    )
    deploy = respx.post(f"{API}/applications/{APP_ID}/deployment-deploy/").mock(
        return_value=httpx.Response(202, json={"status": "deploying"})
    )

    await acedatacloud_update_application_balance_policy(APP_ID, True, confirm=True)
    await acedatacloud_save_deployment_config(APP_ID, {"region": "hk"}, step=2, confirm=True)
    await acedatacloud_deploy_application(
        APP_ID,
        config={"region": "hk"},
        helm_overrides={"resources.requests.cpu": "250m"},
        confirm=True,
    )

    assert json.loads(policy.calls[0].request.content) == {"allow_consume_global": True}
    assert json.loads(save.calls[0].request.content) == {"config": {"region": "hk"}, "step": 2}
    assert json.loads(deploy.calls[0].request.content) == {
        "config": {"region": "hk"},
        "helm_overrides": {"resources.requests.cpu": "250m"},
    }


@respx.mock
@pytest.mark.asyncio
async def test_deployment_actions_and_teardown():
    restart = respx.post(f"{API}/applications/{APP_ID}/deployment-restart/").mock(
        return_value=httpx.Response(200, json={"status": "restarting"})
    )
    teardown = respx.post(f"{API}/applications/{APP_ID}/deployment-teardown/").mock(
        return_value=httpx.Response(200, json={"status": "deleted"})
    )

    await acedatacloud_control_deployment(APP_ID, "restart", confirm=True)
    await acedatacloud_teardown_deployment(APP_ID, force=True, confirm=True)

    assert restart.call_count == 1
    assert teardown.calls[0].request.url.params["force"] == "true"


@respx.mock
@pytest.mark.asyncio
async def test_all_application_mutation_previews_make_zero_http_calls():
    results = [
        await acedatacloud_create_application(service_id="svc-1"),
        await acedatacloud_update_application_balance_policy(APP_ID, True),
        await acedatacloud_save_deployment_config(APP_ID, {"secret": "value"}),
        await acedatacloud_deploy_application(APP_ID, helm_overrides={"token": "value"}),
        await acedatacloud_control_deployment(APP_ID, "stop"),
        await acedatacloud_teardown_deployment(APP_ID, force=True),
    ]
    assert all(json.loads(result)["status"] == "confirmation_required" for result in results)
    assert respx.calls.call_count == 0
    assert "value" not in results[2]
    assert "value" not in results[3]
