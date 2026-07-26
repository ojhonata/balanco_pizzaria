from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ROleChecker
from app.data.db_session import get_db
from app.repository.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserResponse
from app.service.user_service import UserService

router = APIRouter()

require_admin = ROleChecker(["admin"])

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(session: AsyncSession = Depends(require_admin)):
    repository = UserRepository(session)

    service = UserService(repository)

    return await service.list_users()


@router.get("/user/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_db)):
    repository = UserRepository(session)
    service = UserService(repository)

    return await service.get_user_by_id(user_id)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def post_user(data: UserCreate, session: AsyncSession = Depends(get_db)):
    repository = UserRepository(session)
    service = UserService(repository)

    return await service.create_user(data)

