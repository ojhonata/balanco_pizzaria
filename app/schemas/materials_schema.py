from uuid import UUID

from pydantic import BaseModel


class MaterialSchema(BaseModel):
    name: str
    code: int
    description: str
    minimum_stock: int
    maximum_stock: int
    quantity: int
    location_id: int


class MaterialCreate(MaterialSchema): ...


class MaterialResponse(MaterialSchema):
    id: UUID
    active: bool


class MaterialUpdate(BaseModel):
    name: str | None = None
    code: int | None = None
    description: str | None = None
    minimum_stock: int | None = None
    maximum_stock: int | None = None
    quantity: int | None = None
    location_id: int | None = None

class MaterialDesactive(BaseModel):
    active: bool
