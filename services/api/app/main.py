
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .config import ALLOWED_ORIGINS, settings
from .routes import auth, keys, pqc, health

# Rate limit by client IP for general, but PQC routes will also be heavy
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="QuantumGuard API", default_response_class=None)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limit exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Routes
app.include_router(health.router, tags=["meta"])
app.include_router(auth.router)
app.include_router(keys.router)
app.include_router(pqc.router)
