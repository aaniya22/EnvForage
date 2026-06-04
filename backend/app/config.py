"""
EnvForge application settings.

All configuration is sourced from environment variables or a local `.env` file.
`load_dotenv()` is invoked here so any code path that imports `app.config`
(FastAPI, Alembic migrations, the seed service, ad-hoc `python -m ...` scripts)
shares the same env-loading bootstrap before `Settings` is read.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

DEV_SECRET_KEY = "dev-secret-key-change-in-production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ── Application ───────────────────────────────────────────
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    secret_key: str = DEV_SECRET_KEY
    app_name: str = "EnvForage"
    app_version: str = "1.0.0"
    custom_template_dir: Path | None = None

    # ── Database ──────────────────────────────────────────────
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/envforge"

    # ── Redis ─────────────────────────────────────────────────
    # If set, the rate limiter will use Redis instead of in-memory storage.
    # Required in production for multi-worker correctness.
    # Format: redis://:password@host:port/db  or  redis://host:port/db
    redis_url: str | None = None
    resolver_cache_ttl_seconds: int = 86400
    run_sync_loop: bool = True

    # ── CORS ─────────────────────────────────────────────────
    allowed_origins: str = "http://localhost:3000"

    @property
    def allowed_origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",")]

    # ── AI / LLM ─────────────────────────────────────────────
    envforge_llm_provider: Literal["openai", "openrouter", "ollama", "mock"] = "mock"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    openrouter_api_key: str = ""
    openrouter_model: str = "openai/gpt-4o"
    ollama_base_url: str = "http://llm:11434"
    ollama_model: str = "llama3"
    ai_max_tokens: int = 2048
    ai_temperature: float = 0.3

    # ── Pagination ────────────────────────────────────────────
    default_page_size: int = 20
    max_page_size: int = 100

    # ── Rate Limiting ─────────────────────────────────────────
    rate_limit_ai_rpm: int = 10  # AI troubleshoot: requests per minute
    rate_limit_repair_rpm: int = 20  # Repair endpoint: requests per minute
    rate_limit_general_rpm: int = 60  # General API: requests per minute
    # ── Admin API Key ─────────────────────────────────────────
    admin_api_key: str = ""

    @model_validator(mode="after")
    def validate_secret_key(self) -> "Settings":
        """Enforce strong SECRET_KEY and validate Redis in production environments.

        The default value (DEV_SECRET_KEY) is committed to the public repository.
        Any deployment that omits SECRET_KEY in staging or production will silently
        sign JWTs with this known-public string, allowing trivial token forgery.

        Redis is required in production for correct rate limiting behavior across
        multiple workers. Without it, each worker maintains separate rate limit state,
        allowing attackers to bypass limits by distributing requests.

        Raises:
            ValueError: When required configuration is missing outside development.
        """
        if self.environment != "development":
            if self.secret_key == DEV_SECRET_KEY:
                raise ValueError(
                    f"A strong SECRET_KEY is required when environment='{self.environment}'. "
                    "Set the SECRET_KEY environment variable to a cryptographically random "
                    "value before deploying. "
                    "The default key ('dev-secret-key-change-in-production') is committed "
                    "to the public repository and must never be used outside local development."
                )

            # Production deployments with multiple workers must use Redis
            if self.environment == "production" and not self.redis_url:
                raise ValueError(
                    "REDIS_URL must be configured when environment='production'. "
                    "In-memory rate limiting is not suitable for distributed deployments. "
                    "Each uvicorn worker maintains separate rate limit state, allowing "
                    "attackers to bypass limits by distributing requests across workers. "
                    "Configure Redis with format: redis://:password@host:port/db or redis://host:port/db"
                )

        return self


@lru_cache
def get_settings() -> Settings:
    """Return cached settings singleton."""
    return Settings()
