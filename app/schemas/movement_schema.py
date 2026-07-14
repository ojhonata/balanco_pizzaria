import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import Location


class MovementSchema(BaseModel):
    sector_id: int
    material_id: UUID
    type: str
    user_id: UUID
    order_id: UUID | None
    location: Location

class MovementResponse(MovementSchema):
    id: UUID
    date: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class MovementCreate(MovementSchema):
    pass

    model_config = ConfigDict(from_attributes=True)

class MovementUpdate(BaseModel):
    sector_id: int | None = None
    material_id: UUID | None = None
    type: str | None = None
    user_id: UUID | None = None
    order_id: UUID | None = None
    location: str | None = None
