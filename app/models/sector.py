import sqlalchemy as sa
from sqlalchemy import orm

from app.models.model_base import ModelBase


class Sector(ModelBase):
    __tablename__: str = "sectors"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, primary_key=True, autoincrement=True
    )
    name: orm.Mapped[str] = orm.mapped_column(
        sa.String(100), unique=True, nullable=False
    )
    uses_location_split: orm.Mapped[bool] = orm.mapped_column(
        sa.Boolean,
        nullable=False,
        server_default=sa.false()
    )
