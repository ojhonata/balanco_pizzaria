from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.material import Material


class MaterialRepository:
    def __init__(self, session: AsyncSession)-> None:
        self.session = session

    async def get_all(
        self,
        limit: int,
        offset: int,
        name: str | None,) -> tuple[list[Material], int]:

        filters: list[Any] = []
        if name:
            filters.append(Material.name.ilike(f"%{name}%")) # type: ignore

        count_query = select(func.count()).select_from(Material).where(*filters)
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        items_query = select(Material).where(*filters).limit(limit).offset(offset)
        items_result = await self.session.execute(items_query)
        items = list(items_result.scalars())

        return items, total

    async def get_by_id(self, material_id: UUID) -> Material | None:
        query = select(Material).where(Material.id == material_id)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def get_by_name(self, material_name: str) -> Material | None:
        query = select(Material).where(Material.name == material_name)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def get_by_name_and_category(self, name: str, category_id: int) -> Material | None:
        query = select(Material).where(
            Material.name == name and Material.category_id == category_id)
        result = await self.session.execute(query)
        return result.scalars().unique().one_or_none()

    async def create(self, data: dict[str, Any]) -> Material:
        material = Material(**data)

        self.session.add(material)
        await self.session.commit()
        await self.session.refresh(material)

        return material

    async def update(self, material: Material) -> Material:
        self.session.add(material)
        await self.session.commit()
        await self.session.refresh(material)

        return material
