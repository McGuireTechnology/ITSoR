from typing import Literal

from pydantic import BaseModel


class PlatformEndpointPermissionEntry(BaseModel):
    principal_type: Literal["user", "group"]
    principal_id: str
    endpoint_name: str
    action: str


class PlatformEndpointPermissionEntryResponse(PlatformEndpointPermissionEntry):
    id: int

    model_config = {"from_attributes": True}


class PlatformEndpointPermissionUpdateRequest(BaseModel):
    principal_type: Literal["user", "group"]
    principal_id: str
    endpoint_name: str
    action: str


class PlatformEndpointPermissionPatchRequest(BaseModel):
    principal_type: Literal["user", "group"] | None = None
    principal_id: str | None = None
    endpoint_name: str | None = None
    action: str | None = None
