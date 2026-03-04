import pytest
from fastapi.testclient import TestClient
from itsor.api.apps.platform_app import app as platform_app
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_user_model import Base
from itsor.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

TEST_DATABASE_URL = "sqlite:///./test_itsor.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(setup_db):
    app.dependency_overrides[get_db] = override_get_db
    platform_app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
    platform_app.dependency_overrides.clear()


def _auth_headers(
    client: TestClient,
    username: str = "admin",
    email: str = "admin@example.com",
    password: str = "adminpass",
) -> dict[str, str]:
    client.post(
        "/signup",
        json={
            "username": username,
            "email": email,
            "password": password,
            "create_tenant_name": f"{username} Tenant",
        },
    )
    resp = client.post("/login", json={"identifier": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_user(client: TestClient, headers: dict[str, str], username: str, email: str) -> dict:
    response = client.post(
        "/platform/users",
        json={
            "username": username,
            "email": email,
            "password": "pw",
            "create_tenant_name": f"{username} Tenant",
        },
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


def _create_group(client: TestClient, headers: dict[str, str], name: str) -> dict:
    response = client.post("/platform/groups", json={"name": name}, headers=headers)
    assert response.status_code == 201
    return response.json()


def _create_tenant(client: TestClient, headers: dict[str, str], name: str) -> dict:
    response = client.post("/platform/tenants", json={"name": name}, headers=headers)
    assert response.status_code == 201
    return response.json()


def test_create_platform_rbac_entities(client: TestClient):
    headers = _auth_headers(client)

    tenant = _create_tenant(client, headers, "RBAC Tenant")
    group = _create_group(client, headers, "RBAC Group")
    user = _create_user(client, headers, "rbacuser", "rbacuser@example.com")

    role_response = client.post(
        "/platform/roles",
        json={
            "name": "RBAC Role",
            "tenant_id": tenant["id"],
            "description": "Role for API tests",
        },
        headers=headers,
    )
    assert role_response.status_code == 201
    role = role_response.json()
    assert role.get("id")

    permission_response = client.post(
        "/platform/permissions",
        json={
            "name": "Read Platform Users",
            "resource": "platform.user",
            "action": "read",
        },
        headers=headers,
    )
    assert permission_response.status_code == 201
    permission = permission_response.json()
    assert permission.get("id")

    user_tenant_response = client.post(
        "/platform/user-tenants",
        json={"user_id": user["id"], "tenant_id": tenant["id"]},
        headers=headers,
    )
    assert user_tenant_response.status_code == 201
    user_tenant = user_tenant_response.json()
    assert user_tenant.get("id")

    user_role_response = client.post(
        "/platform/user-roles",
        json={"user_id": user["id"], "role_id": role["id"]},
        headers=headers,
    )
    assert user_role_response.status_code == 201
    user_role = user_role_response.json()
    assert user_role.get("id")

    group_role_response = client.post(
        "/platform/group-roles",
        json={"group_id": group["id"], "role_id": role["id"]},
        headers=headers,
    )
    assert group_role_response.status_code == 201
    group_role = group_role_response.json()
    assert group_role.get("id")

    role_permission_response = client.post(
        "/platform/role-permissions",
        json={"role_id": role["id"], "permission_id": permission["id"]},
        headers=headers,
    )
    assert role_permission_response.status_code == 201
    role_permission = role_permission_response.json()
    assert role_permission.get("id")

    roles = client.get("/platform/roles", headers=headers).json()
    permissions = client.get("/platform/permissions", headers=headers).json()
    user_tenants = client.get("/platform/user-tenants", headers=headers).json()
    user_roles = client.get("/platform/user-roles", headers=headers).json()
    group_roles = client.get("/platform/group-roles", headers=headers).json()
    role_permissions = client.get("/platform/role-permissions", headers=headers).json()

    assert any(item["id"] == role["id"] for item in roles)
    assert any(item["id"] == permission["id"] for item in permissions)
    assert any(item["id"] == user_tenant["id"] for item in user_tenants)
    assert any(item["id"] == user_role["id"] for item in user_roles)
    assert any(item["id"] == group_role["id"] for item in group_roles)
    assert any(item["id"] == role_permission["id"] for item in role_permissions)


def test_platform_permission_rejects_execute_action(client: TestClient):
    headers = _auth_headers(client)

    response = client.post(
        "/platform/permissions",
        json={"name": "Execute Not Allowed", "resource": "platform.user", "action": "execute"},
        headers=headers,
    )

    assert response.status_code == 422
    details = response.json().get("detail", [])
    assert any(
        "Platform permission action must be one of: create, read, update, delete"
        in str(item.get("msg", ""))
        for item in details
        if isinstance(item, dict)
    )
