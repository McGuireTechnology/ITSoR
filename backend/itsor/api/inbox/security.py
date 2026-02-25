from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import ulid

from fastapi import HTTPException, status


@dataclass
class User:
    id: str
    username: str
    password: str
    tenant_ids: set[str] = field(default_factory=set)
    group_ids: set[str] = field(default_factory=set)


@dataclass
class Tenant:
    id: str
    name: str
    member_user_ids: set[str] = field(default_factory=set)


@dataclass
class Group:
    id: str
    name: str
    tenant_id: str
    member_user_ids: set[str] = field(default_factory=set)


@dataclass
class Record:
    id: str
    entity_id: str
    data: dict[str, Any] = field(default_factory=dict)
    owner_user_id: str = ""
    owner_perms: set[str] = field(default_factory=lambda: {"create", "read", "update", "delete"})
    group_perms: dict[str, set[str]] = field(default_factory=dict)
    tenant_perms: dict[str, set[str]] = field(default_factory=dict)
    public_perms: set[str] = field(default_factory=set)


USERS: dict[str, User] = {
    "user-admin": User(
        id="user-admin",
        username="admin",
        password="admin",
        tenant_ids={"tenant-default"},
        group_ids={"group-admins"},
    )
}

TENANTS: dict[str, Tenant] = {
    "tenant-default": Tenant(
        id="tenant-default",
        name="Default Tenant",
        member_user_ids={"user-admin"},
    )
}

GROUPS: dict[str, Group] = {
    "group-admins": Group(
        id="group-admins",
        name="Admins",
        tenant_id="tenant-default",
        member_user_ids={"user-admin"},
    )
}

RECORDS: dict[str, Record] = {}
TOKENS: dict[str, str] = {}


def _new_id(prefix: str) -> str:
    return f"{prefix}-{str(ulid.new())[:8].lower()}"


def _user_to_dict(user: User) -> dict[str, Any]:
    return {
        "id": user.id,
        "username": user.username,
        "tenant_ids": sorted(user.tenant_ids),
        "group_ids": sorted(user.group_ids),
    }


def _tenant_to_dict(tenant: Tenant) -> dict[str, Any]:
    return {
        "id": tenant.id,
        "name": tenant.name,
        "member_user_ids": sorted(tenant.member_user_ids),
    }


def _group_to_dict(group: Group) -> dict[str, Any]:
    return {
        "id": group.id,
        "name": group.name,
        "tenant_id": group.tenant_id,
        "member_user_ids": sorted(group.member_user_ids),
    }


def _record_to_dict(record: Record) -> dict[str, Any]:
    return {
        "id": record.id,
        "entity_id": record.entity_id,
        "data": record.data,
        "acl": {
            "owner_user_id": record.owner_user_id,
            "owner_perms": sorted(record.owner_perms),
            "group_perms": {
                key: sorted(value) for key, value in record.group_perms.items()
            },
            "tenant_perms": {
                key: sorted(value) for key, value in record.tenant_perms.items()
            },
            "public_perms": sorted(record.public_perms),
        },
    }


CRUD_PERMISSIONS = {"create", "read", "update", "delete"}


def _normalize_permission_set(value: Any, default: set[str] | None = None) -> set[str]:
    if value is None:
        return set(default or set())

    if isinstance(value, str):
        trimmed = value.strip()
        if not trimmed:
            return set(default or set())
        letter_map = {
            "c": "create",
            "r": "read",
            "u": "update",
            "d": "delete",
            "w": "update",
            "x": "delete",
        }
        if "," in trimmed:
            candidates = [item.strip().lower() for item in trimmed.split(",") if item.strip()]
        elif " " in trimmed:
            candidates = [item.strip().lower() for item in trimmed.split(" ") if item.strip()]
        elif all(char.lower() in letter_map for char in trimmed):
            candidates = [letter_map[char.lower()] for char in trimmed]
        else:
            candidates = [trimmed.lower()]
    elif isinstance(value, list):
        candidates = [str(item).strip().lower() for item in value if str(item).strip()]
    else:
        return set(default or set())

    normalized: set[str] = set()
    for candidate in candidates:
        if candidate in CRUD_PERMISSIONS:
            normalized.add(candidate)
    return normalized


def _normalize_permission_map(value: Any) -> dict[str, set[str]]:
    if not isinstance(value, dict):
        return {}

    result: dict[str, set[str]] = {}
    for key, perms in value.items():
        key_str = str(key)
        result[key_str] = _normalize_permission_set(perms)
    return result


def authenticate_user(username: str, password: str) -> User | None:
    for user in USERS.values():
        if user.username == username and user.password == password:
            return user
    return None


def issue_access_token(user: User) -> str:
    token = f"token-{user.id}-{str(ulid.new())[:8].lower()}"
    TOKENS[token] = user.id
    return token


def get_user_by_token(token: str) -> User:
    user_id = TOKENS.get(token)
    if user_id is None or user_id not in USERS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return USERS[user_id]


def list_users() -> list[dict[str, Any]]:
    return [_user_to_dict(user) for user in USERS.values()]


def create_user(payload: dict[str, Any]) -> dict[str, Any]:
    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password are required")

    user_id = payload.get("id") or _new_id("user")
    if user_id in USERS:
        raise HTTPException(status_code=409, detail="user id already exists")

    user = User(id=user_id, username=username, password=password)
    USERS[user.id] = user

    for tenant_id in payload.get("tenant_ids", []):
        add_user_to_tenant(user.id, tenant_id)
    for group_id in payload.get("group_ids", []):
        add_user_to_group(user.id, group_id)

    return _user_to_dict(user)


def get_user(user_id: str) -> dict[str, Any]:
    user = USERS.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return _user_to_dict(user)


def replace_user(user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    user = USERS.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    username = payload.get("username")
    password = payload.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="username and password are required")

    for tenant in TENANTS.values():
        tenant.member_user_ids.discard(user_id)
    for group in GROUPS.values():
        group.member_user_ids.discard(user_id)

    user.username = username
    user.password = password
    user.tenant_ids = set()
    user.group_ids = set()

    for tenant_id in payload.get("tenant_ids", []):
        add_user_to_tenant(user.id, tenant_id)
    for group_id in payload.get("group_ids", []):
        add_user_to_group(user.id, group_id)

    return _user_to_dict(user)


def update_user(user_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    user = USERS.get(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    if "username" in payload:
        user.username = payload["username"]
    if "password" in payload:
        user.password = payload["password"]
    if "tenant_ids" in payload:
        for tenant in TENANTS.values():
            tenant.member_user_ids.discard(user_id)
        user.tenant_ids = set()
        for tenant_id in payload["tenant_ids"]:
            add_user_to_tenant(user.id, tenant_id)
    if "group_ids" in payload:
        for group in GROUPS.values():
            group.member_user_ids.discard(user_id)
        user.group_ids = set()
        for group_id in payload["group_ids"]:
            add_user_to_group(user.id, group_id)

    return _user_to_dict(user)


def delete_user(user_id: str) -> dict[str, Any]:
    user = USERS.pop(user_id, None)
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")

    for tenant in TENANTS.values():
        tenant.member_user_ids.discard(user_id)
    for group in GROUPS.values():
        group.member_user_ids.discard(user_id)

    return {"id": user_id, "status": "deleted"}


def list_tenants() -> list[dict[str, Any]]:
    return [_tenant_to_dict(tenant) for tenant in TENANTS.values()]


def create_tenant(payload: dict[str, Any]) -> dict[str, Any]:
    tenant_name = payload.get("name")
    if not tenant_name:
        raise HTTPException(status_code=400, detail="name is required")

    tenant_id = payload.get("id") or _new_id("tenant")
    if tenant_id in TENANTS:
        raise HTTPException(status_code=409, detail="tenant id already exists")

    tenant = Tenant(id=tenant_id, name=tenant_name)
    TENANTS[tenant.id] = tenant

    for user_id in payload.get("member_user_ids", []):
        add_user_to_tenant(user_id, tenant.id)

    return _tenant_to_dict(tenant)


def get_tenant(tenant_id: str) -> dict[str, Any]:
    tenant = TENANTS.get(tenant_id)
    if tenant is None:
        raise HTTPException(status_code=404, detail="tenant not found")
    return _tenant_to_dict(tenant)


def replace_tenant(tenant_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    tenant = TENANTS.get(tenant_id)
    if tenant is None:
        raise HTTPException(status_code=404, detail="tenant not found")

    name = payload.get("name")
    if not name:
        raise HTTPException(status_code=400, detail="name is required")

    for user in USERS.values():
        user.tenant_ids.discard(tenant_id)

    tenant.name = name
    tenant.member_user_ids = set()

    for user_id in payload.get("member_user_ids", []):
        add_user_to_tenant(user_id, tenant_id)

    return _tenant_to_dict(tenant)


def update_tenant(tenant_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    tenant = TENANTS.get(tenant_id)
    if tenant is None:
        raise HTTPException(status_code=404, detail="tenant not found")

    if "name" in payload:
        tenant.name = payload["name"]
    if "member_user_ids" in payload:
        for user in USERS.values():
            user.tenant_ids.discard(tenant_id)
        tenant.member_user_ids = set()
        for user_id in payload["member_user_ids"]:
            add_user_to_tenant(user_id, tenant_id)

    return _tenant_to_dict(tenant)


def delete_tenant(tenant_id: str) -> dict[str, Any]:
    tenant = TENANTS.pop(tenant_id, None)
    if tenant is None:
        raise HTTPException(status_code=404, detail="tenant not found")

    for user in USERS.values():
        user.tenant_ids.discard(tenant_id)

    for group in list(GROUPS.values()):
        if group.tenant_id == tenant_id:
            delete_group(group.id)

    return {"id": tenant_id, "status": "deleted"}


def list_groups() -> list[dict[str, Any]]:
    return [_group_to_dict(group) for group in GROUPS.values()]


def create_group(payload: dict[str, Any]) -> dict[str, Any]:
    name = payload.get("name")
    tenant_id = payload.get("tenant_id")
    if not name or not tenant_id:
        raise HTTPException(status_code=400, detail="name and tenant_id are required")
    if tenant_id not in TENANTS:
        raise HTTPException(status_code=404, detail="tenant not found")

    group_id = payload.get("id") or _new_id("group")
    if group_id in GROUPS:
        raise HTTPException(status_code=409, detail="group id already exists")

    group = Group(id=group_id, name=name, tenant_id=tenant_id)
    GROUPS[group.id] = group

    for user_id in payload.get("member_user_ids", []):
        add_user_to_group(user_id, group.id)

    return _group_to_dict(group)


def get_group(group_id: str) -> dict[str, Any]:
    group = GROUPS.get(group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="group not found")
    return _group_to_dict(group)


def replace_group(group_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    group = GROUPS.get(group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="group not found")

    name = payload.get("name")
    tenant_id = payload.get("tenant_id")
    if not name or not tenant_id:
        raise HTTPException(status_code=400, detail="name and tenant_id are required")
    if tenant_id not in TENANTS:
        raise HTTPException(status_code=404, detail="tenant not found")

    for user in USERS.values():
        user.group_ids.discard(group_id)

    group.name = name
    group.tenant_id = tenant_id
    group.member_user_ids = set()

    for user_id in payload.get("member_user_ids", []):
        add_user_to_group(user_id, group.id)

    return _group_to_dict(group)


def update_group(group_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    group = GROUPS.get(group_id)
    if group is None:
        raise HTTPException(status_code=404, detail="group not found")

    if "name" in payload:
        group.name = payload["name"]
    if "tenant_id" in payload:
        tenant_id = payload["tenant_id"]
        if tenant_id not in TENANTS:
            raise HTTPException(status_code=404, detail="tenant not found")
        group.tenant_id = tenant_id
    if "member_user_ids" in payload:
        for user in USERS.values():
            user.group_ids.discard(group_id)
        group.member_user_ids = set()
        for user_id in payload["member_user_ids"]:
            add_user_to_group(user_id, group.id)

    return _group_to_dict(group)


def delete_group(group_id: str) -> dict[str, Any]:
    group = GROUPS.pop(group_id, None)
    if group is None:
        raise HTTPException(status_code=404, detail="group not found")

    for user in USERS.values():
        user.group_ids.discard(group_id)

    return {"id": group_id, "status": "deleted"}


def add_user_to_tenant(user_id: str, tenant_id: str) -> None:
    user = USERS.get(user_id)
    tenant = TENANTS.get(tenant_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"user '{user_id}' not found")
    if tenant is None:
        raise HTTPException(status_code=404, detail=f"tenant '{tenant_id}' not found")
    user.tenant_ids.add(tenant_id)
    tenant.member_user_ids.add(user_id)


def add_user_to_group(user_id: str, group_id: str) -> None:
    user = USERS.get(user_id)
    group = GROUPS.get(group_id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"user '{user_id}' not found")
    if group is None:
        raise HTTPException(status_code=404, detail=f"group '{group_id}' not found")

    user.group_ids.add(group_id)
    user.tenant_ids.add(group.tenant_id)
    group.member_user_ids.add(user_id)

    tenant = TENANTS.get(group.tenant_id)
    if tenant is not None:
        tenant.member_user_ids.add(user_id)


def list_records() -> list[dict[str, Any]]:
    return [_record_to_dict(record) for record in RECORDS.values()]


def create_record(payload: dict[str, Any], owner_user_id: str) -> dict[str, Any]:
    record_id = payload.get("id") or _new_id("record")
    if record_id in RECORDS:
        raise HTTPException(status_code=409, detail="record id already exists")

    entity_id = payload.get("entity_id")
    if not entity_id:
        raise HTTPException(status_code=400, detail="entity_id is required")

    acl = payload.get("acl", {})

    record = Record(
        id=record_id,
        entity_id=entity_id,
        data=payload.get("data", {}),
        owner_user_id=acl.get("owner_user_id", owner_user_id),
        owner_perms=_normalize_permission_set(
            acl.get("owner_perms"),
            default={"create", "read", "update", "delete"},
        ),
        group_perms=_normalize_permission_map(acl.get("group_perms", {})),
        tenant_perms=_normalize_permission_map(acl.get("tenant_perms", {})),
        public_perms=_normalize_permission_set(acl.get("public_perms")),
    )
    RECORDS[record.id] = record
    return _record_to_dict(record)


def get_record(record_id: str) -> Record:
    record = RECORDS.get(record_id)
    if record is None:
        raise HTTPException(status_code=404, detail="record not found")
    return record


def replace_record(record_id: str, payload: dict[str, Any], owner_user_id: str) -> dict[str, Any]:
    existing = get_record(record_id)
    entity_id = payload.get("entity_id")
    if not entity_id:
        raise HTTPException(status_code=400, detail="entity_id is required")

    acl = payload.get("acl", {})
    existing.entity_id = entity_id
    existing.data = payload.get("data", {})
    existing.owner_user_id = acl.get("owner_user_id", existing.owner_user_id or owner_user_id)
    existing.owner_perms = _normalize_permission_set(
        acl.get("owner_perms"),
        default={"create", "read", "update", "delete"},
    )
    existing.group_perms = _normalize_permission_map(acl.get("group_perms", {}))
    existing.tenant_perms = _normalize_permission_map(acl.get("tenant_perms", {}))
    existing.public_perms = _normalize_permission_set(acl.get("public_perms"))

    return _record_to_dict(existing)


def update_record(record_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    existing = get_record(record_id)
    if "entity_id" in payload:
        existing.entity_id = payload["entity_id"]
    if "data" in payload:
        existing.data = payload["data"]
    if "acl" in payload:
        acl = payload["acl"]
        if "owner_user_id" in acl:
            existing.owner_user_id = acl["owner_user_id"]
        if "owner_perms" in acl:
            existing.owner_perms = _normalize_permission_set(acl["owner_perms"])
        if "group_perms" in acl:
            existing.group_perms = _normalize_permission_map(acl["group_perms"])
        if "tenant_perms" in acl:
            existing.tenant_perms = _normalize_permission_map(acl["tenant_perms"])
        if "public_perms" in acl:
            existing.public_perms = _normalize_permission_set(acl["public_perms"])

    return _record_to_dict(existing)


def delete_record(record_id: str) -> dict[str, Any]:
    if record_id not in RECORDS:
        raise HTTPException(status_code=404, detail="record not found")
    del RECORDS[record_id]
    return {"id": record_id, "status": "deleted"}


def has_record_permission(user: User, record: Record, required_perm: str) -> bool:
    if required_perm not in CRUD_PERMISSIONS:
        return False

    if user.id == record.owner_user_id and required_perm in record.owner_perms:
        return True

    for group_id in user.group_ids:
        group_perms = record.group_perms.get(group_id, set())
        if required_perm in group_perms:
            return True

    for tenant_id in user.tenant_ids:
        tenant_perms = record.tenant_perms.get(tenant_id, set())
        if required_perm in tenant_perms:
            return True

    if required_perm in record.public_perms:
        return True

    return False


def require_record_permission(user: User, record_id: str, required_perm: str) -> Record:
    record = get_record(record_id)
    if not has_record_permission(user, record, required_perm):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Missing '{required_perm}' permission for record '{record_id}'",
        )
    return record
