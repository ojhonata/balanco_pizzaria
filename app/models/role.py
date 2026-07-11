
import sqlalchemy as sa
from sqlalchemy import orm

from app.models.model_base import ModelBase


class Role(ModelBase):
    __tablename__: str = "roles"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(20), nullable=False)
