from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.location import Location
from app.schemas.location_schema import LocationCreate, LocationUpdate


def get_all_location(session: Session) -> list[Location]:
    return session.execute(select(Location)).scalars().all()  # pyright: ignore


def get_by_id(session: Session, id: int) -> Location | None:
    return session.execute(
        select(Location).where(Location.id == id)
    ).scalar_onr_or_one()  # pyright: ignore


def create_location(session: Session, data: LocationCreate) -> Location:
    location = Location(name=data.name, shlef=data.shelf_id)

    session.add(location)
    session.commit()
    session.refresh(location)

    return location


def update_location(session: Session, id: int, data: LocationUpdate) -> Location | None:
    location = get_by_id(session, id)

    if not location:
        return None

    if data.name is not None:
        location.name = data.name
    if data.shelf_id is not None:
        location.shelf_id = data.shelf_id

    return location

def get_by_name(session: Session, name: str) -> Location | None:
    return session.execute(select(Location).where(Location.name == name)).scalar_one_or_none() #pyright: ignore