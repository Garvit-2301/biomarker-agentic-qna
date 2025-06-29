import json
from typing import Dict, Any
from ..common.base import BaseAgent

class MetagenomicsExplainerAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        term = context.get("term", "")
        
        # Extract metagenomics-specific data for context
        microbiome_data = report.get("microbiome_data", {})
        diversity_scores = report.get("diversity_scores", {})
        functional_markers = report.get("functional_markers", {})
        
        prompt = (
f"""
You are a gut microbiome specialist explaining concepts for user {user_id}.

MICROBIOME CONTEXT:
{json.dumps(microbiome_data, indent=2)}

DIVERSITY SCORES:
{json.dumps(diversity_scores, indent=2)}

FUNCTIONAL MARKERS:
{json.dumps(functional_markers, indent=2)}

TERM TO EXPLAIN: {term}

USER QUESTION: {user_query}

Provide a comprehensive explanation that includes:

1. DEFINITION:
   - Clear, simple definition of the term
   - What it measures or represents
   - Why it's important for microbiome analysis

2. SCIENTIFIC CONTEXT:
   - How it relates to gut microbiome
   - Biological mechanisms involved
   - Role in gut health

3. HEALTH IMPLICATIONS:
   - What healthy vs unhealthy patterns look like
   - How it affects overall health
   - Disease associations

4. PERSONAL RELEVANCE:
   - How this term relates to the user's microbiome data
   - What their specific values mean
   - Implications for their gut health

5. PRACTICAL UNDERSTANDING:
   - Simple analogies or examples
   - What changes in this value indicate
   - How it can be influenced

6. End with a single-sentence summary in **bold**.

Use clear, non-technical language and provide specific examples. Make the explanation relevant to the user's microbiome profile.
"""
        )
        return self.generate(prompt, max_tokens=600) 