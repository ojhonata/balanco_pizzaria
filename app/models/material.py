import uuid

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
    minimum_stock: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)
    maximum_stock: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)
    quantity: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)

    category_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("categories.id"), nullable=False
    )

    category: orm.Mapped[Category] = orm.relationship("Category", lazy="joined")

    active: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.true())
