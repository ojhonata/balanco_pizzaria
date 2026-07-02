from pydantic import BaseModel


class LocationCreate(BaseModel):
    name: str
    shelf_id: int


class LocationResponse(BaseModel):
    id: int
    name: str
    shelf_id: int


class LocationUpdate(BaseModel):
    name: str | None = None
    shelf_id: int | None = None
