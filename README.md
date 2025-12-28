# AgenticArchitect

AgenticArchitect: Transforming raw client specifications into production-ready AI/Data solutions, powered by local LLMs.

![demo](/docs/global_demo.jpg)

## 🔍 Related Research & Agentic Tools

Here are some useful resources and projects for deep research and agentic AI systems:

- [GPT Researcher – Open deep research agent for web + local documents](https://github.com/assafelovic/gpt-researcher)
- [AutoAgent – Fully-Automated and Zero-Code Framework for LLM Agents (arXiv)](https://arxiv.org/abs/2502.05957v3)
- [ASTA – Accelerating science through trustworthy agentic AI (Allen Institute)](https://allenai.org/blog/asta)
- [Agent Laboratory – Interactive environment for multi-agent scientific research](https://agentlaboratory.github.io/)

Other relevant resources:

- [LangGraph – Framework for building stateful, multi-actor LLM applications](https://github.com/langchain-ai/langgraph)
- [AutoGen – Multi-agent conversation framework for LLM applications](https://github.com/microsoft/autogen)
- [Elicit – AI research assistant for literature review and scientific workflows](https://elicit.org/)


## Deployment

### 1. Local (Docker Compose)
#### Prerequisites
- Docker and Docker Compose installed.
- NVIDIA GPU + NVIDIA Container Toolkit drivers.

#### Run
```bash
./scripts/deploy.sh local
```
Access the app at [http://localhost:3000](http://localhost:3000).

---

### 2. Cloud (AWS/GCP)
#### Prerequisites
- AWS/GCP account with permissions.
- Terraform and Helm installed.

#### Run
```bash
./scripts/deploy.sh cloud
```
Get the frontend service URL:
```bash
kubectl get services frontend
```