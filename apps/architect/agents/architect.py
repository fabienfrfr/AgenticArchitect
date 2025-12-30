from abc import ABC, abstractmethod
from typing import Dict
from pydantic import BaseModel

class ADR(BaseModel):
    title: str
    context: str
    decision: str
    consequences: list

class ArchitectAgent:
    def generate_c4_diagram(self, requirements: Dict) -> str:
        return """graph TD
            A[Client] --> B[FastAPI]
            B --> C[Architect Agent]"""

    def generate_adr(self, context: Dict) -> ADR:
        return ADR(
            title="Use ChromaDB",
            context="Need local RAG",
            decision="Deploy ChromaDB in Docker",
            consequences=["Pros: Local", "Cons: No HA"]
        )
