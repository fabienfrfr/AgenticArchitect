# ADR 005: Integration of Langfuse for Agentic Observability (LLMOps)

**Status:** Proposed

**Context:** The **AgenticArchitect** system uses a multi-agent bus (LangGraph) with local LLMs (Ollama/Gemma). We need a way to visualize the "Chain of Thought", monitor performance (latency, token usage), and debug agent interactions without relying on messy, unformatted raw text files.

**Decision:** We will integrate **Langfuse** as the primary observability layer. It will replace raw file logging for agent traces while providing a structured UI for inspecting agent reasoning.

**Consequences:** * **Pros:** Deep visibility into nested agent calls, native LangGraph integration, local-first deployment (via Docker), and a "Playground" for prompt testing.

* **Cons:** Requires an additional PostgreSQL database and a running Langfuse container.