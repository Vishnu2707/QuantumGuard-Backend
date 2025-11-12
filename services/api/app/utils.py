import hashlib, time
from bson import ObjectId
from .config import settings
from .db import apilogs

def hash_api_key(api_key: str) -> str:
    salt = settings.APIKEY_KDF_SALT.encode()
    return hashlib.sha256(api_key.encode() + salt).hexdigest()

async def log_api_call(user_id: str | None, endpoint: str, ok: bool, started: float):
    doc = {
        "userId": ObjectId(user_id) if user_id else None,
        "endpoint": endpoint,
        "ok": ok,
        "rt_ms": int((time.time() - started) * 1000),
        "ts": int(time.time()),
    }
    try:
        await apilogs.insert_one(doc)
    except Exception:
        pass
