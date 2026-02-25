from sqlalchemy.orm import Session

from itsor.domain.models import User
from itsor.domain.ports.user_repository import UserRepository
from itsor.infrastructure.adapters.sqlalchemy_base_repository import SQLAlchemyBaseRepository
from itsor.infrastructure.models.sqlalchemy_user_model import UserModel


class SQLAlchemyUserRepository(SQLAlchemyBaseRepository[User, UserModel], UserRepository):
    model_class = UserModel

    def __init__(self, db: Session) -> None:
        super().__init__(db, "User")

    def _to_domain(self, record: UserModel) -> User:
        return User(
            id=record.id,
            name=record.name,
            username=record.username,
            email=record.email,
            password_hash=record.password_hash,
            group_id=record.group_id,
        )

    def _to_model(self, user: User) -> UserModel:
        return UserModel(
            id=user.id,
            name=user.name,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            group_id=user.group_id,
        )

    def _apply_updates(self, record: UserModel, user: User) -> None:
        record.name = user.name
        record.username = user.username
        record.email = user.email
        record.password_hash = user.password_hash
        record.group_id = user.group_id

    def get_by_email(self, email: str) -> User | None:
        record = self._db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(record) if record else None

    def get_by_username(self, username: str) -> User | None:
        record = self._db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_domain(record) if record else None
