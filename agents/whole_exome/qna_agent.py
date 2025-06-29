import json
from typing import Dict, Any
from ..common.base import BaseAgent

class WholeExomeQNAAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract whole exome-specific data for context
        variants_data = report.get("variants_data", {})
        carrier_status = report.get("carrier_status", {})
        pharmacogenomics = report.get("pharmacogenomics", {})
        
        prompt = (
f"""
You are a whole exome sequencing specialist answering questions for user {user_id}.

VARIANTS DATA:
{json.dumps(variants_data, indent=2)}

CARRIER STATUS:
{json.dumps(carrier_status, indent=2)}

PHARMACOGENOMICS:
{json.dumps(pharmacogenomics, indent=2)}

USER QUESTION: {user_query}

Provide a comprehensive answer that includes:

1. DIRECT ANSWER:
   - Clear response to the user's question
   - Specific information from their genetic data
   - Relevant scientific context

2. DATA INTERPRETATION:
   - How their specific genetic variants relate to the question
   - What their values mean in context
   - Comparison to population frequencies if applicable

3. HEALTH IMPLICATIONS:
   - What this means for their health
   - Potential risks or benefits
   - Clinical significance

4. PRACTICAL RELEVANCE:
   - How this affects their daily life
   - What they can do with this information
   - Actionable insights

5. SCIENTIFIC CONTEXT:
   - Background on genetic variation
   - Current research findings
   - Limitations of current knowledge

Provide a thorough, evidence-based answer that directly addresses the user's question while being accessible and actionable.
"""
        )
        return self.generate(prompt, max_tokens=500) 