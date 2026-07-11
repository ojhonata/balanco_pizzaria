import uuid
from datetime import datetime
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import func, orm

from app.models.enums import OrderStatus
from app.models.material import Material
from app.models.model_base import ModelBase
from app.models.sector import Sector
from app.models.user import User


class Order(ModelBase):
    __tablename__: str = "orders"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        primary_key=True,
        server_default=sa.text("gen_random_uuid()")
    )
    quantity_requested: orm.Mapped[Decimal] = orm.mapped_column(
        sa.DECIMAL(11, 2),
        nullable=False
    )
    quantity_received: orm.Mapped[Decimal | None] = orm.mapped_column(
        sa.DECIMAL(11, 2),
        nullable=True
    )
    order_date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DATETIME(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    received_date: orm.Mapped[datetime | None] = orm.mapped_column(
        sa.DATETIME(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True
    )
    requested_by: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("users.id"),
        nullable=False
    )
    received_by: orm.Mapped[uuid.UUID | None] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("users.id"),
        nullable=True
    )
    user: orm.Mapped[User] = orm.relationship("User", back_populates="orders")

    sector_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("sectors.id"),
        nullable=False
    )
    sector: orm.Mapped[Sector] = orm.relationship("Sector", back_populates="orders")

    material_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("materials.id"),
        nullable=False
    )
    material: orm.Mapped[Material] = orm.relationship("Material", back_populates="orders")

    status: orm.Mapped[OrderStatus] = orm.mapped_column()

