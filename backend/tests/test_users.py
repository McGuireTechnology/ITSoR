import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from itsor.main import app
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_user_model import Base

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
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_signup(client):
    response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "secret123",
        },
    )
    assert response.status_code == 201
    assert "set-cookie" in response.headers
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_signup_does_not_create_tenant(client):
    client.post(
        "/signup",
        json={"username": "plainuser", "email": "plain@example.com", "password": "pw"},
    )
    login = client.post("/login", json={"identifier": "plain@example.com", "password": "pw"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    tenants = client.get("/tenants", headers=headers)
    assert tenants.status_code == 200
    assert tenants.json() == []


def test_signup_duplicate(client):
    client.post(
        "/signup",
        json={"username": "dupuser", "email": "dup@example.com", "password": "pw", "create_tenant_name": "Dup Tenant"},
    )
    response = client.post(
        "/signup",
        json={"username": "dupuser2", "email": "dup@example.com", "password": "pw2", "create_tenant_name": "Dup2 Tenant"},
    )
    assert response.status_code == 409


def test_login(client):
    client.post(
        "/signup",
        json={"username": "user1", "email": "user@example.com", "password": "pass", "create_tenant_name": "User1 Tenant"},
    )
    response = client.post("/login", json={"identifier": "user@example.com", "password": "pass"})
    assert response.status_code == 200
    assert "set-cookie" in response.headers
    assert "access_token" in response.json()


def test_login_with_username(client):
    client.post(
        "/signup",
        json={"username": "user2", "email": "user2@example.com", "password": "pass", "create_tenant_name": "User2 Tenant"},
    )
    response = client.post("/login", json={"identifier": "user2", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid(client):
    response = client.post("/login", json={"identifier": "nobody@example.com", "password": "wrong"})
    assert response.status_code == 401


def test_logout(client):
    client.post(
        "/signup",
        json={"username": "logoutuser", "email": "logout@example.com", "password": "pass", "create_tenant_name": "Logout Tenant"},
    )
    client.post("/login", json={"identifier": "logout@example.com", "password": "pass"})
    response = client.post("/logout")
    assert response.status_code == 204


def test_logout_requires_auth(client):
    response = client.post("/logout")
    assert response.status_code == 401


def _auth_headers(client, username="admin", email="admin@example.com", password="adminpass"):
    client.post(
        "/signup",
        json={"username": username, "email": email, "password": password, "create_tenant_name": f"{username} Tenant"},
    )
    resp = client.post("/login", json={"identifier": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_list_users(client):
    headers = _auth_headers(client)
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user(client):
    headers = _auth_headers(client)
    response = client.post(
        "/users",
        json={"username": "newuser", "email": "new@example.com", "password": "pw", "create_tenant_name": "New User Tenant"},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data


def test_get_user(client):
    headers = _auth_headers(client)
    created = client.post(
        "/users",
        json={"username": "getuser", "email": "get@example.com", "password": "pw", "create_tenant_name": "Get User Tenant"},
        headers=headers,
    ).json()
    response = client.get(f"/users/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "get@example.com"


def test_update_user(client):
    headers = _auth_headers(client)
    created = client.post(
        "/users",
        json={"username": "patchuser", "email": "patch@example.com", "password": "pw", "create_tenant_name": "Patch User Tenant"},
        headers=headers,
    ).json()
    response = client.patch(f"/users/{created['id']}", json={"username": "patcheduser", "email": "patched@example.com"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "patcheduser"
    assert response.json()["email"] == "patched@example.com"


def test_replace_user(client):
    headers = _auth_headers(client)
    created = client.post(
        "/users",
        json={"username": "putuser", "email": "put@example.com", "password": "pw", "create_tenant_name": "Put User Tenant"},
        headers=headers,
    ).json()
    response = client.put(f"/users/{created['id']}", json={"username": "replaceduser", "email": "replaced@example.com", "password": "newpw"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["username"] == "replaceduser"
    assert response.json()["email"] == "replaced@example.com"


def test_delete_user(client):
    headers = _auth_headers(client)
    created = client.post(
        "/users",
        json={"username": "deluser", "email": "del@example.com", "password": "pw", "create_tenant_name": "Del User Tenant"},
        headers=headers,
    ).json()
    response = client.delete(f"/users/{created['id']}", headers=headers)
    assert response.status_code == 204
    get_resp = client.get(f"/users/{created['id']}", headers=headers)
    assert get_resp.status_code == 404


def test_get_user_not_found(client):
    headers = _auth_headers(client)
    response = client.get("/users/01ARZ3NDEKTSV4RRFFQ69G5FAV", headers=headers)
    assert response.status_code == 404


def test_unauthorized_without_token(client):
    response = client.get("/users")
    assert response.status_code == 401


def test_cookie_auth_without_bearer_header(client):
    client.post(
        "/signup",
        json={"username": "cookieuser", "email": "cookie@example.com", "password": "pass", "create_tenant_name": "Cookie Tenant"},
    )
    client.post("/login", json={"identifier": "cookie@example.com", "password": "pass"})

    response = client.get("/users")
    assert response.status_code == 200


def test_list_tenants(client):
    headers = _auth_headers(client)
    response = client.get("/tenants", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_tenant(client):
    headers = _auth_headers(client)
    response = client.post("/tenants", json={"name": "Acme"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Acme"
    assert "id" in data


def test_create_tenant_duplicate_name(client):
    headers = _auth_headers(client)
    client.post("/tenants", json={"name": "Acme"}, headers=headers)
    response = client.post("/tenants", json={"name": "Acme"}, headers=headers)
    assert response.status_code == 409


def test_get_tenant(client):
    headers = _auth_headers(client)
    created = client.post("/tenants", json={"name": "Acme"}, headers=headers).json()
    response = client.get(f"/tenants/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Acme"


def test_update_tenant(client):
    headers = _auth_headers(client)
    created = client.post("/tenants", json={"name": "Acme"}, headers=headers).json()
    response = client.patch(f"/tenants/{created['id']}", json={"name": "Acme Updated"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Acme Updated"


def test_delete_tenant(client):
    headers = _auth_headers(client)
    created = client.post("/tenants", json={"name": "Acme"}, headers=headers).json()
    response = client.delete(f"/tenants/{created['id']}", headers=headers)
    assert response.status_code == 204
    get_resp = client.get(f"/tenants/{created['id']}", headers=headers)
    assert get_resp.status_code == 404


def test_tenants_requires_auth(client):
    response = client.get("/tenants")
    assert response.status_code == 401


def test_list_groups(client):
    headers = _auth_headers(client)
    response = client.get("/groups", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_group(client):
    headers = _auth_headers(client)
    response = client.post("/groups", json={"name": "Engineering"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Engineering"
    assert "id" in data


def test_create_group_duplicate_name(client):
    headers = _auth_headers(client)
    client.post("/groups", json={"name": "Engineering"}, headers=headers)
    response = client.post("/groups", json={"name": "Engineering"}, headers=headers)
    assert response.status_code == 409


def test_get_group(client):
    headers = _auth_headers(client)
    created = client.post("/groups", json={"name": "Engineering"}, headers=headers).json()
    response = client.get(f"/groups/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Engineering"


def test_update_group(client):
    headers = _auth_headers(client)
    created = client.post("/groups", json={"name": "Engineering"}, headers=headers).json()
    response = client.patch(f"/groups/{created['id']}", json={"name": "Platform"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Platform"


def test_delete_group(client):
    headers = _auth_headers(client)
    created = client.post("/groups", json={"name": "Engineering"}, headers=headers).json()
    response = client.delete(f"/groups/{created['id']}", headers=headers)
    assert response.status_code == 204
    get_resp = client.get(f"/groups/{created['id']}", headers=headers)
    assert get_resp.status_code == 404


def test_groups_requires_auth(client):
    response = client.get("/groups")
    assert response.status_code == 401


def test_create_tenant_creates_default_tenant_groups(client):
    headers = _auth_headers(client)
    created_tenant = client.post("/tenants", json={"name": "Beta"}, headers=headers).json()

    groups = client.get("/groups", headers=headers).json()
    tenant_groups = [g for g in groups if g.get("tenant_id") == created_tenant["id"]]

    names = sorted(g["name"] for g in tenant_groups)
    assert names == ["Tenant Admins", "Tenant Users"]


def test_eav_scaffold_flow(client):
    headers = _auth_headers(client)

    workspace = client.post(
        "/workspaces",
        json={"name": "CRM Workspace", "tenant_id": "tenant-alpha"},
        headers=headers,
    ).json()
    assert workspace["name"] == "CRM Workspace"

    namespace = client.post(
        "/namespaces",
        json={"name": "sales", "workspace_id": workspace["id"]},
        headers=headers,
    ).json()
    assert namespace["workspace_id"] == workspace["id"]

    entity_type = client.post(
        "/entity-types",
        json={
            "name": "customer",
            "namespace_id": namespace["id"],
            "attributes_json": {
                "email": {"type": "string", "required": True},
                "lifetime_value": {"type": "number", "required": False},
            },
        },
        headers=headers,
    ).json()
    assert entity_type["name"] == "customer"

    entity_record = client.post(
        "/entity-records",
        json={
            "entity_type_id": entity_type["id"],
            "name": "cust-001",
            "values_json": {
                "email": "user@example.com",
                "lifetime_value": 1250.5,
                "tags": ["vip", "north-america"],
            },
        },
        headers=headers,
    ).json()
    assert entity_record["values_json"]["email"] == "user@example.com"
    assert entity_record["entity_type_id"] == entity_type["id"]

    listed_records = client.get(
        f"/entity-records?entity_type_id={entity_type['id']}",
        headers=headers,
    )
    assert listed_records.status_code == 200
    assert len(listed_records.json()) == 1


def test_eav_routes_require_auth(client):
    assert client.get("/workspaces").status_code == 401
    assert client.get("/namespaces").status_code == 401
    assert client.get("/entity-types").status_code == 401
    assert client.get("/entity-records").status_code == 401


def test_eav_entity_record_search(client):
    headers = _auth_headers(client)

    workspace = client.post(
        "/workspaces",
        json={"name": "Search Workspace", "tenant_id": "tenant-beta"},
        headers=headers,
    ).json()
    namespace = client.post(
        "/namespaces",
        json={"name": "ops", "workspace_id": workspace["id"]},
        headers=headers,
    ).json()
    entity_type = client.post(
        "/entity-types",
        json={"name": "asset", "namespace_id": namespace["id"], "attributes_json": {}},
        headers=headers,
    ).json()

    client.post(
        "/entity-records",
        json={
            "entity_type_id": entity_type["id"],
            "name": "asset-1",
            "values_json": {"status": "active", "region": "us"},
        },
        headers=headers,
    )
    client.post(
        "/entity-records",
        json={
            "entity_type_id": entity_type["id"],
            "name": "asset-2",
            "values_json": {"status": "retired", "region": "eu"},
        },
        headers=headers,
    )

    response = client.get(
        f"/entity-records?entity_type_id={entity_type['id']}&field=status&value=active",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "asset-1"

    neq_response = client.get(
        f"/entity-records?entity_type_id={entity_type['id']}&field=status&value=active&operator=neq",
        headers=headers,
    )
    assert neq_response.status_code == 200
    neq_data = neq_response.json()
    assert len(neq_data) == 1
    assert neq_data[0]["name"] == "asset-2"

    contains_response = client.get(
        f"/entity-records?entity_type_id={entity_type['id']}&field=region&value=u&operator=contains",
        headers=headers,
    )
    assert contains_response.status_code == 200
    contains_data = contains_response.json()
    assert len(contains_data) == 2

    invalid_operator = client.get(
        f"/entity-records?entity_type_id={entity_type['id']}&field=status&value=active&operator=gt",
        headers=headers,
    )
    assert invalid_operator.status_code == 400


def test_eav_replace_endpoints(client):
    headers = _auth_headers(client)

    workspace = client.post(
        "/workspaces",
        json={"name": "Replace Workspace", "tenant_id": "tenant-replace"},
        headers=headers,
    ).json()
    replaced_workspace = client.put(
        f"/workspaces/{workspace['id']}",
        json={"name": "Replace Workspace 2", "tenant_id": "tenant-replace-2"},
        headers=headers,
    )
    assert replaced_workspace.status_code == 200
    assert replaced_workspace.json()["name"] == "Replace Workspace 2"
    assert replaced_workspace.json()["tenant_id"] == "tenant-replace-2"

    namespace = client.post(
        "/namespaces",
        json={"name": "replace-ns", "workspace_id": workspace["id"]},
        headers=headers,
    ).json()
    replaced_namespace = client.put(
        f"/namespaces/{namespace['id']}",
        json={"name": "replace-ns-2", "workspace_id": workspace["id"]},
        headers=headers,
    )
    assert replaced_namespace.status_code == 200
    assert replaced_namespace.json()["name"] == "replace-ns-2"

    entity_type = client.post(
        "/entity-types",
        json={"name": "replace-entity", "namespace_id": namespace["id"], "attributes_json": {"a": 1}},
        headers=headers,
    ).json()
    replaced_entity_type = client.put(
        f"/entity-types/{entity_type['id']}",
        json={"name": "replace-entity-2", "namespace_id": namespace["id"], "attributes_json": {"b": 2}},
        headers=headers,
    )
    assert replaced_entity_type.status_code == 200
    assert replaced_entity_type.json()["name"] == "replace-entity-2"
    assert replaced_entity_type.json()["attributes_json"] == {"b": 2}

    entity_record = client.post(
        "/entity-records",
        json={"entity_type_id": entity_type["id"], "name": "rec-1", "values_json": {"x": 1}},
        headers=headers,
    ).json()
    replaced_entity_record = client.put(
        f"/entity-records/{entity_record['id']}",
        json={"entity_type_id": entity_type["id"], "name": "rec-2", "values_json": {"x": 2}},
        headers=headers,
    )
    assert replaced_entity_record.status_code == 200
    assert replaced_entity_record.json()["name"] == "rec-2"
    assert replaced_entity_record.json()["values_json"] == {"x": 2}


def test_eav_workspace_delete_cascades(client):
    headers = _auth_headers(client)

    workspace = client.post(
        "/workspaces",
        json={"name": "Cascade Workspace", "tenant_id": "tenant-gamma"},
        headers=headers,
    ).json()
    namespace = client.post(
        "/namespaces",
        json={"name": "finance", "workspace_id": workspace["id"]},
        headers=headers,
    ).json()
    entity_type = client.post(
        "/entity-types",
        json={"name": "invoice", "namespace_id": namespace["id"], "attributes_json": {}},
        headers=headers,
    ).json()
    entity_record = client.post(
        "/entity-records",
        json={
            "entity_type_id": entity_type["id"],
            "name": "inv-1",
            "values_json": {"amount": 100},
        },
        headers=headers,
    ).json()

    delete_response = client.delete(f"/workspaces/{workspace['id']}", headers=headers)
    assert delete_response.status_code == 204

    assert client.get(f"/workspaces/{workspace['id']}", headers=headers).status_code == 404
    assert client.get(f"/namespaces/{namespace['id']}", headers=headers).status_code == 404
    assert client.get(f"/entity-types/{entity_type['id']}", headers=headers).status_code == 404
    assert client.get(f"/entity-records/{entity_record['id']}", headers=headers).status_code == 404
