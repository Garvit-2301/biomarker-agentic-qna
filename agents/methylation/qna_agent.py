import json
from typing import Dict, Any
from ..common.base import BaseAgent

class MethylationQNAAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract methylation-specific data for context
        methylation_data = report.get("methylation_data", {})
        epigenetic_age = report.get("epigenetic_age", {})
        cpg_sites = report.get("cpg_sites", {})
        
        prompt = (
f"""
You are a DNA methylation specialist answering questions for user {user_id}.

METHYLATION DATA:
{json.dumps(methylation_data, indent=2)}

EPIGENETIC AGE:
{json.dumps(epigenetic_age, indent=2)}

CPG SITES:
{json.dumps(cpg_sites, indent=2)}

USER QUESTION: {user_query}

Provide a comprehensive answer that includes:

1. DIRECT ANSWER:
   - Clear response to the user's question
   - Specific information from their methylation data
   - Relevant scientific context

2. DATA INTERPRETATION:
   - How their specific methylation patterns relate to the question
   - What their values mean in context
   - Comparison to normal ranges if applicable

3. HEALTH IMPLICATIONS:
   - What this means for their health
   - Potential risks or benefits
   - Clinical significance

4. PRACTICAL RELEVANCE:
   - How this affects their daily life
   - What they can do with this information
   - Actionable insights

5. SCIENTIFIC CONTEXT:
   - Background on methylation biology
   - Current research findings
   - Limitations of current knowledge

Provide a thorough, evidence-based answer that directly addresses the user's question while being accessible and actionable.
"""
        )
        return self.generate(prompt, max_tokens=500) 