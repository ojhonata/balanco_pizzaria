from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import AuthService
from app.data.db_session import get_db
from app.repository.user_repository import UserRepository


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    repository = UserRepository(db)
    return AuthService(repository)
