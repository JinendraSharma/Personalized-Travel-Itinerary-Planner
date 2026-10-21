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
    secret_key: str = Field(default_factory=lambda: os.getenv("SECRET_KEY", "development-only-insecure-secret-key-change-me"))
    algorithm: str = Field(default_factory=lambda: os.getenv("ALGORITHM", "HS256"))
    access_token_expire_minutes: int = Field(default_factory=lambda: int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")))

    # AI Model
    ai_provider: str = Field(default_factory=lambda: os.getenv("AI_PROVIDER", "groq"))
    groq_api_key: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY", ""))
    huggingface_api_key: str = Field(default_factory=lambda: os.getenv("HUGGINGFACE_API_KEY", ""))
    ollama_base_url: str = Field(default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"))
    ollama_model: str = Field(default_factory=lambda: os.getenv("OLLAMA_MODEL", "llama3"))

    # Server
    debug: bool = Field(default_factory=lambda: os.getenv("DEBUG", "true").lower() == "true")
    environment: str = Field(default_factory=lambda: os.getenv("ENVIRONMENT", "development"))
    backend_url: str = Field(default_factory=lambda: os.getenv("BACKEND_URL", "http://localhost:8000"))
    frontend_url: str = Field(default_factory=lambda: os.getenv("FRONTEND_URL", "http://localhost:5173"))

    @property
    def allowed_origins(self) -> list[str]:
        """Configured browser origins for CORS (comma-separated in FRONTEND_URL)."""
        return [origin.strip().rstrip("/") for origin in self.frontend_url.split(",") if origin.strip()]

    def validate_for_runtime(self) -> None:
        """Fail fast on unsafe or incomplete production configuration."""
        if self.environment.lower() not in {"development", "staging", "production"}:
            raise ValueError("ENVIRONMENT must be development, staging, or production")
        if self.algorithm != "HS256":
            raise ValueError("Only HS256 is supported for application JWTs")
        if self.access_token_expire_minutes < 1:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")
        if self.ai_provider not in {"groq", "ollama", "local"}:
            raise ValueError("Supported AI_PROVIDER values are groq, ollama, and local")

        if self.environment.lower() in {"staging", "production"}:
            if self.debug:
                raise ValueError("DEBUG must be false in staging and production")
            if (
                len(self.secret_key) < 32
                or self.secret_key.startswith(("development-only", "replace_with", "your_"))
            ):
                raise ValueError("Set SECRET_KEY to a unique random value of at least 32 characters in staging/production")
            if (
                not self.supabase_url.startswith("https://")
                or self.supabase_url.startswith("https://your_")
                or not self.supabase_service_role_key
                or self.supabase_service_role_key.startswith("your_")
            ):
                raise ValueError("Staging/production require SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY")
            if not self.allowed_origins or any(
                "localhost" in origin or "127.0.0.1" in origin for origin in self.allowed_origins
            ):
                raise ValueError("FRONTEND_URL must contain deployed origins, not localhost")
            if self.ai_provider == "groq" and (
                not self.groq_api_key or self.groq_api_key.startswith("your_")
            ):
                raise ValueError("GROQ_API_KEY is required when AI_PROVIDER=groq")
            if self.environment.lower() == "production" and self.ai_provider == "local":
                raise ValueError("AI_PROVIDER=local is for development; production requires groq or ollama")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached Settings instance."""
    return Settings()
