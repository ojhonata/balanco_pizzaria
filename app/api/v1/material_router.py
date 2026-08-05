
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import RoleChecker, get_currente_user
from app.data.db_session import get_db
from app.models.user import User
from app.repository.material_repository import MaterialRepository
from app.schemas.materials_schema import (
    MaterialCreate,
    MaterialResponse,
    MaterialUpdate,
)
from app.schemas.pagenation_schema import MaterialPageResponse
from app.service.material_service import MaterialService

router = APIRouter()

require_admin = RoleChecker(["ADMIN"])

@router.get("/", response_model=list[MaterialPageResponse], status_code=status.HTTP_200_OK)
async def get_materials(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_currente_user), # type: ignore
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    name: str | None = None
    ) -> list[MaterialPageResponse]:
    repository = MaterialRepository(session)
    service = MaterialService(repository)

    materials, total = await service.list_materials(limit, offset, name)

    return MaterialPageResponse(items=materials, total=total, limit=limit, offset=offset) # type: ignore

@router.get("/{material_id}", response_model=MaterialResponse, status_code=status.HTTP_200_OK)
async def get_material(
        material_id: UUID,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(require_admin) #pyright: ignore
    ):
    repository = MaterialRepository(session)
    service = MaterialService(repository)

    return await service.get_material_by_id(material_id)

# @router.get("/{material_name}", response_model=MaterialResponse, status_code=status.HTTP_200_OK)
# async def get_materia_by_name(
#         material_name: str,
#         session: AsyncSession = Depends(get_db),
#         current_user = Depends(get_currente_user) # pyright: ignore
#     ):
#     repository = MaterialRepository(session)
#     service = MaterialService(repository)

#     return await service.get_material_by_name(material_name)

@router.post("/", response_model=MaterialResponse, status_code=status.HTTP_201_CREATED)
async def post_material(
        data: MaterialCreate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(require_admin) # pyright:ignore
    ):
    repository = MaterialRepository(session)
    service = MaterialService(repository)

    return await service.create_material(data)

@router.patch("/{material_id}", response_model=MaterialResponse, status_code=status.HTTP_200_OK)
async def patch_material(
        material_id: UUID,
        data: MaterialUpdate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(require_admin) # pyright: ignore
    ):
    repository = MaterialRepository(session)
    service = MaterialService(repository)

    return await service.update_material(material_id, data)

@router.delete("/", response_model=MaterialResponse, status_code=status.HTTP_200_OK)
async def delete_material(
        material_id: UUID,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(require_admin) # pyright: ignore
    ):
    repository = MaterialRepository(session)
    service = MaterialService(repository)

    return await service.delete_material(material_id)


