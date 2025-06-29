import json
from typing import Dict, Any
from ..common.base import BaseAgent

class MethylationRecommendationAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract methylation-specific data for context
        methylation_data = report.get("methylation_data", {})
        epigenetic_age = report.get("epigenetic_age", {})
        cpg_sites = report.get("cpg_sites", {})
        health_implications = report.get("health_implications", {})
        
        prompt = (
f"""
You are a DNA methylation specialist providing personalized recommendations for user {user_id}.

METHYLATION DATA:
{json.dumps(methylation_data, indent=2)}

EPIGENETIC AGE:
{json.dumps(epigenetic_age, indent=2)}

CPG SITES:
{json.dumps(cpg_sites, indent=2)}

HEALTH IMPLICATIONS:
{json.dumps(health_implications, indent=2)}

USER QUESTION: {user_query}

Provide comprehensive, personalized methylation recommendations including:

1. NUTRITION RECOMMENDATIONS:
   - Methylation-supporting foods
   - Folate and B-vitamin rich foods
   - Foods that support epigenetic health
   - Supplements for methylation support

2. LIFESTYLE INTERVENTIONS:
   - Exercise recommendations for epigenetic health
   - Stress management for methylation
   - Sleep optimization strategies
   - Environmental toxin avoidance

3. METHYLATION SUPPORT:
   - Specific methylation pathway support
   - Detoxification support
   - Antioxidant recommendations
   - Anti-inflammatory strategies

4. MONITORING STRATEGIES:
   - Follow-up methylation testing
   - Timeline for reassessment
   - Key methylation markers to track
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

Provide actionable, evidence-based recommendations that are personalized to the user's specific methylation profile and health goals.
"""
        )
        return self.generate(prompt, max_tokens=600) 