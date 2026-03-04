from typing import Any, Protocol


class IdmGroupGateway(Protocol):
	def list_groups(self) -> list[Any]: ...

	def create_group(self, *, name: str, description: str = "") -> Any: ...

	def get_group(self, group_id: str) -> Any | None: ...

	def update_group(
		self,
		*,
		group_id: str,
		name: str | None = None,
		description: str | None = None,
	) -> Any: ...

	def delete_group(self, group_id: str) -> None: ...


class IdmUserGateway(Protocol):
	def list_users(self) -> list[Any]: ...

	def create_user(self, *, person_id: str, username: str, account_status: str = "active") -> Any: ...

	def get_user(self, user_id: str) -> Any | None: ...

	def update_user(
		self,
		*,
		user_id: str,
		username: str | None = None,
		account_status: str | None = None,
	) -> Any: ...

	def delete_user(self, user_id: str) -> None: ...


class IdmPersonGateway(Protocol):
	def list_people(self) -> list[Any]: ...

	def create_person(self, *, display_name: str = "", current_identity_id: str | None = None) -> Any: ...

	def get_person(self, person_id: str) -> Any | None: ...

	def update_person(
		self,
		*,
		person_id: str,
		display_name: str | None = None,
		current_identity_id: str | None = None,
	) -> Any: ...

	def delete_person(self, person_id: str) -> None: ...


class IdmIdentityGateway(Protocol):
	def list_identities(self) -> list[Any]: ...

	def create_identity(
		self,
		*,
		person_id: str,
		source_system: str,
		source_record_id: str,
		demographic_payload: dict[str, Any] | None = None,
		valid_from: Any | None = None,
		valid_to: Any | None = None,
		superseded_at: Any | None = None,
	) -> Any: ...

	def get_identity(self, identity_id: str) -> Any | None: ...

	def update_identity(
		self,
		*,
		identity_id: str,
		source_system: str | None = None,
		source_record_id: str | None = None,
		demographic_payload: dict[str, Any] | None = None,
		valid_from: Any | None = None,
		valid_to: Any | None = None,
		superseded_at: Any | None = None,
	) -> Any: ...

	def delete_identity(self, identity_id: str) -> None: ...


class IdmGroupMembershipGateway(Protocol):
	def list_group_memberships(self) -> list[Any]: ...

	def create_group_membership(
		self,
		*,
		group_id: str,
		member_type: str,
		member_user_id: str | None = None,
		member_group_id: str | None = None,
	) -> Any: ...

	def get_group_membership(self, membership_id: str) -> Any | None: ...

	def update_group_membership(
		self,
		*,
		membership_id: str,
		member_type: str | None = None,
		member_user_id: str | None = None,
		member_group_id: str | None = None,
	) -> Any: ...

	def delete_group_membership(self, membership_id: str) -> None: ...


class IdmGroupUseCases:
	def __init__(self, gateway: IdmGroupGateway) -> None:
		self._gateway = gateway

	def list_groups(self) -> list[Any]:
		return self._gateway.list_groups()

	def create_group(self, *, name: str, description: str = "") -> Any:
		return self._gateway.create_group(name=name, description=description)

	def get_group(self, group_id: str) -> Any | None:
		return self._gateway.get_group(group_id)

	def update_group(
		self,
		*,
		group_id: str,
		name: str | None = None,
		description: str | None = None,
	) -> Any:
		return self._gateway.update_group(
			group_id=group_id,
			name=name,
			description=description,
		)

	def delete_group(self, group_id: str) -> None:
		self._gateway.delete_group(group_id)


class IdmUserUseCases:
	def __init__(self, gateway: IdmUserGateway) -> None:
		self._gateway = gateway

	def list_users(self) -> list[Any]:
		return self._gateway.list_users()

	def create_user(self, *, person_id: str, username: str, account_status: str = "active") -> Any:
		return self._gateway.create_user(person_id=person_id, username=username, account_status=account_status)

	def get_user(self, user_id: str) -> Any | None:
		return self._gateway.get_user(user_id)

	def update_user(
		self,
		*,
		user_id: str,
		username: str | None = None,
		account_status: str | None = None,
	) -> Any:
		return self._gateway.update_user(
			user_id=user_id,
			username=username,
			account_status=account_status,
		)

	def delete_user(self, user_id: str) -> None:
		self._gateway.delete_user(user_id)


class IdmPersonUseCases:
	def __init__(self, gateway: IdmPersonGateway) -> None:
		self._gateway = gateway

	def list_people(self) -> list[Any]:
		return self._gateway.list_people()

	def create_person(self, *, display_name: str = "", current_identity_id: str | None = None) -> Any:
		return self._gateway.create_person(
			display_name=display_name,
			current_identity_id=current_identity_id,
		)

	def get_person(self, person_id: str) -> Any | None:
		return self._gateway.get_person(person_id)

	def update_person(
		self,
		*,
		person_id: str,
		display_name: str | None = None,
		current_identity_id: str | None = None,
	) -> Any:
		return self._gateway.update_person(
			person_id=person_id,
			display_name=display_name,
			current_identity_id=current_identity_id,
		)

	def delete_person(self, person_id: str) -> None:
		self._gateway.delete_person(person_id)


class IdmIdentityUseCases:
	def __init__(self, gateway: IdmIdentityGateway) -> None:
		self._gateway = gateway

	def list_identities(self) -> list[Any]:
		return self._gateway.list_identities()

	def create_identity(
		self,
		*,
		person_id: str,
		source_system: str,
		source_record_id: str,
		demographic_payload: dict[str, Any] | None = None,
		valid_from: Any | None = None,
		valid_to: Any | None = None,
		superseded_at: Any | None = None,
	) -> Any:
		return self._gateway.create_identity(
			person_id=person_id,
			source_system=source_system,
			source_record_id=source_record_id,
			demographic_payload=demographic_payload,
			valid_from=valid_from,
			valid_to=valid_to,
			superseded_at=superseded_at,
		)

	def get_identity(self, identity_id: str) -> Any | None:
		return self._gateway.get_identity(identity_id)

	def update_identity(
		self,
		*,
		identity_id: str,
		source_system: str | None = None,
		source_record_id: str | None = None,
		demographic_payload: dict[str, Any] | None = None,
		valid_from: Any | None = None,
		valid_to: Any | None = None,
		superseded_at: Any | None = None,
	) -> Any:
		return self._gateway.update_identity(
			identity_id=identity_id,
			source_system=source_system,
			source_record_id=source_record_id,
			demographic_payload=demographic_payload,
			valid_from=valid_from,
			valid_to=valid_to,
			superseded_at=superseded_at,
		)

	def delete_identity(self, identity_id: str) -> None:
		self._gateway.delete_identity(identity_id)


class IdmGroupMembershipUseCases:
	def __init__(self, gateway: IdmGroupMembershipGateway) -> None:
		self._gateway = gateway

	def list_group_memberships(self) -> list[Any]:
		return self._gateway.list_group_memberships()

	def create_group_membership(
		self,
		*,
		group_id: str,
		member_type: str,
		member_user_id: str | None = None,
		member_group_id: str | None = None,
	) -> Any:
		return self._gateway.create_group_membership(
			group_id=group_id,
			member_type=member_type,
			member_user_id=member_user_id,
			member_group_id=member_group_id,
		)

	def get_group_membership(self, membership_id: str) -> Any | None:
		return self._gateway.get_group_membership(membership_id)

	def update_group_membership(
		self,
		*,
		membership_id: str,
		member_type: str | None = None,
		member_user_id: str | None = None,
		member_group_id: str | None = None,
	) -> Any:
		return self._gateway.update_group_membership(
			membership_id=membership_id,
			member_type=member_type,
			member_user_id=member_user_id,
			member_group_id=member_group_id,
		)

	def delete_group_membership(self, membership_id: str) -> None:
		self._gateway.delete_group_membership(membership_id)


__all__ = [
	"IdmGroupGateway",
	"IdmGroupUseCases",
	"IdmGroupMembershipGateway",
	"IdmGroupMembershipUseCases",
	"IdmIdentityGateway",
	"IdmIdentityUseCases",
	"IdmPersonGateway",
	"IdmPersonUseCases",
	"IdmUserGateway",
	"IdmUserUseCases",
]