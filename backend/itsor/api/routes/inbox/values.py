from fastapi import APIRouter

router = APIRouter(tags=["values"])


@router.get("/values")
def list_values() -> dict:
    return {
        "resource": "value",
        "status": "listed",
        "items": [],
    }


@router.post("/values")
def create_value(payload: dict) -> dict:
    return {
        "resource": "value",
        "status": "created",
        "payload": payload,
    }


@router.get("/values/{value_id}")
def get_value(value_id: str) -> dict:
    return {
        "resource": "value",
        "id": value_id,
        "status": "retrieved",
    }


@router.put("/values/{value_id}")
def replace_value(value_id: str, payload: dict) -> dict:
    return {
        "resource": "value",
        "id": value_id,
        "status": "replaced",
        "payload": payload,
    }


@router.patch("/values/{value_id}")
def update_value(value_id: str, payload: dict) -> dict:
    return {
        "resource": "value",
        "id": value_id,
        "status": "updated",
        "payload": payload,
    }


@router.delete("/values/{value_id}")
def delete_value(value_id: str) -> dict:
    return {
        "resource": "value",
        "id": value_id,
        "status": "deleted",
    }
