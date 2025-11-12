from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client["quantumguard"]

users = db["users"]
apikeys = db["apikeys"]
api_keys = apikeys
apilogs = db["apilogs"]
transactions = db["transactions"]
pqc_results = db["pqc_results"]
