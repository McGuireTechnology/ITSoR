from fastapi import APIRouter

router = APIRouter(tags=["attributes"])


@router.get("/attributes")
def list_attributes() -> dict:
    return {
        "resource": "attribute",
        "status": "listed",
        "items": [],
    }


@router.post("/attributes")
def create_attribute(payload: dict) -> dict:
    return {
        "resource": "attribute",
        "status": "created",
        "payload": payload,
    }


@router.get("/attributes/{attribute_id}")
def get_attribute(attribute_id: str) -> dict:
    return {
        "resource": "attribute",
        "id": attribute_id,
        "status": "retrieved",
    }


@router.put("/attributes/{attribute_id}")
def replace_attribute(attribute_id: str, payload: dict) -> dict:
    return {
        "resource": "attribute",
        "id": attribute_id,
        "status": "replaced",
        "payload": payload,
    }


@router.patch("/attributes/{attribute_id}")
def update_attribute(attribute_id: str, payload: dict) -> dict:
    return {
        "resource": "attribute",
        "id": attribute_id,
        "status": "updated",
        "payload": payload,
    }


@router.delete("/attributes/{attribute_id}")
def delete_attribute(attribute_id: str) -> dict:
    return {
        "resource": "attribute",
        "id": attribute_id,
        "status": "deleted",
    }
