from datetime import UTC, datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from app.core.security import check_code
from app.models.user import User
from app.repository.user_repository import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate(self, code: str) -> User | None:
        user = await self.user_repository.get_by_code(code)

        if not user:
            return None

        if not user.active:
            return None

        if not check_code(code, user.code_hash):
            return None
        return user

    def _create_token(self, token_type: str, tempo_vida: timedelta, sub: str) -> str:
        payload = {}

        now = datetime.now(UTC)
        expira = now + tempo_vida

        payload["type"] = token_type
        payload["exp"] = expira
        payload["iat"] = now
        payload["sub"] = str(sub)

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM) # type: ignore

    def create_token_access(self, sub: str) -> str:
        return self._create_token(
            token_type = "access_token",
            tempo_vida = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            sub = sub
        )
