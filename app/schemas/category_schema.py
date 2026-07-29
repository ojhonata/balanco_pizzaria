
from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    sector_id: int


class CategoryResponse(BaseModel):
    id: int
    name: str
    sector_id: int


class CategoryUpdate(BaseModel):
    name: str | None = None
    sector_id: int | None = None
