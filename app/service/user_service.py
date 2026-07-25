from uuid import UUID

from fastapi import HTTPException, status

from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def list_user(self) -> list[User]:
        try:
            return await self.repository.get_all_user()
        except Exception as e:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao buscar por usuários: {e}"
            ) from e

    async def get_user_by_id(self, user_id: UUID) -> User:
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
        user_existing = await self.repository.get_by_name(data.name)

        if user_existing:
            raise HTTPException(status.HTTP_409_CONFLICT, detail="Nome já cadastrado")

        user_dict = data.model_dump()

        return await self.repository.create_user(user_dict)


    async def update_user(self, user_id: UUID, data: UserUpdate) -> User:
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

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)

        return await self.repository.update_user(user) # type: ignore

    async def delete_user(self, user_id: UUID) -> User | None:
        db_user = await self.repository.get_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        if not db_user.active:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST,
                detail="Usuário inativo"
            )

        db_user.active = True

        return await self.repository.update_user(db_user)
