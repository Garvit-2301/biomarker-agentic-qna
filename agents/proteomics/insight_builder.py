import json
from typing import Dict, Any
from ..common.base import BaseAgent

class ProteomicsInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract proteomics-specific data for context
        protein_data = report.get("protein_data", {})
        biomarker_levels = report.get("biomarker_levels", {})
        pathway_analysis = report.get("pathway_analysis", {})
        health_implications = report.get("health_implications", {})
        
        prompt = (
f"""
You are a proteomics specialist analyzing data for user {user_id}.

PROTEIN DATA:
{json.dumps(protein_data, indent=2)}

BIOMARKER LEVELS:
{json.dumps(biomarker_levels, indent=2)}

PATHWAY ANALYSIS:
{json.dumps(pathway_analysis, indent=2)}

HEALTH IMPLICATIONS:
{json.dumps(health_implications, indent=2)}

USER QUESTION: {user_query}

Provide comprehensive proteomics insights including:

1. PROTEIN EXPRESSION ANALYSIS:
   - Overall protein expression patterns
   - Key protein biomarkers
   - Expression level variations
   - Tissue-specific patterns

2. BIOMARKER ASSESSMENT:
   - Clinical biomarker levels
   - Disease-associated proteins
   - Health status indicators
   - Risk factor proteins

3. PATHWAY ANALYSIS:
   - Metabolic pathway activity
   - Signaling pathway status
   - Protein interaction networks
   - Functional implications

4. HEALTH IMPLICATIONS:
   - Disease risk assessment
   - Metabolic health indicators
   - Inflammation markers
   - Organ function status

5. LIFESTYLE FACTORS:
   - How diet affects protein expression
   - Exercise and protein patterns
   - Stress impact on biomarkers
   - Environmental influences

6. ACTIONABLE INSIGHTS:
   - Specific protein targets
   - Intervention opportunities
   - Monitoring recommendations
   - Prevention strategies

Provide evidence-based insights that explain protein expression patterns in the context of overall health and wellness.
"""
        )
        return self.generate(prompt, max_tokens=600) 