from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import AuthService
from app.core.deps import ROleChecker
from app.data.db_session import get_db
from app.models.user import User
from app.repository.user_repository import UserRepository
from app.schemas.token_schema import TokenResponse
from app.schemas.user_schema import UserCreate, UserResponse
from app.service.get_auth_service import get_auth_service
from app.service.user_service import UserService

router = APIRouter()

require_pizzaria = ROleChecker(["PIZZARIA"])

@router.get("/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_loggedin(user_loggedin: User = Depends(require_pizzaria)) -> User:
    return user_loggedin

@router.get("/", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(current_user: User = Depends(require_pizzaria), session: AsyncSession = Depends(get_db)):
    repository = UserRepository(session)

    service = UserService(repository)

    return await service.list_users()


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_db)):
    repository = UserRepository(session)
    service = UserService(repository)

    return await service.get_user_by_id(user_id)


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def post_user(data: UserCreate, session: AsyncSession = Depends(get_db)):
    repository = UserRepository(session)
    service = UserService(repository)

    return await service.create_user(data)

@router.post("/login", status_code=status.HTTP_201_CREATED, response_model=TokenResponse)
async def loin(
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_service: AuthService = Depends(get_auth_service)
    ):
    user = await auth_service.authenticate(name= form_data.username, code = form_data.password)

    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Dados incorretos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuário inativo"
        )

    return {
        "access_token": auth_service.create_token_access(sub=user.id), # type: ignore
        "token_type": "bearer"
    }
