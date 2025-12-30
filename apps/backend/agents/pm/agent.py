from langchain_core.prompts import ChatPromptTemplate
from apps.backend.core.llm import get_llm


class PMAgent:
    def __init__(self):
        self.llm = get_llm(json_mode=True)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a Project Manager. Analyze the client requirements. "
                    "Return JSON with keys: 'is_smart' (bool), 'gaps' (list), 'hypotheses' (list).",
                ),
                ("user", "{requirements}"),
            ]
        )

    def check_requirements(self, requirements: str):
        chain = self.prompt | self.llm
        return chain.invoke({"requirements": requirements})
