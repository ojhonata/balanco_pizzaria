
import sqlalchemy as sa
from sqlalchemy import orm

from app.models.model_base import ModelBase
from app.models.sector import Sector


class Category(ModelBase):
    __tablename__: str = "categories"

    __table_args__ = (
        sa.UniqueConstraint(
            "name",
            "sector_id",
            name="uq_name_sector"
        )
    )

    id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer, primary_key=True, autoincrement=True
    )
    name: orm.Mapped[str] = orm.mapped_column(sa.String(100), nullable=False)

    sector_id: orm.Mapped[int] = orm.mapped_column(
        sa.Integer,
        sa.ForeignKey("sectors.id"),
        nullable=False
    )
    sector: orm.Mapped[Sector] = orm.relationship("Sector", lazy="joined")
