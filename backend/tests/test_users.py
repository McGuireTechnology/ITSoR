import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from itsor.main import app
from itsor.infrastructure.container.database import get_db
from itsor.infrastructure.models.user import Base

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
    response = client.post("/signup", json={"email": "test@example.com", "password": "secret123"})
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_signup_duplicate(client):
    client.post("/signup", json={"email": "dup@example.com", "password": "pw"})
    response = client.post("/signup", json={"email": "dup@example.com", "password": "pw2"})
    assert response.status_code == 409


def test_login(client):
    client.post("/signup", json={"email": "user@example.com", "password": "pass"})
    response = client.post("/login", json={"email": "user@example.com", "password": "pass"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_invalid(client):
    response = client.post("/login", json={"email": "nobody@example.com", "password": "wrong"})
    assert response.status_code == 401


def test_logout(client):
    response = client.post("/logout")
    assert response.status_code == 204


def _auth_headers(client, email="admin@example.com", password="adminpass"):
    client.post("/signup", json={"email": email, "password": password})
    resp = client.post("/login", json={"email": email, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_list_users(client):
    headers = _auth_headers(client)
    response = client.get("/users", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user(client):
    headers = _auth_headers(client)
    response = client.post("/users", json={"email": "new@example.com", "password": "pw"}, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data


def test_get_user(client):
    headers = _auth_headers(client)
    created = client.post("/users", json={"email": "get@example.com", "password": "pw"}, headers=headers).json()
    response = client.get(f"/users/{created['id']}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "get@example.com"


def test_update_user(client):
    headers = _auth_headers(client)
    created = client.post("/users", json={"email": "patch@example.com", "password": "pw"}, headers=headers).json()
    response = client.patch(f"/users/{created['id']}", json={"email": "patched@example.com"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "patched@example.com"


def test_replace_user(client):
    headers = _auth_headers(client)
    created = client.post("/users", json={"email": "put@example.com", "password": "pw"}, headers=headers).json()
    response = client.put(f"/users/{created['id']}", json={"email": "replaced@example.com", "password": "newpw"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "replaced@example.com"


def test_delete_user(client):
    headers = _auth_headers(client)
    created = client.post("/users", json={"email": "del@example.com", "password": "pw"}, headers=headers).json()
    response = client.delete(f"/users/{created['id']}", headers=headers)
    assert response.status_code == 204
    get_resp = client.get(f"/users/{created['id']}", headers=headers)
    assert get_resp.status_code == 404


def test_get_user_not_found(client):
    headers = _auth_headers(client)
    response = client.get("/users/00000000-0000-0000-0000-000000000000", headers=headers)
    assert response.status_code == 404


def test_unauthorized_without_token(client):
    response = client.get("/users")
    assert response.status_code == 401
