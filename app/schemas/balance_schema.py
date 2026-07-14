import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import BalanceStatus


class BalanceSchema(BaseModel):
    sector_id: int
    week_start_date: datetime.date

    model_config = ConfigDict(from_attributes=True)

class BalanceResponse(BalanceSchema):
    id: UUID
    status: BalanceStatus
    closed_by: UUID | None
    closed_at: datetime.datetime | None

class BalanceCreate(BalanceSchema):
    pass

class BalanceClose(BaseModel):
    closed_by: UUID
