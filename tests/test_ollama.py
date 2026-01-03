import pytest
import httpx
import os


# Fixture to centralize configuration (SRP/DRY)
@pytest.fixture
def ollama_config():
    # NEED : ollama pull gemma3:270m
    return {
        "url": os.getenv("OLLAMA_URL", "http://localhost:11434"),
        "model": "gemma3:270m",
    }


@pytest.mark.asyncio
async def test_ollama_server_connection(ollama_config):
    """
    Responsibility: Verify the physical availability of the Ollama API.
    """
    async with httpx.AsyncClient(timeout=2.0) as client:
        try:
            response = await client.get(ollama_config["url"])
            assert response.status_code == 200
        except (httpx.ConnectError, httpx.ConnectTimeout):
            pytest.fail(f"Service unreachable at {ollama_config['url']}")


@pytest.mark.asyncio
async def test_required_model_is_pulled(ollama_config):
    """
    Responsibility: Verify that the specific test model exists in the local registry.
    """
    target_model = ollama_config["model"]
    async with httpx.AsyncClient(timeout=5.0) as client:
        # We only catch communication errors, not assertion errors (SOLID)
        try:
            response = await client.get(f"{ollama_config['url']}/api/tags")
            assert response.status_code == 200
        except (httpx.ConnectError, httpx.TimeoutException) as e:
            pytest.fail(f"Infrastructure error: {str(e)}")

        models_data = response.json().get("models", [])
        local_model_names = [m["name"] for m in models_data]

        # This will raise a clean AssertionError if the model is missing
        assert any(
            target_model in name for name in local_model_names
        ), f"Model {target_model} not found. Run 'ollama pull {target_model}'"
