from sqlalchemy import CheckConstraint, Column, ForeignKey, String

from itsor.infrastructure.models.sqlalchemy_user_model import Base


class PlatformGroupMembershipModel(Base):
    __tablename__ = "platform_group_memberships"
    __table_args__ = (
        CheckConstraint("member_type in ('user', 'group')", name="ck_platform_membership_member_type"),
        CheckConstraint(
            "(member_type = 'user' and member_user_id is not null and member_group_id is null) or "
            "(member_type = 'group' and member_group_id is not null and member_user_id is null)",
            name="ck_platform_membership_member_ref",
        ),
    )

    id = Column(String(36), primary_key=True)
    group_id = Column(String(36), ForeignKey("platform_groups.id"), nullable=False, index=True)
    member_type = Column(String(16), nullable=False)
    member_user_id = Column(String(36), ForeignKey("platform_users.id"), nullable=True, index=True)
    member_group_id = Column(String(36), ForeignKey("platform_groups.id"), nullable=True, index=True)