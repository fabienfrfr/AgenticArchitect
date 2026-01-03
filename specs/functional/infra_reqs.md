# Infra Specifications: External Services

## 1. LLM Engine (Ollama)

**Requirement ID:** REQ-INFRA-01
**Description:** The system shall interact with an Ollama instance to perform local inference.
**Constraint:**

- Model version: `gemma3:270m`
- Availability: Must respond to HTTP GET on port 11434.

## 2. Observability (Langfuse)

**Requirement ID:** REQ-INFRA-02
**Description:** The system shall record every agent step (traces) into Langfuse.
**Constraint:**

- Authentication: Requires a valid Public/Secret key pair.
- Availability: Must respond to `auth_check()` via the SDK.
