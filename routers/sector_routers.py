from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from data.conf.db_session import get_session
from schemas.sector_schema import SectorCreate, SectorResponse, SectorUpdate
from service import sector_service

router = APIRouter()


@router.get("/sectors", response_model=list[SectorResponse])
def list_sectors(session: Session = Depends(get_session)):
    return sector_service.get_all(session)


@router.get("/sector/{id}", response_model=SectorResponse)
def list_by_id(id: int, session: Session = Depends(get_session)):
    try:
        return sector_service.get_sector_by_id(session, id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/create_sector", response_model=SectorCreate)
def create_sector(data: SectorCreate, session: Session = Depends(get_session)):
    try:
        return sector_service.post_sector(session, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/update_sector/{id}", response_model=SectorResponse)
def update_sector(
    id: int, data: SectorUpdate, session: Session = Depends(get_session)
):
    try:
        return sector_service.update_sector(session, id, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
