from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.data.db_session import get_session
from app.schemas.category_schema import CategoryCreate, CategoryResponse
from app.service import category_service

router = APIRouter()


@router.get("/locations", response_model=list[CategoryResponse])
def list_locations(session: Session = Depends(get_session)):
    return category_service.get_all(session)


@router.get("location/{id}", response_model=CategoryResponse)
def list_by_id(id: int, session: Session = Depends(get_session)):
    try:
        return category_service.get_location_by_id(session, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create_location", response_model=CategoryCreate)
def create_location(
    data: CategoryCreate, session: Session = Depends(get_session)
):
    try:
        return category_service.post_location(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
