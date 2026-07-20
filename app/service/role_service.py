from sqlalchemy.orm import Session

from app.models.category import Category
from app.repository import shelf_repository
from app.schemas.container_count import RoleCreate, ShelfUpdate


def get_all(session: Session) -> list[Category]:
    return shelf_repository.get_all_shelf(session)


def get_shelf_by_id(session: Session, id: int) -> Category:
    shelf = shelf_repository.get_by_id(session, id)

    if not shelf:
        raise ValueError("Prateleira não encontrada")

    return shelf


def post_shelf(session: Session, data: RoleCreate) -> Category:
    existing_shelf = shelf_repository.get_by_name(session, data.name)

    if existing_shelf:
        raise ValueError("Prateleira já cadastrada!")
    return shelf_repository.create_shelf(session, data.name)


def update_shelf(session: Session, id: int, data: ShelfUpdate) -> Category:
    existing_shelf = shelf_repository.get_by_id(session, id)

    if not existing_shelf:
        raise ValueError("Prateleira não encontrada")
    if data.name is not None:
        existing_shelf.name = data.name
    session.flush()
    session.refresh(existing_shelf)
    return existing_shelf
