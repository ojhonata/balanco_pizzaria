from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repository import user_repository
from app.repository.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def list_users(self) -> list[User]:
        try:
            return await self.repository.get_all_user()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Erro interno ao busacar todos os usuários: {e}")


    async def get_user_name(self, name_user: str) -> User | None:
        user = await self.repository.get_by_name(name_user)

        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        if not user.active:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Usuário inativo"
            )

        return user


    async def get_user_by_id(self, user_id: UUID) -> User | None:
        user = await self.repository.get_by_id(user_id)

        if not user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        if not user.active:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Usuário inativo"
            )

        return user


    async def create_user(self, data: UserCreate) -> User:
        existing_user = await self.repository.get_by_name(data.name)

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
