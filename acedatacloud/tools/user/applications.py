"""Application and deployment self-service tools."""

from typing import Annotated, Any, Literal

from pydantic import Field

from core.client import client, get_request_user_id
from core.exceptions import PlatformError
from core.server import mcp
from core.utils import confirmation_required, dumps, error_json

ApplicationType = Literal["Usage", "Period"]
ApplicationScope = Literal["Individual", "Global"]
Affiliation = Literal["owner", "granted"]
DeploymentAction = Literal["start", "stop", "restart"]


def _body(**values: Any) -> dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


@mcp.tool()
async def acedatacloud_list_applications(
    service_id: Annotated[
        str | list[str] | None, Field(description="Filter by one or more service UUIDs.")
    ] = None,
    application_type: Annotated[
        ApplicationType | list[ApplicationType] | None,
        Field(description="Filter by Usage or Period application type."),
    ] = None,
    scope: Annotated[
        ApplicationScope | list[ApplicationScope] | None,
        Field(description="Filter by Individual or Global scope."),
    ] = None,
    affiliation: Annotated[
        list[Affiliation] | None,
        Field(description="Filter applications owned by or granted to the caller."),
    ] = None,
    ordering: Annotated[
        Literal["created_at", "-created_at"] | None, Field(description="Order by creation time.")
    ] = None,
    limit: Annotated[int, Field(description="Max applications to return.", ge=1, le=200)] = 50,
    offset: Annotated[int, Field(description="Pagination offset.", ge=0)] = 0,
) -> str:
    """List account subscriptions with owner/grantee and multi-value filters."""
    try:
        result = await client.get(
            "/applications/",
            {
                "user_id": await get_request_user_id(),
                "service_id": service_id,
                "type": application_type,
                "scope": scope,
                "affiliation": affiliation,
                "ordering": ordering,
                "limit": limit,
                "offset": offset,
            },
        )
        return dumps(result)
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_create_application(
    service_id: Annotated[
        str | None, Field(description="Service UUID; required for Individual scope.")
    ] = None,
    application_type: Annotated[
        ApplicationType, Field(description="Usage or Period application.")
    ] = "Usage",
    scope: Annotated[
        ApplicationScope, Field(description="Individual or Global scope.")
    ] = "Individual",
    confirm: Annotated[bool, Field(description="Must be true to create the application.")] = False,
) -> str:
    """Create an application subscription. Requires ``confirm=true``."""
    body = _body(service_id=service_id, type=application_type, scope=scope)
    if not confirm:
        return confirmation_required("POST /applications/", body)
    try:
        return dumps(await client.post("/applications/", body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_application(
    application_id: Annotated[str, Field(description="Application UUID.")],
) -> str:
    """Get one application and its service/pricing details."""
    try:
        return dumps(await client.get(f"/applications/{application_id}"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_update_application_balance_policy(
    application_id: Annotated[str, Field(description="Application UUID.")],
    allow_consume_global: Annotated[
        bool, Field(description="Allow fallback to the global balance.")
    ],
    confirm: Annotated[bool, Field(description="Must be true to update the policy.")] = False,
) -> str:
    """Update global-balance fallback for an application. Requires ``confirm=true``."""
    body = {"allow_consume_global": allow_consume_global}
    endpoint = f"/applications/{application_id}/update-allow-consume-global/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", body)
    try:
        return dumps(await client.post(endpoint, body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_save_deployment_config(
    application_id: Annotated[str, Field(description="Deployment application UUID.")],
    config: Annotated[dict[str, Any], Field(description="Raw deployment wizard configuration.")],
    step: Annotated[
        int | None, Field(description="Optional wizard step to resume from.", ge=0)
    ] = None,
    confirm: Annotated[bool, Field(description="Must be true to save the draft.")] = False,
) -> str:
    """Save deployment configuration without deploying. Requires ``confirm=true``."""
    body = _body(config=config, step=step)
    endpoint = f"/applications/{application_id}/deployment-save-config/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", body)
    try:
        return dumps(await client.post(endpoint, body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_deploy_application(
    application_id: Annotated[str, Field(description="Deployment application UUID.")],
    config: Annotated[
        dict[str, Any] | None, Field(description="Raw deployment configuration to persist.")
    ] = None,
    helm_overrides: Annotated[
        dict[str, Any] | None, Field(description="Flat, service-supported Helm value overrides.")
    ] = None,
    confirm: Annotated[bool, Field(description="Must be true to start deployment.")] = False,
) -> str:
    """Start or redeploy an application workload. Requires ``confirm=true``."""
    body = {"config": config or {}, "helm_overrides": helm_overrides or {}}
    endpoint = f"/applications/{application_id}/deployment-deploy/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", body)
    try:
        return dumps(await client.post(endpoint, body))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_deployment_status(
    application_id: Annotated[str, Field(description="Deployment application UUID.")],
) -> str:
    """Get live deployment status and redacted access metadata."""
    try:
        return dumps(await client.get(f"/applications/{application_id}/deployment-status/"))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_control_deployment(
    application_id: Annotated[str, Field(description="Deployment application UUID.")],
    action: Annotated[
        DeploymentAction, Field(description="Power action: start, stop, or restart.")
    ],
    confirm: Annotated[bool, Field(description="Must be true to perform the action.")] = False,
) -> str:
    """Start, stop, or restart a deployment. Requires ``confirm=true``."""
    endpoint = f"/applications/{application_id}/deployment-{action}/"
    if not confirm:
        return confirmation_required(f"POST {endpoint}", {"action": action})
    try:
        return dumps(await client.post(endpoint, {}))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_teardown_deployment(
    application_id: Annotated[str, Field(description="Deployment application UUID.")],
    force: Annotated[
        bool, Field(description="Delete the record even if resource teardown fails.")
    ] = False,
    confirm: Annotated[
        bool, Field(description="Must be true to destroy the workload and application.")
    ] = False,
) -> str:
    """Destroy a deployment and delete its application. Irreversible; requires confirmation."""
    endpoint = f"/applications/{application_id}/deployment-teardown/"
    target = {"application_id": application_id, "force": force}
    if not confirm:
        return confirmation_required(f"POST {endpoint}?force={str(force).lower()}", target)
    try:
        return dumps(await client.post(endpoint, {}, params={"force": str(force).lower()}))
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_deployment_logs(
    application_id: Annotated[str, Field(description="Deployment application UUID.")],
    tail: Annotated[int, Field(description="Number of log lines.", ge=1, le=1000)] = 100,
    since: Annotated[
        str | None, Field(description="Duration such as '30s', '5m', or '1h'.")
    ] = None,
    container: Annotated[str | None, Field(description="Optional container name.")] = None,
) -> str:
    """Get bounded workload logs for a deployment."""
    try:
        return dumps(
            await client.get(
                f"/applications/{application_id}/deployment-logs/",
                {"tail": tail, "since": since, "container": container},
            )
        )
    except PlatformError as error:
        return error_json(error.code, error.message)


@mcp.tool()
async def acedatacloud_get_deployment_events(
    application_id: Annotated[str, Field(description="Deployment application UUID.")],
) -> str:
    """Get workload scheduling and image-pull events for a deployment."""
    try:
        return dumps(await client.get(f"/applications/{application_id}/deployment-events/"))
    except PlatformError as error:
        return error_json(error.code, error.message)
