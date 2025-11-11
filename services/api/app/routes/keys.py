
from fastapi import APIRouter, Depends
from ..models import ApiKeyCreateIn, ApiKeyOut
from ..security import random_api_key, hash_api_key
from ..db import api_keys
from ..deps import current_user_id
from datetime import datetime, timezone

router = APIRouter(prefix="/v1/keys", tags=["keys"])

@router.post("", response_model=ApiKeyOut)
async def create_key(body: ApiKeyCreateIn, user_id: str = Depends(current_user_id)):
    raw = random_api_key()
    h = hash_api_key(raw)
    await api_keys.insert_one({
        "user_id": user_id,
        "label": body.label,
        "key_hash": h,
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    return {"apiKey": raw}

@router.get("")
async def list_keys(user_id: str = Depends(current_user_id)):
    cur = api_keys.find({"user_id": user_id}).sort("created_at", -1)
    items = []
    async for k in cur:
        items.append({"label": k["label"], "createdAt": k["created_at"]})
    return {"keys": items}
