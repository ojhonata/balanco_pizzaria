from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_user(self) -> list[User]:
        result = await self.session.execute(select(User))
        return list(result.scalars().all())

    async def get_by_name(self, name_user: str) -> User | None:
        query = select(User).where(User.name == name_user)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def get_by_code(self, code_user: str) -> User | None:
        query = select(User).where(User.code_hash == code_user)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(User).where(User.id == user_id)
        result = await self.session.execute(query)

        return result.scalars().unique().one_or_none()

    async def create_user(self, data: dict[str, Any]) -> User:
        user = User(**data)

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def update_user(self, user: User) -> User | None:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
