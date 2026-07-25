from fastapi import HTTPException, status

from app.models.sector import Sector
from app.repository.sector_repository import SectorRepository
from app.schemas.sector_schema import SectorCreate, SectorUpdate


class SectorService:
    def __init__(self, repository: SectorRepository):
        self.repository = repository

    def list_sector(self) -> list[Sector]:
        try:
            return self.repository.get_all() # type: ignore
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro interno ao buscar por setores: {e}"
            ) from e

    async def get_sector_by_id(self, sector_id: int) -> Sector | None:
        sector = await self.repository.get_by_id(sector_id)

        if not sector:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sector não encontrado"
            )

        return sector

    async def get_sector_by_name(self, sector_name: str) -> Sector | None:
        sector = await self.repository.get_by_name(sector_name)

        if not sector:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sector não encontrado"
            )

        return sector


    async def create_sector(self, data: SectorCreate) -> Sector:
        existing_sector = await self.repository.get_by_name(data.name)

        if existing_sector:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nome de usuário já cadastrado"
            )

        user_dict = data.model_dump()

        return await self.repository.create(user_dict)


    async def update_sector(self, sector_id: int, data: SectorUpdate) -> Sector| None:
        db_sector = await self.repository.get_by_id(sector_id)

        if not db_sector:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Setor não encontrado"
            )

        if data.name and data.name != db_sector.name:
            existing_sector = await self.repository.get_by_name(data.name)
            if existing_sector:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Setor ja está cadastrado"
                )

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
                setattr(db_sector, key, value)

        return await self.repository.update(db_sector)

