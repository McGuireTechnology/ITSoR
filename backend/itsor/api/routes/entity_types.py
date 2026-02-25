from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_entity_type_use_cases
from itsor.api.schemas.entity_type_schamas import (
    EntityTypeCreate,
    EntityTypeReplace,
    EntityTypeResponse,
    EntityTypeUpdate,
)
from itsor.domain.models import User
from itsor.domain.use_cases.entity_type_use_cases import EntityTypeUseCases

router = APIRouter(prefix="/entity-types", tags=["entity-types"])


@router.get("", response_model=List[EntityTypeResponse])
def list_entity_types(
    namespace_id: str | None = None,
    use_cases: EntityTypeUseCases = Depends(get_entity_type_use_cases),
    _: User = Depends(get_current_user),
):
    return use_cases.list_entity_types(namespace_id)


@router.post("", response_model=EntityTypeResponse, status_code=status.HTTP_201_CREATED)
def create_entity_type(
    body: EntityTypeCreate,
    use_cases: EntityTypeUseCases = Depends(get_entity_type_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.create_entity_type(body.name, body.namespace_id, body.attributes_json)
    except ValueError as exc:
        detail = str(exc)
        if detail == "Namespace not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.get("/{entity_type_id}", response_model=EntityTypeResponse)
def get_entity_type(
    entity_type_id: str,
    use_cases: EntityTypeUseCases = Depends(get_entity_type_use_cases),
    _: User = Depends(get_current_user),
):
    entity_type = use_cases.get_entity_type(entity_type_id)
    if not entity_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity type not found")
    return entity_type


@router.patch("/{entity_type_id}", response_model=EntityTypeResponse)
def update_entity_type(
    entity_type_id: str,
    body: EntityTypeUpdate,
    use_cases: EntityTypeUseCases = Depends(get_entity_type_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.update_entity_type(entity_type_id, body.name, body.attributes_json)
    except ValueError as exc:
        detail = str(exc)
        if detail == "Entity type not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.put("/{entity_type_id}", response_model=EntityTypeResponse)
def replace_entity_type(
    entity_type_id: str,
    body: EntityTypeReplace,
    use_cases: EntityTypeUseCases = Depends(get_entity_type_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.replace_entity_type(
            entity_type_id,
            body.name,
            body.namespace_id,
            body.attributes_json,
        )
    except ValueError as exc:
        detail = str(exc)
        if detail in {"Entity type not found", "Namespace not found"}:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.delete("/{entity_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entity_type(
    entity_type_id: str,
    use_cases: EntityTypeUseCases = Depends(get_entity_type_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        use_cases.delete_entity_type(entity_type_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
