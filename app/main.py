from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.api.routes.scans import router as scans_router

app = FastAPI(
    title="Network Scanner API",
    version="1.0.0",
    description="FastAPI backend pentru network scanning autorizat.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, tags=["health"])
app.include_router(scans_router, prefix="/scans", tags=["scans"])