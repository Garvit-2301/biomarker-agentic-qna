import json
from .base import BaseAgent

class RecommendationAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        prompt = (
f"""
You are a microbiome specialist providing personalized recommendations for user {user_id}.

USER DATA:
{json.dumps(report, indent=2)}

USER QUESTION: {user_query}

Provide comprehensive, personalized recommendations including:

1. DIETARY RECOMMENDATIONS:
   - Specific foods to include/avoid
   - Macronutrient adjustments
   - Timing and frequency of meals
   - Supplements to consider

2. LIFESTYLE INTERVENTIONS:
   - Exercise recommendations
   - Stress management strategies
   - Sleep optimization
   - Environmental factors

3. MICROBIOME SUPPORT:
   - Prebiotic and probiotic recommendations
   - Fermented foods to include
   - Foods that support beneficial bacteria
   - Avoidance of microbiome disruptors

4. MONITORING STRATEGIES:
   - Follow-up testing recommendations
   - Timeline for reassessment
   - Key metrics to track
   - Progress indicators

5. CLINICAL CONSIDERATIONS:
   - Specialist referrals if needed
   - Medical monitoring requirements
   - Integration with existing treatments
   - Emergency considerations

6. IMPLEMENTATION PLAN:
   - Priority order for changes
   - Realistic timeline for implementation
   - Support resources needed
   - Success metrics

Provide actionable, evidence-based recommendations that are personalized to the user's specific microbiome profile and health goals.
"""
        )
        return self.generate(prompt, max_tokens=600)

