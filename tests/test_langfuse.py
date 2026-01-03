import pytest
import httpx
import os
from langfuse import Langfuse


# Fixture to centralize Langfuse configuration (SRP/DRY)
@pytest.fixture
def langfuse_config():
    return {
        "host": os.getenv("LANGFUSE_HOST", "http://localhost:3000"),
        "public_key": os.getenv("LANGFUSE_PUBLIC_KEY"),
        "secret_key": os.getenv("LANGFUSE_SECRET_KEY"),
    }


@pytest.mark.asyncio
async def test_langfuse_server_is_reachable(langfuse_config):
    """
    Responsibility: Verify the physical availability of the Langfuse UI/API.
    """
    async with httpx.AsyncClient(timeout=2.0) as client:
        try:
            # Checking the health or main page of Langfuse
            response = await client.get(langfuse_config["host"])
            assert response.status_code == 200
        except (httpx.ConnectError, httpx.ConnectTimeout):
            pytest.fail(f"Langfuse server is unreachable at {langfuse_config['host']}")


def test_langfuse_sdk_authentication(langfuse_config):
    """
    Responsibility: Verify that the API credentials (Public/Secret keys) are valid.
    """
    if not langfuse_config["public_key"] or not langfuse_config["secret_key"]:
        pytest.fail("Langfuse credentials are missing in environment variables.")

    # Initialize the SDK
    langfuse = Langfuse(
        public_key=langfuse_config["public_key"],
        secret_key=langfuse_config["secret_key"],
        host=langfuse_config["host"],
    )

    # Attempt to authenticate via the SDK's internal health check
    try:
        assert (
            langfuse.auth_check() is True
        ), "Langfuse authentication failed with provided keys."
    except Exception as e:
        pytest.fail(f"Langfuse SDK Error: {str(e)}")
