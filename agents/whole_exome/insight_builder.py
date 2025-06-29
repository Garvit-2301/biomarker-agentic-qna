import json
from typing import Dict, Any
from ..common.base import BaseAgent

class WholeExomeInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract whole exome-specific data for context
        variants_data = report.get("variants_data", {})
        carrier_status = report.get("carrier_status", {})
        pharmacogenomics = report.get("pharmacogenomics", {})
        health_implications = report.get("health_implications", {})
        
        prompt = (
f"""
You are a whole exome sequencing specialist analyzing data for user {user_id}.

VARIANTS DATA:
{json.dumps(variants_data, indent=2)}

CARRIER STATUS:
{json.dumps(carrier_status, indent=2)}

PHARMACOGENOMICS:
{json.dumps(pharmacogenomics, indent=2)}

HEALTH IMPLICATIONS:
{json.dumps(health_implications, indent=2)}

USER QUESTION: {user_query}

Provide comprehensive whole exome insights including:

1. GENETIC VARIANT ANALYSIS:
   - Overall variant burden
   - Key genetic variants identified
   - Variant classification and significance
   - Population frequency comparisons

2. CARRIER STATUS ASSESSMENT:
   - Recessive disease carrier status
   - Family planning implications
   - Risk assessment for offspring
   - Genetic counseling considerations

3. PHARMACOGENOMICS:
   - Drug metabolism variants
   - Medication response predictions
   - Personalized dosing recommendations
   - Adverse drug reaction risks

4. HEALTH IMPLICATIONS:
   - Disease risk assessment
   - Monogenic disorder risks
   - Complex trait associations
   - Preventive health opportunities

5. CLINICAL RELEVANCE:
   - Actionable genetic findings
   - Screening recommendations
   - Specialist referrals if needed
   - Monitoring strategies

6. ACTIONABLE INSIGHTS:
   - Specific genetic targets
   - Intervention opportunities
   - Family screening recommendations
   - Prevention strategies

Provide evidence-based insights that explain genetic variants in the context of overall health and wellness.
"""
        )
        return self.generate(prompt, max_tokens=600) 