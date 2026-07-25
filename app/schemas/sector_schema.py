from pydantic import BaseModel


class SectorResponse(BaseModel):
    id: int
    name: str
    uses_location_split: bool


class SectorCreate(BaseModel):
    name: str
    uses_location_split: bool


class SectorUpdate(BaseModel):
    name: str | None = None
    uses_location_split: bool | None = None
