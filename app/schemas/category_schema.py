from pydantic import BaseModel


class LocationCreate(BaseModel):
    name: str


class LocationResponse(BaseModel):
    id: int
    name: str


class LocationUpdate(BaseModel):
    name: str | None = None
