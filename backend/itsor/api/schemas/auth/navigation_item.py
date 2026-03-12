from typing import Literal

from pydantic import BaseModel, Field


ItemTypeLiteral = Literal["route", "record", "action"]


class NavigationItemCreate(BaseModel):
    view_id: str
    label: str
    item_type: ItemTypeLiteral
    route: str
    resource_id: str
    icon: str | None = None
    order: int = 0
    metadata: dict[str, str] = Field(default_factory=dict)


class NavigationItemReplace(NavigationItemCreate):
    pass


class NavigationItemUpdate(BaseModel):
    view_id: str | None = None
    label: str | None = None
    item_type: ItemTypeLiteral | None = None
    route: str | None = None
    resource_id: str | None = None
    icon: str | None = None
    order: int | None = None
    metadata: dict[str, str] | None = None


class NavigationItemResponse(BaseModel):
    id: str
    view_id: str
    label: str
    item_type: ItemTypeLiteral
    route: str
    resource_id: str
    icon: str | None = None
    order: int = 0
    metadata: dict[str, str] = Field(default_factory=dict)

    model_config = {"from_attributes": True}
