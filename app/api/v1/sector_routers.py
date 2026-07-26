from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db_session import get_db
from app.repository.sector_repository import SectorRepository
from app.schemas.sector_schema import SectorCreate, SectorResponse
from app.service.sector_service import SectorService

router = APIRouter()


@router.get("/", response_model=list[SectorResponse], status_code=status.HTTP_200_OK)
async def list_sectors(session: AsyncSession = Depends(get_db)):
    repository = SectorRepository(session)
    service =  SectorService(repository)

    return await service.list_sector()


# @router.get("/{id}", response_model=SectorResponse)
# def list_by_id(id: int, session: Session = Depends(get_session)):
#     try:
#         return sector_service.get_sector_by_id(session, id)
#     except ValueError as e:
#         raise HTTPException(status_code=404, detail=str(e))


@router.post("/", response_model=SectorResponse, status_code=status.HTTP_201_CREATED)
async def post_sector(data: SectorCreate, session: AsyncSession = Depends(get_db)):
    repository = SectorRepository(session)
    service = SectorService(repository)

    return await service.create_sector(data)

