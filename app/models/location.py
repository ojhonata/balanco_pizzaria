import sqlalchemy as sa
from sqlalchemy import ForeignKey, orm

from app.models.model_base import ModelBase
from app.models.shelf import Shelf


class Location(ModelBase):
    __tablename__: str = "locations"

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, primary_key=True, autoincrement=True
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(5), nullable=False)

    shelf_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, ForeignKey("shelves.id")
    )

    shelf: orm.Mapped[list[Shelf]] = orm.relationship(
        "Shelf", lazy="joined"
    )
