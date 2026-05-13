from fastapi import FastAPI

from routers import (
    location_routers,
    material_router,
    sector_routers,
    shelf_routers,
    type_routers,
    user_routers,
)

app = FastAPI()

app.include_router(user_routers.router, tags=["Users"])
app.include_router(sector_routers.router, tags=["Sectors"])
app.include_router(type_routers.router, tags=["Type"])
app.include_router(shelf_routers.router, tags=["Shelves"])
app.include_router(location_routers.router, tags=["Locations"])
app.include_router(material_router.router, tags=["Materials"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)
