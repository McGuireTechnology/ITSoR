from typing import get_type_hints

from itsor.domain.ids import AppId, ModuleId, NavigationItemId, ResourceId
from itsor.domain.models.resource_models import ResourceAction, ResourceAutomationBot, ResourceSlice, Table
from itsor.domain.models.view_models import AppView, ItemType, NavigationItem


def test_app_id_and_module_id_are_distinct_newtypes() -> None:
	assert AppId is not ModuleId
	assert AppId("app-1") == "app-1"
	assert ModuleId("module-1") == "module-1"


def test_app_models_use_app_id_annotations() -> None:
	assert get_type_hints(Table)["app_id"] is AppId
	assert get_type_hints(ResourceSlice)["app_id"] is AppId
	assert get_type_hints(ResourceAction)["app_id"] is AppId
	assert get_type_hints(ResourceAutomationBot)["app_id"] is AppId
	assert get_type_hints(AppView)["app_id"] is AppId


def test_navigation_item_uses_typed_navigation_item_id() -> None:
	assert get_type_hints(NavigationItem)["id"] is NavigationItemId

	item = NavigationItem(
		label="Users",
		item_type=ItemType.ROUTE,
		route="/users",
		resource_id=ResourceId("resource-users"),
	)

	assert isinstance(item.id, str)
	assert item.id