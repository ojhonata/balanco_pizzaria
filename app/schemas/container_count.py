from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ContainerCountCreate(BaseModel):
    material_id: UUID
    counted_cascos: int
    description: str | None = None

class ContainerCountCreateSystem(BaseModel):
    expected_from_sales: int

class ContainerCountResponse(BaseModel):
    id: UUID
    count_date: datetime
    material_id: UUID
    counted_cascos: int
    description: str | None = None
    expected_from_sales: int
    difference: int
    unit_sale_price: Decimal
    value_impacte : Decimal
    counted_by: UUID

    model_config = ConfigDict(from_attributes=True)

class ContainerCountUpdate(BaseModel):
    material_id: UUID | None = None
    counted_cascos: int | None = None
    description: str | None = None
    expected_from_sales: int | None = None
    difference: int | None = None
    unit_sale_price: Decimal | None = None
    value_impacte : Decimal | None = None

