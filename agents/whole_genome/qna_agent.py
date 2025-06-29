import json
from typing import Dict, Any
from ..common.base import BaseAgent

class WholeGenomeQNAAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract whole genome-specific data for context
        genome_data = report.get("genome_data", {})
        snps = report.get("snps", {})
        structural_variants = report.get("structural_variants", {})
        ancestry = report.get("ancestry", {})
        
        prompt = (
f"""
You are a whole genome sequencing specialist answering questions for user {user_id}.

GENOME DATA:
{json.dumps(genome_data, indent=2)}

SNPS:
{json.dumps(snps, indent=2)}

STRUCTURAL VARIANTS:
{json.dumps(structural_variants, indent=2)}

ANCESTRY:
{json.dumps(ancestry, indent=2)}

USER QUESTION: {user_query}

Provide a comprehensive answer that includes:

1. DIRECT ANSWER:
   - Clear response to the user's question
   - Specific information from their genome data
   - Relevant scientific context

2. DATA INTERPRETATION:
   - How their specific genome patterns relate to the question
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
   - Background on genome biology
   - Current research findings
   - Limitations of current knowledge

Provide a thorough, evidence-based answer that directly addresses the user's question while being accessible and actionable.
"""
        )
        return self.generate(prompt, max_tokens=500) 