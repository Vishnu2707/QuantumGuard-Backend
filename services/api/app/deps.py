from fastapi import Header, HTTPException, Depends
from jose import jwt, JWTError
from bson import ObjectId
from .config import settings
from .db import users, apikeys
from .utils import hash_api_key


# ---------------------------------------
# 🧩 Decode JWT and get user email
# ---------------------------------------
async def current_user_email(authorization: str | None = Header(default=None)):
    """Extract user email from JWT Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")
        if not await users.find_one({"email": sub}):
            raise HTTPException(status_code=401, detail="User not found")
        return sub
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------------------------------
# 🧩 Decode JWT and get user ID (for internal use)
# ---------------------------------------
async def current_user_id(authorization: str | None = Header(default=None)):
    """Extract user ID from JWT Bearer token."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        sub = payload.get("sub")
        if not sub:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = await users.find_one({"email": sub})
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return str(user["_id"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


# ---------------------------------------
# 🗝️ API Key validation
# ---------------------------------------
async def api_key_owner_id(x_api_key: str | None = Header(default=None)) -> str:
    """Return user ID that owns the given API key."""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")

    hashed = hash_api_key(x_api_key)
    rec = await apikeys.find_one({"hashed": hashed})
    if not rec:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return str(rec["userId"])
