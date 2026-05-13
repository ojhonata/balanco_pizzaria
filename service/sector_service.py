from fastapi import HTTPException
from sqlalchemy.orm import Session

from data.models.sector import Sector
from data.repository import sector_repository
from schemas.sector_schema import SectorCreate, SectorUpdate


def get_all(session: Session) -> list[Sector]:
    try:
        return sector_repository.get_all_sector(session)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_sector_by_id(session: Session, id: int) -> Sector:
    sector = sector_repository.get_by_id(session, id)

    if not sector:
        raise ValueError("Setor não encontrado")

    return sector


def post_sector(session: Session, data: SectorCreate) -> Sector:
    existing_sector = sector_repository.get_by_name(session, data.name)

    if existing_sector:
        raise ValueError("Setor já cadastrado!")
    return sector_repository.create_sector(session, data)


def update_sector(session: Session, id: int, data: SectorUpdate) -> Sector:
    existing_sector = sector_repository.get_by_id(session, id)

    if not existing_sector:
        raise ValueError("Setor não encontrado")
    if data.name is not None:
        existing_sector.name = data.name
    session.flush()
    session.refresh(existing_sector)
    return existing_sector
