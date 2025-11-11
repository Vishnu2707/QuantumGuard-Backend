
from fastapi import Header, HTTPException, Depends
from .db import users, api_keys
from .security import verify_jwt, hash_api_key

async def current_user_id(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    sub = verify_jwt(token)
    if not sub:
        raise HTTPException(status_code=401, detail="Invalid token")
    u = await users.find_one({"email": sub})
    if not u:
        raise HTTPException(status_code=401, detail="User not found")
    return str(u["_id"])

async def api_key_owner_id(x_api_key: str = Header(None)) -> str:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")
    h = hash_api_key(x_api_key)
    k = await api_keys.find_one({"key_hash": h})
    if not k:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return str(k["user_id"])
