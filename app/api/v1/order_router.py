from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_currente_user
from app.data.db_session import get_db
from app.models.enums import OrderStatus
from app.models.user import User
from app.repository.order_repository import OrderRepository
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderUpdate
from app.schemas.pagenation_schema import OrderPageResponse
from app.service.order_service import OrderService

router = APIRouter()


@router.get("/", response_model=OrderPageResponse, status_code=status.HTTP_200_OK)
async def get_orders(
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_currente_user),
        limit: Annotated[int, Query(ge=0, le=100)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0,
        sector_id: Annotated[int | None, Query(description="ID do setor")] = None,
        status_order: Annotated[OrderStatus | None, Query(description="status do pedido")] = None
    ) -> OrderPageResponse:
    repository = OrderRepository(session)
    service = OrderService(repository)

    orders, total = await service.list_orders(limit, offset, sector_id, status_order)

    items = [OrderResponse.model_validate(m) for m in orders] # validação

    return OrderPageResponse(items=items, total=total, limit=limit, offset=offset)

@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(
        order_id: UUID,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_currente_user)
    ):
    repository = OrderRepository(session)
    service = OrderService(repository)

    return await service.get_order_by_id(order_id)

@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def post_order(
        data: OrderCreate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_currente_user)
    ):
    requested_by = current_user.id
    repository = OrderRepository(session)
    service = OrderService(repository)

    return await service.create_order(data, requested_by)

@router.patch("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_202_ACCEPTED)
async def patch_order(
        order_id: UUID,
        data: OrderUpdate,
        session: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_currente_user)
    ):
    repository = OrderRepository(session)
    service = OrderService(repository)

    return await service.order_update(data, order_id)
