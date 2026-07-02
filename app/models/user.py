import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.model_base import ModelBase
from app.models.sector import Sector


class User(ModelBase):
    __tablename__: str = "users"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, primary_key=True, server_default=sa.func.gen_random_uuid()
    )

    name: orm.Mapped[str] = orm.mapped_column(sa.String(100), nullable=False)
    cs: orm.Mapped[int] = orm.mapped_column(sa.Integer, unique=True, nullable=False)
    password: orm.Mapped[str] = orm.mapped_column(sa.String(8), nullable=False)
    role: orm.Mapped[str] = orm.mapped_column(sa.String(20), server_default="user")

    sector_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("sectors.id"), nullable=False
    )

    sector: orm.Mapped[Sector] = orm.relationship("Sector", lazy="joined")

    active: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.true())
