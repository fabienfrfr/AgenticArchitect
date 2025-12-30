import pytest
from pytest_bdd import scenario, given, when, then
from apps.backend.agents.pm import PMAgent


@scenario(
    "../features/pm.feature",
    "Incomplete requirements trigger gaps identification",
)
def test_pm_logic():
    pass


@pytest.fixture
def agent():
    return PMAgent()


@given('a client provides "<text>"', target_fixture="context")
def provide_text(text):
    return {"input": text}


@when("the PM Agent analyzes the request")
def analyze(agent, context):
    context["charter"] = agent.analyze_requirements(context["input"])


@then("the Charter should be marked as incomplete")
def check_incomplete(context):
    assert context["charter"].is_complete is False
