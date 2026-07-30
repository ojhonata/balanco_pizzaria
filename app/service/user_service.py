from uuid import UUID

from fastapi import HTTPException, status

from app.core.security import generate_code_hash
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def list_users(self) -> list[User]:
        try:
            return await self.repository.get_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao busacar todos os usuários: {e}") from e


    async def get_user_by_name(self, name_user: str) -> User | None:
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
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nome de usuário já cadastrado"
            )

        user_dict = data.model_dump()

        user_dict["code_hash"] = generate_code_hash(data.code)
        user_dict.pop("code")

        return await self.repository.create(user_dict)



    async def update_user(self, user_id: UUID, data: UserUpdate) -> User | None:
        db_user = await self.repository.get_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        existing_user = await self.repository.get_by_name(data.name) # type: ignore
        if existing_user and existing_user.id != user_id: # type: ignore
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nome do usuário já cadastrado"
            )

        update_data = data.model_dump(exclude_unset=True)

        if update_data.get("new_code"):
            update_data["code_hash"] = generate_code_hash(update_data.pop("new_code")) # type: ignore

        for key, value in update_data.items():
            setattr(db_user, key, value)

        return await self.repository.update(db_user)

    async def delete_user(self, user_id: UUID) -> User | None:
        db_user = await self.repository.get_by_id(user_id)

        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado"
            )

        if not db_user.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuário inativo"
            )

        db_user.active = False

        return await self.repository.update(db_user)

