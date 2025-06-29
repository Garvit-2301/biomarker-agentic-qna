
import json
from .base import BaseAgent

class IntentClassifierAgent(BaseAgent):
    CATEGORIES = ["Insight", "Recommendation", "Compare", "Explain_Score", "Unknown"]

    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        prompt = (
            "Classify query into one of: %s. " % self.CATEGORIES +
            "Return JSON with keys 'intent' & 'confidence'.

" +
            f"Query: '{user_query}'"
        )
        raw = self.llm.generate(prompt, max_tokens=120, temperature=0)
        try:
            data = json.loads(raw)
            intent = data.get("intent", "Unknown")
        except Exception:
            intent = "Unknown"
        return intent if intent in self.CATEGORIES else "Unknown"

