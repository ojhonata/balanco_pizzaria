import uuid
from typing import Any

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.inventory_count import InventoryCount
from app.models.material import Material
from app.models.model_base import ModelBase


class InventoryCountItem(ModelBase):
    __tablename__: str = "inventory_count_item"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, primary_key=True, server_default=sa.func.gen_random_uuid()
    )

    counted_quantity: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)
    system_quantity: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)
    difference: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)

    material_id: orm.Mapped[sa.UUID[Any]] = orm.mapped_column(
        sa.UUID, sa.ForeignKey("materials.id"), nullable=False
    )
    material: orm.Mapped[Material] = orm.relationship("Material", lazy="joined")

    count_id: orm.Mapped[sa.UUID[Any]] = orm.mapped_column(
        sa.UUID, sa.ForeignKey("inventory_count.id"), nullable=False
    )
    count: orm.Mapped[InventoryCount] = orm.relationship(
        "InventoryCount", lazy="joined"
    )
