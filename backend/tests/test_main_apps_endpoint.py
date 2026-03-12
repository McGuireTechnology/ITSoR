from fastapi.testclient import TestClient

from itsor.main import app


client = TestClient(app)


def test_apps_endpoint_lists_active_apps_with_docs_links():
    response = client.get("/apps")

    assert response.status_code == 200
    payload = response.json()

    assert "apps" in payload
    assert isinstance(payload["apps"], list)

    apps_by_key = {item["key"]: item for item in payload["apps"]}
    assert set(apps_by_key) == {"auth", "itam", "oscal"}

    assert apps_by_key["auth"]["mount_path"] == "/auth"
    assert apps_by_key["auth"]["docs_url"] == "/auth/docs"
    assert apps_by_key["auth"]["openapi_url"] == "/auth/openapi.json"

    assert apps_by_key["itam"]["mount_path"] == "/itam"
    assert apps_by_key["itam"]["docs_url"] == "/itam/docs"
    assert apps_by_key["itam"]["openapi_url"] == "/itam/openapi.json"

    assert apps_by_key["oscal"]["mount_path"] == "/oscal"
    assert apps_by_key["oscal"]["docs_url"] == "/oscal/docs"
    assert apps_by_key["oscal"]["openapi_url"] == "/oscal/openapi.json"


def test_docs_page_includes_apps_menu_injection():
    response = client.get("/docs")

    assert response.status_code == 200
    assert "itsor-app-docs-links" in response.text
    assert "new URL('./apps'" in response.text
    assert "itsor-swagger-app-menu-fixed" in response.text
    assert 'href="/docs">Root API<' in response.text
    assert 'href="/apps">Apps JSON<' not in response.text
