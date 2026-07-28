from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import RoleChecker, get_currente_user
from app.data.db_session import get_db
from app.repository.sector_repository import SectorRepository
from app.schemas.sector_schema import SectorCreate, SectorResponse, SectorUpdate
from app.service.sector_service import SectorService

router = APIRouter()

require_admin = RoleChecker(["ADMIN"])

@router.get("/", response_model=list[SectorResponse], status_code=status.HTTP_200_OK)
async def list_sectors(
        session: AsyncSession = Depends(get_db),
        current_user = Depends(get_currente_user) # type: ignore
    ):
    repository = SectorRepository(session)
    service =  SectorService(repository)

    return await service.list_sector()


@router.get("/{id}", response_model=SectorResponse)
async def get_sector(
        sector_id: int,
        session: AsyncSession = Depends(get_db),
        current_user = Depends(get_currente_user) # type: ignore
    ):
    repository = SectorRepository(session)
    service = SectorService(repository)

    return await service.get_sector_by_id(sector_id)


@router.post("/", response_model=SectorResponse, status_code=status.HTTP_201_CREATED)
async def post_sector(
        data: SectorCreate,
        session: AsyncSession = Depends(get_db),
        current_user = Depends(require_admin) # type: ignore
    ):
    repository = SectorRepository(session)
    service = SectorService(repository)

    return await service.create_sector(data)

@router.patch("/{sector_id}", response_model=SectorResponse, status_code=status.HTTP_200_OK)
async def patch_sector(
        sector_id: int,
        data: SectorUpdate,
        session: AsyncSession = Depends(get_db),
        current_user = Depends(require_admin) # type: ignore
    ):
    repository = SectorRepository(session)
    service = SectorService(repository)

    return await service.update_sector(sector_id, data)

