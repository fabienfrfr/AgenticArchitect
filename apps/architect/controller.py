import asyncio
from typing import Dict, Any
from apps.architect.core.orchestrator import app_workflow


class ArchitectController:
    """SOLID: Handles the logic execution for the UI."""

    async def run_full_pipeline(self, requirements: str) -> Dict[str, Any]:
        """Runs the LangGraph swimlane directly in Python."""
        initial_state = {
            "requirements": requirements,
            "charter_data": {},
            "is_ready": False,
            "retry_count": 0,
        }
        # On utilise asyncio pour ne pas freezer l'interface pendant que l'IA réfléchit
        return await asyncio.to_thread(app_workflow.invoke, initial_state)
