import os
import hashlib
import secrets
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------------------------------
# 🔑 Password Hashing and Verification
# ---------------------------------------

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(password, hashed_password)


# ---------------------------------------
# 🪪 JWT Token Utilities
# ---------------------------------------

def create_access_token(subject: str) -> str:
    """Generate a signed JWT token."""
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"sub": subject, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")


# ---------------------------------------
# 🗝️ API Key Utilities
# ---------------------------------------

def random_api_key() -> str:
    """Generate a new random API key (256-bit hex)."""
    return secrets.token_hex(32)


def hash_api_key(api_key: str) -> str:
    """Hash an API key with HMAC-SHA256 and project salt."""
    key_salt = bytes.fromhex(settings.APIKEY_KDF_SALT)
    return hashlib.pbkdf2_hmac("sha256", api_key.encode(), key_salt, 100_000).hex()
