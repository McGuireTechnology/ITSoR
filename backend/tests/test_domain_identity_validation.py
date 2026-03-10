import pytest

from itsor.domain.models.role_models import Role
from itsor.domain.models.tenant_models import Tenant
from itsor.domain.models.user_models import User


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_user_rejects_empty_required_strings(value: str) -> None:
    with pytest.raises(ValueError):
        User(name=value, username="valid-user", email="valid@example.com", password_hash="hash")

    with pytest.raises(ValueError):
        User(name="Valid User", username=value, email="valid@example.com", password_hash="hash")

    with pytest.raises(ValueError):
        User(name="Valid User", username="valid-user", email=value, password_hash="hash")


@pytest.mark.parametrize("value", ["", "   ", "\t\n"])
def test_role_and_tenant_reject_empty_name(value: str) -> None:
    with pytest.raises(ValueError):
        Role(name=value, tenant_id=None)

    with pytest.raises(ValueError):
        Tenant(name=value)


def test_user_normalizes_trimmed_values() -> None:
    user = User(
        name="  Jane Doe  ",
        username="  janedoe  ",
        email="  jane@example.com  ",
        password_hash="hash",
    )

    assert user.name == "Jane Doe"
    assert user.username == "janedoe"
    assert user.email == "jane@example.com"


def test_role_and_tenant_normalize_trimmed_name() -> None:
    role = Role(name="  Admin  ", tenant_id=None, description="  Ops role  ")
    tenant = Tenant(name="  Acme Corp  ")

    assert role.name == "Admin"
    assert role.description == "Ops role"
    assert tenant.name == "Acme Corp"
