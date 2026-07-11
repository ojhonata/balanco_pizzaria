#import datetime
import uuid
from datetime import date, datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.enums import BalanceStatus
from app.models.model_base import ModelBase
from app.models.sector import Sector
from app.models.user import User


class Balance(ModelBase):
    __tablename__: str = "balances"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        primary_key=True,
        server_default=sa.text("gen_random_uuid()")
    )
    week_start_date: orm.Mapped[date] = orm.mapped_column(
        sa.Date  # retorna somente ano-mes-dia
    )
    sector: orm.Mapped[Sector] = orm.relationship(
        "Sector",
        back_populates="balances"
    )

    closed_by: orm.Mapped[uuid.UUID | None] = orm.mapped_column(
        sa.UUID,
        sa.ForeignKey("users.id"),
        nullable=True
    )
    user: orm.Mapped[User | None] = orm.relationship("User", back_populates="balances")
    status: orm.Mapped[BalanceStatus] = orm.mapped_column()
    closed_at: orm.Mapped[datetime] = orm.mapped_column(sa.DateTime(timezone=True))
