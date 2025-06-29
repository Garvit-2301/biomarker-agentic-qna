import json
from typing import Dict, Any
from ..common.base import BaseAgent

class MetagenomicsInsightBuilderAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract metagenomics-specific data for context
        microbiome_data = report.get("microbiome_data", {})
        diversity_scores = report.get("diversity_scores", {})
        functional_markers = report.get("functional_markers", {})
        health_implications = report.get("health_implications", {})
        
        prompt = (
f"""
You are a gut microbiome specialist analyzing data for user {user_id}.

MICROBIOME DATA:
{json.dumps(microbiome_data, indent=2)}

DIVERSITY SCORES:
{json.dumps(diversity_scores, indent=2)}

FUNCTIONAL MARKERS:
{json.dumps(functional_markers, indent=2)}

HEALTH IMPLICATIONS:
{json.dumps(health_implications, indent=2)}

USER QUESTION: {user_query}

Provide comprehensive microbiome insights including:

1. MICROBIOME COMPOSITION ANALYSIS:
   - Overall bacterial diversity
   - Key species abundance
   - Balance between phyla
   - Dysbiosis indicators

2. DIVERSITY ASSESSMENT:
   - Alpha diversity metrics
   - Beta diversity patterns
   - Species richness and evenness
   - Health implications of diversity levels

3. FUNCTIONAL CAPACITY:
   - Metabolic pathway analysis
   - Short-chain fatty acid production
   - Vitamin synthesis capacity
   - Immune modulation potential

4. HEALTH IMPLICATIONS:
   - Gut barrier function
   - Inflammation markers
   - Metabolic health indicators
   - Immune system interactions

5. LIFESTYLE FACTORS:
   - How diet affects microbiome
   - Exercise and microbiome health
   - Stress impact on gut bacteria
   - Environmental influences

6. ACTIONABLE INSIGHTS:
   - Specific microbiome targets
   - Intervention opportunities
   - Monitoring recommendations
   - Prevention strategies

Provide evidence-based insights that explain microbiome patterns in the context of overall health and wellness.
"""
        )
        return self.generate(prompt, max_tokens=600) 