from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from data.models.user import User
from schemas.user_schema import UserCreate, UserUpdate


def get_all_user(session: Session) -> list[User]:
    return session.execute(select(User)).scalars().all()  # pyright: ignore


def get_by_cs(session: Session, cs: int) -> User | None:
    return session.execute(select(User).where(User.cs == cs)).scalars().first()

def get_by_id(session: Session, id: UUID) -> User:
    return session.execute(select(User).where(User.id == id)).scalar_one_or_none()

def create_user(session: Session, data: UserCreate) -> User:
    user = User(
        name=data.name,
        cs=data.cs,
        sector_id=data.sector_id,
        password=data.password,
        role=data.role,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def update_user(session: Session, cs: int, data: UserUpdate) -> User | None:
    user = get_by_cs(session, cs)

    if not user:
        return None

    if data.name is not None:
        user.name = data.name
    if data.cs is not None:
        user.cs = data.cs
    if data.active is not None:
        user.active = data.active
    if data.sector_id is not None:
        user.sector_id = data.sector_id
    if data.password is not None:
        user.password = data.password

    session.commit()
    session.refresh(user)
    return user
