from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_currente_user
from app.data.db_session import get_db
from app.models.enums import OrderStatus
from app.models.user import User
from app.repository.order_repository import OrderRepository
from app.schemas.pagenation_schema import OrderPageResponse
from app.service.order_service import OrderService

router = APIRouter()


@router.get("/", response_model=list[OrderPageResponse], status_code=status.HTTP_200_OK)
async def get_orders(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_currente_user),
        limit: Annotated[int, Query(ge=0, le=100)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0,
        sector_id: Annotated[int | None, Query(description="ID do setor")] = None,
        status_order: Annotated[OrderStatus | None, Query(description="status do pedido")] = None
    ) -> list[OrderPageResponse]:
    repository = OrderRepository(session)
    service = OrderService(repository)

    orders, total = await service.list_orders(limit, offset, sector_id, status_order)

    return OrderPageResponse(items=orders, total=total, limit=limit, offset=offset) # type: ignore
