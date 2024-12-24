from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Mati AI Builder"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    
    class Config:
        env_file = ".env"

settings = Settings()