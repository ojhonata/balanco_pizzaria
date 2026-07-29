from decimal import Decimal
from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, model_validator


class MaterialSchema(BaseModel):
    name: str
    category_id: int
    unit: str
    description: str
    minimum_stock: int | None = None
    tracks_container: bool = False
    sale_price: Decimal | None = None

    @model_validator(mode="after")
    def varify_tracks_and_price(self) -> Self:
        if self.tracks_container and self.sale_price is None:
            raise ValueError("sale_price é obrigatório quando tracks_container=True")
        return self

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
    tracks_container: bool = False
    sale_price: Decimal | None = None

    @model_validator(mode="after")
    def varify_tracks_and_price(self) -> Self:
        if self.tracks_container and self.sale_price is None:
            raise ValueError("sale_price é obrigatório quando tracks_container=True")
        return self

