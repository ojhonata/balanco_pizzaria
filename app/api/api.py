from fastapi import APIRouter

from app.api.v1 import category_routers, sector_routers, user_routers

api_router = APIRouter()

api_router.include_router(user_routers.router, prefix="/users", tags=["Users"])
api_router.include_router(sector_routers.router, prefix="/sectors", tags=["Sectors"])
# api_router.include_router(type_routers.router, tags=["Type"])
# api_router.include_router(role_routers.router, tags=["Roles"])
api_router.include_router(category_routers.router, prefix="/categories", tags=["Categories"])
# api_router.include_router(material_router.router, tags=["Materials"])
