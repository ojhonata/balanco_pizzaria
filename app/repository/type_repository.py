from app.models.type import Type
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.schemas.order_schema import OrderCreate


def get_all_type(session: Session) -> list[Type]:
    return session.execute(select(Type)).scalars().all()  # pyright: ignore


def get_by_id(session: Session, id: int) -> Type | None:
    return session.execute(select(Type).where(Type.id == id)).scalar_one_or_none()  # pyright: ignore


def create_type(session: Session, data: OrderCreate) -> Type:
    type = Type(name=data.name)
    session.add(type)
    session.commit()
    session.refresh(type)

    return type


def get_by_name(session: Session, name: str) -> Type | None:
    return session.execute(select(Type).where(Type.name == name)).scalars().first()
