import uuid
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.category import Category
from app.models.model_base import ModelBase


class Material(ModelBase):
    __tablename__: str = "materials"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(255), nullable=True)
    unit: orm.Mapped[str] = orm.mapped_column(sa.String(10), nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(sa.Text)
    minimum_stock: orm.Mapped[int | None] = orm.mapped_column(sa.Integer, nullable=True)
    # maximum_stock: orm.Mapped[int | None] = orm.mapped_column(sa.Integer, nullable=True)

    category_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("categories.id"), nullable=False
    )
    category: orm.Mapped[Category] = orm.relationship("Category", lazy="joined")
    tracks_container: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean,
        server_default=sa.false()
    )
    sale_price: orm.Mapped[Decimal | None] = orm.mapped_column(sa.DECIMAL(10, 2), nullable=True)

    active: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.true())
