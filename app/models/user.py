import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.enums import Roles
from app.models.model_base import ModelBase
from app.models.sector import Sector


class User(ModelBase):
    __tablename__: str = "users"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")
    )

    name: orm.Mapped[str] = orm.mapped_column(sa.String(100), nullable=False, unique=True)
    code: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        nullable=False,
        unique=True
    ) # método de login
    role_id: orm.Mapped[Roles] = orm.mapped_column(
        nullable=False
    )

    sector_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("sectors.id"),
        nullable=False
    )

    sector: orm.Mapped[Sector] = orm.relationship("Sector", lazy="joined")
    active: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.true())
