from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas.category_schema import LocationCreate, LocationUpdate


def get_all_location(session: Session) -> list[Role]:
    return session.execute(select(Role)).scalars().all()  # pyright: ignore


def get_by_id(session: Session, id: int) -> Role | None:
    return session.execute(
        select(Role).where(Role.id == id)
    ).scalar_onr_or_one()  # pyright: ignore


def create_location(session: Session, data: LocationCreate) -> Role:
    location = Role(name=data.name, shlef=data.shelf_id)

    session.add(location)
    session.commit()
    session.refresh(location)

    return location


def update_location(session: Session, id: int, data: LocationUpdate) -> Role | None:
    location = get_by_id(session, id)

    if not location:
        return None

    if data.name is not None:
        location.name = data.name
    if data.shelf_id is not None:
        location.shelf_id = data.shelf_id

    return location

def get_by_name(session: Session, name: str) -> Role | None:
    return session.execute(select(Role).where(Role.name == name)).scalar_one_or_none() #pyright: ignore
