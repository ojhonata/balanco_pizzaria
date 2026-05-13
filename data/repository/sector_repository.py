from sqlalchemy import select
from sqlalchemy.orm import Session

from data.models.sector import Sector
from schemas.sector_schema import SectorCreate, SectorUpdate


def get_all_sector(session: Session) -> list[Sector]:
    return session.execute(select(Sector)).scalars().all() #pyright: ignore

def get_by_id(session: Session, id: int) -> Sector | None:
    return session.execute(select(Sector).where(Sector.id == id)).scalar_one_or_none() #pyright: ignore

def create_sector(session: Session, data: SectorCreate) -> Sector:
    sector = Sector(name = data.name)
    session.add(sector)
    session.commit()
    session.refresh(sector)

    return sector

def update_sector(session: Session, id: int, data: SectorUpdate) -> Sector | None:
    sector = get_by_id(session, id)

    if not sector:
        return None

    if data.name is not None:
        sector.name = data.name

    session.commit()
    session.refresh(sector)

    return sector

def get_by_name(session: Session, name: str) -> Sector | None:
    return session.execute(select(Sector).where(Sector.name == name)).scalar_one_or_none() #pyright: ignore
