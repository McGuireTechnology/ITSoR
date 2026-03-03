from typing import Literal

from pydantic import BaseModel

from itsor.domain.models import PlatformResourceAction


class PlatformEndpointPermissionEntry(BaseModel):
    principal_type: Literal["user", "group"]
    principal_id: str
    endpoint_name: str
    action: PlatformResourceAction


class PlatformEndpointPermissionEntryResponse(PlatformEndpointPermissionEntry):
    id: int

    model_config = {"from_attributes": True}


class PlatformEndpointPermissionUpdateRequest(BaseModel):
    principal_type: Literal["user", "group"]
    principal_id: str
    endpoint_name: str
    action: PlatformResourceAction


class PlatformEndpointPermissionPatchRequest(BaseModel):
    principal_type: Literal["user", "group"] | None = None
    principal_id: str | None = None
    endpoint_name: str | None = None
    action: PlatformResourceAction | None = None
