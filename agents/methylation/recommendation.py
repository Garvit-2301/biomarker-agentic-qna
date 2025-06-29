import json
from ..common.base import BaseAgent

class MethylationRecommendationAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        demographics = context.get("demographics", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract methylation-specific data
        methylation_score = report.get("methylation_score", 0)
        epigenetic_age = report.get("epigenetic_age", {})
        methylation_patterns = report.get("methylation_patterns", {})
        health_implications = report.get("health_implications", {})
        
        prompt = (
f"""
You are a methylation specialist providing personalized recommendations for user {user_id}.

USER PROFILE:
Demographics: {demographics}
Methylation Score: {methylation_score}
Epigenetic Age: {epigenetic_age}
Methylation Patterns: {methylation_patterns}
Health Implications: {health_implications}

Provide personalized, evidence-based recommendations (3-4 specific suggestions each):

1. NUTRITION FOR METHYLATION:
   - Methyl donors (folate, B12, choline)
   - Foods that support methylation pathways
   - Dietary factors that influence epigenetic age

2. LIFESTYLE INTERVENTIONS:
   - Exercise recommendations for methylation
   - Stress management techniques
   - Sleep optimization for epigenetic health

3. SUPPLEMENTS (if appropriate):
   - Methylation-supporting supplements
   - Dosage recommendations
   - Timing considerations

4. ENVIRONMENTAL FACTORS:
   - Toxin avoidance strategies
   - Environmental influences on methylation
   - Protective measures

5. MONITORING SUGGESTIONS:
   - Follow-up testing recommendations
   - Progress tracking methods
   - Timeline for reassessment

Make recommendations specific to this user's methylation profile and epigenetic age.
"""
        )
        return self.llm.generate(prompt, max_tokens=600) 