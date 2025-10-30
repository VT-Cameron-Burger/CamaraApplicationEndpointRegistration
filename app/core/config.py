"""
Application Configuration Settings
"""

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # Basic settings
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Project info
    PROJECT_NAME: str = "Python HTTP API"
    VERSION: str = "1.0.0"

    # Security
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # CORS
    ALLOWED_HOSTS: list[str] | str = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
    ]

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)


# Create settings instance
settings = Settings()
