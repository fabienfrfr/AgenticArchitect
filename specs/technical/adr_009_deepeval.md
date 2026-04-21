### ADR 009: AI-Native Evaluation & Testing Strategy

**Status:** Accepted

**Decider:** Fabien Furfaro

**Context:** The project requires automated, rigorous validation of AI agent outputs to meet banking compliance standards. Traditional testing frameworks lack native AI-metric support (hallucinations, bias, relevance), while external platforms introduce architectural bloat.

**Decision:** We will adopt a **"Test-as-Code"** approach using **DeepEval** integrated directly into our `pytest-bdd` workflow.

1. **Integrated Metrics:** DeepEval validates AI outputs for hallucination, bias, and relevance within the standard test suite.
2. **Living Documentation:** Requirements and acceptance criteria are embedded directly into Gherkin (`.feature`) files.
3. **CI/CD Native:** AI evaluation runs automatically via `pytest`, ensuring quality gates are enforced before deployment.

**Consequences:**

* **Pros:** * **Efficiency:** Eliminates redundant documentation; requirements and tests are unified in single `.feature` files.
    * **Traceability:** Provides a direct audit trail between regulatory requirements (Gherkin tags) and technical validation scores (DeepEval).
    * **Regression Prevention:** Automatically catches AI logic drift and regressions during the development loop.
* **Cons:** * **Judge Latency:** Running evaluations requires calls to a "Judge LLM," increasing test execution time.
    * **External Dependency:** Testing depends on the availability and performance of the model acting as the judge.