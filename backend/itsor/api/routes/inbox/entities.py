from fastapi import APIRouter

router = APIRouter(tags=["entities"])


@router.get("/entities")
def list_entities() -> dict:
    return {
        "resource": "entity",
        "status": "listed",
        "items": [],
    }


@router.post("/entities")
def create_entity(payload: dict) -> dict:
    return {
        "resource": "entity",
        "status": "created",
        "payload": payload,
    }


@router.get("/entities/{entity_id}")
def get_entity(entity_id: str) -> dict:
    return {
        "resource": "entity",
        "id": entity_id,
        "status": "retrieved",
    }


@router.put("/entities/{entity_id}")
def replace_entity(entity_id: str, payload: dict) -> dict:
    return {
        "resource": "entity",
        "id": entity_id,
        "status": "replaced",
        "payload": payload,
    }


@router.patch("/entities/{entity_id}")
def update_entity(entity_id: str, payload: dict) -> dict:
    return {
        "resource": "entity",
        "id": entity_id,
        "status": "updated",
        "payload": payload,
    }


@router.delete("/entities/{entity_id}")
def delete_entity(entity_id: str) -> dict:
    return {
        "resource": "entity",
        "id": entity_id,
        "status": "deleted",
    }
