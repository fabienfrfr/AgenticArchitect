from langfuse.callback import CallbackHandler
from typing import List
import os

class ObservabilityManager:
    """
    Handles telemetry and tracing. 
    Respects Single Responsibility by separating logic from UI/Core.
    """
    def __init__(self):
        self.langfuse_handler = CallbackHandler(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
            host=os.getenv("LANGFUSE_HOST", "http://localhost:3000")
        )

    def get_callbacks(self) -> List:
        return [self.langfuse_handler]