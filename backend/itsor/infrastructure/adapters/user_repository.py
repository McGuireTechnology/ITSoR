from typing import Optional, List

from sqlalchemy.orm import Session

from itsor.domain.models.user import User
from itsor.domain.ports.user_repository import UserRepository
from itsor.infrastructure.models.user import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session) -> None:
        self._db = db

    def _to_domain(self, record: UserModel) -> User:
        return User(
            id=record.id,
            username=record.username,
            email=record.email,
            password_hash=record.password_hash,
        )

    def _to_model(self, user: User) -> UserModel:
        return UserModel(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
        )

    def get_by_id(self, user_id: str) -> Optional[User]:
        record = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        return self._to_domain(record) if record else None

    def get_by_email(self, email: str) -> Optional[User]:
        record = self._db.query(UserModel).filter(UserModel.email == email).first()
        return self._to_domain(record) if record else None

    def get_by_username(self, username: str) -> Optional[User]:
        record = self._db.query(UserModel).filter(UserModel.username == username).first()
        return self._to_domain(record) if record else None

    def list(self) -> List[User]:
        records = self._db.query(UserModel).all()
        return [self._to_domain(r) for r in records]

    def create(self, user: User) -> User:
        record = self._to_model(user)
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return self._to_domain(record)

    def update(self, user: User) -> User:
        record = self._db.query(UserModel).filter(UserModel.id == user.id).first()
        if not record:
            raise ValueError(f"User {user.id} not found")
        record.username = user.username
        record.email = user.email
        record.password_hash = user.password_hash
        self._db.commit()
        self._db.refresh(record)
        return self._to_domain(record)

    def delete(self, user_id: str) -> None:
        record = self._db.query(UserModel).filter(UserModel.id == user_id).first()
        if record:
            self._db.delete(record)
            self._db.commit()
