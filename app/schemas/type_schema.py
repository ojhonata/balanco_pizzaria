from pydantic import BaseModel


class TypeResponse(BaseModel):
    id: int
    name: str


class TypeCreate(BaseModel):
    name: str

