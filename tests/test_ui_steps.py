import pytest
from pytest_bdd import scenario, given, when, then
from apps.architect.controller import ArchitectController


@scenario("../specs/features/ui_workflow.feature", "Successful SMART validation")
def test_ui_logic_flow():
    pass


@given(
    'the client input "Building a Python API with Docker and SQL"',
    target_fixture="input_data",
)
def input_data():
    return "Building a Python API with Docker and SQL"


@when("the user clicks on START AGENTIC WORKFLOW", target_fixture="workflow_result")
async def trigger_workflow(input_data):
    controller = ArchitectController()
    # We test the controller logic directly
    result = await controller.run_full_pipeline(input_data)
    return result


@then('the PM status should be "✅ SMART"')
def check_pm_status(workflow_result):
    assert workflow_result["charter_data"]["is_smart"] is True


@then("a C4 diagram should be displayed")
def check_diagram(workflow_result):
    assert "graph TD" in workflow_result["architecture_specs"]["diagram"]
