from typing import Any
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import OrderStatus
from app.models.order import Order


class OrderRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(
        self,
        limit: int,
        offset: int,
        sector_id: int | None,
        status: OrderStatus | None,
    ) -> tuple[list[Order], int]:
        filters: list[Any] = []

        if sector_id is not None:
            filters.append(Order.sector_id == sector_id)

        if status:
            filters.append(Order.status == status)

        count_query = select(func.count()).select_from(Order).where(*filters)
        total_result = await self.session.execute(count_query)
        total = total_result.scalar_one()

        items_query = select(Order).where(*filters).limit(limit).offset(offset)
        items_result = await self.session.execute(items_query)
        items = list(items_result.scalars().unique())

        return items, total

    async def get_by_id(self, order_id: UUID) -> Order | None:
        query = select(Order).where(Order.id == order_id)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def create(self, data: dict[str, Any]) -> Order:
        order = Order(**data)

        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)

        return order

    async def update(self, order: Order) -> Order | None:
        self.session.add(order)
        await self.session.commit()
        await self.session.refresh(order)

        return order
