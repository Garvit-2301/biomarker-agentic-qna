import json
from typing import Dict, Any
from ..common.base import BaseAgent

class MethylationInsightBuilderAgent(BaseAgent):
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
You are a DNA methylation specialist analyzing data for user {user_id}.

METHYLATION DATA:
{json.dumps(methylation_data, indent=2)}

EPIGENETIC AGE:
{json.dumps(epigenetic_age, indent=2)}

CPG SITES:
{json.dumps(cpg_sites, indent=2)}

HEALTH IMPLICATIONS:
{json.dumps(health_implications, indent=2)}

USER QUESTION: {user_query}

Provide comprehensive methylation insights including:

1. METHYLATION PATTERN ANALYSIS:
   - Overall methylation status
   - Key patterns and trends
   - Deviations from normal ranges
   - Age-related methylation changes

2. EPIGENETIC AGE ASSESSMENT:
   - Biological vs chronological age
   - Accelerated aging indicators
   - Youthful methylation patterns
   - Health implications of age differences

3. CPG SITE ANALYSIS:
   - Important CpG sites identified
   - Gene-specific methylation patterns
   - Regulatory region methylation
   - Functional implications

4. HEALTH IMPLICATIONS:
   - Disease risk associations
   - Metabolic health indicators
   - Cognitive health markers
   - Longevity factors

5. LIFESTYLE FACTORS:
   - How diet affects methylation
   - Exercise and methylation patterns
   - Stress impact on epigenetic markers
   - Environmental influences

6. ACTIONABLE INSIGHTS:
   - Specific methylation targets
   - Intervention opportunities
   - Monitoring recommendations
   - Prevention strategies

Provide evidence-based insights that explain methylation patterns in the context of overall health and wellness.
"""
        )
        return self.generate(prompt, max_tokens=600) 