import uuid
from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import ForeignKey, orm

from app.models.enums import Location, Type
from app.models.material import Material
from app.models.model_base import ModelBase
from app.models.order import Order
from app.models.sector import Sector
from app.models.user import User


class Movement(ModelBase):
    __tablename__: str = "movements"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")
    )
    transfer_ref: orm.Mapped[uuid.UUID | None] = orm.mapped_column(
        sa.UUID,
        nullable=True,
        index=True
    )

    date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, server_default=sa.func.now(), index=True
    )

    type: orm.Mapped[Type] = orm.mapped_column()
    location: orm.Mapped[Location | None] = orm.mapped_column(nullable=True)
    quantity: orm.Mapped[Decimal] = orm.mapped_column(sa.DECIMAL(11, 2), nullable=False)

    sector_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, ForeignKey("sectors.id"), nullable=False
    )
    sector: orm.Mapped[Sector] = orm.relationship("Sector", lazy="joined")

    material_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, ForeignKey("materials.id"), nullable=False
    )
    material: orm.Mapped[Material] = orm.relationship("Material", lazy="joined")

    user_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, ForeignKey("users.id"), nullable=False
    )
    user: orm.Mapped[User] = orm.relationship("User", lazy="joined")

    order_id: orm.Mapped[uuid.UUID | None] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("orders.id"),
        nullable=True
    )
    order: orm.Mapped[Order] = orm.relationship("Order", lazy="joined")
