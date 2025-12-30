from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END
from apps.backend.agents.pm_agent import PMAgent


class AgentState(TypedDict):
    requirements: str
    charter_data: dict
    is_ready: bool


def pm_node(state: AgentState):
    pm = PMAgent()
    result = pm.check_requirements(state["requirements"])
    # LangChain returns a message, we parse the content
    import json

    data = json.loads(result.content)
    return {"charter_data": data, "is_ready": data.get("is_smart", False)}


def router(state: AgentState):
    if state["is_ready"]:
        return "architect"
    return END


# Build the Graph
workflow = StateGraph(AgentState)
workflow.add_node("pm", pm_node)
workflow.add_edge(START, "pm")
workflow.add_conditional_edges(
    "pm", router, {"architect": END, END: END}  # To be replaced by architect node later
)

app_workflow = workflow.compile()
