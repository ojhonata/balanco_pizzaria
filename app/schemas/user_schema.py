from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserSchema(BaseModel):
    name: str
    sector_id: int
    role_id: int

    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserSchema):
    code_hash: int = Field(max_length=4, examples=["1234"])

class UserResponse(UserSchema):
    id: UUID
    active: bool

class UserUpdate(BaseModel):
    name: str | None = None
    code: int | None = None
    sector_id: int | None = None
    role_id: int | None = None
    active: bool | None = None
