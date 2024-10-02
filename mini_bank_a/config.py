import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./bank.db"
    SECRET_KEY: str = os.urandom(32).hex()
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

settings = Settings()