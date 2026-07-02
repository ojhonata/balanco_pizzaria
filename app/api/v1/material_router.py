from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.conf.db_session import get_session
from app.schemas.materials_schema import MaterialCreate, MaterialResponse, MaterialUpdate
from app.service import material_service

router = APIRouter()


@router.get("/materials", response_model=list[MaterialResponse])
def list_materials(session: Session = Depends(get_session)):
    return material_service.get_all(session)


@router.get("/material/{id}", response_model=MaterialResponse)
def list_material_by_id(id: UUID, session: Session = Depends(get_session)):
    try:
        return material_service.get_material_by_id(session, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create_material", response_model=MaterialCreate)
def post_material(data: MaterialCreate, session: Session = Depends(get_session)):
    try:
        return material_service.post_material(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/update_material/{id}", response_model=MaterialUpdate)
def update_material(
    data: MaterialUpdate, id: UUID, session: Session = Depends(get_session)
):
    try:
        return material_service.update_material(session, data, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
