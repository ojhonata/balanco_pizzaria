import datetime
import uuid
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
    quantity_ordered: orm.Mapped[Decimal | None] = orm.mapped_column(
        sa.DECIMAL(11, 2),
        nullable=True
    )
    requested_at: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    received_date: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        sa.DateTime(timezone=True),
        nullable=True
    )
    ordered_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        sa.DateTime(timezone=True),
        nullable=True
    )
    ordered_by: orm.Mapped[uuid.UUID | None] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("users.id"),
        nullable=True
    )
    ordered: orm.Mapped[User | None] = orm.relationship("User", foreign_keys=[ordered_by])

    requested_by: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("users.id"),
        nullable=False
    )
    requested: orm.Mapped[User] = orm.relationship("User", foreign_keys=[requested_by])

    received_by: orm.Mapped[uuid.UUID | None] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("users.id"),
        nullable=True
    )
    received: orm.Mapped[User | None] = orm.relationship("User", foreign_keys=[received_by])

    sector_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("sectors.id"),
        nullable=False
    )
    sector: orm.Mapped[Sector] = orm.relationship("Sector", lazy="joined")

    material_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("materials.id"),
        nullable=False
    )
    material: orm.Mapped[Material] = orm.relationship("Material", lazy="joined")

    status: orm.Mapped[OrderStatus] = orm.mapped_column(
        sa.Enum(OrderStatus, name="orderstatus"),
        server_default=sa.text(f"'{OrderStatus.SOLICITADO.name}'"),
        nullable=False
    )
    description: orm.Mapped[str | None] = orm.mapped_column(sa.Text, nullable=True)

