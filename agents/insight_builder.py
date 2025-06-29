import json
from .base import BaseAgent

class InsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        prompt = (
f"""
You are a microbiome specialist analyzing user {user_id}'s data.

USER DATA:
{json.dumps(report, indent=2)}

USER QUESTION: {user_query}

Provide comprehensive insights including:

1. KEY FINDINGS:
   - Most important observations from the data
   - Patterns and trends identified
   - Notable deviations from normal ranges

2. HEALTH IMPLICATIONS:
   - What the findings mean for overall health
   - Potential health benefits or risks
   - Areas of concern or strength

3. MICROBIOME ASSESSMENT:
   - Diversity and balance evaluation
   - Functional capacity analysis
   - Stability and resilience indicators

4. LIFESTYLE FACTORS:
   - How diet, exercise, stress might influence results
   - Environmental factors to consider
   - Behavioral patterns that could impact microbiome

5. CLINICAL RELEVANCE:
   - Medical conditions that might be affected
   - Symptoms that could be related
   - Preventive health opportunities

6. ACTIONABLE INSIGHTS:
   - Specific recommendations based on findings
   - Areas for improvement
   - Monitoring suggestions

Provide evidence-based insights that are practical and actionable for the user.
"""
        )
        return self.generate(prompt, max_tokens=500)

