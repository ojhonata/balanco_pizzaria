from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Category]:
        result = await self.session.execute(select(Category))
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Category | None:
        query = select(Category).where(Category.id == category_id)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def get_by_name(self, category_name: str) -> Category | None:
        query = select(Category).where(Category.name == category_name)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def get_by_name_and_sector(self, name: str, sector_id: int) -> Category | None:
        query = select(Category).where(
            Category.name == name and Category.sector_id == sector_id
        )
        result = await self.session.execute(query)
        return result.scalars().unique().one_or_none()

    async def create(self, data: dict[str, Any]) -> Category:
        category = Category(**data)

        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)

        return category

    async def update(self, category: Category) -> Category | None:
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)

        return category
