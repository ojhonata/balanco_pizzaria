from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category


def get_all_shelf(session: Session) -> list[Category]:
    return session.execute(select(Category)).scalars().all()  # pyright: ignore

def get_by_id(session: Session, id: int) -> Category | None:
    return session.execute(select(Category).where(Category.id == id)).scalar_one_or_none()  # pyright: ignore

def create_shelf(session: Session, name: str) -> Category:
    shelf = Category(name=name)
    session.add(shelf)
    session.commit()
    session.refresh(shelf)

    return shelf

def update_shelf(session: Session, id: int, name: str) -> Category | None:
    shelf = get_by_id(session, id)

    if not shelf:
        return None

    shelf.name = name

    session.commit()
    session.refresh(shelf)

    return shelf

def get_by_name(session: Session, name: str) -> Category | None:
    return session.execute(select(Category).where(Category.name == name)).scalar_one_or_none()
