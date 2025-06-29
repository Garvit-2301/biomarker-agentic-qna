import json
from typing import Dict, Any
from ..common.base import BaseAgent

class ProteomicsQNAAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        
        # Extract proteomics-specific data for context
        protein_data = report.get("protein_data", {})
        biomarker_levels = report.get("biomarker_levels", {})
        pathway_analysis = report.get("pathway_analysis", {})
        
        prompt = (
f"""
You are a proteomics specialist answering questions for user {user_id}.

PROTEIN DATA:
{json.dumps(protein_data, indent=2)}

BIOMARKER LEVELS:
{json.dumps(biomarker_levels, indent=2)}

PATHWAY ANALYSIS:
{json.dumps(pathway_analysis, indent=2)}

USER QUESTION: {user_query}

Provide a comprehensive answer that includes:

1. DIRECT ANSWER:
   - Clear response to the user's question
   - Specific information from their protein data
   - Relevant scientific context

2. DATA INTERPRETATION:
   - How their specific protein patterns relate to the question
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
   - Background on protein biology
   - Current research findings
   - Limitations of current knowledge

Provide a thorough, evidence-based answer that directly addresses the user's question while being accessible and actionable.
"""
        )
        return self.generate(prompt, max_tokens=500) 