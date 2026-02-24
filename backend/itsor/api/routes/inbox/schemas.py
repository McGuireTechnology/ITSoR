from fastapi import APIRouter

router = APIRouter(tags=["schemas"])


@router.get("/schemas")
def list_schemas() -> dict:
    return {
        "resource": "schema",
        "status": "listed",
        "items": [],
    }


@router.post("/schemas")
def create_schema(payload: dict) -> dict:
    return {
        "resource": "schema",
        "status": "created",
        "payload": payload,
    }


@router.get("/schemas/{schema_id}")
def get_schema(schema_id: str) -> dict:
    return {
        "resource": "schema",
        "id": schema_id,
        "status": "retrieved",
    }


@router.put("/schemas/{schema_id}")
def replace_schema(schema_id: str, payload: dict) -> dict:
    return {
        "resource": "schema",
        "id": schema_id,
        "status": "replaced",
        "payload": payload,
    }


@router.patch("/schemas/{schema_id}")
def update_schema(schema_id: str, payload: dict) -> dict:
    return {
        "resource": "schema",
        "id": schema_id,
        "status": "updated",
        "payload": payload,
    }


@router.delete("/schemas/{schema_id}")
def delete_schema(schema_id: str) -> dict:
    return {
        "resource": "schema",
        "id": schema_id,
        "status": "deleted",
    }
