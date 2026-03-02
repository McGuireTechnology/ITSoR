import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from itsor.api.apps.platform import app as platform_app
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.sqlalchemy_user_model import Base
from itsor.main import app

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


def _auth_headers(client: TestClient, username: str = "admin", email: str = "admin@example.com", password: str = "adminpass") -> dict[str, str]:
    client.post(
        "/signup",
        json={"username": username, "email": email, "password": password, "create_tenant_name": f"{username} Tenant"},
    )
    resp = client.post("/login", json={"identifier": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_group(client: TestClient, headers: dict[str, str], name: str) -> dict:
    response = client.post("/platform/groups", json={"name": name}, headers=headers)
    assert response.status_code == 201
    return response.json()


def _create_user(client: TestClient, headers: dict[str, str], username: str, email: str) -> dict:
    response = client.post(
        "/platform/users",
        json={"username": username, "email": email, "password": "pw", "create_tenant_name": f"{username} Tenant"},
        headers=headers,
    )
    assert response.status_code == 201
    return response.json()


def test_create_group_membership_with_user_member(client: TestClient):
    headers = _auth_headers(client)
    group = _create_group(client, headers, "Parent Group")
    member_user = _create_user(client, headers, "member_user", "member_user@example.com")

    response = client.post(
        "/platform/group-memberships",
        json={
            "group_id": group["id"],
            "member_type": "user",
            "member_user_id": member_user["id"],
        },
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["group_id"] == group["id"]
    assert data["member_type"] == "user"
    assert data["member_user_id"] == member_user["id"]
    assert data["member_group_id"] is None


def test_create_group_membership_with_group_member(client: TestClient):
    headers = _auth_headers(client)
    parent_group = _create_group(client, headers, "Parent Group")
    child_group = _create_group(client, headers, "Child Group")

    response = client.post(
        "/platform/group-memberships",
        json={
            "group_id": parent_group["id"],
            "member_type": "group",
            "member_group_id": child_group["id"],
        },
        headers=headers,
    )

    assert response.status_code == 201
    data = response.json()
    assert data["group_id"] == parent_group["id"]
    assert data["member_type"] == "group"
    assert data["member_group_id"] == child_group["id"]
    assert data["member_user_id"] is None


def test_group_cannot_contain_itself(client: TestClient):
    headers = _auth_headers(client)
    group = _create_group(client, headers, "Self Group")

    response = client.post(
        "/platform/group-memberships",
        json={
            "group_id": group["id"],
            "member_type": "group",
            "member_group_id": group["id"],
        },
        headers=headers,
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Group cannot directly contain itself"


def test_invalid_member_type_returns_conflict(client: TestClient):
    headers = _auth_headers(client)
    group = _create_group(client, headers, "Type Group")

    response = client.post(
        "/platform/group-memberships",
        json={
            "group_id": group["id"],
            "member_type": "service",
            "member_user_id": "01ARZ3NDEKTSV4RRFFQ69G5FAV",
        },
        headers=headers,
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "member_type must be 'user' or 'group'"


def test_list_get_update_delete_group_membership(client: TestClient):
    headers = _auth_headers(client)
    parent_group = _create_group(client, headers, "Parent")
    child_group_a = _create_group(client, headers, "Child A")
    child_group_b = _create_group(client, headers, "Child B")

    created = client.post(
        "/platform/group-memberships",
        json={
            "group_id": parent_group["id"],
            "member_type": "group",
            "member_group_id": child_group_a["id"],
        },
        headers=headers,
    )
    assert created.status_code == 201
    membership_id = created.json()["id"]

    listed = client.get("/platform/group-memberships", headers=headers)
    assert listed.status_code == 200
    assert any(item["id"] == membership_id for item in listed.json())

    fetched = client.get(f"/platform/group-memberships/{membership_id}", headers=headers)
    assert fetched.status_code == 200
    assert fetched.json()["member_group_id"] == child_group_a["id"]

    updated = client.patch(
        f"/platform/group-memberships/{membership_id}",
        json={"member_group_id": child_group_b["id"]},
        headers=headers,
    )
    assert updated.status_code == 200
    assert updated.json()["member_group_id"] == child_group_b["id"]

    deleted = client.delete(f"/platform/group-memberships/{membership_id}", headers=headers)
    assert deleted.status_code == 204

    not_found = client.get(f"/platform/group-memberships/{membership_id}", headers=headers)
    assert not_found.status_code == 404
