import datetime
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

    __table_args__ = (
        sa.UniqueConstraint(
            "balance_id",
            "material_id",
            name="uq_balance_material"
        ),
    )

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        primary_key=True,
        server_default=sa.text("gen_random_uuid()")
    )

    expected_quantity: orm.Mapped[Decimal] = orm.mapped_column(
        sa.DECIMAL(11,2),
        nullable=False
    )
    counted_quantity: orm.Mapped[Decimal] = orm.mapped_column(
        sa.DECIMAL(11, 2),
        nullable=False
    )
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
        nullable=False
    )
    balance: orm.Mapped[Balance] = orm.relationship(
        "Balance",
        back_populates="balance_items"
    )

    material_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("materials.id"),
        nullable=False
    )
    material: orm.Mapped[Material] = orm.relationship(
        "Material",
        back_populates="balance_items")

    revision_note: orm.Mapped[str | None] = orm.mapped_column(
        sa.Text,
        nullable=True
    )
    revised_at: orm.Mapped[datetime.datetime | None] = orm.mapped_column(
        sa.DateTime(timezone=True),
        nullable=True
    )
    # expected_quantity_fundo: orm.Mapped[Decimal | None] = orm.mapped_column(
    #     sa.DECIMAL(11, 2),
    #     nullable=True
    # )
    # expected_quantity_frente: orm.Mapped[Decimal | None] = orm.mapped_column(
    #     sa.DECIMAL(11, 2),
    #     nullable=True
    # )
    counted_quantity_fundo: orm.Mapped[Decimal | None] = orm.mapped_column(
        sa.DECIMAL(11, 2),
        nullable=True
    )
    counted_quantity_frente: orm.Mapped[Decimal | None] = orm.mapped_column(
        sa.DECIMAL(11, 2),
        nullable=True
    )
