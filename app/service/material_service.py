from uuid import UUID

from fastapi import HTTPException, status

from app.models.material import Material
from app.repository.material_repository import MaterialRepository
from app.schemas.materials_schema import MaterialCreate, MaterialUpdate


class MaterialService:
    def __init__(self, repository: MaterialRepository) -> None:
        self.repository = repository

    async def list_materials(self) -> list[Material]:
        try:
            return await self.repository.get_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar por todos os materiais {e}"
            )from e

    async def get_material_by_name(self, material_name: str) -> Material:
        material = await self.repository.get_by_name(material_name)

        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Material não encontrado"
            )

        if not material.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Material inativo"
            )

        return material

    async def get_material_by_id(self, material_id: UUID) -> Material:
        material = await self.repository.get_by_id(material_id)

        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Material não encontrado"
            )

        if not material.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Material inativo"
            )

        return material

    async def create_material(self, data: MaterialCreate) -> Material:
        existing_material_category = await self.repository.get_by_name_and_category(
            data.name, data.category_id
        )

        if data.minimum_stock and data.minimum_stock < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="O estoque minimo não pode ser negativo"
            )

        if existing_material_category:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Material já está cadastrado nessa categoria"
            )

        material_dict = data.model_dump()

        return await self.repository.create(material_dict)

    async def update_material(self, material_id:UUID, data: MaterialUpdate) -> Material | None:
        db_material = await self.repository.get_by_id(material_id)

        if not db_material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Material não encontrado"
            )

        if not db_material:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Material inativo"
            )

        update_data = data.model_dump(exclude_unset=True)

        new_name = update_data.get("name", db_material.name)
        new_category = update_data.get("category_id", db_material.category_id)

        if new_name != db_material.name or new_category != db_material.category_id:
            conflit = await self.repository.get_by_name_and_category(new_name, new_category)
            if conflit and conflit.id != db_material.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Material já cadastrado nessa categoria"
                )

        for key, value in update_data.items():
                    setattr(db_material, key, value)

        return await self.repository.update(db_material)

    async def delete_material(self, material_id: UUID) -> Material | None:
        material = await self.repository.get_by_id(material_id)

        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Material não encontrado"
            )

        if not material.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Material inativo"
            )

        material.active = False

        return await self.repository.update(material)

    async def active_material(self, material_id: UUID) -> Material | None:
        material = await self.repository.get_by_id(material_id)

        if not material:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Material não encontrado"
            )

        if material.active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Material já está ativo"
            )

        material.active = True

        return await self.repository.update(material)
