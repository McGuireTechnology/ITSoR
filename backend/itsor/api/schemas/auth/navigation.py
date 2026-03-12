from typing import Literal

from pydantic import BaseModel, Field


ModuleTypeLiteral = Literal["system", "custom", "app"]
ViewTypeLiteral = Literal["list", "detail", "form", "board", "calendar", "dashboard"]


class NavigationViewResponse(BaseModel):
    id: str
    key: str
    label: str
    view_type: ViewTypeLiteral
    route: str
    resource_id: str
    tenant_id: str | None = None
    source_id: str | None = None
    icon: str | None = None
    order: int = 0
    enabled: bool = True

    model_config = {"from_attributes": True}


class NavigationResourceResponse(BaseModel):
    id: str
    key: str
    label: str
    module_id: str
    list_route: str
    tenant_id: str | None = None
    source_id: str | None = None
    icon: str | None = None
    order: int = 0
    enabled: bool = True
    views: list[NavigationViewResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class NavigationModuleResponse(BaseModel):
    id: str
    key: str
    label: str
    module_type: ModuleTypeLiteral
    tenant_id: str | None = None
    source_id: str | None = None
    icon: str | None = None
    order: int = 0
    enabled: bool = True
    resources: list[NavigationResourceResponse] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class NavigationModuleCreate(BaseModel):
    key: str
    label: str
    module_type: ModuleTypeLiteral = "custom"
    tenant_id: str | None = None
    source_id: str | None = None
    icon: str | None = None
    order: int = 0
    enabled: bool = True


class NavigationModuleUpdate(BaseModel):
    tenant_id: str | None = None
    label: str | None = None
    icon: str | None = None
    order: int | None = None
    enabled: bool | None = None


class NavigationResourceCreate(BaseModel):
    key: str
    label: str
    module_id: str
    list_route: str
    tenant_id: str | None = None
    source_id: str | None = None
    icon: str | None = None
    order: int = 0
    enabled: bool = True


class NavigationResourceUpdate(BaseModel):
    tenant_id: str | None = None
    label: str | None = None
    module_id: str | None = None
    list_route: str | None = None
    icon: str | None = None
    order: int | None = None
    enabled: bool | None = None


class NavigationViewCreate(BaseModel):
    key: str
    label: str
    view_type: ViewTypeLiteral = "list"
    route: str
    resource_id: str
    tenant_id: str | None = None
    source_id: str | None = None
    icon: str | None = None
    order: int = 0
    enabled: bool = True


class NavigationViewUpdate(BaseModel):
    tenant_id: str | None = None
    label: str | None = None
    resource_id: str | None = None
    route: str | None = None
    icon: str | None = None
    order: int | None = None
    enabled: bool | None = None


class NavigationLoadDefaultsRequest(BaseModel):
    tenant_id: str | None = None


class NavigationSetDefaultRequest(BaseModel):
    tenant_id: str | None = None
    module_id: str
    resource_id: str | None = None
    view_id: str | None = None


class NavigationDefaultResponse(BaseModel):
    module_id: str
    resource_id: str
    view_id: str


ModuleCreate = NavigationModuleCreate
ModuleUpdate = NavigationModuleUpdate
ModuleResponse = NavigationModuleResponse
ModuleResourceCreate = NavigationResourceCreate
ModuleResourceUpdate = NavigationResourceUpdate
ModuleResourceResponse = NavigationResourceResponse
MenuViewCreate = NavigationViewCreate
MenuViewUpdate = NavigationViewUpdate
MenuViewResponse = NavigationViewResponse
