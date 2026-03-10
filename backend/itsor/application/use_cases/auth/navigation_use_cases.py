from __future__ import annotations

from copy import deepcopy
from typing import Any

from itsor.application.ports.auth.repositories import (
    NavigationModuleRepository,
    NavigationResourceRepository,
    NavigationViewRepository,
)
from itsor.domain.models import Module, ModuleResource, ModuleType, NavigationView, ViewType


class NavigationAdminUseCases:
    def __init__(
        self,
        module_repo: NavigationModuleRepository,
        resource_repo: NavigationResourceRepository,
        view_repo: NavigationViewRepository,
    ) -> None:
        self._module_repo = module_repo
        self._resource_repo = resource_repo
        self._view_repo = view_repo

    def ensure_system_defaults(self) -> None:
        self._seed_default_catalog()

    def load_defaults(self, tenant_id: str | None = None) -> list[Module]:
        self.ensure_system_defaults()
        if tenant_id is None:
            return self.list_navigation(tenant_id=None, include_disabled=True)

        system_modules = self._module_repo.list_by_tenant(None)
        system_resources = self._resource_repo.list_by_tenant(None)
        system_views = self._view_repo.list_by_tenant(None)

        tenant_modules = self._module_repo.list_by_tenant(tenant_id)
        tenant_resources = self._resource_repo.list_by_tenant(tenant_id)
        tenant_views = self._view_repo.list_by_tenant(tenant_id)

        module_override_by_source = {item.source_id: item for item in tenant_modules if item.source_id}
        resource_override_by_source = {item.source_id: item for item in tenant_resources if item.source_id}
        view_override_by_source = {item.source_id: item for item in tenant_views if item.source_id}

        for system_module in system_modules:
            module_override = module_override_by_source.get(system_module.id)
            if module_override is None:
                module_override = self._module_repo.create(
                    Module(
                        key=system_module.key,
                        label=system_module.label,
                        module_type=system_module.module_type,
                        tenant_id=tenant_id,
                        source_id=system_module.id,
                        icon=system_module.icon,
                        order=system_module.order,
                        enabled=system_module.enabled,
                    )
                )
                module_override_by_source[system_module.id] = module_override

        for system_resource in system_resources:
            module_override = module_override_by_source.get(system_resource.module_id)
            if module_override is None:
                continue
            resource_override = resource_override_by_source.get(system_resource.id)
            if resource_override is None:
                resource_override = self._resource_repo.create(
                    ModuleResource(
                        key=system_resource.key,
                        label=system_resource.label,
                        module_id=module_override.id,
                        list_route=system_resource.list_route,
                        tenant_id=tenant_id,
                        source_id=system_resource.id,
                        icon=system_resource.icon,
                        order=system_resource.order,
                        enabled=system_resource.enabled,
                    )
                )
                resource_override_by_source[system_resource.id] = resource_override

        for system_view in system_views:
            resource_override = resource_override_by_source.get(system_view.resource_id)
            if resource_override is None:
                continue
            if view_override_by_source.get(system_view.id) is None:
                self._view_repo.create(
                    NavigationView(
                        key=system_view.key,
                        label=system_view.label,
                        view_type=system_view.view_type,
                        route=system_view.route,
                        resource_id=resource_override.id,
                        tenant_id=tenant_id,
                        source_id=system_view.id,
                        icon=system_view.icon,
                        order=system_view.order,
                        enabled=system_view.enabled,
                    )
                )

        return self.list_navigation(tenant_id=tenant_id, include_disabled=True)

    def set_default_menu(
        self,
        *,
        tenant_id: str | None,
        module_id: str,
        resource_id: str | None = None,
        view_id: str | None = None,
    ) -> dict[str, str]:
        module = self._resolve_module_for_update(module_id=module_id, tenant_id=tenant_id)
        scoped_modules = self._module_repo.list_by_tenant(module.tenant_id)
        self._promote_first(scoped_modules, selected_id=module.id, persist=self._module_repo.update)

        scoped_resources = [item for item in self._resource_repo.list_by_tenant(module.tenant_id) if item.module_id == module.id]
        if not scoped_resources:
            raise ValueError("Selected module has no resources")

        if resource_id:
            resource = self._resolve_resource_for_update(resource_id=resource_id, tenant_id=tenant_id)
            if resource.module_id != module.id:
                resource.module_id = module.id
                self._resource_repo.update(resource)
        else:
            resource = sorted(scoped_resources, key=lambda item: (item.order, item.label))[0]

        scoped_resources = [item for item in self._resource_repo.list_by_tenant(module.tenant_id) if item.module_id == module.id]
        self._promote_first(scoped_resources, selected_id=resource.id, persist=self._resource_repo.update)

        scoped_views = [item for item in self._view_repo.list_by_tenant(resource.tenant_id) if item.resource_id == resource.id]
        if not scoped_views:
            raise ValueError("Selected resource has no views")

        if view_id:
            view = self._resolve_view_for_update(view_id=view_id, tenant_id=tenant_id)
            if view.resource_id != resource.id:
                view.resource_id = resource.id
                self._view_repo.update(view)
        else:
            view = sorted(scoped_views, key=lambda item: (item.order, item.label))[0]

        scoped_views = [item for item in self._view_repo.list_by_tenant(resource.tenant_id) if item.resource_id == resource.id]
        self._promote_first(scoped_views, selected_id=view.id, persist=self._view_repo.update)

        return {
            "module_id": module.id,
            "resource_id": resource.id,
            "view_id": view.id,
        }

    def list_navigation(self, tenant_id: str | None = None, include_disabled: bool = True) -> list[Module]:
        self.ensure_system_defaults()

        system_modules = self._module_repo.list_by_tenant(None)
        system_resources = self._resource_repo.list_by_tenant(None)
        system_views = self._view_repo.list_by_tenant(None)

        tenant_modules = self._module_repo.list_by_tenant(tenant_id) if tenant_id else []
        tenant_resources = self._resource_repo.list_by_tenant(tenant_id) if tenant_id else []
        tenant_views = self._view_repo.list_by_tenant(tenant_id) if tenant_id else []

        module_overrides = {item.source_id: item for item in tenant_modules if item.source_id}
        resource_overrides = {item.source_id: item for item in tenant_resources if item.source_id}
        view_overrides = {item.source_id: item for item in tenant_views if item.source_id}

        effective_modules: list[Module] = []
        for system_module in system_modules:
            effective_modules.append(deepcopy(module_overrides.get(system_module.id, system_module)))
        effective_modules.extend(item for item in tenant_modules if item.source_id is None)

        for module in effective_modules:
            base_module_id = module.source_id or module.id
            scoped_system_resources = [item for item in system_resources if item.module_id == base_module_id]
            scoped_tenant_resources = [
                item
                for item in tenant_resources
                if item.source_id is None and item.module_id in {module.id, base_module_id}
            ]

            effective_resources: list[ModuleResource] = []
            for system_resource in scoped_system_resources:
                effective_resources.append(deepcopy(resource_overrides.get(system_resource.id, system_resource)))
            effective_resources.extend(scoped_tenant_resources)

            for resource in effective_resources:
                base_resource_id = resource.source_id or resource.id
                scoped_system_views = [item for item in system_views if item.resource_id == base_resource_id]
                scoped_tenant_views = [
                    item
                    for item in tenant_views
                    if item.source_id is None and item.resource_id in {resource.id, base_resource_id}
                ]

                effective_views: list[NavigationView] = []
                for system_view in scoped_system_views:
                    effective_views.append(deepcopy(view_overrides.get(system_view.id, system_view)))
                effective_views.extend(scoped_tenant_views)

                resource.views = self._sorted_filtered(effective_views, include_disabled=include_disabled)

            module.resources = self._sorted_filtered(effective_resources, include_disabled=include_disabled)

        return self._sorted_filtered(effective_modules, include_disabled=include_disabled)

    def create_module(
        self,
        *,
        key: str,
        label: str,
        module_type: ModuleType | str,
        order: int = 0,
        enabled: bool = True,
        icon: str | None = None,
        tenant_id: str | None = None,
        source_id: str | None = None,
    ) -> Module:
        module = Module(
            key=key,
            label=label,
            module_type=self._to_module_type(module_type),
            order=order,
            enabled=enabled,
            icon=icon,
            tenant_id=tenant_id,
            source_id=source_id,
        )
        return self._module_repo.create(module)

    def create_resource(
        self,
        *,
        key: str,
        label: str,
        module_id: str,
        list_route: str,
        order: int = 0,
        enabled: bool = True,
        icon: str | None = None,
        tenant_id: str | None = None,
        source_id: str | None = None,
    ) -> ModuleResource:
        resource = ModuleResource(
            key=key,
            label=label,
            module_id=module_id,
            list_route=list_route,
            order=order,
            enabled=enabled,
            icon=icon,
            tenant_id=tenant_id,
            source_id=source_id,
        )
        return self._resource_repo.create(resource)

    def create_view(
        self,
        *,
        key: str,
        label: str,
        view_type: ViewType | str,
        route: str,
        resource_id: str,
        order: int = 0,
        enabled: bool = True,
        icon: str | None = None,
        tenant_id: str | None = None,
        source_id: str | None = None,
    ) -> NavigationView:
        view = NavigationView(
            key=key,
            label=label,
            view_type=self._to_view_type(view_type),
            route=route,
            resource_id=resource_id,
            order=order,
            enabled=enabled,
            icon=icon,
            tenant_id=tenant_id,
            source_id=source_id,
        )
        return self._view_repo.create(view)

    def update_module(
        self,
        *,
        module_id: str,
        tenant_id: str | None,
        label: str | None = None,
        order: int | None = None,
        enabled: bool | None = None,
        icon: str | None = None,
    ) -> Module:
        module = self._resolve_module_for_update(module_id=module_id, tenant_id=tenant_id)
        if label is not None:
            module.label = label
        if order is not None:
            module.order = order
        if enabled is not None:
            module.enabled = enabled
        if icon is not None:
            module.icon = icon
        return self._module_repo.update(module)

    def update_resource(
        self,
        *,
        resource_id: str,
        tenant_id: str | None,
        label: str | None = None,
        module_id: str | None = None,
        list_route: str | None = None,
        order: int | None = None,
        enabled: bool | None = None,
        icon: str | None = None,
    ) -> ModuleResource:
        resource = self._resolve_resource_for_update(resource_id=resource_id, tenant_id=tenant_id)
        if label is not None:
            resource.label = label
        if module_id is not None:
            resource.module_id = module_id
        if list_route is not None:
            resource.list_route = list_route
        if order is not None:
            resource.order = order
        if enabled is not None:
            resource.enabled = enabled
        if icon is not None:
            resource.icon = icon
        return self._resource_repo.update(resource)

    def update_view(
        self,
        *,
        view_id: str,
        tenant_id: str | None,
        label: str | None = None,
        resource_id: str | None = None,
        route: str | None = None,
        order: int | None = None,
        enabled: bool | None = None,
        icon: str | None = None,
    ) -> NavigationView:
        view = self._resolve_view_for_update(view_id=view_id, tenant_id=tenant_id)
        if label is not None:
            view.label = label
        if resource_id is not None:
            view.resource_id = resource_id
        if route is not None:
            view.route = route
        if order is not None:
            view.order = order
        if enabled is not None:
            view.enabled = enabled
        if icon is not None:
            view.icon = icon
        return self._view_repo.update(view)

    def delete_module(self, *, module_id: str, tenant_id: str | None) -> None:
        module = self._resolve_module_for_delete(module_id=module_id, tenant_id=tenant_id)
        tenant_resources = self._resource_repo.list_by_tenant(module.tenant_id)
        for resource in [item for item in tenant_resources if item.module_id == module.id]:
            self.delete_resource(resource_id=resource.id, tenant_id=module.tenant_id)
        self._module_repo.delete(module.id)

    def delete_resource(self, *, resource_id: str, tenant_id: str | None) -> None:
        resource = self._resolve_resource_for_delete(resource_id=resource_id, tenant_id=tenant_id)
        tenant_views = self._view_repo.list_by_tenant(resource.tenant_id)
        for view in [item for item in tenant_views if item.resource_id == resource.id]:
            self._view_repo.delete(view.id)
        self._resource_repo.delete(resource.id)

    def delete_view(self, *, view_id: str, tenant_id: str | None) -> None:
        view = self._resolve_view_for_delete(view_id=view_id, tenant_id=tenant_id)
        self._view_repo.delete(view.id)

    def _resolve_module_for_update(self, *, module_id: str, tenant_id: str | None) -> Module:
        current = self._module_repo.get_by_id(module_id)
        if current is None:
            raise ValueError("Module not found")

        if tenant_id is None:
            if current.tenant_id is not None:
                raise ValueError("Tenant module requires tenant scope")
            return current

        if current.tenant_id == tenant_id:
            return current

        if current.tenant_id is not None and current.tenant_id != tenant_id:
            raise ValueError("Module does not belong to tenant")

        for item in self._module_repo.list_by_tenant(tenant_id):
            if item.source_id == current.id:
                return item

        return self._module_repo.create(
            Module(
                key=current.key,
                label=current.label,
                module_type=current.module_type,
                tenant_id=tenant_id,
                source_id=current.id,
                icon=current.icon,
                order=current.order,
                enabled=current.enabled,
            )
        )

    def _resolve_resource_for_update(self, *, resource_id: str, tenant_id: str | None) -> ModuleResource:
        current = self._resource_repo.get_by_id(resource_id)
        if current is None:
            raise ValueError("Resource not found")

        if tenant_id is None:
            if current.tenant_id is not None:
                raise ValueError("Tenant resource requires tenant scope")
            return current

        if current.tenant_id == tenant_id:
            return current

        if current.tenant_id is not None and current.tenant_id != tenant_id:
            raise ValueError("Resource does not belong to tenant")

        for item in self._resource_repo.list_by_tenant(tenant_id):
            if item.source_id == current.id:
                return item

        return self._resource_repo.create(
            ModuleResource(
                key=current.key,
                label=current.label,
                module_id=current.module_id,
                list_route=current.list_route,
                tenant_id=tenant_id,
                source_id=current.id,
                icon=current.icon,
                order=current.order,
                enabled=current.enabled,
            )
        )

    def _resolve_view_for_update(self, *, view_id: str, tenant_id: str | None) -> NavigationView:
        current = self._view_repo.get_by_id(view_id)
        if current is None:
            raise ValueError("View not found")

        if tenant_id is None:
            if current.tenant_id is not None:
                raise ValueError("Tenant view requires tenant scope")
            return current

        if current.tenant_id == tenant_id:
            return current

        if current.tenant_id is not None and current.tenant_id != tenant_id:
            raise ValueError("View does not belong to tenant")

        for item in self._view_repo.list_by_tenant(tenant_id):
            if item.source_id == current.id:
                return item

        return self._view_repo.create(
            NavigationView(
                key=current.key,
                label=current.label,
                view_type=current.view_type,
                route=current.route,
                resource_id=current.resource_id,
                tenant_id=tenant_id,
                source_id=current.id,
                icon=current.icon,
                order=current.order,
                enabled=current.enabled,
            )
        )

    def _resolve_module_for_delete(self, *, module_id: str, tenant_id: str | None) -> Module:
        current = self._module_repo.get_by_id(module_id)
        if current is None:
            raise ValueError("Module not found")
        if tenant_id is None and current.tenant_id is not None:
            raise ValueError("Tenant module requires tenant scope")
        if tenant_id is not None and current.tenant_id != tenant_id:
            raise ValueError("Module does not belong to tenant")
        return current

    def _resolve_resource_for_delete(self, *, resource_id: str, tenant_id: str | None) -> ModuleResource:
        current = self._resource_repo.get_by_id(resource_id)
        if current is None:
            raise ValueError("Resource not found")
        if tenant_id is None and current.tenant_id is not None:
            raise ValueError("Tenant resource requires tenant scope")
        if tenant_id is not None and current.tenant_id != tenant_id:
            raise ValueError("Resource does not belong to tenant")
        return current

    def _resolve_view_for_delete(self, *, view_id: str, tenant_id: str | None) -> NavigationView:
        current = self._view_repo.get_by_id(view_id)
        if current is None:
            raise ValueError("View not found")
        if tenant_id is None and current.tenant_id is not None:
            raise ValueError("Tenant view requires tenant scope")
        if tenant_id is not None and current.tenant_id != tenant_id:
            raise ValueError("View does not belong to tenant")
        return current

    def _seed_default_catalog(self) -> None:
        default_catalog: list[dict[str, Any]] = [
            {
                "module": {"key": "admin", "label": "Admin", "module_type": ModuleType.SYSTEM, "order": 0},
                "resources": [
                    {"key": "overview", "label": "Overview", "list_route": "/admin/overview", "order": 0},
                    {"key": "users", "label": "Users", "list_route": "/admin/users", "order": 10},
                    {"key": "groups", "label": "Groups", "list_route": "/admin/groups", "order": 20},
                    {"key": "roles", "label": "Roles", "list_route": "/admin/roles", "order": 30},
                    {"key": "permissions", "label": "Permissions", "list_route": "/admin/permissions", "order": 40},
                    {"key": "tenants", "label": "Tenants", "list_route": "/admin/tenants", "order": 50},
                    {"key": "navigation", "label": "Navigation", "list_route": "/admin/navigation", "order": 60},
                ],
            },
            {
                "module": {"key": "idm", "label": "Identity", "module_type": ModuleType.SYSTEM, "order": 100},
                "resources": [
                    {"key": "overview", "label": "Overview", "list_route": "/idm/overview", "order": 0},
                    {"key": "people", "label": "People", "list_route": "/idm/people", "order": 10},
                    {"key": "identities", "label": "Identities", "list_route": "/idm/identities", "order": 20},
                    {"key": "users", "label": "Users", "list_route": "/idm/users", "order": 30},
                    {"key": "groups", "label": "Groups", "list_route": "/idm/groups", "order": 40},
                    {"key": "group-memberships", "label": "Group Memberships", "list_route": "/idm/group-memberships", "order": 50},
                ],
            },
            {
                "module": {"key": "customization", "label": "Customization", "module_type": ModuleType.SYSTEM, "order": 200},
                "resources": [
                    {"key": "overview", "label": "Overview", "list_route": "/customization/overview", "order": 0},
                    {"key": "workspaces", "label": "Workspaces", "list_route": "/customization/workspaces", "order": 10},
                    {"key": "namespaces", "label": "Namespaces", "list_route": "/customization/namespaces", "order": 20},
                    {"key": "entity-types", "label": "Entity Types", "list_route": "/customization/entity-types", "order": 30},
                    {"key": "entity-records", "label": "Entity Records", "list_route": "/customization/entity-records", "order": 40},
                ],
            },
        ]

        system_modules = self._module_repo.list_by_tenant(None)
        system_resources = self._resource_repo.list_by_tenant(None)
        system_views = self._view_repo.list_by_tenant(None)

        module_by_key = {item.key: item for item in system_modules}

        for module_spec in default_catalog:
            module_info = module_spec["module"]
            module = module_by_key.get(module_info["key"])
            if module is None:
                module = self._module_repo.create(
                    Module(
                        key=module_info["key"],
                        label=module_info["label"],
                        module_type=module_info["module_type"],
                        order=module_info["order"],
                        enabled=True,
                    )
                )
                module_by_key[module.key] = module

            resource_by_key = {
                item.key: item
                for item in system_resources
                if item.module_id == module.id
            }

            for resource_spec in module_spec["resources"]:
                resource = resource_by_key.get(resource_spec["key"])
                if resource is None:
                    resource = self._resource_repo.create(
                        ModuleResource(
                            key=resource_spec["key"],
                            label=resource_spec["label"],
                            module_id=module.id,
                            list_route=resource_spec["list_route"],
                            order=resource_spec["order"],
                            enabled=True,
                        )
                    )
                    resource_by_key[resource.key] = resource

                view_exists = any(item.resource_id == resource.id and item.key == "default" for item in system_views)
                if not view_exists:
                    self._view_repo.create(
                        NavigationView(
                            key="default",
                            label=f"{resource.label} View",
                            view_type=ViewType.LIST,
                            route=resource.list_route,
                            resource_id=resource.id,
                            order=resource.order,
                            enabled=True,
                        )
                    )

    @staticmethod
    def _promote_first(items: list[Any], *, selected_id: str, persist) -> None:
        ordered = sorted(items, key=lambda item: (int(getattr(item, "order", 0)), str(getattr(item, "label", ""))))
        selected = next((item for item in ordered if str(item.id) == str(selected_id)), None)
        if selected is None:
            raise ValueError("Selection not found")

        reordered = [selected] + [item for item in ordered if str(item.id) != str(selected_id)]
        for index, item in enumerate(reordered):
            if int(getattr(item, "order", 0)) != index:
                item.order = index
                persist(item)

    @staticmethod
    def _sorted_filtered(items: list[Any], *, include_disabled: bool) -> list[Any]:
        if not include_disabled:
            items = [item for item in items if getattr(item, "enabled", True)]
        return sorted(items, key=lambda item: (int(getattr(item, "order", 0)), str(getattr(item, "label", ""))))

    @staticmethod
    def _to_module_type(value: ModuleType | str) -> ModuleType:
        if isinstance(value, ModuleType):
            return value
        return ModuleType(str(value).strip().lower())

    @staticmethod
    def _to_view_type(value: ViewType | str) -> ViewType:
        if isinstance(value, ViewType):
            return value
        return ViewType(str(value).strip().lower())
