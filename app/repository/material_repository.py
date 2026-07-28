from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.material import Material


class MaterialRepository:
    def __init__(self, session: AsyncSession)-> None:
        self.session = session

    async def get_all(self) -> list[Material]:
        result = await self.session.execute(select(Material))
        return list(result.scalars().all())

    async def get_by_id(self, material_id: UUID) -> Material | None:
        query = select(Material).where(Material.id == material_id)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def get_by_name(self, material_name: str) -> Material | None:
        query = select(Material).where(Material.name == material_name)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    