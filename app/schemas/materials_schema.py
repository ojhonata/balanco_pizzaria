from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MaterialSchema(BaseModel):
    name: str
    category_id: int
    unit: str
    description: str
    minimum_stock: int

class MaterialCreate(MaterialSchema):
    pass

    model_config = ConfigDict(from_attributes=True)

class MaterialResponse(MaterialSchema):
    id: UUID
    active: bool

    model_config = ConfigDict(from_attributes=True)


class MaterialUpdate(BaseModel):
    name: str | None = None
    category_id: int | None = None
    unit: str | None = None
    description: str | None = None
    minimum_stock: int | None = None
    active: bool | None = None

