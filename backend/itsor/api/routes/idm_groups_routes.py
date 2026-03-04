from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import CurrentUser as User, get_current_user, get_idm_group_use_cases
from itsor.api.schemas.idm_groups_schemas import IdmGroupCreate, IdmGroupResponse, IdmGroupUpdate
from itsor.application.use_cases.identity_use_cases import IdmGroupUseCases

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("", response_model=list[IdmGroupResponse])
def list_idm_groups(_: User = Depends(get_current_user), use_cases: IdmGroupUseCases = Depends(get_idm_group_use_cases)):
    return use_cases.list_groups()


@router.post("", response_model=IdmGroupResponse, status_code=status.HTTP_201_CREATED)
def create_idm_group(body: IdmGroupCreate, _: User = Depends(get_current_user), use_cases: IdmGroupUseCases = Depends(get_idm_group_use_cases)):
    return use_cases.create_group(name=body.name, description=body.description)


@router.get("/{group_id}", response_model=IdmGroupResponse)
def get_idm_group(group_id: str, _: User = Depends(get_current_user), use_cases: IdmGroupUseCases = Depends(get_idm_group_use_cases)):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="IDM group not found")
    return group


@router.patch("/{group_id}", response_model=IdmGroupResponse)
def update_idm_group(group_id: str, body: IdmGroupUpdate, _: User = Depends(get_current_user), use_cases: IdmGroupUseCases = Depends(get_idm_group_use_cases)):
    try:
        return use_cases.update_group(
            group_id=group_id,
            name=body.name,
            description=body.description,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_idm_group(group_id: str, _: User = Depends(get_current_user), use_cases: IdmGroupUseCases = Depends(get_idm_group_use_cases)):
    try:
        use_cases.delete_group(group_id)
    except ValueError as exc:
        detail = str(exc)
        status_code = status.HTTP_409_CONFLICT if detail == "IDM group is referenced by memberships" else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status_code, detail=detail)
