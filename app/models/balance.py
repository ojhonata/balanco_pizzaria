import uuid

import sqlalchemy as sa
from sqlalchemy import orm

from app.models.model_base import ModelBase


class Balance(ModelBase):
    __tablename__: str = "balance_sheets"

    id: orm.Mapped[uuid.UUID] = orm.mapped_column(
        sa.UUID,
        primary_key=True,
        server_default=sa.text("gen_random_uuid()")
    )

