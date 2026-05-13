from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from data.models.material import Material
from data.repository import material_repository
from schemas.materials_schema import MaterialCreate, MaterialUpdate


def get_all(session: Session) -> list[Material]:
    try:
        return material_repository.get_all_materials(session)
    except ValueError as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_materiel_by_code(session: Session, code: int) -> Material:
    material = material_repository.get_by_code(session, code)

    if not material:
        raise ValueError(f"Material com o código {code} não encontrado")

    if not material.active:
        raise ValueError(f"Material com o código {code} desativado")

    return material


def get_material_by_id(session: Session, material_id: UUID) -> Material:
    material = material_repository.get_by_id(session, material_id)

    if not material:
        raise ValueError("Material não encontrado")

    if not material.active:
        raise ValueError("Material desativado")

    return material


def post_material(session: Session, data: MaterialCreate) -> Material:
    existing_material = material_repository.get_by_code(session, data.code)

    if existing_material:
        raise ValueError("Material já cadastrado")

    if len(str(data.code)) != 7:
        raise ValueError("O código do material precisa ter 7 números")

    return material_repository.create_material(session, data)


def update_material(session: Session, data: MaterialUpdate, id: UUID) -> Material:
    material = material_repository.get_by_id(session, id)

    if not material:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Material não encontrado"
        )

    if len(str(data.code)) != 7:
        raise ValueError("O código do material precisa ter 7 números")

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "location":
            material.location_id = value
        else:
            setattr(material, key, value)
    session.flush()
    session.refresh(material)
    return material
