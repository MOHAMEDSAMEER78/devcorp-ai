"""Centralized Application Configuration Loader."""
from pathlib import Path
from typing import Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseSettings):
    """DevCorp AI Environment & Service Configuration."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Project metadata
    project_name: str = "DevCorp AI"
    environment: str = Field(default="development", description="development, staging, production")
    debug: bool = Field(default=False)

    # Database & Storage
    postgres_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/devcorp",
        description="PostgreSQL connection string for LangGraph checkpoints"
    )
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection string for circuit breakers"
    )

    # Inference & Gateway
    litellm_proxy_url: str = Field(
        default="http://localhost:4000",
        description="LiteLLM gateway endpoint"
    )
    litellm_master_key: str = Field(
        default="sk-devcorp-master-key",
        description="LiteLLM admin master key"
    )
    providers_config_path: str = Field(
        default="providers.yaml",
        description="Path to providers.yaml registry"
    )

    # Local vLLM
    local_gpu_enabled: bool = Field(default=False)
    local_vllm_url: str = Field(default="http://localhost:8000/v1")

    # API Keys for Cloud Providers
    gemini_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    groq_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None

    # Standup & Dashboard
    dashboard_port: int = Field(default=3000)
    dashboard_auth_secret: str = Field(default="dev-auth-secret-key-change-in-prod")
    google_calendar_credentials_json: Optional[str] = None
    ms_teams_bot_app_id: Optional[str] = None
    ms_teams_bot_app_password: Optional[str] = None


config = AppConfig()
