import os
from collections.abc import Generator

import sqlalchemy as sa
from dotenv import load_dotenv
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.models.model_base import ModelBase

load_dotenv()
__engine: Engine | None = None
__SessionLocal: sessionmaker[Session] | None = None


# config banco de dados
def create_engine(sqlite: bool = False) -> Engine:
    global __engine

    if __engine is not None:
        return __engine

    conn_str = os.getenv("DATABASE_URL")
    if conn_str is None:
        raise ValueError("DATABASE_URL não definida no .env")
    __engine = sa.create_engine(url=conn_str.strip(), echo=False)

    return __engine


# sessão para a conexão ao banco de dados
def create_session() -> sessionmaker[Session]:
    global __SessionLocal

    if __SessionLocal is not None:
        return __SessionLocal

    __SessionLocal = sessionmaker(
        bind=create_engine(),
        expire_on_commit=False,
        class_=Session,
    )
    return __SessionLocal


# Dependency para o FastAPI — use com Depends()
def get_session() -> Generator[Session]:
    factory = create_session()
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def create_table() -> None:
    global __engine

    if not __engine:
        create_engine()

    import app.models.__all_models  # pyright: ignore  # noqa: F401
    # ModelBase.metadata.drop_all(__engine)
    ModelBase.metadata.create_all(__engine)
