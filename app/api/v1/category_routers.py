from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import RoleChecker, get_currente_user
from app.data.db_session import get_db
from app.repository.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from app.service.category_service import CategoryService

router = APIRouter()

requisre_admin = RoleChecker(["ADMIN"])

@router.get("/", response_model=list[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_categories(
        current_user = Depends(get_currente_user), # type: ignore
        session: AsyncSession = Depends(get_db)
    ):
    repository = CategoryRepository(session)
    service = CategoryService(repository)

    return await service.list_categories()

@router.get("/{category_id}", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def get_category(
        category_id: int,
        currente_user = Depends(get_currente_user), # type: ignore
        session: AsyncSession = Depends(get_db)
    ):
    repository = CategoryRepository(session)
    service = CategoryService(repository)

    return await service.get_category_by_id(category_id)

@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def post_category(
        data: CategoryCreate,
        currente_user = Depends(requisre_admin), # pyright: ignore
        session: AsyncSession = Depends(get_db)
    ):
    repository = CategoryRepository(session)
    service = CategoryService(repository)

    return await service.create_category(data)

@router.patch("/", response_model=CategoryResponse, status_code=status.HTTP_200_OK)
async def patch_category(
        category_id: int,
        data: CategoryUpdate,
        current_user = Depends(requisre_admin), # type: ignore
        session: AsyncSession = Depends(get_db)
    ):
    repository = CategoryRepository(session)
    service = CategoryService(repository)

    return await service.update_category(category_id, data)


