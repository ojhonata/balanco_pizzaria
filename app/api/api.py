from fastapi import APIRouter

from app.api.v1 import category_routers, material_router, sector_routers, user_routers

api_router = APIRouter()

api_router.include_router(user_routers.router, prefix="/users", tags=["Users"])
api_router.include_router(sector_routers.router, prefix="/sectors", tags=["Sectors"])
api_router.include_router(category_routers.router, prefix="/categories", tags=["Categories"])
api_router.include_router(material_router.router, prefix="/materials", tags=["Materials"])
