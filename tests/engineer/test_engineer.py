import pytest
from apps.backend.agents.engineer.agent import EngineerAgent

@pytest.mark.bdd
class TestEngineerAgent:
    def test_generate_solid_code(self):
        agent = EngineerAgent()
        code = agent.generate_solid_code({}, {})
        assert code.class_name == "DataValidator"
        assert "validate" in code.methods
