from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from apps.backend.core.orchestrator import app_workflow

app = FastAPI(title="AgenticArchitect API")


class ProjectRequest(BaseModel):
    requirements: str


@app.post("/process_project")
async def process_project(request: ProjectRequest):
    """
    Main entry point that follows the AgenticArchitect Swimlane.
    It triggers the LangGraph workflow: PM -> Analyst -> Architect -> Engineer.
    """
    try:
        # Initial state for the workflow
        initial_state = {
            "requirements": request.requirements,
            "charter_data": {},
            "is_ready": False,
            "status": "started",
        }

        # Execute the graph (Swimlane logic)
        final_result = app_workflow.invoke(initial_state)

        return {"success": True, "data": final_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "up", "environment": "check config for model info"}
