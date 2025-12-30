import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "local")  # 'test' or 'local'
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://ollama:11434")

    @property
    def MODEL_NAME(self) -> str:
        # If testing, use the ultra-light Gemma 3
        if self.ENV == "test":
            return "gemma3:270m"
        # In production/local, use the powerful Nemotron (Transoformer X Mamba MOE)
        return "nemotron-3-nano:30b"


config = Settings()
