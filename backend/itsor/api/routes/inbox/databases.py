from fastapi import APIRouter

router = APIRouter(tags=["databases"])


@router.get("/databases")
def list_databases() -> dict:
    return {
        "resource": "database",
        "status": "listed",
        "items": [],
    }


@router.post("/databases")
def create_database(payload: dict) -> dict:
    return {
        "resource": "database",
        "status": "created",
        "payload": payload,
    }


@router.get("/databases/{database_id}")
def get_database(database_id: str) -> dict:
    return {
        "resource": "database",
        "id": database_id,
        "status": "retrieved",
    }


@router.put("/databases/{database_id}")
def replace_database(database_id: str, payload: dict) -> dict:
    return {
        "resource": "database",
        "id": database_id,
        "status": "replaced",
        "payload": payload,
    }


@router.patch("/databases/{database_id}")
def update_database(database_id: str, payload: dict) -> dict:
    return {
        "resource": "database",
        "id": database_id,
        "status": "updated",
        "payload": payload,
    }


@router.delete("/databases/{database_id}")
def delete_database(database_id: str) -> dict:
    return {
        "resource": "database",
        "id": database_id,
        "status": "deleted",
    }
