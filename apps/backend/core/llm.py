from langchain_ollama import ChatOllama
from apps.backend.core.config import config


def get_llm(json_mode: bool = True):
    """Factory to get the LLM based on environment."""
    return ChatOllama(
        model=config.MODEL_NAME,
        base_url=config.OLLAMA_URL,
        temperature=0,
        format="json" if json_mode else "",
    )
