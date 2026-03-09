from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import ulid


class ModuleType(str, Enum):
    SYSTEM = "system"
    CUSTOM = "custom"
    APP = "app"


class ViewType(str, Enum):
    LIST = "list"
    DETAIL = "detail"
    FORM = "form"
    BOARD = "board"
    CALENDAR = "calendar"
    DASHBOARD = "dashboard"


class ItemType(str, Enum):
    ROUTE = "route"
    RECORD = "record"
    ACTION = "action"


@dataclass
class NavigationItem:
    id: str = field(default_factory=lambda: str(ulid.new()), init=False)
    label: str
    item_type: ItemType
    route: str
    resource_id: str
    icon: str | None = None
    order: int = 0
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("Navigation item label cannot be empty")

        if not self.route.strip():
            raise ValueError("Navigation item route cannot be empty")

        if self.order < 0:
            raise ValueError("Navigation item order cannot be negative")


@dataclass
class NavigationView:
    id: str = field(default_factory=lambda: str(ulid.new()), init=False)
    key: str
    label: str
    view_type: ViewType
    route: str
    resource_id: str
    icon: str | None = None
    order: int = 0
    items: list[NavigationItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("Navigation view key cannot be empty")

        if not self.label.strip():
            raise ValueError("Navigation view label cannot be empty")

        if not self.route.strip():
            raise ValueError("Navigation view route cannot be empty")

        if self.order < 0:
            raise ValueError("Navigation view order cannot be negative")


@dataclass
class ModuleResource:
    id: str = field(default_factory=lambda: str(ulid.new()), init=False)
    key: str
    label: str
    module_id: str
    list_route: str
    icon: str | None = None
    order: int = 0
    views: list[NavigationView] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("Module resource key cannot be empty")

        if not self.label.strip():
            raise ValueError("Module resource label cannot be empty")

        if not self.list_route.strip():
            raise ValueError("Module resource list_route cannot be empty")

        if self.order < 0:
            raise ValueError("Module resource order cannot be negative")


@dataclass
class Module:
    id: str = field(default_factory=lambda: str(ulid.new()), init=False)
    key: str
    label: str
    module_type: ModuleType = ModuleType.CUSTOM
    icon: str | None = None
    order: int = 0
    enabled: bool = True
    resources: list[ModuleResource] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.key.strip():
            raise ValueError("Module key cannot be empty")

        if not self.label.strip():
            raise ValueError("Module label cannot be empty")

        if self.order < 0:
            raise ValueError("Module order cannot be negative")


__all__ = [
    "ItemType",
    "Module",
    "ModuleResource",
    "ModuleType",
    "NavigationItem",
    "NavigationView",
    "ViewType",
]
