from sqlalchemy import CheckConstraint, Column, DateTime, ForeignKey, String, Text

from itsor.infrastructure.database.sqlalchemy.models.auth import Base


class IdmPersonModel(Base):
	__tablename__ = "idm_people"

	id = Column(String(36), primary_key=True)
	display_name = Column(String(255), nullable=False, default="")
	current_identity_id = Column(String(36), nullable=True, index=True)


class IdmIdentityModel(Base):
	__tablename__ = "idm_identities"

	id = Column(String(36), primary_key=True)
	person_id = Column(String(36), ForeignKey("idm_people.id"), nullable=False, index=True)
	source_system = Column(String(128), nullable=False, index=True)
	source_record_id = Column(String(255), nullable=False, index=True)
	demographic_payload = Column(Text, nullable=False, default="{}")
	valid_from = Column(DateTime, nullable=True, index=True)
	valid_to = Column(DateTime, nullable=True, index=True)
	superseded_at = Column(DateTime, nullable=True, index=True)


class IdmGroupModel(Base):
	__tablename__ = "idm_groups"

	id = Column(String(36), primary_key=True)
	name = Column(String(255), nullable=False, index=True)
	description = Column(String(255), nullable=False, default="")


class IdmAccountModel(Base):
	__tablename__ = "idm_users"

	id = Column(String(36), primary_key=True)
	person_id = Column(String(36), ForeignKey("idm_people.id"), nullable=False, index=True)
	username = Column(String(255), nullable=False, index=True)
	account_status = Column(String(64), nullable=False, default="active")


IdmUserModel = IdmAccountModel


class IdmGroupMembershipModel(Base):
	__tablename__ = "idm_group_memberships"
	__table_args__ = (
		CheckConstraint("member_type in ('user', 'group')", name="ck_idm_membership_member_type"),
		CheckConstraint(
			"(member_type = 'user' and member_user_id is not null and member_group_id is null) or "
			"(member_type = 'group' and member_group_id is not null and member_user_id is null)",
			name="ck_idm_membership_member_ref",
		),
	)

	id = Column(String(36), primary_key=True)
	group_id = Column(String(36), ForeignKey("idm_groups.id"), nullable=False, index=True)
	member_type = Column(String(16), nullable=False)
	member_user_id = Column(String(36), ForeignKey("idm_users.id"), nullable=True, index=True)
	member_group_id = Column(String(36), ForeignKey("idm_groups.id"), nullable=True, index=True)


__all__ = [
	"IdmAccountModel",
	"IdmGroupMembershipModel",
	"IdmGroupModel",
	"IdmIdentityModel",
	"IdmPersonModel",
	"IdmUserModel",
]