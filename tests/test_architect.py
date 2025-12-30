import pytest
from apps.architect.agents.architect import ArchitectAgent


@pytest.mark.bdd
class TestArchitectAgent:
    def test_generate_c4(self):
        agent = ArchitectAgent()
        diagram = agent.generate_c4_diagram({})
        assert "graph TD" in diagram

    def test_generate_adr(self):
        agent = ArchitectAgent()
        adr = agent.generate_adr({})
        assert adr.title == "Use ChromaDB"
