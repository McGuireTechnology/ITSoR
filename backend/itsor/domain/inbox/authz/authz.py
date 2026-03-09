from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Literal, TypeAlias


class ResourceAction(str, Enum):
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"

    @classmethod
    def from_verb(cls, verb: str) -> ResourceAction:
        normalized = verb.strip().lower()
        if normalized in {"write", "modify"}:
            normalized = cls.UPDATE.value
        try:
            return cls(normalized)
        except ValueError as exc:
            raise ValueError(f"Unsupported action verb '{verb}'") from exc

    @classmethod
    def from_nibble(cls, value: int) -> ResourceAction:
        nibble_map = {
            0x1: cls.CREATE,
            0x2: cls.READ,
            0x4: cls.UPDATE,
            0x8: cls.DELETE,
            0x10: cls.EXECUTE,
        }
        try:
            return nibble_map[value]
        except KeyError as exc:
            raise ValueError(f"Unsupported action nibble '{value}'") from exc

    def to_nibble(self) -> int:
        nibble_map = {
            ResourceAction.CREATE: 0x1,
            ResourceAction.READ: 0x2,
            ResourceAction.UPDATE: 0x4,
            ResourceAction.DELETE: 0x8,
            ResourceAction.EXECUTE: 0x10,
        }
        return nibble_map[self]


ResourceKey: TypeAlias = str
ResourceCatalog: TypeAlias = dict[ResourceKey, frozenset[ResourceAction]]


class ResourceProvider(ABC):
    @classmethod
    @abstractmethod
    def catalog(cls) -> ResourceCatalog:
        raise NotImplementedError


MergePolicy = Literal[
    "error_on_conflict",
    "union_actions",
    "platform_overrides_idm",
    "last_wins",
]


def merge_resource_catalogs(
    providers: list[type[ResourceProvider]],
    *,
    policy: MergePolicy = "error_on_conflict",
) -> ResourceCatalog:
    merged: ResourceCatalog = {}
    key_sources: dict[ResourceKey, type[ResourceProvider]] = {}

    for provider in providers:
        for resource_key, actions in provider.catalog().items():
            if resource_key not in merged:
                merged[resource_key] = actions
                key_sources[resource_key] = provider
                continue

            if policy == "error_on_conflict" and merged[resource_key] != actions:
                raise ValueError(
                    f"Conflicting actions for resource '{resource_key}' from provider '{provider.__name__}'"
                )

            if policy == "union_actions":
                merged[resource_key] = frozenset((*merged[resource_key], *actions))
                continue

            if policy == "platform_overrides_idm":
                current_name = provider.__name__.lower()
                previous_name = key_sources[resource_key].__name__.lower()
                current_is_platform = "platform" in current_name
                previous_is_platform = "platform" in previous_name

                if current_is_platform or not previous_is_platform:
                    merged[resource_key] = actions
                    key_sources[resource_key] = provider
            else:
                merged[resource_key] = actions
                key_sources[resource_key] = provider

    return merged
