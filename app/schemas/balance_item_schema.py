from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class BalanceItemSchema(BaseModel):
    balance_id: UUID
    material_id: UUID
    #expected_quantity: Decimal
    counted_quantity: Decimal
    
