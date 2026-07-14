from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.data.db_session import get_session
from app.schemas.role_schema import RoleCreate, RoleResponse, ShelfUpdate
from app.service import role_service

router = APIRouter()


@router.get("/shelves", response_model=list[RoleResponse])
def list_shelfs(session: Session = Depends(get_session)):
    return role_service.get_all(session)


@router.get("/shelf/{id}", response_model=RoleResponse)
def list_by_id(id: int, session: Session = Depends(get_session)):
    try:
        return role_service.get_shelf_by_id(session, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create_shelf", response_model=RoleCreate)
def create_shelf(data: RoleCreate, session: Session = Depends(get_session)):
    try:
        return role_service.post_shelf(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update_shelf/{id}", response_model=ShelfUpdate)
def update_shelf(
    id: int, data: ShelfUpdate, session: Session = Depends(get_session)
):
    try:
        return role_service.update_shelf(session, id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
