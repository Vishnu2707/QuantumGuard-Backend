from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MONGO_URI: str
    DB_NAME: str = "quantumguard"
    JWT_SECRET: str
    APIKEY_KDF_SALT: str
    CORS_ORIGINS: str | None = None
    ACCESS_TOKEN_TTL_SEC: int = 1800

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
