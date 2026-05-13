from sqlalchemy import select
from sqlalchemy.orm import Session

from data.models.shelf import Shelf

def get_all_shelf(session: Session) -> list[Shelf]:
    return session.execute(select(Shelf)).scalars().all()  # pyright: ignore

def get_by_id(session: Session, id: int) -> Shelf | None:
    return session.execute(select(Shelf).where(Shelf.id == id)).scalar_one_or_none()  # pyright: ignore

def create_shelf(session: Session, name: str) -> Shelf:
    shelf = Shelf(name=name)
    session.add(shelf)
    session.commit()
    session.refresh(shelf)

    return shelf

def update_shelf(session: Session, id: int, name: str) -> Shelf | None:
    shelf = get_by_id(session, id)

    if not shelf:
        return None

    shelf.name = name

    session.commit()
    session.refresh(shelf)

    return shelf

def get_by_name(session: Session, name: str) -> Shelf | None:
    return session.execute(select(Shelf).where(Shelf.name == name)).scalar_one_or_none()
