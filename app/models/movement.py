import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import ForeignKey, orm

from app.models.model_base import ModelBase
from app.models.sector import Sector
from app.models.type import Type
from app.models.user import User


class Movement(ModelBase):
    __tablename__: str = "movements"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, primary_key=True, server_default=sa.func.gen_random_uuid()
    )

    ordem_number: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=True)
    date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, server_default=sa.func.now(), index=True
    )

    sector_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, ForeignKey("sectors.id"), nullable=False
    )
    sector: orm.Mapped[Sector] = orm.relationship("Sector", lazy="joined")

    type_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, ForeignKey("types.id"), nullable=False
    )
    type: orm.Mapped[Type] = orm.relationship("Type", lazy="joined")

    user_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, ForeignKey("users.id"), nullable=False
    )
    user: orm.Mapped[User] = orm.relationship("User", lazy="joined")
