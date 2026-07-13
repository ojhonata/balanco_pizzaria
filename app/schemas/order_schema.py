import datetime
from uuid import UUID

from pydantic import BaseModel


class OrderSchema(BaseModel):
    sector_id: int
    material_id: UUID
    quantity_requested: float
    quantity_received: float | None
    requested_by: UUID
    received_by: UUID | None

class OrderCreate(OrderSchema):
    status: str

class OrderResponse(OrderSchema):
    id: UUID
    status: str
    order_date: datetime.datetime
    received_date: datetime.datetime

class OrderUpdaate(BaseModel):
    sector_id: int | None = None
    material_id: UUID | None = None
    quantity_requested: float | None = None
    quantity_received: float | None
    requested_by: UUID | None = None
    received_by: UUID | None = None
    status: str | None = None
    order_date: datetime.datetime | None = None
    received_date: datetime.datetime | None = None

