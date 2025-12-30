import json
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, START, END

# Corrected Imports
from apps.backend.agents.pm import PMAgent
from apps.backend.agents.analyst import AnalystAgent
from apps.backend.agents.architect import ArchitectAgent
from apps.backend.agents.engineer import EngineerAgent


class AgentState(TypedDict):
    requirements: str
    charter_data: dict
    analysis_report: Optional[dict]
    architecture_specs: Optional[dict]
    final_code: Optional[dict]
    is_ready: bool


# --- Node Functions ---


def pm_node(state: AgentState):
    agent = PMAgent()
    response = agent.check_requirements(state["requirements"])
    data = json.loads(response.content)
    return {"charter_data": data, "is_ready": data.get("is_smart", False)}


def analyst_node(state: AgentState):
    agent = AnalystAgent()
    # Logic to adapt your old Analyst to the new flow
    report = agent.analyze(state["requirements"])
    return {"analysis_report": report.dict()}


def architect_node(state: AgentState):
    agent = ArchitectAgent()
    # Generate C4 & ADR based on requirements
    diagram = agent.generate_c4_diagram({"req": state["requirements"]})
    adr = agent.generate_adr({"context": "Local Deployment"})
    return {"architecture_specs": {"diagram": diagram, "adr": adr.dict()}}


def engineer_node(state: AgentState):
    agent = EngineerAgent()
    specs = state["architecture_specs"]
    code = agent.generate_solid_code(specs["adr"], specs["diagram"])
    return {"final_code": code.dict()}


# --- Routing ---


def route_after_pm(state: AgentState):
    if state["is_ready"]:
        return "analyst"
    return END  # Stops if requirements are not SMART


# --- Graph Construction ---

workflow = StateGraph(AgentState)

workflow.add_node("pm", pm_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("architect", architect_node)
workflow.add_node("engineer", engineer_node)

workflow.add_edge(START, "pm")
workflow.add_conditional_edges("pm", route_after_pm)
workflow.add_edge("analyst", "architect")
workflow.add_edge("architect", "engineer")
workflow.add_edge("engineer", END)

app_workflow = workflow.compile()
