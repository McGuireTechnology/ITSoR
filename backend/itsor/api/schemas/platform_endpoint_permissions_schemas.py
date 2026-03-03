from typing import Literal

from pydantic import BaseModel


PrincipalType = Literal["user", "group"]
EndpointAction = Literal["read", "write"]


class PlatformEndpointPermissionEntry(BaseModel):
    principal_type: PrincipalType
    principal_id: str
    endpoint_name: str
    action: EndpointAction


class PlatformEndpointPermissionUpdateRequest(BaseModel):
    principal_type: PrincipalType
    principal_id: str
    endpoint_name: str
    action: EndpointAction


class PlatformEndpointPermissionPatchRequest(BaseModel):
    principal_type: PrincipalType | None = None
    principal_id: str | None = None
    endpoint_name: str | None = None
    action: EndpointAction | None = None


class PlatformEndpointPermissionEntryResponse(BaseModel):
    id: int
    principal_type: PrincipalType
    principal_id: str
    endpoint_name: str
    action: EndpointAction

    model_config = {"from_attributes": True}
