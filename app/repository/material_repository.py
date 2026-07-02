from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.material import Material
from app.schemas.materials_schema import MaterialCreate, MaterialUpdate


def get_all_materials(session: Session) -> list[Material]:
    return session.execute(select(Material)).scalars().all()  # pyright: ignore


def get_by_id(session: Session, id: UUID) -> Material | None:
    return session.execute(
        select(Material).where(Material.id == id)
    ).scalar_one_or_none()  # pyright: ignore


def get_by_code(session: Session, code: int) -> Material | None:
    return session.execute(
        select(Material).Where(Material.code == code)  # pyright: ignore
    ).scalar_one_or_none()


def create_material(session: Session, data: MaterialCreate) -> Material:
    material = Material(
        name=data.name,
        code=data.code,
        decription=data.description,
        minimum_stock=data.minimum_stock,
        maximum_stock=data.maximum_stock,
        quantity=data.quantity,
        location_id=data.location_id,
    )

    session.add(material)
    session.commit()
    session.refresh(material)

    return material


def update_material(session: Session, data: MaterialUpdate, id: UUID) -> Material | None:
    material = get_by_id(session, id)

    if not material:
        return None

    if data.name is not None:
        material.name = data.name
    if data.code is not None:
        material.code = data.code
    if data.description is not None:
        material.description = data.description
    if data.minimum_stock is not None:
        material.minimum_stock = data.minimum_stock
    if data.maximum_stock is not None:
        material.maximum_stock = data.maximum_stock
    if data.quantity is not None:
        material.quantity = data.quantity
    if data.location_id is not None:
        material.location_id = data.location_id

    session.commit()
    session.refresh(material)

    return material
