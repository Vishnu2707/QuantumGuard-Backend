
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
import hmac, hashlib, secrets
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)

def create_jwt(sub: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

def verify_jwt(token: str) -> str | None:
    try:
        data = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return data.get("sub")
    except Exception:
        return None

def random_api_key() -> str:
    # 256-bit urlsafe key
    return secrets.token_urlsafe(32)

def hash_api_key(api_key: str) -> str:
    return hmac.new(settings.APIKEY_KDF_SALT.encode(), api_key.encode(), hashlib.sha256).hexdigest()
