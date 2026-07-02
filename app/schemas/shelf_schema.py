from pydantic import BaseModel


class ShlefResponse(BaseModel):
    id: int
    name: str


class ShelfCreate(BaseModel):
    name: str


class ShelfUpdate(BaseModel):
    id: int
    name: str | None
