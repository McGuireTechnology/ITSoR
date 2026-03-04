from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import AuthorizationService, CurrentUser as User, get_authorization_service, get_current_user, get_entity_record_use_cases
from itsor.api.schemas.entity_record_schamas import (
    EntityRecordCreate,
    EntityRecordReplace,
    EntityRecordResponse,
    EntityRecordUpdate,
)
from itsor.application.use_cases.custom_use_cases import EntityRecordUseCases

router = APIRouter(prefix="/entity-records", tags=["entity-records"])


@router.get("", response_model=List[EntityRecordResponse])
def list_entity_records(
    entity_type_id: str | None = None,
    field: str | None = None,
    value: str | None = None,
    operator: str = "eq",
    use_cases: EntityRecordUseCases = Depends(get_entity_record_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    if entity_type_id:
        tenant_id = authz.resolve_tenant_id_for_entity_type(entity_type_id)
        if tenant_id:
            authz.authorize_tenant_scope(
                current_user=current_user,
                tenant_id=tenant_id,
                action="read",
                endpoint_name="entity-records",
            )

    if field is None and value is None:
        return use_cases.list_entity_records(entity_type_id)
    if not field or value is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="field and value are required when filtering",
        )
    try:
        return use_cases.search_entity_records(entity_type_id, field, value, operator)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("", response_model=EntityRecordResponse, status_code=status.HTTP_201_CREATED)
def create_entity_record(
    body: EntityRecordCreate,
    use_cases: EntityRecordUseCases = Depends(get_entity_record_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    tenant_id = authz.resolve_tenant_id_for_entity_type(body.entity_type_id)
    if tenant_id:
        authz.authorize_tenant_scope(
            current_user=current_user,
            tenant_id=tenant_id,
            action="write",
            endpoint_name="entity-records",
        )

    try:
        return use_cases.create_entity_record(body.entity_type_id, body.values_json, body.name, creator_user_id=current_user.id)
    except ValueError as exc:
        detail = str(exc)
        if detail == "Entity type not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.get("/{entity_record_id}", response_model=EntityRecordResponse)
def get_entity_record(
    entity_record_id: str,
    use_cases: EntityRecordUseCases = Depends(get_entity_record_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    entity_record = use_cases.get_entity_record(entity_record_id)
    if not entity_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity record not found")
    authz.authorize_resource_action(current_user=current_user, resource=entity_record, action="read", endpoint_name="entity-records")
    return entity_record


@router.patch("/{entity_record_id}", response_model=EntityRecordResponse)
def update_entity_record(
    entity_record_id: str,
    body: EntityRecordUpdate,
    use_cases: EntityRecordUseCases = Depends(get_entity_record_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    entity_record = use_cases.get_entity_record(entity_record_id)
    if not entity_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity record not found")
    authz.authorize_resource_action(current_user=current_user, resource=entity_record, action="write", endpoint_name="entity-records")

    try:
        return use_cases.update_entity_record(entity_record_id, body.name, body.values_json)
    except ValueError as exc:
        detail = str(exc)
        if detail == "Entity record not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.put("/{entity_record_id}", response_model=EntityRecordResponse)
def replace_entity_record(
    entity_record_id: str,
    body: EntityRecordReplace,
    use_cases: EntityRecordUseCases = Depends(get_entity_record_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    entity_record = use_cases.get_entity_record(entity_record_id)
    if not entity_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity record not found")
    authz.authorize_resource_action(current_user=current_user, resource=entity_record, action="write", endpoint_name="entity-records")

    try:
        return use_cases.replace_entity_record(
            entity_record_id,
            body.entity_type_id,
            body.values_json,
            body.name,
        )
    except ValueError as exc:
        detail = str(exc)
        if detail in {"Entity record not found", "Entity type not found"}:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.delete("/{entity_record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_entity_record(
    entity_record_id: str,
    use_cases: EntityRecordUseCases = Depends(get_entity_record_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    entity_record = use_cases.get_entity_record(entity_record_id)
    if not entity_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entity record not found")
    authz.authorize_resource_action(current_user=current_user, resource=entity_record, action="write", endpoint_name="entity-records")

    try:
        use_cases.delete_entity_record(entity_record_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
