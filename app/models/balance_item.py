import uuid
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.balance import Balance
from app.models.material import Material
from app.models.model_base import ModelBase
from app.models.user import User


class BalanceItem(ModelBase):
    __tablename__: str = "balance_items"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        primary_key=True,
        server_default=sa.text("gen_random_uuid()")
    )

    expected_quantity: orm.Mapped[Decimal] = orm.mapped_column(sa.DECIMAL(11,2), nullable=False)
    counted_quantity: orm.Mapped[Decimal] = orm.mapped_column(sa.DECIMAL(11, 2), nullable=False)
    difference: orm.Mapped[Decimal] = orm.mapped_column(sa.DECIMAL(11, 2), nullable=False)
    revised_expected_quantity: orm.Mapped[Decimal | None] = orm.mapped_column(
        sa.DECIMAL(11, 2),
        nullable=True
    )

    counted_by: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("users.id"),
        nullable=False
    )
    user: orm.Mapped[User] = orm.relationship("User", back_populates="balance_items")

    balance_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("balances.id"),
        nullabel=False
    )
    balance: orm.Mapped[Balance] = orm.relationship("Balance", back_populates="balance_items")

    material_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("materials.id"),
        nullabel=False
    )
    material: orm.Mapped[Material] = orm.relationship("Material", back_populates="balance_items")

