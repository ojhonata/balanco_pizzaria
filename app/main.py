from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)


app = FastAPI(title="FloorLy API",
    description="Backend para mapeamento indoor e BI - Projeto MVP",
    version="1.0",
    #lifespan=lifespan
    )

app.include_router(api_router, prefix="/v1")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
