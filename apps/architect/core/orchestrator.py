import json
import logging
from typing import TypedDict, List, Optional, Dict, Any
from langgraph.graph import StateGraph, START, END

# --- Standardized Imports ---
# Ensure these paths match your folder structure exactly
from apps.architect.agents.pm import PMAgent
from apps.architect.agents.analyst import AnalystAgent
from apps.architect.agents.architect import ArchitectAgent
from apps.architect.agents.engineer import EngineerAgent

# --- State Definition ---


class AgentState(TypedDict):
    requirements: str
    charter_data: Optional[Dict[str, Any]]
    analysis_report: Optional[Dict[str, Any]]
    architecture_specs: Optional[Dict[str, Any]]
    final_code: Optional[Dict[str, Any]]
    is_ready: bool
    retry_count: int
    latest_error: Optional[str]


# --- Node Functions ---


def pm_node(state: AgentState) -> Dict[str, Any]:
    """Executes PM analysis and catches potential parsing errors (BASE Logic)."""
    agent = PMAgent()
    current_retry = state.get("retry_count", 0)

    try:
        response = agent.check_requirements(state["requirements"])
        # If the LLM returns invalid JSON, json.loads will raise an error here
        data = json.loads(response.content)

        return {
            "charter_data": data,
            "is_ready": data.get("is_smart", False),
            "latest_error": None,
            "retry_count": current_retry,  # Maintain count
        }
    except Exception as e:
        logging.error(f"Inference error on try {current_retry}: {str(e)}")
        return {"latest_error": str(e), "retry_count": current_retry + 1}


def analyst_node(state: AgentState) -> Dict[str, Any]:
    """Analyst Agent: Performs data discovery and EDA requirements."""
    agent = AnalystAgent()
    # Using model_dump() for Pydantic V2 compatibility
    report = agent.analyze(state["requirements"])
    return {
        "analysis_report": (
            report.model_dump() if hasattr(report, "model_dump") else report.dict()
        )
    }


def architect_node(state: AgentState) -> Dict[str, Any]:
    """Architect Agent: Generates C4 diagrams and Architecture Decision Records (ADR)."""
    agent = ArchitectAgent()
    # Generate artifacts based on input requirements
    diagram = agent.generate_c4_diagram({"req": state["requirements"]})
    adr = agent.generate_adr({"context": "Local Deployment"})

    return {
        "architecture_specs": {
            "diagram": diagram,
            "adr": adr.model_dump() if hasattr(adr, "model_dump") else adr.dict(),
        }
    }


def engineer_node(state: AgentState) -> Dict[str, Any]:
    """Engineer Agent: Generates SOLID-compliant code from architecture specs."""
    agent = EngineerAgent()
    specs = state.get("architecture_specs")

    if not specs:
        raise ValueError(
            "Critical Error: Missing architecture specs in state for Engineer Agent."
        )

    code = agent.generate_solid_code(specs["adr"], specs["diagram"])
    return {
        "final_code": code.model_dump() if hasattr(code, "model_dump") else code.dict()
    }


def review_node(state: AgentState):
    """
    Critiques the proposed solution based on the 'Less is More' principle.
    """
    # This node sends the plan to a critic agent (or the same LLM with a specific prompt)
    # to identify unnecessary complexity or redundant dependencies.
    prompt = "Review the following proposal. Identify 3 things that can be removed to make it simpler."
    # ... logic to call the LLM ...
    return state

# --- Routing Logic (The Deciders) ---


def retry_router(state: AgentState) -> str:
    """
    Explicit Router for Error Handling and Business Logic.
    Implements a loop for self-healing if the LLM fails.
    """
    # 1. Error Handling: Retry if an error occurred and we haven't hit the limit (3)
    if state.get("latest_error") and state.get("retry_count", 0) < 3:
        return "retry"

    # 2. Business Logic: If PM marked it ready, proceed to Analyst
    if state.get("is_ready"):
        return "continue"

    # 3. Terminal State: Either too many errors or the project description is not SMART enough
    return "stop"


# --- Graph Construction ---

# Initialize the state machine
workflow = StateGraph(AgentState)

# Add all agents as nodes
workflow.add_node("pm", pm_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("architect", architect_node)
workflow.add_node("engineer", engineer_node)
workflow.add_node("reviewer", review_node)
# Set the entry point to the PM Agent
workflow.add_edge(START, "pm")

#
# Define the conditional logic after PM analysis
workflow.add_conditional_edges(
    "pm",
    retry_router,
    {
        "retry": "pm",  # Loop back for self-healing
        "continue": "analyst",  # Move to the next swimlane phase
        "stop": END,  # Stop the process
    },
)

# Linear flow for the remaining agents (Post-validation)
workflow.add_edge("analyst", "architect")
workflow.add_edge("architect", "engineer")
workflow.add_edge("engineer", "reviewer")
workflow.add_edge("reviewer", END)

# Compile the graph into an executable app
app_workflow = workflow.compile()
