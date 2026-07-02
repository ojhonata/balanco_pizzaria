from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repository import user_repository
from app.schemas.user_schema import UserCreate, UserUpdate


def get_all(session: Session) -> list[User]:
    try:
        return user_repository.get_all_user(session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_user_by_cs(session: Session, cs: int) -> User:
    if len(str(cs)) != 6:
        raise ValueError("cs inválida")

    user = user_repository.get_by_cs(session, cs)

    if not user:
        raise ValueError(f"Usuário com a cs {cs} não encontradao")

    if not user.active:
        raise ValueError("Usuário desativado")

    return user


def get_user_by_id(session: Session, id: UUID) -> User:
    user = user_repository.get_by_id(session, id)

    if not user:
        raise ValueError("Usuário não encontrado")
    if not user.active:
        raise ValueError("Usuário desativado")

    return user


def post_user(session: Session, data: UserCreate) -> User:
    existing_user = user_repository.get_by_cs(session, data.cs)

    if len(str(data.password)) != 8:
        raise ValueError("A senha precisa ter 10 caracteres")

    if len(str(data.cs)) != 6:
        raise ValueError("cs inválida")

    if existing_user:
        raise ValueError("Usuário ja cadastrado")
    return user_repository.create_user(session, data)


def update_user(session: Session, cs: int, data: UserUpdate) -> User:
    user = user_repository.get_by_cs(session, cs)
    if len(str(data.cs)) != 6:
        raise ValueError("cs precisa ter 6 caracteres")

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado"
        )

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        if key == "sector":
            user.sector_id = value
        else:
            setattr(user, key, value)
    session.flush()
    session.refresh(user)
    return user
