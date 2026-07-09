import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.model_base import ModelBase
from app.models.role import Role
from app.models.sector import Sector


class User(ModelBase):
    __tablename__: str = "users"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, primary_key=True, server_default=sa.text("gen_random_uuid()")
    )

    name: orm.Mapped[str] = orm.mapped_column(sa.String(100), nullable=False, unique=True)
    code: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False) # método de login
    role_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("roles.id"),
        nullable=False,
        server_default="1",
        default=1
    )
    role: orm.Mapped[Role] = orm.relationship("Role", lazy="joined")

    sector_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("sectors.id"),
        nullable=False
    )

    sector: orm.Mapped[Sector] = orm.relationship("Sector", lazy="joined")

    active: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.true())
