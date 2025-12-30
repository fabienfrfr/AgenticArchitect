import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    # Pydantic will automatically look for an environment variable named 'ENV'
    # If not found, it defaults to 'local'
    ENV: str = Field(default="local", alias="ENV")
    OLLAMA_URL: str = Field(default="http://localhost:11434", alias="OLLAMA_URL")

    @property
    def MODEL_NAME(self) -> str:
        # Use case-insensitive check for robustness
        if self.ENV.lower() == "test":
            return "gemma3:270m"
        return "nemotron-3-nano:30b"

    class Config:
        # This allows loading from a .env file if present
        env_file = ".env"


config = Settings()
