import uuid
from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.model_base import ModelBase
from app.models.user import User


class InventoryCount(ModelBase):
    __tablename__: str = "inventory_count"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, primary_key=True, server_default=sa.func.gen_random_uuid()
    )
    date: orm.Mapped[datetime] = orm.mapped_column(
        sa.DateTime, server_default=sa.func.now(), index=True
    )

    user_id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID, sa.ForeignKey("users.id")
    )

    user: orm.Mapped[User] = orm.relationship("User", lazy="joined")
