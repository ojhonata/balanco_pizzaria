
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import RoleChecker, get_currente_user
from app.data.db_session import get_db
from app.repository.material_repository import MaterialRepository
from app.schemas.materials_schema import MaterialResponse
from app.service.material_service import MaterialService

router = APIRouter()

require_admin = RoleChecker(["ADMIN"])

@router.get("/", response_model=list[MaterialResponse], status_code=status.HTTP_200_OK)
async def list_materials(
    session: AsyncSession = Depends(get_db),
    current_user = Depends(get_currente_user)): # type: ignore
    repository = MaterialRepository(session)
    service = MaterialService(repository)

    return await service.list_materials()

@router.get("/", response_model=MaterialResponse, status_code=status.HTTP_200_OK)
async def get_material(
        material_id: UUID,
        session: AsyncSession = Depends(get_db),
        currentUser = Depends(require_admin) #pyright: ignore
    ):
    repository = MaterialRepository(session)
    service = MaterialService(repository)

    return await service.get_material_by_id(material_id)
