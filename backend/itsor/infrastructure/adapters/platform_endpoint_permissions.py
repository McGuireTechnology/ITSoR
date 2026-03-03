from sqlalchemy.orm import Session

from itsor.domain.models import ResourceAction
from itsor.infrastructure.models.sqlalchemy_platform_endpoint_permission_model import PlatformEndpointPermissionModel


def _normalize_action(value: str | ResourceAction) -> str:
    if isinstance(value, ResourceAction):
        return value.value
    candidate = str(value).strip().lower()
    return candidate


def _to_action(value: str) -> ResourceAction | str:
    candidate = str(value).strip().lower()
    try:
        return ResourceAction(candidate)
    except ValueError:
        return candidate


def fetch_platform_endpoint_permissions(
    db: Session,
    *,
    principal_type: str,
    principal_id: str | None,
) -> dict[str, list[ResourceAction | str]]:
    if not principal_id:
        return {}

    rows = (
        db.query(PlatformEndpointPermissionModel)
        .filter(
            PlatformEndpointPermissionModel.principal_type == principal_type,
            PlatformEndpointPermissionModel.principal_id == principal_id,
        )
        .all()
    )

    mapped: dict[str, list[ResourceAction | str]] = {}
    for row in rows:
        endpoint = str(row.endpoint_name)
        action = _to_action(str(row.action))
        actions = mapped.setdefault(endpoint, [])
        if action not in actions:
            actions.append(action)
    return mapped


def replace_platform_endpoint_permissions(
    db: Session,
    *,
    principal_type: str,
    principal_id: str | None,
    permissions: dict[str, list[ResourceAction | str]] | None,
) -> None:
    if not principal_id:
        return

    (
        db.query(PlatformEndpointPermissionModel)
        .filter(
            PlatformEndpointPermissionModel.principal_type == principal_type,
            PlatformEndpointPermissionModel.principal_id == principal_id,
        )
        .delete()
    )

    normalized = permissions or {}
    for endpoint_name, actions in normalized.items():
        if not isinstance(actions, list):
            continue
        for action in actions:
            db.add(
                PlatformEndpointPermissionModel(
                    principal_type=principal_type,
                    principal_id=principal_id,
                    endpoint_name=str(endpoint_name),
                    action=_normalize_action(action),
                )
            )

    db.commit()
