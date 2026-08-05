from uuid import UUID

from fastapi import HTTPException, status

from app.models.enums import OrderStatus
from app.models.order import Order
from app.repository.order_repository import OrderRepository
from app.schemas.order_schema import OrderCreate


class OrderService:
    def __init__(self, repository: OrderRepository) -> None:
        self.repository = repository

    async def list_orders(
        self,
        limit: int,
        offset: int,
        sector_id: int | None = None,
        status_order: OrderStatus | None = None
    ) -> tuple[list[Order], int]:
        try:
            return await self.repository.get_all(
                limit,
                offset,
                sector_id,
                status_order
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar por todos os pedidos {e}"
            )from e

    async def get_order(
        self,
        order_id: UUID,
    ) -> Order | None:
        order = await self.repository.get_by_id(order_id)

        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado"
            )

        return order

    async def create_order(self, data: OrderCreate) -> Order:
        if data.quantity_requested <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="A quantidade não pode ser negativa ou zero"
            )

        order_data = data.model_dump()

        return await self.repository.create(order_data)
