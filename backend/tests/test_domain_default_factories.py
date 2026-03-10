from itsor.domain.models.group_models import Group
from itsor.domain.models.module_models import Module
from itsor.domain.models.permission_models import Permission, PermissionEffect
from itsor.domain.models.resource_models import (
	ModuleResource,
	Resource,
	ResourceAutomationTask,
	ResourceAutomationTaskType,
	ResourcePermissionAction,
	ResourceRecord,
	ResourceSlice,
)
from itsor.domain.models.role_models import Role
from itsor.domain.models.tenant_models import Tenant
from itsor.domain.models.user_models import User
from itsor.domain.models.view_models import ItemType, NavigationItem, NavigationView, ViewType


def test_mutable_default_factories_create_unique_containers() -> None:
	module_a = Module(key="users", label="Users")
	module_b = Module(key="roles", label="Roles")
	assert module_a.resources is not module_b.resources

	nav_item_a = NavigationItem(
		label="Users",
		item_type=ItemType.ROUTE,
		route="/users",
		resource_id="resource-users",
	)
	nav_item_b = NavigationItem(
		label="Roles",
		item_type=ItemType.ROUTE,
		route="/roles",
		resource_id="resource-roles",
	)
	assert nav_item_a.metadata is not nav_item_b.metadata

	nav_view_a = NavigationView(
		key="main-users",
		label="Main Users",
		view_type=ViewType.LIST,
		route="/users",
		resource_id="resource-users",
	)
	nav_view_b = NavigationView(
		key="main-roles",
		label="Main Roles",
		view_type=ViewType.LIST,
		route="/roles",
		resource_id="resource-roles",
	)
	assert nav_view_a.items is not nav_view_b.items

	slice_a = ResourceSlice(app_id="app-1", name="Users", table_id="table-1")
	slice_b = ResourceSlice(app_id="app-1", name="Roles", table_id="table-1")
	assert slice_a.column_list is not slice_b.column_list

	record_a = ResourceRecord(table_id="table-1")
	record_b = ResourceRecord(table_id="table-1")
	assert record_a.data_json is not record_b.data_json

	task_a = ResourceAutomationTask(
		process_id="process-1",
		type=ResourceAutomationTaskType.CALL_WEBHOOK,
	)
	task_b = ResourceAutomationTask(
		process_id="process-1",
		type=ResourceAutomationTaskType.CALL_WEBHOOK,
	)
	assert task_a.config_json is not task_b.config_json

	resource_a = ModuleResource(
		key="users",
		label="Users",
		module_id="module-1",
		list_route="/users",
	)
	resource_b = ModuleResource(
		key="roles",
		label="Roles",
		module_id="module-1",
		list_route="/roles",
	)
	assert resource_a.views is not resource_b.views


def test_entity_ids_are_auto_generated_and_type_compatible() -> None:
	user = User(
		name="User One",
		username="user-one",
		email="user.one@example.com",
		password_hash="hash",
	)
	tenant = Tenant(name="Tenant One")
	role = Role(name="Admin", tenant_id=None)
	module = Module(key="people", label="People")
	group = Group(tenant_id=None, name="All Users")
	permission = Permission(
		name="Can Read Users",
		resource=Resource.USER,
		action=ResourcePermissionAction.READ,
		effect=PermissionEffect.ALLOW,
	)
	record = ResourceRecord(table_id="table-1")
	view = NavigationView(
		key="users-list",
		label="Users List",
		view_type=ViewType.LIST,
		route="/users",
		resource_id="resource-users",
	)

	ids = [
		user.id,
		tenant.id,
		role.id,
		module.id,
		group.id,
		permission.id,
		record.id,
		view.id,
	]

	assert all(isinstance(entity_id, str) and entity_id for entity_id in ids)
	assert len(set(ids)) == len(ids)
