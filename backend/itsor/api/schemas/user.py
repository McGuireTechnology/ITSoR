from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserReplace(UserBase):
    password: str


class UserResponse(UserBase):
    id: UUID

    model_config = {"from_attributes": True}
