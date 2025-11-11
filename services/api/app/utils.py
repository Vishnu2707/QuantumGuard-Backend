
import time
from fastapi import Request
from .db import api_logs
from typing import Optional

async def log_api_call(user_id, endpoint: str, algorithm: Optional[str], status: int, started_at: float):
    try:
        await api_logs.insert_one({
            "user_id": user_id,
            "endpoint": endpoint,
            "algorithm": algorithm,
            "status": status,
            "latency_ms": int((time.time() - started_at) * 1000),
            "ts": time.time()
        })
    except Exception:
        pass
