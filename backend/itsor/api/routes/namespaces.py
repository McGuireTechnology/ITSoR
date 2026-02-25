from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from itsor.api.deps import get_current_user, get_namespace_use_cases
from itsor.api.schemas.namespace_schamas import (
    NamespaceCreate,
    NamespaceReplace,
    NamespaceResponse,
    NamespaceUpdate,
)
from itsor.domain.models import User
from itsor.domain.use_cases.namespace_use_cases import NamespaceUseCases

router = APIRouter(prefix="/namespaces", tags=["namespaces"])


@router.get("", response_model=List[NamespaceResponse])
def list_namespaces(
    workspace_id: str | None = None,
    use_cases: NamespaceUseCases = Depends(get_namespace_use_cases),
    _: User = Depends(get_current_user),
):
    return use_cases.list_namespaces(workspace_id)


@router.post("", response_model=NamespaceResponse, status_code=status.HTTP_201_CREATED)
def create_namespace(
    body: NamespaceCreate,
    use_cases: NamespaceUseCases = Depends(get_namespace_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.create_namespace(body.name, body.workspace_id)
    except ValueError as exc:
        detail = str(exc)
        if detail == "Workspace not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.get("/{namespace_id}", response_model=NamespaceResponse)
def get_namespace(
    namespace_id: str,
    use_cases: NamespaceUseCases = Depends(get_namespace_use_cases),
    _: User = Depends(get_current_user),
):
    namespace = use_cases.get_namespace(namespace_id)
    if not namespace:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Namespace not found")
    return namespace


@router.patch("/{namespace_id}", response_model=NamespaceResponse)
def update_namespace(
    namespace_id: str,
    body: NamespaceUpdate,
    use_cases: NamespaceUseCases = Depends(get_namespace_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.update_namespace(namespace_id, body.name)
    except ValueError as exc:
        detail = str(exc)
        if detail == "Namespace not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.put("/{namespace_id}", response_model=NamespaceResponse)
def replace_namespace(
    namespace_id: str,
    body: NamespaceReplace,
    use_cases: NamespaceUseCases = Depends(get_namespace_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        return use_cases.replace_namespace(namespace_id, body.name, body.workspace_id)
    except ValueError as exc:
        detail = str(exc)
        if detail in {"Namespace not found", "Workspace not found"}:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)


@router.delete("/{namespace_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_namespace(
    namespace_id: str,
    use_cases: NamespaceUseCases = Depends(get_namespace_use_cases),
    _: User = Depends(get_current_user),
):
    try:
        use_cases.delete_namespace(namespace_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
