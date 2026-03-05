from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_group_use_cases
from itsor.api.schemas.auth.group import GroupCreate, GroupReplace, GroupResponse, GroupUpdate
from itsor.application.use_cases.auth import GroupUseCases
from itsor.domain.ids import GroupId, TenantId

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/", response_model=list[GroupResponse])
def read_groups(use_cases: GroupUseCases = Depends(get_group_use_cases)):
    return use_cases.list_groups()


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group(body: GroupCreate, use_cases: GroupUseCases = Depends(get_group_use_cases)):
    try:
        tenant_id = TenantId(body.tenant_id) if body.tenant_id else None
        return use_cases.create_group(name=body.name, tenant_id=tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{group_id}", response_model=GroupResponse)
def read_group(group_id: GroupId, use_cases: GroupUseCases = Depends(get_group_use_cases)):
    group = use_cases.get_group(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Group not found")
    return group


@router.put("/{group_id}", response_model=GroupResponse)
def replace_group(group_id: GroupId, body: GroupReplace, use_cases: GroupUseCases = Depends(get_group_use_cases)):
    try:
        tenant_id = TenantId(body.tenant_id) if body.tenant_id else None
        return use_cases.replace_group(group_id=group_id, name=body.name, tenant_id=tenant_id)
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_409_CONFLICT if "already" in message.lower() else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=code, detail=message)


@router.patch("/{group_id}", response_model=GroupResponse)
def update_group(group_id: GroupId, body: GroupUpdate, use_cases: GroupUseCases = Depends(get_group_use_cases)):
    try:
        return use_cases.update_group(group_id=group_id, name=body.name)
    except ValueError as exc:
        message = str(exc)
        code = status.HTTP_409_CONFLICT if "already" in message.lower() else status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=code, detail=message)


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(group_id: GroupId, use_cases: GroupUseCases = Depends(get_group_use_cases)):
    try:
        use_cases.delete_group(group_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return None


