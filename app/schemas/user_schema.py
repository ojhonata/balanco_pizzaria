from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserSchema(BaseModel):
    name: str
    cs: int
    sector_id: int

    model_config = ConfigDict(from_attributes=True)


class UserCreate(UserSchema):
    password: str
    role: str | None = "user"


class UserUpdate(BaseModel):
    name: str | None = None
    cs: int | None = None
    sector_id: int | None = None
    password: str | None = None
    role: str | None = None
    active: bool | None = None


class UserResponse(UserSchema):
    id: UUID
    active: bool
    role: str
