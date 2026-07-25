from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sector import Sector


class SectorRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Sector]:
        result = await self.session.execute(select(Sector))
        return list(result.scalars().all())

    async def get_by_id(self, sector_id: int) -> Sector | None:
        query = select(Sector).where(Sector.id == sector_id)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def get_by_name(self, name_sector: str) -> Sector | None:
        query = select(Sector).where(Sector.name == name_sector)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def create(self, data: dict[str, Any]) -> Sector:
        sector = Sector(**data)

        self.session.add(sector)
        await self.session.commit()
        await self.session.refresh(sector)

        return sector

    async def update(self, sector: Sector) -> Sector | None:
        self.session.add(sector)
        await self.session.commit()
        await self.session.refresh(sector)

        return sector
