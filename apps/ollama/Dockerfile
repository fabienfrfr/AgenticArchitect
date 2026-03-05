FROM ollama/ollama:latest

ENV OLLAMA_MODELS=/root/.ollama/models

RUN nohup bash -c "ollama serve &" && \
    sleep 5 && \
    # Ultra light model (min think and tool)
    ollama pull qwen3.5:0.8b && \
    # ollama run smollm2:135m && \
    pkill ollama

EXPOSE 11434

# Public container
LABEL org.opencontainers.image.source="https://github.com/fabienfrfr/L-Architecte"
LABEL org.opencontainers.image.description="TheArchitect - Ollama with light model included"