from app.models.type import Type
from sqlalchemy.orm import Session

from app.repository import category_repository
from app.schemas.order_schema import OrderCreate


def get_all(session: Session) -> list[Type]:
    return category_repository.get_all_type(session)


def get_type_by_id(session: Session, id: int) -> Type:
    type = category_repository.get_by_id(session, id)

    if not type:
        raise ValueError("Tipo não encontrado")
    return type


def post_type(session: Session, data: OrderCreate) -> Type:
    existing_type = category_repository.get_by_name(session, data.name)

    if existing_type:
        raise ValueError("Tipo já está cadastrado")

    return category_repository.create_type(session, data)

