from pydantic import BaseModel

from itsor.api.schemas.base_schemas import TenantScopedNameSchema
from itsor.domain.models import ResourceAction


class GroupCreate(TenantScopedNameSchema):
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None


class GroupUpdate(BaseModel):
    name: str | None = None
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None


class GroupReplace(TenantScopedNameSchema):
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]] | None = None


class GroupResponse(TenantScopedNameSchema):
    id: str
    owner_id: str | None = None
    group_id: str | None = None
    permissions: int
    platform_endpoint_permissions: dict[str, list[ResourceAction | str]]

    model_config = {"from_attributes": True}
