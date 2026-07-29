
from fastapi import HTTPException, status

from app.models.category import Category
from app.repository.category_repository import CategoryRepository
from app.schemas.category_schema import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository = repository

    async def list_categories(self) -> list[Category]:
        try:
            return await self.repository.get_all()
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro interno ao buscar por todos os setores"
            ) from e

    async def get_category_by_id(self, category_id: int) -> Category | None:
        category = await self.repository.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada"
            )

        return category

    async def get_category_by_name(self, category_name: str) -> Category | None:
        category = await self.repository.get_by_name(category_name)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada"
            )

        return category

    async def create_category(self, data:CategoryCreate) -> Category:
        existing_category = await self.repository.get_by_name_and_sector(data.name, data.sector_id)

        if existing_category and existing_category.sector_id == data.sector_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Categoria já cadastrada neste setor"
            )
        category_dict = data.model_dump()

        return await self.repository.create(category_dict)

    async def update_category(self, category_id: int, data: CategoryUpdate) -> Category | None:
        category = await self.repository.get_by_id(category_id)

        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoria não encontrada"
            )

        update_data = data.model_dump(exclude_unset=True)

        new_name = update_data.get("name", category.name)
        new_sector = update_data.get("sdector_id", category.sector_id)

        if new_name != category.name or new_sector != category.sector_id:
            conflit = await self.repository.get_by_name_and_sector(new_name, new_sector)
            if conflit and conflit.id != category.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Categoria já cadstrada neste setor"
                )

        for key, value in update_data.items():
            setattr(category, key, value)

        return await self.repository.update(category)

