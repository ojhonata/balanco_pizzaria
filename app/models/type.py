import sqlalchemy as sa
from sqlalchemy import orm

from app.models.model_base import ModelBase


class Type(ModelBase):
    __tablename__: str = "types"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, primary_key=True, autoincrement=True
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(10), nullable=False)
