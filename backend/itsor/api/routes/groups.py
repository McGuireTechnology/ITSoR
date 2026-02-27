from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import AuthorizationService, get_authorization_service, get_current_user, get_group_use_cases
from itsor.api.schemas.group_schamas import GroupCreate, GroupUpdate, GroupReplace, GroupResponse
from itsor.domain.models import User
from itsor.domain.use_cases.group_use_cases import GroupUseCases

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=List[GroupResponse])
def list_groups(
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    _: User = Depends(get_current_user),
):
    return use_cases.list_groups()


@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(
    body: GroupCreate,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    if body.tenant_id:
        authz.authorize_tenant_scope(
            current_user=current_user,
            tenant_id=body.tenant_id,
            action="write",
            endpoint_name="groups",
        )

    try:
        return use_cases.create_group(
            body.name,
            body.tenant_id,
            creator_user_id=current_user.id,
            platform_endpoint_permissions=body.platform_endpoint_permissions,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{group_id}", response_model=GroupResponse)
def get_group(
    group_id: str,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    authz.authorize_resource_action(current_user=current_user, resource=group, action="read", endpoint_name="groups")
    return group


@router.patch("/{group_id}", response_model=GroupResponse)
def update_group(
    group_id: str,
    body: GroupUpdate,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    authz.authorize_resource_action(current_user=current_user, resource=group, action="write", endpoint_name="groups")

    try:
        return use_cases.update_group(group_id, body.name, body.platform_endpoint_permissions)
    except ValueError as exc:
        error_detail = str(exc)
        if error_detail == "Group not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_detail)


@router.put("/{group_id}", response_model=GroupResponse)
def replace_group(
    group_id: str,
    body: GroupReplace,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    authz.authorize_resource_action(current_user=current_user, resource=group, action="write", endpoint_name="groups")

    try:
        return use_cases.replace_group(group_id, body.name, body.platform_endpoint_permissions)
    except ValueError as exc:
        error_detail = str(exc)
        if error_detail == "Group not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error_detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=error_detail)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(
    group_id: str,
    use_cases: GroupUseCases = Depends(get_group_use_cases),
    current_user: User = Depends(get_current_user),
    authz: AuthorizationService = Depends(get_authorization_service),
):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    authz.authorize_resource_action(current_user=current_user, resource=group, action="write", endpoint_name="groups")

    try:
        use_cases.delete_group(group_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
