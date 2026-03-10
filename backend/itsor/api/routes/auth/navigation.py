from fastapi import APIRouter, Depends, HTTPException, Query, status

from itsor.api.deps import get_current_user, get_navigation_admin_use_cases
from itsor.api.schemas.auth.navigation import (
    NavigationDefaultResponse,
    NavigationLoadDefaultsRequest,
    NavigationModuleCreate,
    NavigationModuleResponse,
    NavigationModuleUpdate,
    NavigationResourceCreate,
    NavigationResourceResponse,
    NavigationResourceUpdate,
    NavigationSetDefaultRequest,
    NavigationViewCreate,
    NavigationViewResponse,
    NavigationViewUpdate,
)
from itsor.application.use_cases.auth import NavigationAdminUseCases

router = APIRouter(prefix="/admin/navigation", tags=["admin-navigation"], dependencies=[Depends(get_current_user)])


@router.get("/", response_model=list[NavigationModuleResponse])
def read_navigation_tree(
    tenant_id: str | None = Query(default=None),
    include_disabled: bool = Query(default=True),
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    return use_cases.list_navigation(tenant_id=tenant_id, include_disabled=include_disabled)


@router.post("/load-defaults", response_model=list[NavigationModuleResponse])
def load_defaults(
    body: NavigationLoadDefaultsRequest,
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        return use_cases.load_defaults(tenant_id=body.tenant_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.post("/set-default", response_model=NavigationDefaultResponse)
def set_default_menu(
    body: NavigationSetDefaultRequest,
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        return use_cases.set_default_menu(
            tenant_id=body.tenant_id,
            module_id=body.module_id,
            resource_id=body.resource_id,
            view_id=body.view_id,
        )
    except ValueError as exc:
        message = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=message)


@router.post("/modules", response_model=NavigationModuleResponse, status_code=status.HTTP_201_CREATED)
def create_module(
    body: NavigationModuleCreate,
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        return use_cases.create_module(
            key=body.key,
            label=body.label,
            module_type=body.module_type,
            tenant_id=body.tenant_id,
            source_id=body.source_id,
            icon=body.icon,
            order=body.order,
            enabled=body.enabled,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.patch("/modules/{module_id}", response_model=NavigationModuleResponse)
def update_module(
    module_id: str,
    body: NavigationModuleUpdate,
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        return use_cases.update_module(
            module_id=module_id,
            tenant_id=body.tenant_id,
            label=body.label,
            icon=body.icon,
            order=body.order,
            enabled=body.enabled,
        )
    except ValueError as exc:
        message = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=message)


@router.delete("/modules/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_module(
    module_id: str,
    tenant_id: str | None = Query(default=None),
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        use_cases.delete_module(module_id=module_id, tenant_id=tenant_id)
    except ValueError as exc:
        message = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=message)
    return None


@router.post("/resources", response_model=NavigationResourceResponse, status_code=status.HTTP_201_CREATED)
def create_resource(
    body: NavigationResourceCreate,
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        return use_cases.create_resource(
            key=body.key,
            label=body.label,
            module_id=body.module_id,
            list_route=body.list_route,
            tenant_id=body.tenant_id,
            source_id=body.source_id,
            icon=body.icon,
            order=body.order,
            enabled=body.enabled,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.patch("/resources/{resource_id}", response_model=NavigationResourceResponse)
def update_resource(
    resource_id: str,
    body: NavigationResourceUpdate,
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        return use_cases.update_resource(
            resource_id=resource_id,
            tenant_id=body.tenant_id,
            label=body.label,
            module_id=body.module_id,
            list_route=body.list_route,
            icon=body.icon,
            order=body.order,
            enabled=body.enabled,
        )
    except ValueError as exc:
        message = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=message)


@router.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: str,
    tenant_id: str | None = Query(default=None),
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        use_cases.delete_resource(resource_id=resource_id, tenant_id=tenant_id)
    except ValueError as exc:
        message = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=message)
    return None


@router.post("/views", response_model=NavigationViewResponse, status_code=status.HTTP_201_CREATED)
def create_view(
    body: NavigationViewCreate,
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        return use_cases.create_view(
            key=body.key,
            label=body.label,
            view_type=body.view_type,
            route=body.route,
            resource_id=body.resource_id,
            tenant_id=body.tenant_id,
            source_id=body.source_id,
            icon=body.icon,
            order=body.order,
            enabled=body.enabled,
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.patch("/views/{view_id}", response_model=NavigationViewResponse)
def update_view(
    view_id: str,
    body: NavigationViewUpdate,
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        return use_cases.update_view(
            view_id=view_id,
            tenant_id=body.tenant_id,
            label=body.label,
            resource_id=body.resource_id,
            route=body.route,
            icon=body.icon,
            order=body.order,
            enabled=body.enabled,
        )
    except ValueError as exc:
        message = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=message)


@router.delete("/views/{view_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_view(
    view_id: str,
    tenant_id: str | None = Query(default=None),
    use_cases: NavigationAdminUseCases = Depends(get_navigation_admin_use_cases),
):
    try:
        use_cases.delete_view(view_id=view_id, tenant_id=tenant_id)
    except ValueError as exc:
        message = str(exc)
        status_code = status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST
        raise HTTPException(status_code=status_code, detail=message)
    return None
