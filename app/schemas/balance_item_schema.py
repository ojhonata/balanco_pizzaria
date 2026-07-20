import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BalanceItemCreate(BaseModel):
    balance_id: UUID
    material_id: UUID
    counted_quantity: Decimal

    counted_quantity_fundo: Decimal | None = None
    counted_quantity_frente: Decimal | None = None

class BalanceItemRevised(BaseModel):
    revised_expected_quantity: Decimal
    revision_note: str

class BalanceItemResponse(BaseModel):
    balance_id: UUID
    material_id: UUID
    counted_quantity: Decimal
    counted_quantity_fundo: Decimal | None = None
    counted_quantity_frente: Decimal | None = None
    revised_expected_quantity: Decimal | None = None
    revision_note: str | None = None
    revised_at: datetime.datetime | None = None

    expected_quantity: Decimal
    difference: Decimal
    counted_by: UUID

    model_config = ConfigDict(from_attributes=True)
