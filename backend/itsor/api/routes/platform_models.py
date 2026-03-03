from dataclasses import MISSING, fields, is_dataclass
from typing import Any

from fastapi import APIRouter, HTTPException, status

from itsor.domain.models import platform_models

router = APIRouter(prefix="/models", tags=["platform-models"])


PLATFORM_MODEL_CLASSES = {
    "User": platform_models.User,
    "Tenant": platform_models.Tenant,
    "Group": platform_models.Group,
    "Role": platform_models.Role,
    "Permission": platform_models.Permission,
    "UserTenant": platform_models.UserTenant,
    "UserGroupMembership": platform_models.UserGroupMembership,
    "UserRole": platform_models.UserRole,
    "GroupRole": platform_models.GroupRole,
    "RolePermission": platform_models.RolePermission,
}


def _render_default(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool, list, dict)):
        return value
    return str(value)


@router.get("", response_model=list[str])
def list_platform_models() -> list[str]:
    return sorted(PLATFORM_MODEL_CLASSES.keys())


@router.get("/{model_name}")
def get_platform_model_details(model_name: str) -> dict[str, Any]:
    model_class = PLATFORM_MODEL_CLASSES.get(model_name)
    if not model_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Platform model not found")

    if not is_dataclass(model_class):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Configured class is not a dataclass")

    model_fields: list[dict[str, Any]] = []
    for field_info in fields(model_class):
        field_type = field_info.type
        type_name = getattr(field_type, "__name__", str(field_type))

        default_value = None
        if field_info.default is not MISSING:
            default_value = _render_default(field_info.default)

        if field_info.default_factory is not MISSING:
            factory_name = getattr(field_info.default_factory, "__name__", str(field_info.default_factory))
        else:
            factory_name = None

        model_fields.append(
            {
                "name": field_info.name,
                "type": type_name,
                "default": default_value,
                "default_factory": factory_name,
                "init": field_info.init,
            }
        )

    return {
        "name": model_class.__name__,
        "module": model_class.__module__,
        "fields": model_fields,
    }
