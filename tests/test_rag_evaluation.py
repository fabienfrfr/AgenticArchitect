import pytest
from pytest_bdd import scenario, given, when, then, parsers
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase
from deepeval.models import DeepEvalBaseLLM
from pydantic_ai.models.openai import OpenAIModel

# 1. Define the PydanticAI-powered Judge
class PydanticAIJudge(DeepEvalBaseLLM):
    def __init__(self, pydantic_model):
        self.model = pydantic_model

    def generate(self, prompt: str) -> str:
        return self.model.generate_text_sync(prompt, deps=None).data

    async def a_generate(self, prompt: str) -> str:
        return (await self.model.generate_text(prompt, deps=None)).data

@pytest.fixture(scope="session")
def judge():
    # Use your production PydanticAI model configuration
    model = OpenAIModel('gpt-4o')
    return PydanticAIJudge(model)

@scenario("features/rag_evaluation.feature", "Verify ArangoDB context accuracy")
def test_rag_accuracy():
    pass

@given(parsers.parse('an input query "{query}"'), target_fixture="ctx")
def step_input(query):
    return {"query": query}

@when("the agent retrieves data from ArangoDB", target_fixture="ctx")
def step_execute(ctx):
    # Simulate your actual Agent call
    # ctx["response"] = your_agent.ask(ctx["query"])
    ctx["response"] = "The security constraint requires TLS 1.3 and RBAC."
    ctx["context"] = ["TLS 1.3 is mandatory for ArangoDB security."]
    return ctx

@then("the final response should be factually accurate")
def step_verify(ctx, judge):
    metric = HallucinationMetric(threshold=0.7)
    
    test_case = LLMTestCase(
        input=ctx["query"],
        actual_output=ctx["response"],
        retrieval_context=ctx["context"]
    )
    
    # Execute evaluation using your PydanticAI judge
    assert_test(test_case, [metric], llm=judge)