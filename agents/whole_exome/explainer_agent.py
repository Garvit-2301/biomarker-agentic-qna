import json
from typing import Dict, Any
from ..common.base import BaseAgent

class WholeExomeExplainerAgent(BaseAgent):
    def run(self, user_query: str, context: Dict[str, Any]) -> str:
        report = context.get("report", {})
        user_id = context.get("user_id", "Unknown")
        term = context.get("term", "")
        
        # Extract whole exome-specific data for context
        variants_data = report.get("variants_data", {})
        carrier_status = report.get("carrier_status", {})
        pharmacogenomics = report.get("pharmacogenomics", {})
        
        prompt = (
f"""
You are a whole exome sequencing specialist explaining concepts for user {user_id}.

WHOLE EXOME CONTEXT:
{json.dumps(variants_data, indent=2)}

CARRIER STATUS:
{json.dumps(carrier_status, indent=2)}

PHARMACOGENOMICS:
{json.dumps(pharmacogenomics, indent=2)}

TERM TO EXPLAIN: {term}

USER QUESTION: {user_query}

Provide a comprehensive explanation that includes:

1. DEFINITION:
   - Clear, simple definition of the term
   - What it measures or represents
   - Why it's important for genetic analysis

2. SCIENTIFIC CONTEXT:
   - How it relates to genetic variation
   - Biological mechanisms involved
   - Role in health and disease

3. HEALTH IMPLICATIONS:
   - What healthy vs unhealthy patterns look like
   - How it affects overall health
   - Disease associations

4. PERSONAL RELEVANCE:
   - How this term relates to the user's whole exome data
   - What their specific values mean
   - Implications for their health

5. PRACTICAL UNDERSTANDING:
   - Simple analogies or examples
   - What changes in this value indicate
   - How it can be influenced

6. End with a single-sentence summary in **bold**.

Use clear, non-technical language and provide specific examples. Make the explanation relevant to the user's whole exome profile.
"""
        )
        return self.generate(prompt, max_tokens=600) 