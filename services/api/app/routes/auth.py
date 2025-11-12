from fastapi import APIRouter, HTTPException
from ..models import SignupIn, LoginIn, TokenOut
from ..security import hash_password, verify_password, create_access_token
from ..db import users

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/signup", response_model=TokenOut)
async def signup(body: SignupIn):
    if await users.find_one({"email": body.email}):
        raise HTTPException(status_code=400, detail="User already exists")
    await users.insert_one({"email": body.email, "password": hash_password(body.password)})
    token = create_access_token(body.email)
    return {"token": token}

@router.post("/login", response_model=TokenOut)
async def login(body: LoginIn):
    rec = await users.find_one({"email": body.email})
    if not rec or not verify_password(body.password, rec["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token(body.email)
    return {"token": token}
