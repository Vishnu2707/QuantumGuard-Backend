
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal

class SignupIn(BaseModel):
    email: EmailStr
    password: str
    industry: Optional[Literal["ai","healthcare","iot","distributed"]] = "ai"
    company: Optional[str] = None

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    token: str

class ApiKeyCreateIn(BaseModel):
    label: str = "default"

class ApiKeyOut(BaseModel):
    apiKey: str

class PQCKEMKeypairIn(BaseModel):
    scheme: Literal["Kyber512","Kyber768","Kyber1024"] = "Kyber1024"

class PQCKEMEncapIn(BaseModel):
    scheme: Literal["Kyber512","Kyber768","Kyber1024"] = "Kyber1024"
    publicKey: str  # hex

class PQCKEMDecapIn(BaseModel):
    scheme: Literal["Kyber512","Kyber768","Kyber1024"] = "Kyber1024"
    secretKey: str
    ciphertext: str

class PQCSigKeypairIn(BaseModel):
    scheme: Literal["Dilithium2","Dilithium3","Dilithium5","Falcon512","Falcon1024"] = "Dilithium3"

class PQCSigSignIn(BaseModel):
    scheme: Literal["Dilithium2","Dilithium3","Dilithium5","Falcon512","Falcon1024"] = "Dilithium3"
    secretKey: str
    message: str

class PQCSigVerifyIn(BaseModel):
    scheme: Literal["Dilithium2","Dilithium3","Dilithium5","Falcon512","Falcon1024"] = "Dilithium3"
    publicKey: str
    message: str
    signature: str
