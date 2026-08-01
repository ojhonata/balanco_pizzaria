
from pydantic import BaseModel

from app.schemas.materials_schema import MaterialResponse


class MaterialPageResponse(BaseModel):
    items: list[MaterialResponse]
    total: int
    limit: int
    offset: int
