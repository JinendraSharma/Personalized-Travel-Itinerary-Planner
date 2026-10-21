"""Application configuration settings."""

import os
from functools import lru_cache
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseModel):
    # Supabase
    supabase_url: str = Field(default_factory=lambda: os.getenv("SUPABASE_URL", ""))
    supabase_key: str = Field(default_factory=lambda: os.getenv("SUPABASE_KEY") or os.getenv("SUPABASE_ANON_KEY", ""))
    supabase_service_role_key: str = Field(default_factory=lambda: os.getenv("SUPABASE_SERVICE_ROLE_KEY", ""))

    # JWT
    secret_key: str = Field(default_factory=lambda: os.getenv("SECRET_KEY", "default-dev-secret-key-at-least-32-chars-long"))
    algorithm: str = Field(default_factory=lambda: os.getenv("ALGORITHM", "HS256"))
    access_token_expire_minutes: int = Field(default_factory=lambda: int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))

    # AI Model
    ai_provider: str = Field(default_factory=lambda: os.getenv("AI_PROVIDER", "groq"))
    groq_api_key: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))
    huggingface_api_key: str = Field(default_factory=lambda: os.getenv("HUGGINGFACE_API_KEY", ""))
    ollama_base_url: str = Field(default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))

    # Server
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "True").lower() == "true")
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    backend_url: str = Field(default_factory=lambda: os.getenv("BACKEND_URL", "http://localhost:8000"))
    frontend_url: str = Field(default_factory=lambda: os.getenv("FRONTEND_URL", "http://localhost:5173"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()
