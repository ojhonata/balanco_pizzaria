from typing import Annotated
from uuid import UUID

import jwt
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import oauth2_scheme
from app.core.config import ALGORITHM, SECRET_KEY
from app.data.db_session import get_db
from app.models.user import User
from app.repository.user_repository import UserRepository


class TokenData(BaseModel):
    user_id: str | None = None


async def get_currente_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # type: ignore
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        token_data = TokenData(user_id=str(user_id))

    except jwt.InvalidTokenError as e:
        raise credentials_exception from e

    try:
        user_uuid = UUID(token_data.user_id)
    except (ValueError, TypeError) as e:
        raise credentials_exception from e

    repository = UserRepository(db)
    user = await repository.get_by_id(user_uuid)

    if user is None:
        raise credentials_exception

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )

    return user

class ROleChecker:
    def __init__(self, allowed_roles: list[str]) -> None:
        self.allowed_roles = allowed_roles

    async def __call__(
        self, current_user: Annotated[User, Depends(get_currente_user)]
    ) -> User:

        if not current_user.role or current_user.role.name not in self.allowed_roles: # type: ignore
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar esse conteúdo"
            )

        return current_user
