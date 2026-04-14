from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Model
    model_id: str = "stabilityai/stable-diffusion-xl-base-1.0"
    device: str = "cuda"
    torch_dtype: str = "float16"

    # Redis / Task Queue
    redis_url: str = "redis://localhost:6379"

    # Storage
    storage_path: str = "./generated"

    # API
    allowed_origins: str = "http://localhost:3000"
    api_prefix: str = "/api"

    # Rate Limiting
    rate_limit_per_minute: int = 10

    # Safety
    enable_nsfw_filter: bool = True
    max_prompt_length: int = 500

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()
