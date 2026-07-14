from pydantic import BaseModel


class RoleResponse(BaseModel):
    id: int
    name: str


class RoleCreate(BaseModel):
    name: str

