import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.location import Location
from app.models.model_base import ModelBase


class Material(ModelBase):
    __tablename__: str = "materials"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, primary_key=True, server_default=sa.func.gen_random_uuid()
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(255), nullable=True)
    code: orm.Mapped[int] = orm.mapped_column(sa.Integer, unique=True, nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(sa.Text)
    minimum_stock: orm.Mapped[int] = orm.mapped_column(sa.Integer)
    maximum_stock: orm.Mapped[int] = orm.mapped_column(sa.Integer)
    quantity: orm.Mapped[int] = orm.mapped_column(sa.Integer, nullable=False)

    location_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, sa.ForeignKey("locations.id"), nullable=False
    )

    location: orm.Mapped[Location] = orm.relationship("Location", lazy="joined")

    active: orm.Mapped[bool] = orm.mapped_column(sa.Boolean, server_default=sa.true())
