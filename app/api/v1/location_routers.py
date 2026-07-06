from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.data.db_session import get_session
from app.schemas.location_schema import LocationCreate, LocationResponse
from app.service import location_service

router = APIRouter()


@router.get("/locations", response_model=list[LocationResponse])
def list_locations(session: Session = Depends(get_session)):
    return location_service.get_all(session)


@router.get("location/{id}", response_model=LocationResponse)
def list_by_id(id: int, session: Session = Depends(get_session)):
    try:
        return location_service.get_location_by_id(session, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create_location", response_model=LocationCreate)
def create_location(
    data: LocationCreate, session: Session = Depends(get_session)
):
    try:
        return location_service.post_location(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
