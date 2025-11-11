
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from ..db import users
from ..models import SignupIn, LoginIn, TokenOut
from ..security import hash_password, verify_password, create_jwt

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/signup", response_model=TokenOut)
async def signup(body: SignupIn):
    existing = await users.find_one({"email": body.email})
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    doc = {
        "email": body.email,
        "password_hash": hash_password(body.password),
        "industry": body.industry,
        "company": body.company,
        "created_at": {"$date": 0}
    }
    res = await users.insert_one(doc)
    token = create_jwt(body.email)
    return {"token": token}

@router.post("/login", response_model=TokenOut)
async def login(body: LoginIn):
    doc = await users.find_one({"email": body.email})
    if not doc or not verify_password(body.password, doc["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt(body.email)
    return {"token": token}
