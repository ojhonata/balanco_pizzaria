from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.data.db_session import get_session
from app.schemas.order_schema import TypeCreate, TypeResponse
from app.service import type_service

router = APIRouter()


@router.get("/types", response_model=list[TypeResponse])
def list_types(session: Session = Depends(get_session)):
    return type_service.get_all(session)


@router.get("/type/{id}", response_model=TypeResponse)
def list_type_by_id(id: int, session: Session = Depends(get_session)):
    try:
        return type_service.get_type_by_id(session, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/type_create/", response_model=TypeCreate)
def create_type(data: TypeCreate, session: Session = Depends(get_session)):
    try:
        return type_service.post_type(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
