from uuid import UUID
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = None


class UserReplace(UserBase):
    password: str


class UserResponse(UserBase):
    id: UUID

    model_config = {"from_attributes": True}
