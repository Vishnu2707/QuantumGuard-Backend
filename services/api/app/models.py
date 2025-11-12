from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from fastapi import Header, HTTPException
from jose import jwt, JWTError
from .config import settings
from .db import users, apikeys
from .utils import hash_api_key


# ---------------------------------------
# 🧠 Auth Models
# ---------------------------------------

class SignupIn(BaseModel):
    email: EmailStr
    password: str


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    token: str


# ---------------------------------------
# 🗝️ API Key Models
# ---------------------------------------

class ApiKeyCreateIn(BaseModel):
    label: str


class ApiKeyOut(BaseModel):
    id: str
    label: str
    userId: str
    hashed: str


# ---------------------------------------
# 🔒 PQC Models (for KEM + Signature)
# ---------------------------------------

# 🔐 KEM (Key Encapsulation Mechanism)

class PQCKEMKeypairIn(BaseModel):
    algorithm: str = Field(..., description="Post-quantum KEM algorithm (e.g., Kyber1024)")
    key_size: int = Field(1024, description="Key size in bits")


class PQCKEMEncapIn(BaseModel):
    algorithm: str
    public_key: str


class PQCKEMDecapIn(BaseModel):
    algorithm: str
    private_key: str
    ciphertext: str


class PQCKEMKeypairOut(BaseModel):
    public_key: str
    private_key: str


class PQCKEMCipherOut(BaseModel):
    ciphertext: str
    shared_secret: str


# ✍️ Signature (Falcon, Dilithium)

class PQCSignIn(BaseModel):
    algorithm: str = Field(..., description="Post-quantum signature algorithm (e.g., Falcon, Dilithium)")
    message: str
    private_key: str


class PQCVerifyIn(BaseModel):
    algorithm: str
    message: str
    signature: str
    public_key: str


class PQCSignOut(BaseModel):
    signature: str


class PQCVerifyOut(BaseModel):
    valid: bool


# ---------------------------------------
# 🔐 Auth Header Dependencies
# ---------------------------------------

async def current_user_email(authorization: str | None = Header(default=None)):
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


async def api_key_owner_id(x_api_key: str | None = Header(default=None)) -> str:
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key")
    hashed = hash_api_key(x_api_key)
    rec = await apikeys.find_one({"hashed": hashed})
    if not rec:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return str(rec["userId"])

# ---------------------------------------
# 🔒 PQC Models (for KEM + Signature)
# ---------------------------------------

# 🔐 KEM (Key Encapsulation Mechanism)
class PQCKEMKeypairIn(BaseModel):
    algorithm: str = Field(..., description="Post-quantum KEM algorithm (e.g., Kyber1024)")
    key_size: int = Field(1024, description="Key size in bits")


class PQCKEMEncapIn(BaseModel):
    algorithm: str
    public_key: str


class PQCKEMDecapIn(BaseModel):
    algorithm: str
    private_key: str
    ciphertext: str


class PQCKEMKeypairOut(BaseModel):
    public_key: str
    private_key: str


class PQCKEMCipherOut(BaseModel):
    ciphertext: str
    shared_secret: str


# ✍️ Signature (Falcon, Dilithium)

class PQCSigKeypairIn(BaseModel):
    algorithm: str = Field(..., description="Post-quantum signature algorithm (e.g., Falcon1024, Dilithium5)")


class PQCSigSignIn(BaseModel):
    algorithm: str
    message: str
    private_key: str


class PQCSigSignOut(BaseModel):
    signature: str


class PQCVerifyIn(BaseModel):
    algorithm: str
    message: str
    signature: str
    public_key: str


class PQCSignOut(BaseModel):
    signature: str


class PQCVerifyOut(BaseModel):
    valid: bool
    
class PQCSigVerifyIn(BaseModel):
    algorithm: str
    message: str
    signature: str
    public_key: str


class PQCSigVerifyOut(BaseModel):
    valid: bool
