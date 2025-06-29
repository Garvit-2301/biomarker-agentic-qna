import json
from typing import Dict, Any
from ..common.base import BaseAgent

class MetagenomicsQNAAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract metagenomics-specific data for context
        microbiome_data = report.get("microbiome_data", {})
        diversity_scores = report.get("diversity_scores", {})
        functional_markers = report.get("functional_markers", {})
        
        prompt = (
f"""
You are a gut microbiome specialist answering questions for user {user_id}.

MICROBIOME DATA:
{json.dumps(microbiome_data, indent=2)}

DIVERSITY SCORES:
{json.dumps(diversity_scores, indent=2)}

FUNCTIONAL MARKERS:
{json.dumps(functional_markers, indent=2)}

USER QUESTION: {user_query}

Provide a comprehensive answer that includes:

1. DIRECT ANSWER:
   - Clear response to the user's question
   - Specific information from their microbiome data
   - Relevant scientific context

2. DATA INTERPRETATION:
   - How their specific microbiome patterns relate to the question
   - What their values mean in context
   - Comparison to normal ranges if applicable

3. HEALTH IMPLICATIONS:
   - What this means for their gut health
   - Potential risks or benefits
   - Clinical significance

4. PRACTICAL RELEVANCE:
   - How this affects their daily life
   - What they can do with this information
   - Actionable insights

5. SCIENTIFIC CONTEXT:
   - Background on microbiome biology
   - Current research findings
   - Limitations of current knowledge

Provide a thorough, evidence-based answer that directly addresses the user's question while being accessible and actionable.
"""
        )
        return self.generate(prompt, max_tokens=500) 