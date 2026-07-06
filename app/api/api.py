from fastapi import APIRouter

from app.api.v1 import (
    location_routers,
    material_router,
    sector_routers,
    shelf_routers,
    type_routers,
    user_routers,
)

api_router = APIRouter()

api_router.include_router(user_routers.router, prefix="/users", tags=["Users"])
api_router.include_router(sector_routers.router, tags=["Sectors"])
api_router.include_router(type_routers.router, tags=["Type"])
api_router.include_router(shelf_routers.router, tags=["Shelves"])
api_router.include_router(location_routers.router, tags=["Locations"])
api_router.include_router(material_router.router, tags=["Materials"])
