import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import OrderStatus


class OrderSchema(BaseModel):
    sector_id: int
    material_id: UUID
    quantity_requested: Decimal
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

class OrderCreate(OrderSchema):
    pass

class OrderResponse(OrderSchema):
    id: UUID
    status: OrderStatus
    requested_by: UUID
    order_date: datetime.datetime
    quantity_received: Decimal | None = None
    received_date: datetime.datetime
    received_by: UUID | None = None

class OrderUpdate(BaseModel):
    sector_id: int | None = None
    material_id: UUID | None = None
    quantity_requested: Decimal | None = None
    quantity_received: Decimal | None
    requested_by: UUID | None = None
    received_by: UUID | None = None
    status: str | None = None
    order_date: datetime.datetime | None = None
    received_date: datetime.datetime | None = None

class OrderReceived(BaseModel):
    quantity_received: Decimal
    received_by: UUID

