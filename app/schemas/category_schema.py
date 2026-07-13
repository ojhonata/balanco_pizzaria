from uuid import UUID

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    sector_id: UUID


class CategoryResponse(BaseModel):
    id: int
    name: str
    sector_id: UUID


class CategoryUpdate(BaseModel):
    name: str | None = None
    sector_id: UUID | None = None
