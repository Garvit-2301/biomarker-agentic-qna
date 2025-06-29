import json
from .base import BaseAgent

class CompareAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        baseline = context.get("baseline", {})
        user_id = context.get("user_id", "Unknown")
        
        prompt = (
f"""
You are a microbiome specialist comparing user {user_id}'s data to population baselines.

USER DATA:
{json.dumps(report, indent=2)}

POPULATION BASELINE:
{json.dumps(baseline, indent=2)}

Provide a comprehensive comparison including:

1. OVERALL ASSESSMENT:
   - How user compares to population average
   - Percentile rankings where available
   - Health implications

2. KEY METRICS COMPARISON:
   - Specific measurements vs population norms
   - Statistical significance of differences
   - Clinical relevance

3. RISK ASSESSMENT:
   - Disease risk compared to population
   - Protective factors identified
   - Areas of concern

4. STRENGTHS AND WEAKNESSES:
   - Above-average areas
   - Below-average areas
   - Neutral findings

5. POPULATION CONTEXT:
   - Age/gender-specific comparisons
   - Ethnic/ancestry considerations
   - Lifestyle factor influences

6. CLINICAL IMPLICATIONS:
   - Monitoring recommendations
   - Intervention opportunities
   - Follow-up testing suggestions

Use specific numbers and explain what they mean for the user's health.
"""
        )
        return self.generate(prompt, max_tokens=500)

