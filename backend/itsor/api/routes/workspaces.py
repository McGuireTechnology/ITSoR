from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_workspace_use_cases
from itsor.api.schemas.workspace_schamas import (
    WorkspaceCreate,
    WorkspaceReplace,
    WorkspaceResponse,
    WorkspaceUpdate,
)
from itsor.domain.models import User
from itsor.domain.use_cases.workspace_use_cases import WorkspaceUseCases

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.get("", response_model=List[WorkspaceResponse])
def list_workspaces(
    tenant_id: str | None = None,
    use_cases: WorkspaceUseCases = Depends(get_workspace_use_cases),
    _: User = Depends(get_current_user),
):
    return use_cases.list_workspaces(tenant_id)


@router.post("", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
def create_workspace(
    body: WorkspaceCreate,
    use_cases: WorkspaceUseCases = Depends(get_workspace_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.create_workspace(body.name, body.tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(
    workspace_id: str,
    use_cases: WorkspaceUseCases = Depends(get_workspace_use_cases),
    _: User = Depends(get_current_user),
):
    workspace = use_cases.get_workspace(workspace_id)
    if not workspace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workspace not found")
    return workspace


@router.patch("/{workspace_id}", response_model=WorkspaceResponse)
def update_workspace(
    workspace_id: str,
    body: WorkspaceUpdate,
    use_cases: WorkspaceUseCases = Depends(get_workspace_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.update_workspace(workspace_id, body.name)
    except ValueError as exc:
        detail = str(exc)
        if detail == "Workspace not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.put("/{workspace_id}", response_model=WorkspaceResponse)
def replace_workspace(
    workspace_id: str,
    body: WorkspaceReplace,
    use_cases: WorkspaceUseCases = Depends(get_workspace_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.replace_workspace(workspace_id, body.name, body.tenant_id)
    except ValueError as exc:
        detail = str(exc)
        if detail == "Workspace not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workspace(
    workspace_id: str,
    use_cases: WorkspaceUseCases = Depends(get_workspace_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        use_cases.delete_workspace(workspace_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
