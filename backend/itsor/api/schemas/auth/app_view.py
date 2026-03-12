from typing import Literal

from pydantic import BaseModel

AppViewTypeLiteral = Literal[
    "table",
    "form",
    "detail",
    "card",
    "deck",
    "gallery",
    "dashboard",
    "map",
]


class AppViewCreate(BaseModel):
    app_id: str
    name: str
    type: AppViewTypeLiteral
    table_id: str | None = None
    position: int = 0
    icon: str | None = None


class AppViewReplace(AppViewCreate):
    pass


class AppViewUpdate(BaseModel):
    app_id: str | None = None
    name: str | None = None
    type: AppViewTypeLiteral | None = None
    table_id: str | None = None
    position: int | None = None
    icon: str | None = None


class AppViewResponse(BaseModel):
    id: str
    app_id: str
    name: str
    type: AppViewTypeLiteral
    table_id: str | None = None
    position: int = 0
    icon: str | None = None

    model_config = {"from_attributes": True}
