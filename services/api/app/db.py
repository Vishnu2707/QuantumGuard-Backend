
from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.DB_NAME]

# Collections
users = db.users          # { _id, email, password_hash, industry, created_at }
api_keys = db.api_keys    # { _id, user_id, label, key_hash, created_at }
api_logs = db.api_logs    # { _id, user_id, endpoint, algorithm, status, latency_ms, ts }
