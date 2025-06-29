import json
from typing import Dict, Any
from ..common.base import BaseAgent

class MethylationExplainerAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        term = context.get("term", "")
        
        # Extract methylation-specific data for context
        methylation_data = report.get("methylation_data", {})
        epigenetic_age = report.get("epigenetic_age", {})
        cpg_sites = report.get("cpg_sites", {})
        
        prompt = (
f"""
You are a DNA methylation specialist explaining concepts for user {user_id}.

METHYLATION CONTEXT:
{json.dumps(methylation_data, indent=2)}

EPIGENETIC AGE:
{json.dumps(epigenetic_age, indent=2)}

CPG SITES:
{json.dumps(cpg_sites, indent=2)}

TERM TO EXPLAIN: {term}

USER QUESTION: {user_query}

Provide a comprehensive explanation that includes:

1. DEFINITION:
   - Clear, simple definition of the term
   - What it measures or represents
   - Why it's important for methylation analysis

2. SCIENTIFIC CONTEXT:
   - How it relates to DNA methylation
   - Biological mechanisms involved
   - Role in epigenetic regulation

3. HEALTH IMPLICATIONS:
   - What healthy vs unhealthy patterns look like
   - How it affects overall health
   - Disease associations

4. PERSONAL RELEVANCE:
   - How this term relates to the user's methylation data
   - What their specific values mean
   - Implications for their health

5. PRACTICAL UNDERSTANDING:
   - Simple analogies or examples
   - What changes in this value indicate
   - How it can be influenced

6. End with a single-sentence summary in **bold**.

Use clear, non-technical language and provide specific examples. Make the explanation relevant to the user's methylation profile.
"""
        )
        return self.generate(prompt, max_tokens=600) 