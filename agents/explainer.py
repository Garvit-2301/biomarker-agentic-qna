
from .base import BaseAgent

class ExplainerAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        term = context.get("term", user_query)
        prompt = (
            "Explain in simple language the microbiome term or metric: '%s'. " % term +
            "Include what it measures, why it matters, and healthy vs unhealthy ranges."
        )
        return self.llm.generate(prompt, max_tokens=350)

