import datetime
import uuid
from decimal import Decimal

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy import orm

from app.models.material import Material
from app.models.user import User


class ContainerCount(BaseModel):
    __tablename__: str  = "container_counts"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        primary_key=True,
        server_default=sa.text("gen_random_uuid()")
    )
    count_date: orm.Mapped[datetime.datetime] = orm.mapped_column(
        sa.DateTime(timezone=True),
        nullable=False,
    )

    material_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("material.id"),
        nullable=False
    )
    material: orm.Mapped[Material] = orm.relationship(
        "Material",
        lazy="joined"
    )

    counted_cascos: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        nullable=False
    )
    expected_from_sales: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        nullable=False
    )
    difference: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.Computed("counted_cascos - expected_from_sales", persisted=True),
        nullable=False
    )

    unit_sale_price: orm.Mapped[Decimal] = orm.mapped_column(
        sa.DECIMAL(10, 2),
        nullable=False
    )
    value_impact: orm.Mapped[Decimal] = orm.mapped_column(
        sa.DECIMAL(10, 2),
        sa.Computed("difference * unit_sale_price", persisted=True),
        nullable=False
    )
    counted_by: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("users.id"),
        nullable=False
    )
    user: orm.Mapped[User] = orm.relationship("User", lazy="joined")

