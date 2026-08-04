
from pydantic import BaseModel

from app.schemas.materials_schema import MaterialResponse
from app.schemas.order_schema import OrderResponse


class PageResponseSchema(BaseModel):
    total: int
    limit: int
    offset: int

class MaterialPageResponse(PageResponseSchema):
    items: list[MaterialResponse]

class OrderPageResponse(PageResponseSchema):
    items: list[OrderResponse]
