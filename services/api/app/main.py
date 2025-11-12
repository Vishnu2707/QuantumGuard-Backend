from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .routes import auth, keys, health, pqc

app = FastAPI(title="QuantumGuard API", version="0.2.0")

allow_origins = ["*"]
if settings.CORS_ORIGINS:
    allow_origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(keys.router)
app.include_router(pqc.router)
