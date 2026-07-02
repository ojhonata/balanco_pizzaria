from pydantic import BaseModel


class SectorResponse(BaseModel):
    id: int
    name: str


class SectorCreate(BaseModel):
    name: str


class SectorUpdate(BaseModel):
    id: int
    name: str | None
