import pytest

from itsor.domain.models.module_models import Module
from itsor.domain.models.resource_models import (
    ModuleResource,
    ResourceAction,
    ResourceActionType,
    ResourceAttribute,
    ResourceAttributeType,
    ResourceAutomationBot,
    ResourceAutomationProcess,
    ResourceSecurityRule,
    ResourceSlice,
    Table,
)
from itsor.domain.models.role_models import Role
from itsor.domain.models.tenant_models import Tenant
from itsor.domain.models.user_models import User
from itsor.domain.models.view_models import AppView, AppViewType, ItemType, NavigationItem, NavigationView, ViewType


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_user_rejects_empty_required_fields(value: str) -> None:
    with pytest.raises(ValueError, match="name is required"):
        User(name=value, username="valid-user", email="valid@example.com", password_hash="hash")

    with pytest.raises(ValueError, match="username is required"):
        User(name="Valid User", username=value, email="valid@example.com", password_hash="hash")

    with pytest.raises(ValueError, match="email is required"):
        User(name="Valid User", username="valid-user", email=value, password_hash="hash")


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_tenant_and_role_reject_empty_name(value: str) -> None:
    with pytest.raises(ValueError, match="name is required"):
        Tenant(name=value)

    with pytest.raises(ValueError, match="name is required"):
        Role(name=value, tenant_id=None)


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_module_rejects_empty_key_or_label(value: str) -> None:
    with pytest.raises(ValueError, match="Module key cannot be empty"):
        Module(key=value, label="Users")

    with pytest.raises(ValueError, match="Module label cannot be empty"):
        Module(key="users", label=value)


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_navigation_view_rejects_empty_key_label_or_route(value: str) -> None:
    with pytest.raises(ValueError, match="Navigation view key cannot be empty"):
        NavigationView(
            key=value,
            label="Users",
            view_type=ViewType.LIST,
            route="/users",
            resource_id="resource-users",
        )

    with pytest.raises(ValueError, match="Navigation view label cannot be empty"):
        NavigationView(
            key="users-list",
            label=value,
            view_type=ViewType.LIST,
            route="/users",
            resource_id="resource-users",
        )

    with pytest.raises(ValueError, match="Navigation view route cannot be empty"):
        NavigationView(
            key="users-list",
            label="Users",
            view_type=ViewType.LIST,
            route=value,
            resource_id="resource-users",
        )


def test_core_entities_normalize_trimmed_values() -> None:
    user = User(
        name="  Jane Doe  ",
        username="  janedoe  ",
        email="  jane@example.com  ",
        password_hash="hash",
    )
    tenant = Tenant(name="  Acme Corp  ")
    role = Role(name="  Admin  ", tenant_id=None, description="  Ops role  ")
    module = Module(key="  users  ", label="  Users  ")
    view = NavigationView(
        key="  users-list  ",
        label="  Users List  ",
        view_type=ViewType.LIST,
        route="  /users  ",
        resource_id="resource-users",
    )

    assert user.name == "Jane Doe"
    assert user.username == "janedoe"
    assert user.email == "jane@example.com"
    assert tenant.name == "Acme Corp"
    assert role.name == "Admin"
    assert role.description == "Ops role"
    assert module.key == "users"
    assert module.label == "Users"
    assert view.key == "users-list"
    assert view.label == "Users List"
    assert view.route == "/users"


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_key_resource_models_reject_empty_required_text(value: str) -> None:
    with pytest.raises(ValueError, match="Table name cannot be empty"):
        Table(app_id="app-1", name=value)

    with pytest.raises(ValueError, match="Column name cannot be empty"):
        ResourceAttribute(table_id="table-1", name=value, type=ResourceAttributeType.TEXT)

    with pytest.raises(ValueError, match="Slice name cannot be empty"):
        ResourceSlice(app_id="app-1", name=value, table_id="table-1")

    with pytest.raises(ValueError, match="Action name cannot be empty"):
        ResourceAction(
            app_id="app-1",
            name=value,
            table_id="table-1",
            type=ResourceActionType.NAVIGATE,
        )

    with pytest.raises(ValueError, match="Bot name cannot be empty"):
        ResourceAutomationBot(app_id="app-1", name=value)

    with pytest.raises(ValueError, match="Process name cannot be empty"):
        ResourceAutomationProcess(bot_id="bot-1", name=value)

    with pytest.raises(ValueError, match="SecurityRule filter_expression cannot be empty"):
        ResourceSecurityRule(table_id="table-1", filter_expression=value)


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_module_resource_rejects_empty_required_fields(value: str) -> None:
    with pytest.raises(ValueError, match="Module resource key cannot be empty"):
        ModuleResource(key=value, label="Users", module_id="module-1", list_route="/users")

    with pytest.raises(ValueError, match="Module resource label cannot be empty"):
        ModuleResource(key="users", label=value, module_id="module-1", list_route="/users")

    with pytest.raises(ValueError, match="Module resource list_route cannot be empty"):
        ModuleResource(key="users", label="Users", module_id="module-1", list_route=value)


def test_key_resource_models_normalize_trimmed_values() -> None:
    table = Table(app_id="app-1", name="  Accounts  ")
    column = ResourceAttribute(table_id="table-1", name="  Name  ", type=ResourceAttributeType.TEXT)
    slice_model = ResourceSlice(app_id="app-1", name="  Active  ", table_id="table-1")
    action = ResourceAction(
        app_id="app-1",
        name="  Open Details  ",
        table_id="table-1",
        type=ResourceActionType.NAVIGATE,
    )
    bot = ResourceAutomationBot(app_id="app-1", name="  Reminder Bot  ")
    process = ResourceAutomationProcess(bot_id="bot-1", name="  Follow Up  ")
    security_rule = ResourceSecurityRule(table_id="table-1", filter_expression="  [Owner] = USEREMAIL()  ")
    resource = ModuleResource(
        key="  users  ",
        label="  Users  ",
        module_id="module-1",
        list_route="  /users  ",
    )

    assert table.name == "Accounts"
    assert column.name == "Name"
    assert slice_model.name == "Active"
    assert action.name == "Open Details"
    assert bot.name == "Reminder Bot"
    assert process.name == "Follow Up"
    assert security_rule.filter_expression == "[Owner] = USEREMAIL()"
    assert resource.key == "users"
    assert resource.label == "Users"
    assert resource.list_route == "/users"


@pytest.mark.parametrize(
    ("factory", "error_message"),
    [
        (lambda: Module(key="users", label="Users", order=-1), "Module order cannot be negative"),
        (
            lambda: ModuleResource(
                key="users",
                label="Users",
                module_id="module-1",
                list_route="/users",
                order=-1,
            ),
            "Module resource order cannot be negative",
        ),
        (
            lambda: NavigationItem(
                label="Users",
                item_type=ItemType.ROUTE,
                route="/users",
                resource_id="resource-users",
                order=-1,
            ),
            "Navigation item order cannot be negative",
        ),
        (
            lambda: NavigationView(
                key="users-list",
                label="Users",
                view_type=ViewType.LIST,
                route="/users",
                resource_id="resource-users",
                order=-1,
            ),
            "Navigation view order cannot be negative",
        ),
        (
            lambda: AppView(
                app_id="app-1",
                name="Users",
                type=AppViewType.TABLE,
                table_id="table-1",
                position=-1,
            ),
            "View position cannot be negative",
        ),
    ],
)
def test_order_and_position_fields_reject_negative_values(factory, error_message: str) -> None:
    with pytest.raises(ValueError, match=error_message):
        factory()


def test_order_and_position_fields_allow_zero_and_positive_values() -> None:
    module = Module(key="users", label="Users", order=0)
    resource = ModuleResource(
        key="users",
        label="Users",
        module_id="module-1",
        list_route="/users",
        order=1,
    )
    item = NavigationItem(
        label="Users",
        item_type=ItemType.ROUTE,
        route="/users",
        resource_id="resource-users",
        order=2,
    )
    view = NavigationView(
        key="users-list",
        label="Users",
        view_type=ViewType.LIST,
        route="/users",
        resource_id="resource-users",
        order=3,
    )
    app_view = AppView(
        app_id="app-1",
        name="Users",
        type=AppViewType.TABLE,
        table_id="table-1",
        position=4,
    )

    assert module.order == 0
    assert resource.order == 1
    assert item.order == 2
    assert view.order == 3
    assert app_view.position == 4
