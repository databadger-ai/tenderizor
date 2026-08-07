from functools import lru_cache
from typing import Any, Literal

from pydantic import AliasChoices, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="TENDER_",
        extra="ignore",
        case_sensitive=False,
    )

    service_name: str = "canadabuys-tender-api"
    environment: str = Field(
        default="development", validation_alias=AliasChoices("APP_ENV", "TENDER_ENVIRONMENT")
    )
    log_level: str = Field(
        default="INFO", validation_alias=AliasChoices("LOG_LEVEL", "TENDER_LOG_LEVEL")
    )
    database_url: str = Field(
        default="postgresql+asyncpg://postgres:postgres@postgres:5432/tenders",
        validation_alias=AliasChoices("DATABASE_URL", "TENDER_DATABASE_URL"),
    )
    temporal_address: str = Field(
        default="temporal:7233",
        validation_alias=AliasChoices("TEMPORAL_ADDRESS", "TENDER_TEMPORAL_ADDRESS"),
    )
    temporal_namespace: str = Field(
        default="default",
        validation_alias=AliasChoices("TEMPORAL_NAMESPACE", "TENDER_TEMPORAL_NAMESPACE"),
    )
    temporal_task_queue: str = Field(
        default="canadabuys-tender-analysis-v1",
        validation_alias=AliasChoices("TEMPORAL_TASK_QUEUE", "TENDER_TEMPORAL_TASK_QUEUE"),
    )
    openai_model: Literal["openai:gpt-5.6-sol"] = Field(
        default="openai:gpt-5.6-sol",
        validation_alias=AliasChoices("OPENAI_MODEL", "TENDER_OPENAI_MODEL"),
    )
    openai_reasoning_effort: Literal["none", "low", "medium", "high", "xhigh", "max"] = Field(
        default="medium",
        validation_alias=AliasChoices(
            "OPENAI_REASONING_EFFORT", "TENDER_OPENAI_REASONING_EFFORT"
        ),
    )
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://localhost:5173"],
        validation_alias=AliasChoices("CORS_ORIGINS", "TENDER_CORS_ORIGINS"),
    )
    dispatch_mode: Literal["temporal", "fake"] = "temporal"
    max_source_text_chars: int = Field(default=200_000, ge=1, le=1_000_000)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> Any:
        if isinstance(value, str) and not value.lstrip().startswith("["):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
