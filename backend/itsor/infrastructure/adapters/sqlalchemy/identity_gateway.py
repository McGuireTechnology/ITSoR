import json
from typing import Any, Protocol

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from itsor.infrastructure.persistence_models.sqlalchemy_idm_group_membership_model import IdmGroupMembershipModel
from itsor.infrastructure.persistence_models.sqlalchemy_idm_group_model import IdmGroupModel
from itsor.infrastructure.persistence_models.sqlalchemy_idm_identity_model import IdmIdentityModel
from itsor.infrastructure.persistence_models.sqlalchemy_idm_person_model import IdmPersonModel
from itsor.infrastructure.persistence_models.sqlalchemy_idm_user_model import IdmUserModel


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


class SQLAlchemyIdmGroupGateway:
    def __init__(self, db: Session) -> None:
        self._db = db

    def list_groups(self) -> list[IdmGroupModel]:
        return self._db.query(IdmGroupModel).all()

    def create_group(self, *, name: str, description: str = "") -> IdmGroupModel:
        group = IdmGroupModel(name=name, description=description)
        self._db.add(group)
        self._db.commit()
        self._db.refresh(group)
        return group

    def get_group(self, group_id: str) -> IdmGroupModel | None:
        return self._db.query(IdmGroupModel).filter(IdmGroupModel.id == group_id).first()

    def update_group(
        self,
        *,
        group_id: str,
        name: str | None = None,
        description: str | None = None,
    ) -> IdmGroupModel:
        group = self.get_group(group_id)
        if not group:
            raise ValueError("IDM group not found")

        target = group
        if name is not None:
            setattr(target, "name", name)
        if description is not None:
            setattr(target, "description", description)

        self._db.commit()
        self._db.refresh(group)
        return group

    def delete_group(self, group_id: str) -> None:
        group = self.get_group(group_id)
        if not group:
            raise ValueError("IDM group not found")

        self._db.delete(group)
        try:
            self._db.commit()
        except IntegrityError as exc:
            self._db.rollback()
            raise ValueError("IDM group is referenced by memberships") from exc

    def list_users(self) -> list[IdmUserModel]:
        return self._db.query(IdmUserModel).all()

    def create_user(self, *, person_id: str, username: str, account_status: str = "active") -> IdmUserModel:
        person = self._db.query(IdmPersonModel).filter(IdmPersonModel.id == person_id).first()
        if not person:
            raise ValueError("Person not found")

        user = IdmUserModel(
            person_id=person_id,
            username=username,
            account_status=account_status,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def get_user(self, user_id: str) -> IdmUserModel | None:
        return self._db.query(IdmUserModel).filter(IdmUserModel.id == user_id).first()

    def update_user(
        self,
        *,
        user_id: str,
        username: str | None = None,
        account_status: str | None = None,
    ) -> IdmUserModel:
        user = self.get_user(user_id)
        if not user:
            raise ValueError("IDM user not found")

        target = user
        if username is not None:
            setattr(target, "username", username)
        if account_status is not None:
            setattr(target, "account_status", account_status)

        self._db.commit()
        self._db.refresh(user)
        return user

    def delete_user(self, user_id: str) -> None:
        user = self.get_user(user_id)
        if not user:
            raise ValueError("IDM user not found")

        self._db.delete(user)
        self._db.commit()

    def list_people(self) -> list[IdmPersonModel]:
        return self._db.query(IdmPersonModel).all()

    def create_person(self, *, display_name: str = "", current_identity_id: str | None = None) -> IdmPersonModel:
        if current_identity_id:
            current_identity = self._db.query(IdmIdentityModel).filter(IdmIdentityModel.id == current_identity_id).first()
            if not current_identity:
                raise ValueError("Current identity not found")

        person = IdmPersonModel(
            display_name=display_name,
            current_identity_id=current_identity_id,
        )
        self._db.add(person)
        self._db.commit()
        self._db.refresh(person)
        return person

    def get_person(self, person_id: str) -> IdmPersonModel | None:
        return self._db.query(IdmPersonModel).filter(IdmPersonModel.id == person_id).first()

    def update_person(
        self,
        *,
        person_id: str,
        display_name: str | None = None,
        current_identity_id: str | None = None,
    ) -> IdmPersonModel:
        person = self.get_person(person_id)
        if not person:
            raise ValueError("Person not found")

        target = person
        if display_name is not None:
            setattr(target, "display_name", display_name)

        if current_identity_id is not None:
            identity = self._db.query(IdmIdentityModel).filter(IdmIdentityModel.id == current_identity_id).first()
            if not identity:
                raise ValueError("Current identity not found")
            if str(getattr(identity, "person_id", "")) != str(getattr(person, "id", "")):
                raise ValueError("Current identity must reference the same person")
            setattr(target, "current_identity_id", current_identity_id)

        self._db.commit()
        self._db.refresh(person)
        return person

    def delete_person(self, person_id: str) -> None:
        person = self.get_person(person_id)
        if not person:
            raise ValueError("Person not found")

        self._db.delete(person)
        try:
            self._db.commit()
        except IntegrityError as exc:
            self._db.rollback()
            raise ValueError("Person is referenced by identities or users") from exc

    def list_identities(self) -> list[IdmIdentityModel]:
        return self._db.query(IdmIdentityModel).all()

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
    ) -> IdmIdentityModel:
        person = self._db.query(IdmPersonModel).filter(IdmPersonModel.id == person_id).first()
        if not person:
            raise ValueError("Person not found")

        identity = IdmIdentityModel(
            person_id=person_id,
            source_system=source_system,
            source_record_id=source_record_id,
            demographic_payload=json.dumps(demographic_payload or {}),
            valid_from=valid_from,
            valid_to=valid_to,
            superseded_at=superseded_at,
        )
        self._db.add(identity)
        self._db.commit()
        self._db.refresh(identity)
        return identity

    def get_identity(self, identity_id: str) -> IdmIdentityModel | None:
        return self._db.query(IdmIdentityModel).filter(IdmIdentityModel.id == identity_id).first()

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
    ) -> IdmIdentityModel:
        identity = self.get_identity(identity_id)
        if not identity:
            raise ValueError("Identity not found")

        target = identity
        if source_system is not None:
            setattr(target, "source_system", source_system)
        if source_record_id is not None:
            setattr(target, "source_record_id", source_record_id)
        if demographic_payload is not None:
            setattr(target, "demographic_payload", json.dumps(demographic_payload))
        if valid_from is not None:
            setattr(target, "valid_from", valid_from)
        if valid_to is not None:
            setattr(target, "valid_to", valid_to)
        if superseded_at is not None:
            setattr(target, "superseded_at", superseded_at)

        self._db.commit()
        self._db.refresh(identity)
        return identity

    def delete_identity(self, identity_id: str) -> None:
        identity = self.get_identity(identity_id)
        if not identity:
            raise ValueError("Identity not found")

        self._db.delete(identity)
        self._db.commit()

    def _validate_member_ref(
        self,
        member_type: str,
        member_user_id: str | None,
        member_group_id: str | None,
    ) -> None:
        if member_type not in {"user", "group"}:
            raise ValueError("member_type must be 'user' or 'group'")

        if member_type == "user":
            if not member_user_id or member_group_id:
                raise ValueError("user membership requires member_user_id only")
            user = self._db.query(IdmUserModel).filter(IdmUserModel.id == member_user_id).first()
            if not user:
                raise ValueError("Member user not found")
            return

        if not member_group_id or member_user_id:
            raise ValueError("group membership requires member_group_id only")
        group = self._db.query(IdmGroupModel).filter(IdmGroupModel.id == member_group_id).first()
        if not group:
            raise ValueError("Member group not found")

    def list_group_memberships(self) -> list[IdmGroupMembershipModel]:
        return self._db.query(IdmGroupMembershipModel).all()

    def create_group_membership(
        self,
        *,
        group_id: str,
        member_type: str,
        member_user_id: str | None = None,
        member_group_id: str | None = None,
    ) -> IdmGroupMembershipModel:
        group = self._db.query(IdmGroupModel).filter(IdmGroupModel.id == group_id).first()
        if not group:
            raise ValueError("Group not found")

        self._validate_member_ref(member_type, member_user_id, member_group_id)

        if member_type == "group" and member_group_id == group_id:
            raise ValueError("Group cannot directly contain itself")

        membership = IdmGroupMembershipModel(
            group_id=group_id,
            member_type=member_type,
            member_user_id=member_user_id,
            member_group_id=member_group_id,
        )
        self._db.add(membership)
        self._db.commit()
        self._db.refresh(membership)
        return membership

    def get_group_membership(self, membership_id: str) -> IdmGroupMembershipModel | None:
        return self._db.query(IdmGroupMembershipModel).filter(IdmGroupMembershipModel.id == membership_id).first()

    def update_group_membership(
        self,
        *,
        membership_id: str,
        member_type: str | None = None,
        member_user_id: str | None = None,
        member_group_id: str | None = None,
    ) -> IdmGroupMembershipModel:
        membership = self.get_group_membership(membership_id)
        if not membership:
            raise ValueError("Group membership not found")

        next_member_type = member_type if member_type is not None else str(getattr(membership, "member_type", ""))
        next_member_user_id = member_user_id if member_user_id is not None else getattr(membership, "member_user_id", None)
        next_member_group_id = member_group_id if member_group_id is not None else getattr(membership, "member_group_id", None)

        self._validate_member_ref(next_member_type, next_member_user_id, next_member_group_id)

        if next_member_type == "group" and str(next_member_group_id) == str(getattr(membership, "group_id", "")):
            raise ValueError("Group cannot directly contain itself")

        target = membership
        if member_type is not None:
            setattr(target, "member_type", member_type)
        if member_user_id is not None:
            setattr(target, "member_user_id", member_user_id)
        if member_group_id is not None:
            setattr(target, "member_group_id", member_group_id)

        self._db.commit()
        self._db.refresh(membership)
        return membership

    def delete_group_membership(self, membership_id: str) -> None:
        membership = self.get_group_membership(membership_id)
        if not membership:
            raise ValueError("Group membership not found")

        self._db.delete(membership)
        self._db.commit()
